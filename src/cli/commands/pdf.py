import os
import click
import json
from typing import List, Dict, Any
from PyPDF2 import PdfReader
from src.chunk.greedy_chunking import greedy_chunking

@click.command()
@click.option("--file", "file_path", type=click.Path(exists=True, dir_okay=False), required=True, help="Path to the PDF file to be processed.")
@click.option("--chunk-strategy", type=str, default="greedy_chunking", help="Strategy for chunking the PDF content.")
@click.option("--chunk-size", type=int, default=200, help="Size of each chunk in characters.")
@click.option("--output-folder", type=click.Path(file_okay=False), default="out", show_default=True, help="Folder to save the output JSONL files.")
def pdf(file_path: str, chunk_strategy: str, chunk_size: int, output_folder: str) -> None:
  """
  Crawl PDF a file and export its data to JSONL format.
  """
  reader: PdfReader = PdfReader(file_path)
  file_base_name: str = os.path.splitext(os.path.basename(file_path))[0]
  os.makedirs(output_folder, exist_ok=True)
  output_path: str = os.path.join(output_folder, f"{file_base_name}.jsonl")

  with open(output_path, "w", encoding="utf-8") as output_file:
    for page_num, page in enumerate(reader.pages, start=1):
      content: str = page.extract_text() or ""
      chunks: List[str] = []

      # Determine chunking strategy
      if chunk_strategy == "greedy_chunking":
        chunks = greedy_chunking(content, chunk_size)

      for chunk_id, chunk in enumerate(chunks, start=1):
        record: Dict[str, Any] = {
          "source": file_path,
          "page_number": page_num,
          "chunk_id": chunk_id,
          "content": chunk
        }
        output_file.write(json.dumps(record, ensure_ascii=False) + "\n")

  click.echo(f"Extracted and chunked {len(reader.pages)} pages to {output_path}")
