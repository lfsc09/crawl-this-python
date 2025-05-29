import click
from typing import List, Dict, Tuple, Any

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
  type=click.Choice(["by_separator", "by_separators", "by_token_tiktoken", "by_token_spacy", "by_token_nltk", "by_token_huggingface"]),
  required=True,
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
  "--chunk-separator",
  type=str,
  multiple=True,
  help="Separator(s) to use for chunking. Can be specified multiple times for multiple separators."
)
@click.option(
  "--output-folder",
  type=click.Path(file_okay=False),
  default="out",
  show_default=True,
  help="Folder to save the output JSONL files."
)
@click.option(
  "--verbose",
  is_flag=True,
  default=False,
  help="Enable verbose output."
)
def pdf(file_path: str, chunk_strategy: str, chunk_size: int, chunk_overlap: int, chunk_separator: Tuple[str, ...], output_folder: str, verbose: bool) -> None:
  """
  Crawl PDF a file, chunk it and export its data to JSONL format.
  """
  import os
  import json
  from PyPDF2 import PdfReader

  # Validate flags
  if chunk_size < chunk_overlap:
    raise click.BadParameter("Chunk size must be greater than or equal to chunk overlap.")
  if chunk_strategy == "by_separator" and len(chunk_separator) > 1:
    raise click.BadParameter("Only one separator can be used with 'by_separator' strategy. Use 'by_separators' for multiple separators.")
  
  # Setup imports
  by_separator_handler = None
  by_separators_handler = None
  by_token_tiktoken_handler = None
  by_token_spacy_handler = None
  by_token_nltk_handler = None
  by_token_huggingface_handler = None

  reader: PdfReader = PdfReader(file_path)
  file_base_name: str = os.path.splitext(os.path.basename(file_path))[0]
  os.makedirs(output_folder, exist_ok=True)
  output_path: str = os.path.join(output_folder, f"{file_base_name}[{chunk_strategy}].jsonl")

  log(verbose, f"Processes PDF file '{file_path}' with [{len(reader.pages)}] pages using:\n  Chunk strategy: '{chunk_strategy}'\n  Chunk size: {chunk_size}\n  Chunk overlap: {chunk_overlap}")
  with open(output_path, "w", encoding="utf-8") as output_file:
    handler_parameters: Dict[str, Any] = {
      "chunk_size": chunk_size,
      "chunk_overlap": chunk_overlap,
    }
    if chunk_strategy == "by_separator":
      handler_parameters["chunk_separator"] = chunk_separator[0] if chunk_separator else ""
      log(verbose, f"  Using separator: '{handler_parameters['chunk_separator']}'")
    elif chunk_strategy == "by_separators":
      handler_parameters["chunk_separators"] = chunk_separator if chunk_separator else ("\n\n", "\n", " ", "")
      log(verbose, f"  Using separators: {handler_parameters['chunk_separators']}")

    for page_num, page in enumerate(reader.pages, start=1):
      content: str = page.extract_text() or ""
      chunks: List[str] = []

      ##
      # Determine chunking strategy.
      # More info in text splitters: https://python.langchain.com/docs/concepts/text_splitters/
      ##
      if chunk_strategy == "by_separator":
        if by_separator_handler is None:
          from src.chunk.split_by_separator import split_single_separator as split
          by_separator_handler = split
        chunks = by_separator_handler(text=content, **handler_parameters)

      elif chunk_strategy == "by_separators":
        if by_separators_handler is None:
          from src.chunk.split_by_separator import split_multi_separator as split
          by_separators_handler = split
        chunks = by_separators_handler(text=content, **handler_parameters)

      elif chunk_strategy == "by_token_tiktoken":
        if by_token_tiktoken_handler is None:
          from src.chunk.split_by_token_tiktoken import split
          by_token_tiktoken_handler = split
        chunks = by_token_tiktoken_handler(text=content, **handler_parameters)

      elif chunk_strategy == "by_token_spacy":
        if by_token_spacy_handler is None:
          from src.chunk.split_by_token_spacy import split
          by_token_spacy_handler = split
        chunks = by_token_spacy_handler(text=content, **handler_parameters)

      elif chunk_strategy == "by_token_nltk":
        if by_token_nltk_handler is None:
          from src.chunk.split_by_token_nltk import split
          by_token_nltk_handler = split
        chunks = by_token_nltk_handler(text=content, **handler_parameters)

      elif chunk_strategy == "by_token_huggingface":
        if by_token_huggingface_handler is None:
          from src.chunk.split_by_token_huggingface import split
          by_token_huggingface_handler = split
        chunks = by_token_huggingface_handler(text=content, **handler_parameters)

      # Write chunks to output file
      for chunk_id, chunk in enumerate(chunks, start=1):
        record: Dict[str, Any] = {
          "source": file_path,
          "page_number": page_num,
          "chunk_id": chunk_id,
          "content": chunk
        }
        output_file.write(json.dumps(record, ensure_ascii=False) + "\n")

def log(verbose: bool, message: str) -> None:
  """
  Log a message if verbose mode is enabled.
  """
  if verbose:
    click.echo(message)
