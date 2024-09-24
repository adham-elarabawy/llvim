from calendar import c
import logging
from multiprocessing import process

from src.llvim.answer_utils import LLVIMConfig
from src.llvim.emulator import VimEmulator
from src.llvim.answer import process_extraction_request
from rich.console import Console


def main():
    with open("static/hamming.txt") as f:
        document_text = f.read()

    config = LLVIMConfig(window_height=100, verbatim_mode=True)

    result = process_extraction_request(
        document_text,
        "the paragraph about newton and edison",
        config=config
    )
    print(result)


if __name__ == "__main__":
    console = Console()
    logging.basicConfig(level=logging.INFO)
    main()
