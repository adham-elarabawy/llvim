import logging
from calendar import c
from multiprocessing import process

from rich.console import Console
from rich.logging import RichHandler

from src.llvim.answer import process_extraction_request
from src.llvim.answer_utils import LLVIMConfig


def main(console: Console):
    with open("static/hamming.txt") as f:
        document_text = f.read()

    config = LLVIMConfig(window_height=100, verbatim_mode=True)
    query = "the blurb about newton and edison"
    extracted_content = process_extraction_request(
        document_text, query, config=config
    )
    console.print(f"[purple][bold]Query:[/bold][/purple]\n{query}")
    console.print(f"[purple][bold]Extracted content:[/bold][/purple]\n{extracted_content}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])
    console = Console()
    main(console)
