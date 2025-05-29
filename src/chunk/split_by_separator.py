from typing import List, Tuple

def split_single_separator(text: str, chunk_size: int, chunk_overlap: int, chunk_separator: str = "\n\n") -> List[str]:
  """
  https://python.langchain.com/docs/how_to/character_text_splitter/
  
  This is the simplest method, it splits based on a given "separator" (character sequence).
  Chunk size is measured by "length_function" (by default caracters), but if text does not contain the separator, it will not split.
  To split in characters, use an empty string as the separator.

  Pros:
    - Predictable chunk sizes.
  Cons:
    - May split in the middle of words or sentences, which can lead to loss of context.

  1. How the text is split: by single character separator.
  2. How the chunk size is measured: by number of characters.

  Args:
      text (str): The text to be split.
      chunk_size (int): The size of each chunk.
      chunk_overlap (int): The number of characters that should overlap between chunks.
      chunk_separator (str): The character or string used to separate chunks. Defaults to "\n\n".

  Returns:
      List[str]: A list of text chunks.
  """
  from langchain_text_splitters import CharacterTextSplitter
  
  return CharacterTextSplitter(
    separator=chunk_separator,
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    length_function=len,
    is_separator_regex=False
  ).split_text(text)

def split_multi_separator(text: str, chunk_size: int, chunk_overlap: int, chunk_separators: Tuple[str, ...] = ("\n\n", "\n", " ", "")) -> List[str]:
  """
  https://python.langchain.com/docs/concepts/text_splitters/#text-structured-based
  
  This is a more advanced and smarter method. It tries to split the text at the largest possible logical boundary (like paragraphs, then sentences, then words, then caracters).
  It uses a list of separators, trying each in order, to preserve as much structure as possible.

  Pros:
    - Preservers more natural language structure, avoids splitting in the middle of sentences or words.

  Args:
      text (str): The text to be split.
      chunk_size (int): The size of each chunk.
      chunk_overlap (int): The number of characters that should overlap between chunks.
      chunk_separators (Tuple[str, ...]): A tuple of strings used as separators for splitting the text. Defaults to ("\n\n", "\n", " ", "").

  Returns:
      List[str]: A list of text chunks.
  """
  from langchain_text_splitters import RecursiveCharacterTextSplitter
  
  return RecursiveCharacterTextSplitter(
    separators=list(chunk_separators),
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    length_function=len
  ).split_text(text)
