![Python Badge](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)

# Crawl This

A simple tool to facilitate:

1. [`[pdf]`](#pdf-command) Extraction and chunking of content from PDF files to `.jsonl`.
2. [`[html]`]() Crawling and chunking of content from html pages to `.jsonl` files.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/lfsc09/crawl-this-python.git
cd crawl-this-python
```

2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download resources:

```bash
python setup_nlp_resources.py
```

</br>

## Usage

```bash
python main.py <command> [--flags]
```

</br>

## Project Structure

```
.
├── chunking/
|   ├── split_by_separator.py             # Logic for simple chunking separator strategies
|   ├── split_by_token_huggingface.py     # Logic for hugginface chunking strategies
|   ├── split_by_token_nltk.py            # Logic for NLTK chunking strategies
|   ├── split_by_token_spacy.py           # Logic for Spacy chunking strategies
│   └── split_by_token_tiktoken.py        # Logic for tiktoken chunking strategies
├── commands/
|   ├── pdf.py                            # CLI command to crawl pdf files
|   └── html.py                           # CLI command to crawl web-sites
├── utils/
|   ├── decode.py                         # Decode operations utilities
|   ├── file.py                           # File operations utilities
|   └── log.py                            # Log operations utilities
├── out/                                  # (Default) output folder for results
├── main.py                               # Main application file
├── setup_nlp_resources.py                # Script to that downloads NLTK and Spacy resources
├── requirements.txt                      # Project dependencies
└── README.md                             # Project documentation
```

</br>

## Dependencies

- `black`: Code formatter used for maintaining consistent code style.
- [`pymupdf`](https://pymupdf.readthedocs.io/en/latest/tutorial.html): High performance Pdf reader.
- [`langchain`](https://github.com/langchain-ai/langchain): To use `langchain_text_splitters` chunk strategies.
- `nltk`: Dependencies used by langchain `langchain_text_splitters`.
- `spacy`: Dependencies used by langchain `langchain_text_splitters`.
- `tiktoken`: Dependencies used by langchain `langchain_text_splitters`.

</br>
</br>

# Commands

## (`pdf`) command

Command to crawl pdfs content data, and chunk it using different strategies to than save them in a `.jsonl` file for posterior use.

Use different flag values to test generate different outputs.

</br>

### Flags

- `--file`: Path to the PDF files or folders to be processed. _(More than one may be specified with multiple `--file`)_ _(`.pdf` files will be searched recursevely in folders)_
- `--chunk-strategy`: The strategies used for chunking the content. _(More than one may be specified within the same `--chunk-strategy` parameter)_ _(Use `"all"` to use all strategies)_
  - **flag values:** `"all"`, `"by_separator"`, `"by_separators"`, `"by_token_tiktoken"`, `"by_token_spacy"` and `"by_token_nltk"`.
- `--chunk-size`: Size of each chunk in the chunk strategy unit. (Default: Per strategy value used)
- `--chunk-overlap`: Overlap size between chunks in characters. (Default: Per strategy value used)
- `--chunk-separator`: Separator(s) to use for chunking. _(More than one may be specified within the same `--chunk-separator` parameter)_ (Default: Per strategy value used)
  - **e.g. values:**
    - `""`: An empty space which will split the content in characters.
    - `" "`: A space which will split the content in words.
    - `"\n"`: A line break which will split the content in sentences.
    - `"\n\n"`: A double line break which will split the content in paragraphs.
- `--output-folder`: Output folder where the `.jsonl` files will be generated. (Default: `./out`)
- `--clean-previous`: To erase the previous `--output-folder` and run fresh. (Default: `false`)
- `--verbose`: Enable verbose output. (Default: `false`)

</br>

### Chunking strategies

Available text splitting strategies are done using [`langchain`](https://python.langchain.com/docs/concepts/text_splitters/) implementations.

- [`by_separator`](https://python.langchain.com/docs/how_to/character_text_splitter/): The simplest method.
  - It splits based on a given `separator`, which defaults to `""`.
  - Chunk length is measured by `length_function` which by default uses the number of characters.
  - It has the downside of splitting in the middle of words or sentences.
  - And if the separator is not existent in the content it will do no splits, and the chunk will stay as the entire content.
- [`by_separators`](https://python.langchain.com/docs/concepts/text_splitters/#text-structured-based): A smarter and recursive method.
  - It splits based on multiple `separators`, which defaults to `["\n\n", "\n", " ", ""]`.
  - Chunk length is also measured by `length_function` which by default uses the number of characters.
- [`by_token_tiktoken`](https://python.langchain.com/docs/how_to/split_by_token/#tiktoken): Uses tiktoken to estimate tokens used. It will probably be more accurate for the OpenAI models.
- [`by_token_spacy`](https://python.langchain.com/docs/how_to/split_by_token/#spacy): LangChain implements splitters based on the spaCy tokenizer.
- [`by_token_nltk`](https://python.langchain.com/docs/how_to/split_by_token/#nltk): Rather than just splitting on "\n\n", we can use NLTK to split based on NLTK tokenizers.
- [`by_token_huggingface`](https://python.langchain.com/docs/how_to/split_by_token/#hugging-face-tokenizer): _not implemented_

</br>

### Use examples

Specifying input files.

```bash
python main.py pdf --file example.pdf --chunk-strategy all
python main.py pdf --file example1.pdf --file example2.pdf --chunk-strategy all
python main.py pdf --file ./input-folder --chunk-strategy all
```

Specifying chunk strategies.

```bash
python main.py pdf --file example.pdf --chunk-strategy by_separator by_separators
```

Specifying chunk size and overlap size.

**_(nltk and spaCy) don't have configurable `chunk-overlap`, so they do not use the flag value._**

```bash
python main.py pdf --file example.pdf --chunk-strategy by_separator by_separators by_token_tiktoken --chunk-size 500 --chunk-overlap 50
```

Specifying chunk separators.

**_(tiktoken) doesn't have configurable `chunk-separator`, so it does not use the flag value._**

**_Also, only `"by_separators"` can takes multiple separator values, an error will raise if multiple values are passed while using other strategies._**

```bash
python main.py pdf --file example.pdf --chunk-strategy by_separators --chunk-separator "" " " "\n" "\n\n"
python main.py pdf --file example.pdf --chunk-strategy by_separator by_token_nltk by_token_spacy --chunk-separator "\n"
```

</br>

### Output files

Output generation will follow a structure like:

`/[chunk-strategy]--[chunk-size]--[chunk-overlap]`, "default" will be used if the flag was not informed at CLI.

```
.
├── out/
|   ├── by-separator--default--default/         # jsonl files for by_separator strategy
│       ├── file1.jsonl
│       └── fileN.jsonl
|   ├── by-separators--default--default/        # jsonl files for by_separators strategy
│       ├── file1.jsonl
│       └── fileN.jsonl
|   ├── by-token-nltk--default--default/        # jsonl files for by_token_nltk strategy
│       ├── file1.jsonl
│       └── fileN.jsonl
|   ├── by-token-spacy--default--default/       # jsonl files for by_token_spacy strategy
│       ├── file1.jsonl
│       └── fileN.jsonl
│   └── by-token-tiktoken--default--deafult/    # jsonl files for by_token_tiktoken strategy
│       ├── file1.jsonl
│       └── fileN.jsonl
```
