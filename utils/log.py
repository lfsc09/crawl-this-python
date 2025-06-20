def log(verbose: bool, message: str) -> None:
    """
    Log a message to the console if verbose mode is enabled.

    Args:
        verbose (bool): If True, the message will be printed to the console.
        message (str): The message to log.
    """
    if verbose:
        print(message)
