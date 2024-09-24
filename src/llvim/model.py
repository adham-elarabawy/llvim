import logging
import time
from enum import Enum
from functools import lru_cache
from pydoc import doc

import spacy
from openai import OpenAI
from pydantic import BaseModel

from src.llvim.emulator import VimEmulator
from src.llvim.utils import PipelineManager


class VimCommandSequence(BaseModel):
    commands: list[str]


class LLVIMPipelineStage(Enum):
    VIM_EMULATOR_SETUP = "vim_emulator_setup"
    ANSWER_MODEL_CALL = "answer_model_call"
    VIM_EMULATOR_EXECUTION = "vim_emulator_execution"


class LLVIMPipelineManager(PipelineManager[LLVIMPipelineStage]):
    pass


def fill_prompt(document_text: str, extraction_instructions: str) -> str:
    prompt_str = open("src/llvim/prompt.txt", encoding="utf-8").read()
    return prompt_str.format(
        document_text=document_text, extraction_instructions=extraction_instructions
    )


def prepare_document_text_for_model(document_text: str) -> str:
    # TODO: preprocess document to make it easier for model to see
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(document_text)
    sentences = [sent.text for sent in doc.sents]
    return "\n".join(sentences)


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI()


def get_structured_completion(prompt: str) -> VimCommandSequence:
    client = get_client()
    start_time = time.perf_counter()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_format=VimCommandSequence,
        max_tokens=1000,
    )
    out = completion.choices[0].message.parsed
    assert out is not None, "Failed to parse completion"
    return out


def process_extraction_request(
    document: str, extraction_query: str, window_height: int
) -> str:
    manager = LLVIMPipelineManager()

    manager.start_stage(LLVIMPipelineStage.VIM_EMULATOR_SETUP)
    document = prepare_document_text_for_model(document)
    emulator = VimEmulator(document, window_height=window_height)
    manager.end_stage()

    # TODO: some loop to chain serial commands
    manager.start_stage(LLVIMPipelineStage.ANSWER_MODEL_CALL)
    prompt = fill_prompt(emulator.get_window_content(), extraction_query)
    command_sequence = get_structured_completion(prompt)
    manager.end_stage()

    manager.start_stage(LLVIMPipelineStage.VIM_EMULATOR_EXECUTION)
    for command in command_sequence.commands:
        logging.info(f"Executing command {command}")
        emulator.execute_command(command)
    # TODO: model-validate the results (limit number of retries)
    content = emulator.get_clipboard_content()
    manager.end_stage()

    return content
