"""`__main__.py` file adds support for running like: `python -m convertion -h`."""

from .cli import convertion_cli

if __name__ == "__main__":
    convertion_cli()
