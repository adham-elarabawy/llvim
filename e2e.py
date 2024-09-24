import logging
from multiprocessing import process

from src.llvim.emulator import VimEmulator
from src.llvim.model import process_extraction_request


def main():
    with open("hamming.txt") as f:
        document_text = f.read()

    result = process_extraction_request(
        document_text,
        "What is the part about the importance of timing and luck?",
        window_height=10,
    )
    print(result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
