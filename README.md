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

```bash
crawl pdf [--flags]
```

### Flags

- `--file`: Path to the PDF file to be processed.
- `--chunk-strategy`: The strategy used for chunking the content.
- `--chunk-size`: Size of each chunk in the chunk strategy unit.
- `--output-folder`: Output folder where the `.jsonl` files will be generated.

#### Chunking strategies

- **Greedy Word** (Word-based fixed-length): Splits the text into words and then greedily groups words together into chunks, ensuring that each chunk does not exceed a specified maximum character length.

</br>

### Examples

</br>
</br>

# Development

### Execute in development

```bash
python -m src.cli.root <command> [--flags]
```