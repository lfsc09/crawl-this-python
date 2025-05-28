from typing import List

def split(text: str, chunk_size: int = 100, chunk_overlap: int = 0) -> List[str]:
  """
  https://python.langchain.com/docs/how_to/split_by_token/#hugging-face-tokenizer
  
  We use Hugging Face tokenizer, the GPT2TokenizerFast to count the text length in tokens.

  1. How the text is split: by character passed in.
  2. How the chunk size is measured: by number of tokens calculated by the Hugging Face tokenizer.

  Args:
      text (str): The text to be split.
      chunk_size (int): The size of each chunk.
      chunk_overlap (int): The number of characters that should overlap between chunks.

  Returns:
      List[str]: A list of text chunks.
  """
  # from transformers import GPT2TokenizerFast
  # from langchain_text_splitters import CharacterTextSplitter

  # tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
  # return CharacterTextSplitter.from_huggingface_tokenizer(
  #   tokenizer,
  #   chunk_size=chunk_size,
  #   chunk_overlap=chunk_overlap
  # ).split_text(text)
  raise NotImplementedError("Hugging Face tokenizer is not implemented yet.")