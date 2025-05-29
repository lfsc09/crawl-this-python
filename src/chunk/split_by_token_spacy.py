from typing import List

def split(text: str, chunk_size: int = 1000, chunk_separator: str = "\n\n") -> List[str]:
  """
  https://python.langchain.com/docs/how_to/split_by_token/#spacy

  USE SPACY DOWNLOADER:
  `python -m spacy download <pkg>`
  
  LangChain implements splitters based on the spaCy tokenizer.

  1. How the text is split: by spaCy tokenizer.
  2. How the chunk size is measured: by number of characters.

  Args:
      text (str): The text to be split.
      chunk_size (int): The size of each chunk.
      chunk_separator (str): The separator to use for splitting the text.

  Returns:
      List[str]: A list of text chunks.
  """
  from langchain_text_splitters import SpacyTextSplitter
  
  return SpacyTextSplitter(
    separator=chunk_separator,
    chunk_size=chunk_size
  ).split_text(text)