import logging
import time
from enum import Enum
from functools import lru_cache
from tabnanny import verbose
from typing import Generic, TypeVar

import spacy
from openai import OpenAI
from pydantic import BaseModel

EnumT = TypeVar("EnumT", bound=Enum)


class PipelineManager(Generic[EnumT]):
    def __init__(self, process_until: EnumT | None = None):
        self.stage_to_elapsed_time: dict[EnumT, float] = {}
        self.process_until = process_until
        self.last_time = None
        self.current_stage = None

    def start_stage(self, stage: EnumT) -> bool:
        """Start a new stage, previous stage must be complete."""
        assert self.current_stage is None
        now = time.time()
        self.last_time = now
        self.current_stage = stage
        if self.process_until and stage == self.process_until:
            logging.info(
                "Halting pipeline at stage: %s per `process_until` config.",
                self.process_until.name,
            )
            return False  # halt
        return True  # continue

    def end_stage(self):
        """End the current stage using the provided end time."""
        assert self.current_stage
        assert self.last_time is not None
        self.stage_to_elapsed_time[self.current_stage] = time.time() - self.last_time
        logging.info(
            "Finished stage: %s in %.2f seconds.",
            self.current_stage.name,
            self.stage_to_elapsed_time[self.current_stage],
        )
        self.current_stage = None

    def get_elapsed_time_for_stage(self, stage: EnumT) -> float | None:
        return self.stage_to_elapsed_time.get(stage, None)

    def get_time_up_to_stage(self, stage: EnumT) -> float:
        prev_stages = [
            prev_stage for prev_stage in type(stage) if prev_stage.value < stage.value
        ]
        assert all(
            self.get_elapsed_time_for_stage(prev_stage) is not None
            for prev_stage in prev_stages
        )
        return sum(self.stage_to_elapsed_time[prev_stage] for prev_stage in prev_stages)


class LLVIMConfig(BaseModel):
    window_height: int
    verbatim_mode: bool = (
        False  # Toggle model also returning verbatim text for synthetic checking
    )
    answer_model: str = "gpt-4o-2024-08-06"
    verbose: bool = False


class VimCommandSequence(BaseModel):
    commands_to_extract_exact_text: list[str] | None


class VimCommandSequenceWithVerbatim(VimCommandSequence):
    verbatim_extracted_text: str | None


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
    # TODO: preprocess document to make it easier for model to see (line numbers)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(document_text)
    sentences = [sent.text for sent in doc.sents]
    return "\n".join(sentences)


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI()


def get_structured_completion(
    sysprompt: str, prompt: str, response_format
) -> VimCommandSequence | VimCommandSequenceWithVerbatim:
    client = get_client()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": sysprompt},
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format=response_format,
        max_tokens=1000,
        temperature=0,
    )
    out = completion.choices[0].message.parsed
    assert out is not None, "Failed to parse completion"
    return out
