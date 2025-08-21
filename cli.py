#!/usr/bin/env python3

from typing import Optional
import typer

app = typer.Typer()


@app.command()
def main(name: Optional[str] = typer.Option(None, "--name", "-n", help="Name to greet")) -> None:
    """Simple CLI application that greets users."""
    if name:
        typer.echo(f"Hello {name}!")
    else:
        typer.echo("Hello World!")


if __name__ == "__main__":
    app()