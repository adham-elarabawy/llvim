import logging
import time
from enum import Enum
from functools import lru_cache
from pydoc import doc

import spacy
from openai import OpenAI
from pydantic import BaseModel

from src.llvim.eval_utils import calculate_tokens_saved, num_tokens, num_tokens_to_price
from src.llvim.emulator import VimEmulator
from src.llvim.answer_utils import LLVIMConfig, LLVIMPipelineManager, LLVIMPipelineStage, PipelineManager, VimCommandSequence, VimCommandSequenceWithVerbatim, fill_prompt, get_structured_completion, prepare_document_text_for_model


def process_extraction_request(
    document: str, extraction_query: str, config:LLVIMConfig
) -> str | None:
    manager = LLVIMPipelineManager()

    manager.start_stage(LLVIMPipelineStage.VIM_EMULATOR_SETUP)
    document = prepare_document_text_for_model(document)
    emulator = VimEmulator(document, window_height=config.window_height)
    manager.end_stage()

    # TODO: some loop to chain serial commands
    manager.start_stage(LLVIMPipelineStage.ANSWER_MODEL_CALL)
    sysprompt = open("src/llvim/sysprompt.txt", encoding="utf-8").read()
    prompt = fill_prompt(emulator.get_window_content(), extraction_query)
    response_format = VimCommandSequenceWithVerbatim if config.verbatim_mode else VimCommandSequence
    command_sequence = get_structured_completion(sysprompt, prompt, response_format)
    logging.info(f'Window content: {emulator.get_window_content()}')
    manager.end_stage()

    manager.start_stage(LLVIMPipelineStage.VIM_EMULATOR_EXECUTION)
    if config.verbatim_mode:
        logging.info(f'Desired text to extract: {command_sequence.verbatim_extracted_text}')
    logging.info(f'Commands to execute: {command_sequence.commands_to_extract_exact_text}')
    content = None
    if command_sequence.commands_to_extract_exact_text:
        for command in command_sequence.commands_to_extract_exact_text:
            logging.info(f"Executing command {command}")
            emulator.execute_command(command)
        # TODO: model-validate the results (limit number of retries)
        content = emulator.get_clipboard_content()
    manager.end_stage()

    # TODO: some token metrics to track savings
    if content:
        num_tokens_extracted = num_tokens(content, config.answer_model)
        num_tokens_saved = calculate_tokens_saved(content, command_sequence, config.answer_model)
        logging.info(f"Number of tokens saved: {num_tokens_saved}")
        logging.info(f"% of tokens saved: {num_tokens_saved / num_tokens_extracted}")
        logging.info(f'$ saved: {num_tokens_to_price(num_tokens_saved, config.answer_model)}')
    return content
