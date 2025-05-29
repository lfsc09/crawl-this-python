![Python Badge](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)

# The project

crawl-this is a simple tool to facilitate:

1. `[pdf]` Extraction and chunking of content from PDF files to a `.jsonl`.
2. `[html]` Crawling and chunking of content from html pages to `.jsonl` files.

Run it like:

```bash
crawl <command> [--flags]
```

</br>
</br>

## (`pdf`) command

#### Regular CLI

```bash
crawl pdf [--flags]
```

#### Script `run_pdf_strategies.sh`

Run the script to execute all the chunking strategies.

- Optionally provide `CHUNK_SIZE`, `CHUNK_OVERLAP` and `OUTPUT_DIR`. If not informed, the python's flag default will be used.
- `ENV_DEV` argument is for running in development which will execute the script like `python -m src.cli.root ...`.

```bash
./run_pdf_strategies
  FILE_OR_FOLDER=/path/to/file_or_folder
  [CHUNK_SIZE=...]
  [CHUNK_OVERLAP=...]
  [OUTPUT_DIR=...]
  [ENV_DEV=TRUE|FALSE]
```

e.g.:

```bash
./run_pdf_strategies.sh FILE_OR_FOLDER=in/ CHUNK_SIZE=200 CHUNK_OVERLAP=20 ENV_DEV=TRUE
```

### Flags

- `--file`: Path to the PDF file to be processed.
- `--chunk-strategy`: The strategy used for chunking the content.
- `--chunk-size`: Size of each chunk in the chunk strategy unit. (Default: `200`)
- `--chunk-overlap`: Overlap size between chunks in characters. (Default: `64`)
- `--chunk-separator`: Separator(s) to use for chunking. Can be specified multiple times for multiple separators.
- `--output-folder`: Output folder where the `.jsonl` files will be generated. (Default: `/out`)
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
- [`by_token_huggingface`](https://python.langchain.com/docs/how_to/split_by_token/#hugging-face-tokenizer): ???

</br>

### Examples

</br>
</br>

# Development

### Setup environments and resources

#### Setup virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Download resources

```bash
python setup_nlp_resources.py
```

</br>

### Execute in development

```bash
python -m src.cli.root <command> [--flags]
```