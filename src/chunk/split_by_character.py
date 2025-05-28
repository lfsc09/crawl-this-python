from typing import List

def split(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
  """
  https://python.langchain.com/docs/how_to/character_text_splitter/
  
  This is the simplest method. This splits based on a given character sequence, which defaults to "\n\n".
  Chunk length is measured by number of characters.

  1. How the text is split: by single character separator.
  2. How the chunk size is measured: by number of characters.

  Args:
      text (str): The text to be split.
      chunk_size (int): The size of each chunk.
      chunk_overlap (int): The number of characters that should overlap between chunks.

  Returns:
      List[str]: A list of text chunks.
  """
  from langchain_text_splitters import CharacterTextSplitter
  
  return CharacterTextSplitter(
    separator="\n\n",
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    lenght_function=len,
    is_separator_regex=False
  ).split_text(text)
