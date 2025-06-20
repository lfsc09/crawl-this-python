import os


def discover_files(
    paths: list[str],
    extensions: tuple[str, ...] = (".pdf",),
) -> list[str]:
    """
    Return a list of files from the specified paths that match the given extensions.

    Args:
        paths (list[str]): A list of paths (it can be folders) to search for files.
        extensions (tuple[str, ...]): A tuple of file extensions to look for.

    Returns:
        list[str]: A list of discovered file paths.
    """
    discovered_files: list[str] = []
    for path in paths:
        if os.path.isfile(path) and path.endswith(extensions):
            discovered_files.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(extensions):
                        discovered_files.append(os.path.join(root, file))
    return discovered_files


def generate_output_folderpath(
    chunk_strategy: str,
    chunk_size: int | None,
    chunk_overlap: int | None,
    output_folder: str,
) -> str:
    """
    Generate the output folder path based on the chunking parameters.

    Args:
        chunk_strategy (str): The chunking strategy used.
        chunk_size (int): The size of each chunk.
        chunk_overlap (int): The overlap size between chunks.
        output_folder (str): The folder where the output will be saved.

    Returns:
        str: The generated output folder path.
    """
    kebab_case_strategy = chunk_strategy.replace("_", "-")
    return os.path.join(
        output_folder,
        f"{kebab_case_strategy}--{chunk_size if chunk_size != None else "default"}--{chunk_overlap if chunk_overlap != None else "default"}",
    )
