import os
import httpx
import asyncio
from shutil import rmtree
from pathlib import Path
from tqdm.asyncio import tqdm
from utils.log import log
from urllib.parse import urlparse
from utils.web import (
    extract_links,
    extract_markdown,
    generate_md_filename_from_link,
)

def start(
    urls: list[str],
    depth: int,
    output_folder: str,
    clean_previous_runs: bool,
    verbose: bool,
) -> None:
    """
    Start the web crawling process.
    1. Look for the URLs from the --url argument(s).
    2. For each URL, crawl the content.
    3. Export the content to Markdown format in the specified output folder.
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

    # log(
    #     verbose=verbose,
    #     message=f"🔍 Discovered {len(urls)} URLs to process.",
    # )

    asyncio.run(crawl_urls(
        urls=urls,
        depth=depth,
        output_folder=output_folder,
        verbose=verbose,
    ))

    log(
        verbose=verbose,
        message=f"✅ Crawling completed. Output files are saved in '{output_folder}'.",
    )


async def crawl_urls(
    urls: List[str],
    depth: int,
    output_folder: str,
    verbose: bool,
) -> None:
    """
    Crawl a single URL and save the content to a Markdown file.
    """
    frontier = set(urls)

    for depth in range(depth + 1):
        tasks = []
        for url in frontier:
            domain = urlparse(url).netloc
            tasks.append(fetch_and_process(url, domain, max_depth - depth, Path(output_dir)))
        results = await tqdm.gather(*tasks)
        new_links = set()
        for link_set in results:
            new_links.update(link_set)
        frontier = new_links - visited_urls


async def fetch_and_process(url: str, domain: str, depth: int, output_dir: Path) -> set[str]:
    async with semaphore:
        if url in visited_urls or depth < 0:
            return set()
        visited_urls.add(url)

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url)
                if resp.status_code != 200 or 'text/html' not in resp.headers.get("Content-Type", ""):
                    return set()
                html = resp.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return set()

        md_text = extract_markdown(html)
        filename = generate_md_filename_from_link(url)
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            f.write(f"# {url}\n\n{md_text}")

        return extract_links(html, url, domain)
