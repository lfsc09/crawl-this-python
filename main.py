import argparse

from utils.decode import decode_escape
from commands.pdf import start as pdf_start

CHUNK_STRATEGIES = [
    "by_separator",
    "by_separators",
    "by_token_tiktoken",
    "by_token_spacy",
    "by_token_nltk",
    # "by_token_huggingface",
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crawl data from websites or pdf files, chunk them using different strategies, and store them in .jsonl files.",
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # Subparser for the 'pdf' command
    pdf_parser = subparsers.add_parser("pdf", help="Crawl data from PDF files")
    pdf_parser.add_argument(
        "--file",
        action="append",
        type=str,
        required=True,
        help="Path to the PDF file or files to be processed.",
    )
    pdf_parser.add_argument(
        "--chunk-strategy",
        choices=["all", *CHUNK_STRATEGIES],
        nargs="+",
        required=True,
        help="Strategy for chunking the PDF content.",
    )
    pdf_parser.add_argument(
        "--chunk-size",
        type=int,
        default=None,
        help="Size of each chunk in 'chunk_strategy' unit.",
    )
    pdf_parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=None,
        help="Overlap size between chunks in 'chunk_strategy' unit.",
    )
    pdf_parser.add_argument(
        "--chunk-separator",
        type=decode_escape,
        default=[],
        nargs="*",
        help="Separator(s) to use for chunking. Can be specified multiple times for multiple separators.",
    )
    pdf_parser.add_argument(
        "--output-folder",
        type=str,
        default="out",
        help="Folder to save the output JSONL files.",
    )
    pdf_parser.add_argument(
        "--clean-previous",
        action="store_true",
        default=False,
        help="Clean the output folder before running the command.",
    )
    pdf_parser.add_argument(
        "--verbose", action="store_true", default=False, help="Enable verbose output."
    )
    pdf_parser.set_defaults(func=pdf_start)

    # Parse
    args = parser.parse_args()

    if args.command == "pdf":
        if "all" in args.chunk_strategy:
            args.chunk_strategy = CHUNK_STRATEGIES

        # Validate pdf flags
        if (
            args.chunk_size is not None
            and args.chunk_overlap is not None
            and args.chunk_size < args.chunk_overlap
        ):
            parser.error("Chunk size must be greater than or equal to chunk overlap.")
        if (
            "by_separator" in args.chunk_strategy
            or "by_token_spacy" in args.chunk_strategy
            or "by_token_nltk" in args.chunk_strategy
        ) and len(args.chunk_separator) > 1:
            parser.error(
                "Only one separator can be used with ('by_separator', 'by_token_nltk' and 'by_token_spacy') strategies. Use 'by_separators' alone for multiple separators."
            )

        print(f"Using chunk separators: {args.chunk_separator}")

        # Dispatch
        args.func(
            file_paths=args.file,
            chunk_strategies=args.chunk_strategy,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            chunk_separators=args.chunk_separator,
            output_folder=args.output_folder,
            clean_previous_runs=args.clean_previous,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    main()
