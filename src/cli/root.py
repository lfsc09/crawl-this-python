import click
from src.cli.commands.pdf import pdf

@click.group()
def crawl() -> None:
  pass

crawl.add_command(pdf)

if __name__ == "__main__":
  crawl()
