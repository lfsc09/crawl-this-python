#!/bin/bash

YELLOW='\033[33m'
NC='\033[0m'

FPATH=""
CHUNK_SIZE=""
CHUNK_OVERLAP=""
OUTPUT_DIR=""
ENV_DEV="FALSE"

# Parse named arguments
for ARG in "$@"; do
  case $ARG in
    FILE_OR_FOLDER=*)
      FPATH="${ARG#*=}"
      ;;
    CHUNK_SIZE=*)
      CHUNK_SIZE="${ARG#*=}"
      ;;
    CHUNK_OVERLAP=*)
      CHUNK_OVERLAP="${ARG#*=}"
      ;;
    OUTPUT_DIR=*)
      OUTPUT_DIR="${ARG#*=}"
      ;;
    ENV_DEV=*)
      ENV_DEV="${ARG#*=}"
      ;;
    *)
      echo -e "${YELLOW}[run.sh] Unknown argument: $ARG${NC}"
      exit 1
      ;;
  esac
done

# Required arguments
if [ -z "$FPATH" ]; then
  echo -e "${YELLOW}[run.sh] Usage: $0 FILE_OR_FOLDER=... [CHUNK_SIZE=...] [CHUNK_OVERLAP=...] [OUTPUT_DIR=...] [ENV_DEV=TRUE|FALSE]${NC}"
  exit 1
fi

# Determine if FPATH is a file or directory
if [ -f "$FPATH" ]; then
  FILES=("$FPATH")
elif [ -d "$FPATH" ]; then
  # Recursively find all .pdf files in the directory
  mapfile -t FILES < <(find "$FPATH" -type f -name '*.pdf')
else
  echo -e "${YELLOW}[run.sh] '$FPATH' is not a valid file or directory.${NC}"
  exit 1
fi

if [ ${#FILES[@]} -eq 0 ]; then
  echo -e "${YELLOW}[run.sh] No files found to process.${NC}"
  exit 1
fi

# Set how to execute python command based on environment
if [ "$ENV_DEV" = "TRUE" ]; then
  PYTHON_CMD="python -m src.cli.root"
# else
  # PYTHON_CMD="python ???"
fi

if [ -z "$PYTHON_CMD" ]; then
  echo -e "${YELLOW}[run.sh] Python executor was not set. Exiting.${NC}"
  exit 1
fi

# Set flags that are optional to python command
if [ -z "$CHUNK_SIZE" ]; then
  CHUNK_SIZE_FLAG=""
else
  CHUNK_SIZE_FLAG="--chunk-size $CHUNK_SIZE"
fi
if [ -z "$CHUNK_OVERLAP" ]; then
  CHUNK_OVERLAP_FLAG=""
else
  CHUNK_OVERLAP_FLAG="--chunk-overlap $CHUNK_OVERLAP"
fi
if [ -z "$OUTPUT_DIR" ]; then
  OUTPUT_FOLDER_FLAG=""
else
  OUTPUT_FOLDER_FLAG="--output-folder $OUTPUT_DIR"
fi

for FILE in "${FILES[@]}"; do
  $PYTHON_CMD pdf --file "$FILE" --chunk-strategy by_separator $CHUNK_SIZE_FLAG $CHUNK_OVERLAP_FLAG $OUTPUT_FOLDER_FLAG &
  $PYTHON_CMD pdf --file "$FILE" --chunk-strategy by_separators  $CHUNK_SIZE_FLAG $CHUNK_OVERLAP_FLAG $OUTPUT_FOLDER_FLAG &
  $PYTHON_CMD pdf --file "$FILE" --chunk-strategy by_token_tiktoken $CHUNK_SIZE_FLAG $CHUNK_OVERLAP_FLAG $OUTPUT_FOLDER_FLAG &
  $PYTHON_CMD pdf --file "$FILE" --chunk-strategy by_token_spacy $CHUNK_SIZE_FLAG $CHUNK_OVERLAP_FLAG $OUTPUT_FOLDER_FLAG &
  $PYTHON_CMD pdf --file "$FILE" --chunk-strategy by_token_nltk $CHUNK_SIZE_FLAG $CHUNK_OVERLAP_FLAG $OUTPUT_FOLDER_FLAG &
done

wait
echo -e "${YELLOW}[run.sh] All processes completed.${NC}"
