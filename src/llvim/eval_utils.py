from functools import lru_cache
import tiktoken

from src.llvim.answer_utils import VimCommandSequence, VimCommandSequenceWithVerbatim

MODEL_TO_PRICE_PER_TOKEN = {
    "gpt-4o-2024-08-06": 10 / 1_000_000,
}

@lru_cache
def num_tokens(content: str, answer_model: str):
    tokenizer = tiktoken.encoding_for_model(answer_model)
    return len(tokenizer.encode(content))

def calculate_tokens_saved(extracted_response: str, command_sequence: VimCommandSequence | VimCommandSequenceWithVerbatim, answer_model: str):
    num_tokens_extracted = num_tokens(extracted_response, answer_model)
    assert command_sequence.commands_to_extract_exact_text is not None
    num_output_tokens = sum(num_tokens(command, answer_model) for command in command_sequence.commands_to_extract_exact_text)
    return num_tokens_extracted - num_output_tokens

def num_tokens_to_price(num_tokens: int, answer_model: str):
    return num_tokens * MODEL_TO_PRICE_PER_TOKEN[answer_model]