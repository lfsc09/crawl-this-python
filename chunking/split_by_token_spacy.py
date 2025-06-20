from typing import List


def split(
    text: str, chunk_size: int | None = None, chunk_separator: str | None = None
) -> List[str]:
    """
    https://python.langchain.com/docs/how_to/split_by_token/#spacy

    USE SPACY DOWNLOADER:
    `python -m spacy download <pkg>`

    LangChain implements splitters based on the spaCy tokenizer.

    1. How the text is split: by spaCy tokenizer.
    2. How the chunk size is measured: by number of characters.

    Args:
        text (str): The text to be split.
        chunk_size (int): The size of each chunk. **Should be greater then 200, spaCy uses a chunk overlap by default of 200**
        chunk_separator (str): The separator to use for splitting the text.

    Returns:
        List[str]: A list of text chunks.
    """
    from langchain_text_splitters import SpacyTextSplitter

    if chunk_size is None:
        chunk_size = 1000
    if not chunk_separator:
        chunk_separator = "\n\n"

    return SpacyTextSplitter(
        separator=chunk_separator, chunk_size=chunk_size
    ).split_text(text)
