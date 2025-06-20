import argparse
import codecs

def decode_escape(value: str) -> str:
    """
    Decode escape sequences in a string.

    Args:
        value (str): The string to decode.

    Returns:
        str: The decoded string.
    """
    try:
        return codecs.decode(value, 'unicode_escape')
    except Exception:
        raise argparse.ArgumentTypeError(
            f"Invalid escape sequence in value: {value}"
        )