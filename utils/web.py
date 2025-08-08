from urllib.parse import urljoin, urlparse, urldefrag
from bs4 import BeautifulSoup

def generate_md_filename_from_link(url: str) -> str:
    """
    Generate a filename from a URL link.
    
    Returns:
        str: The generated filename.
    """
    import re

    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_")
    name = f"{parsed.netloc}_{path or 'index'}"
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name) + ".md"

def is_internal_link(url: str, domain: str) -> bool:
    """
    Check if a URL is an internal link based on the domain.
    Args:
        url (str): The URL to check.
        domain (str): The domain to compare against.
    Returns:
        bool: True if the URL is an internal link, False otherwise.
    """
    parsed = urlparse(url)
    return (parsed.netloc == "" or parsed.netloc == domain)

def extract_links(html: str, base_url: str, domain: str) -> set[str]:
    """
    Extract all internal links from the HTML content.
    Args:
        html (str): The HTML content to parse.
        base_url (str): The base URL to resolve relative links.
        domain (str): The domain to check for internal links.
    Returns:
        Set[str]: A set of internal links found in the HTML content.
    """
    soup = BeautifulSoup(html, "html.parser")
    links: set[str] = set()
    for tag in soup.find_all("a", href=True):
        href = tag['href'] # type: ignore
        absolute = urljoin(base_url, href) # type: ignore
        clean_url = urldefrag(absolute)[0]
        if is_internal_link(clean_url, domain):
            links.add(clean_url)
    return links

def extract_markdown(html: str) -> str:
    """
    Extract content from HTML by removing scripts, styles, and converting headings to be in a Markdown format.
    Args:
        html (str): The HTML content to convert.
    Returns:
        str: The extracted content in Markdown.
    """
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()
    for i in range(1, 7):
        for tag in soup.find_all(f'h{i}'):
            tag.insert_before(f"\n{'#' * i} {tag.get_text(strip=True)}\n")
            tag.decompose()
    return soup.get_text(separator="\n", strip=True)

