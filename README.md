# LLVim: **Verifiable and Token-Efficient Text Extraction Using LLMs and Vim.**
[![DOI](https://zenodo.org/badge/862087488.svg)](https://zenodo.org/doi/10.5281/zenodo.13835827)
[![CC BY 4.0][cc-by-shield]][cc-by]

LLVim uses Large Language Models (LLMs) to operate on text documents through a Vim client. This approach **ensures model-extracted content exists in the source text**, eliminating hallucinations common in traditional LLM extraction.  LLVim achieves over **95% reduction in token usage** compared to verbatim extraction methods, and is **robust on weakly supported languages** that even frontier models struggle with. It operates a headless Neovim instance to execute LLM-generated Vim commands, providing verifiable and efficient text extraction.

![CleanShot 2024-09-24 at 16 11 51](https://github.com/user-attachments/assets/bc11c89a-31e2-4c35-95c2-19098fbba8ec)



## Roadmap
- [x] Vim emulator with helpers for llm interaction.
- [x] End-to-end single-turn proof-of-concept, with Hamming's [You and Your Research](https://fs.blog/great-talks/richard-hamming-your-research/).
- [x] Token savings metric. Aim to answer "how many tokens do we save by doing this?"
- [x] Plot token savings vs extracted length. (compared to verbatim extraction methods)
- [ ] Plot pipeline latency vs extracted length. (compared to verbatim extraction methods)
- [ ] Plot partial-ratio existence (verifiable extraction) vs extracted length. (compared to verbatim extraction methods)
- [ ] Ablate vim window size
- [ ] End-to-end multi-turn proof-of-concept (navigating a large document efficiently).
- [ ] Replicate results on open-source models.
- [ ] Concise & direct whitepaper to demonstrate findings.
- [ ] [Maybe] synthetically bootstrap some finetuning data (output is easily verifiable, synthetic data is applicable).
- [ ] [Maybe] fine-tune lightweight OS model on this.

## Artifacts
Plot token savings vs extracted length. (compared to verbatim extraction methods)
![image](https://github.com/user-attachments/assets/83c03b4d-7989-4e43-a905-f46de683c70b)


## Cite this work
```bibtex
@misc{llvim,
  author = {Adham Elarabawy},
  title = {LLVim: Verifiable and Token-Efficient Text Extraction Using LLMs and Vim.},
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
