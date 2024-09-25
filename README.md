# LLVim: **Verifiable and Token-Efficient Text Extraction Using LLMs and Vim Commands.**
[![DOI](https://zenodo.org/badge/862087488.svg)](https://zenodo.org/doi/10.5281/zenodo.13835827)

LLVim uses Large Language Models (LLMs) to interact with text documents through Vim commands. This approach **ensures extracted content exists in the source text**, eliminating hallucinations common in traditional LLM extraction. LLVim achieves over **95% reduction in token usage** compared to verbatim extraction methods, and is **robust on weakly supported languages** that even frontier models struggle with. It operates a headless Neovim instance to execute LLM-generated Vim commands, providing verifiable and efficient text extraction.

## Cite this work
```bibtex
@misc{llvim,
  author = {Adham Elarabawy},
  title = {LLVim: Verifiable and Token-Efficient Text Extraction Using LLMs and Vim Commands.},
  year = {2024},
  version = {0.1.0},
  url = {https://github.com/adham-elarabawy/llvim},
  doi = {10.5281/zenodo.13835827},  # Optional
}