import typer
from rich.console import Console
from rich.panel import Panel
from aes_utils import desencriptar

app = typer.Typer(help="Desencripta texto usando AES-256-CBC.")
console = Console()


@app.command()
def main(
    texto_encriptado: str = typer.Argument(..., help="Texto encriptado en hexadecimal."),
    llave: str = typer.Argument(..., help="Llave secreta usada en la encriptación."),
):
    """
    Desencripta un texto en hexadecimal usando AES-256-CBC y muestra el resultado.
    """
    try:
        resultado = desencriptar(texto_encriptado, llave)
        console.print(
            Panel(f"[bold cyan]{resultado}[/]", title="Texto Desencriptado", expand=False)
        )
    except (ValueError, UnicodeDecodeError) as e:
        console.print(
            Panel(f"[bold red]Error: {e}[/]", title="Fallo en desencriptación", expand=False)
        )


if __name__ == "__main__":
    app()
