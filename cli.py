#!/usr/bin/env python3

import typer
from typing import Optional

app = typer.Typer()


@app.command()
def main(name: Optional[str] = typer.Option(None, "--name", "-n", help="Name to greet")) -> None:
    """Simple greeting CLI application."""
    if name:
        typer.echo(f"Hello {name}!")
    else:
        typer.echo("Hello World!")


if __name__ == "__main__":
    app()