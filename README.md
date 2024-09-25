# LLVim: **Verifiable and Token-Efficient Text Extraction Using LLMs and Vim Commands.**
[![DOI](https://zenodo.org/badge/862087488.svg)](https://zenodo.org/doi/10.5281/zenodo.13835827)
[![CC BY 4.0][cc-by-shield]][cc-by]

LLVim uses Large Language Models (LLMs) to interact with text documents through Vim commands. This approach **ensures model-extracted content exists in the source text**, eliminating hallucinations common in traditional LLM extraction.  LLVim achieves over **95% reduction in token usage** compared to verbatim extraction methods, and is **robust on weakly supported languages** that even frontier models struggle with. It operates a headless Neovim instance to execute LLM-generated Vim commands, providing verifiable and efficient text extraction.

![CleanShot 2024-09-24 at 15 53 17](https://github.com/user-attachments/assets/614c81d5-04fd-40c8-a0b8-241e572d3c99)


## Roadmap
- [x] Vim emulator with helpers for llm interaction.
- [x] End-to-end single-turn proof-of-concept, with Hamming's [You and Your Research](https://fs.blog/great-talks/richard-hamming-your-research/).
- [x] Token savings metric. Aim to answer "how many tokens do we save by doing this?"
- [ ] Plot token savings vs extracted length. (compared to verbatim extraction methods)
- [ ] Plot pipeline latency vs extracted length. (compared to verbatim extraction methods)
- [ ] Plot partial-ratio existence (verifiable extraction) vs extracted length. (compared to verbatim extraction methods)
- [ ] End-to-end multi-turn proof-of-concept (navigating a large document efficiently).
- [ ] Concise & direct whitepaper to demonstrate findings.

## Cite this work
```bibtex
@misc{llvim,
  author = {Adham Elarabawy},
  title = {LLVim: Verifiable and Token-Efficient Text Extraction Using LLMs and Vim Commands.},
  year = {2024},
  version = {0.1.0},
  url = {https://github.com/adham-elarabawy/llvim},
  doi = {10.5281/zenodo.13835827},
}

```

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by]. This imposes that you must provide proper attribution (citation above) when referencing, using, or deriving from this work.


[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
