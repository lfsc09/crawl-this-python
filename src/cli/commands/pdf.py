import click
from typing import List, Dict, Any

@click.command()
@click.option(
  "--file",
  "file_path",
  type=click.Path(exists=True, dir_okay=False),
  required=True,
  help="Path to the PDF file to be processed."
)
@click.option(
  "--chunk-strategy",
  type=click.Choice(["by_char", "by_token_tiktoken", "by_token_spacy", "by_token_nltk", "by_token_huggingface"]),
  default="fixed_chunking",
  help="Strategy for chunking the PDF content."
)
@click.option(
  "--chunk-size",
  type=int,
  default=200,
  help="Size of each chunk in characters."
)
@click.option(
  "--chunk-overlap",
  type=int,
  default=64,
  help="Overlap size between chunks in characters."
)
@click.option(
  "--output-folder",
  type=click.Path(file_okay=False),
  default="out",
  show_default=True,
  help="Folder to save the output JSONL files."
)
def pdf(file_path: str, chunk_strategy: str, chunk_size: int, chunk_overlap: int, output_folder: str) -> None:
  """
  Crawl PDF a file, chunk it and export its data to JSONL format.
  """
  import os
  import json
  from PyPDF2 import PdfReader

  # Setup imports
  by_char_handler = None
  by_token_tiktoken_handler = None
  by_token_spacy_handler = None
  by_token_nltk_handler = None
  by_token_huggingface_handler = None

  reader: PdfReader = PdfReader(file_path)
  file_base_name: str = os.path.splitext(os.path.basename(file_path))[0]
  os.makedirs(output_folder, exist_ok=True)
  output_path: str = os.path.join(output_folder, f"{file_base_name}[{chunk_strategy}].jsonl")

  with open(output_path, "w", encoding="utf-8") as output_file:
    for page_num, page in enumerate(reader.pages, start=1):
      content: str = page.extract_text() or ""
      chunks: List[str] = []

      ##
      # Determine chunking strategy.
      # More info in text splitters: https://python.langchain.com/docs/concepts/text_splitters/
      ##
      if chunk_strategy == "by_char":
        if by_char_handler is None:
          from src.chunk.split_by_character import split
          by_char_handler = split
        chunks = by_char_handler(text=content, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

      elif chunk_strategy == "by_token_tiktoken":
        if by_token_tiktoken_handler is None:
          from src.chunk.split_by_token_tiktoken import split
          by_token_tiktoken_handler = split
        chunks = by_token_tiktoken_handler(text=content, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

      elif chunk_strategy == "by_token_spacy":
        if by_token_spacy_handler is None:
          from src.chunk.split_by_token_spacy import split
          by_token_spacy_handler = split
        chunks = by_token_spacy_handler(text=content, chunk_size=chunk_size)

      elif chunk_strategy == "by_token_nltk":
        if by_token_nltk_handler is None:
          from src.chunk.split_by_token_nltk import split
          by_token_nltk_handler = split
        chunks = by_token_nltk_handler(text=content, chunk_size=chunk_size)

      elif chunk_strategy == "by_token_huggingface":
        if by_token_huggingface_handler is None:
          from src.chunk.split_by_token_huggingface import split
          by_token_huggingface_handler = split
        chunks = by_token_huggingface_handler(text=content, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

      # Write chunks to output file
      for chunk_id, chunk in enumerate(chunks, start=1):
        record: Dict[str, Any] = {
          "source": file_path,
          "page_number": page_num,
          "chunk_id": chunk_id,
          "content": chunk
        }
        output_file.write(json.dumps(record, ensure_ascii=False) + "\n")

  click.echo(f"Extracted and chunked {len(reader.pages)} pages to {output_path}, using strategy '{chunk_strategy}' with chunk size {chunk_size} and overlap {chunk_overlap}.")
