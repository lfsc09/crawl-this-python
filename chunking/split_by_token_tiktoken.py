from typing import List


def split(
    text: str, chunk_size: int | None = None, chunk_overlap: int | None = None
) -> List[str]:
    """
    https://python.langchain.com/docs/how_to/split_by_token/#tiktoken

    Uses tiktoken to estimate tokens used. It will probably be more accurate for the OpenAI models.

    1. How the text is split: by character passed in.
    2. How the chunk size is measured: by tiktoken tokenizer.

    Args:
        text (str): The text to be split.
        chunk_size (int): The size of each chunk.
        chunk_overlap (int): The number of characters that should overlap between chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    from langchain_text_splitters import CharacterTextSplitter

    if chunk_size is None:
        chunk_size = 100
    if chunk_overlap is None:
        chunk_overlap = 0

    return CharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base", chunk_size=chunk_size, chunk_overlap=chunk_overlap
    ).split_text(text)
