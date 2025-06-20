# type: ignore
import pymupdf
import os
import json
from shutil import rmtree
from typing import Any, List, Dict
from utils.log import log
from utils.file import discover_files, generate_output_folderpath
from chunking.split_by_separator import (
    split_single_separator as by_separator,
    split_multi_separator as by_separators,
)
from chunking.split_by_token_tiktoken import split as by_token_tiktoken
from chunking.split_by_token_spacy import split as by_token_spacy
from chunking.split_by_token_nltk import split as by_token_nltk
from chunking.split_by_token_huggingface import split as by_token_huggingface


def start(
    file_paths: List[str],
    chunk_strategies: List[str],
    chunk_size: int | None,
    chunk_overlap: int | None,
    chunk_separators: List[str],
    output_folder: str,
    clean_previous_runs: bool,
    verbose: bool,
) -> None:
    """
    Start the PDF crawling process.
    1. Look for the PDF files from the --file argument(s).
    2. For each file, read its content.
    3. Chunk the content based on the specified chunk strategies.
    4. Export the chunks to JSONL format in the specified output folder.
    """
    if clean_previous_runs:
        log(
            verbose=verbose,
            message=f"🧹 Cleaning previous runs in '{output_folder}'.",
        )
        rmtree(output_folder, ignore_errors=True)
        os.makedirs(output_folder, exist_ok=False)
    else:
        os.makedirs(output_folder, exist_ok=True)

    files_to_crawl = discover_files(
        paths=file_paths,
        extensions=(".pdf",),
    )

    log(
        verbose=verbose,
        message=f"🔍 Discovered {len(files_to_crawl)} PDF files to process.",
    )

    for file_path in files_to_crawl:
        crawl_file(
            file_path=file_path,
            chunk_strategies=chunk_strategies,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            chunk_separators=chunk_separators,
            output_folder=output_folder,
            verbose=verbose,
        )

    log(
        verbose=verbose,
        message=f"✅ Crawling completed. Output files are saved in '{output_folder}'.",
    )


def crawl_file(
    file_path: str,
    chunk_strategies: List[str],
    chunk_size: int | None,
    chunk_overlap: int | None,
    chunk_separators: List[str],
    output_folder: str,
    verbose: bool,
) -> None:
    """
    Crawl PDF a file, chunk it and export its data to JSONL format.
    """
    doc = pymupdf.open(file_path)

    log(
        verbose=verbose,
        message=f"📊 Processing file '{file_path}' that [{doc.page_count}] pages.",
    )

    for chunk_strategy in chunk_strategies:
        output_filename = os.path.basename(file_path).replace(".pdf", "")
        output_foldername = generate_output_folderpath(
            chunk_strategy, chunk_size, chunk_overlap, output_folder
        )
        output_filepath = f"{output_foldername}/{output_filename}.jsonl"

        rmtree(output_foldername, ignore_errors=True)
        os.makedirs(output_foldername, exist_ok=True)

        with open(output_filepath, "w", encoding="utf-8") as output_file:
            for page_number, page in enumerate(doc, start=1):
                content = page.get_text("text")
                chunks: List[str] = []

                ##
                # Determine chunking strategy.
                # More info in text splitters: https://python.langchain.com/docs/concepts/text_splitters/
                ##
                if chunk_strategy == "by_separator":
                    separator = chunk_separators[0] if chunk_separators else ""
                    chunks = by_separator(
                        text=content,
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap,
                        chunk_separator=separator,
                    )

                elif chunk_strategy == "by_separators":
                    separators = (
                        chunk_separators
                        if chunk_separators
                        else ("\n\n", "\n", " ", "")
                    )
                    chunks = by_separators(
                        text=content,
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap,
                        chunk_separators=separators,
                    )

                elif chunk_strategy == "by_token_tiktoken":
                    chunks = by_token_tiktoken(
                        text=content, chunk_size=chunk_size, chunk_overlap=chunk_overlap
                    )

                elif chunk_strategy == "by_token_spacy":
                    separator = chunk_separators[0] if chunk_separators else ""
                    chunks = by_token_spacy(
                        text=content, chunk_size=chunk_size, chunk_separator=separator
                    )

                elif chunk_strategy == "by_token_nltk":
                    separator = chunk_separators[0] if chunk_separators else ""
                    chunks = by_token_nltk(
                        text=content, chunk_size=chunk_size, chunk_separator=separator
                    )

                elif chunk_strategy == "by_token_huggingface":
                    chunks = by_token_huggingface(
                        text=content, chunk_size=chunk_size, chunk_overlap=chunk_overlap
                    )

                for chunk_id, chunk in enumerate(chunks):
                    record: Dict[str, Any] = {
                        "source": f"{output_filename}#page={page_number}",
                        "page_number": page_number,
                        "chunk_id": chunk_id,
                        "content": chunk,
                    }
                    json.dump(record, output_file, ensure_ascii=False)
                    output_file.write("\n")
