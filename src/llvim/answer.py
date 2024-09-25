import logging

from src.llvim.answer_utils import (
    LLVIMConfig,
    LLVIMPipelineManager,
    LLVIMPipelineStage,
    VimCommandSequence,
    VimCommandSequenceWithVerbatim,
    fill_prompt,
    get_structured_completion,
    prepare_document_text_for_model,
)
from src.llvim.emulator import VimEmulator
from src.llvim.eval_utils import calculate_tokens_saved, num_tokens, num_tokens_to_price


def process_extraction_request(
    document: str, extraction_query: str, config: LLVIMConfig
) -> str | None:
    manager = LLVIMPipelineManager()

    manager.start_stage(LLVIMPipelineStage.VIM_EMULATOR_SETUP)
    document = prepare_document_text_for_model(document)
    emulator = VimEmulator(document, window_height=config.window_height)
    manager.end_stage()

    # TODO: some loop to chain serial commands
    # TODO: allow model to traverse document using vim commands (e.g. hjkl), then observe window content state
    manager.start_stage(LLVIMPipelineStage.ANSWER_MODEL_CALL)
    sysprompt = open("src/llvim/sysprompt.txt", encoding="utf-8").read()
    prompt = fill_prompt(emulator.get_window_content(), extraction_query)
    response_format = (
        VimCommandSequenceWithVerbatim if config.verbatim_mode else VimCommandSequence
    )
    command_sequence = get_structured_completion(sysprompt, prompt, response_format)
    if config.verbose:
        logging.info("Window content: %s", emulator.get_window_content())
    manager.end_stage()

    manager.start_stage(LLVIMPipelineStage.VIM_EMULATOR_EXECUTION)
    if isinstance(command_sequence, VimCommandSequenceWithVerbatim) and config.verbose:
        logging.info(
            "Desired text to extract: %s", command_sequence.verbatim_extracted_text
        )
    logging.info(
        "Executing vim commands: %s", command_sequence.commands_to_extract_exact_text
    )
    content = None
    if command_sequence.commands_to_extract_exact_text:
        for command in command_sequence.commands_to_extract_exact_text:
            # logging.info("Executing command %s", command)
            emulator.execute_command(command)
        # TODO: model-validate the results (limit number of retries)
        content = emulator.get_clipboard_content()
    manager.end_stage()

    # TODO: some token metrics to track savings
    if content:
        num_tokens_extracted = num_tokens(content, config.answer_model)
        num_tokens_saved = calculate_tokens_saved(
            content, command_sequence, config.answer_model
        )
        logging.info("Number of tokens saved: %s", num_tokens_saved)
        percentage_saved = (num_tokens_saved / num_tokens_extracted) * 100
        logging.info("%% of tokens saved: %.2f%%", percentage_saved)
        logging.info(
            "$ saved: %.5f", num_tokens_to_price(num_tokens_saved, config.answer_model)
        )
    return content
