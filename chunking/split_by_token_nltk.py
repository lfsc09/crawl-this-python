from typing import List


def split(
    text: str,
    chunk_size: int | None = None,
    chunk_separator: str | None = None,
    language: str = "english",
) -> List[str]:
    """
    https://python.langchain.com/docs/how_to/split_by_token/#nltk

    USE NLTK DOWNLOADER:
    `python -m nltk.downloader <pkg>`

    Rather than just splitting on "\n\n", we can use NLTK to split based on NLTK tokenizers.

    1. How the text is split: by NLTK tokenizer.
    2. How the chunk size is measured: by number of characters.

    Args:
        text (str): The text to be split.
        chunk_size (int): The size of each chunk.
        chunk_separator (str): The separator to use for splitting the text.
        language (str): The language to use for tokenization (default is "english").

    Returns:
        List[str]: A list of text chunks.
    """
    from langchain_text_splitters import NLTKTextSplitter

    if chunk_size is None:
        chunk_size = 1000
    if chunk_separator is None:
        chunk_separator = "\n\n"

    return NLTKTextSplitter(
        separator=chunk_separator,
        language=language,
        chunk_size=chunk_size,
    ).split_text(text)
