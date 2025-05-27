from typing import List

def greedy_chunking(text: str, chunk_size: int) -> List[str]:
  """
  Does a simple word-based fixed-lenght chunking of the text.
  (Splits the text into chunks of approximately chunk_size words each)
  
  Args:
    text (str): The input text to be chunked.
    chunk_size (int): The maximum number of words per chunk.
      
  Returns:
    list: A list of text chunks.
  """
  words: List[str] = text.split()
  chunks: List[str] = []
  
  for i in range(0, len(words), chunk_size):
    chunk: str = ' '.join(words[i:i + chunk_size])
    chunks.append(chunk)
  
  return chunks