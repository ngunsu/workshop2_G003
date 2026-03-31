import typer
from rich.console import Console
from rich.panel import Panel
from aes_utils import desencriptar

app = typer.Typer(help="Desencripta texto cifrado con AES-256-CBC.")
console = Console()


@app.command()
def main(
    texto_encriptado: str = typer.Argument(..., help="Texto encriptado en formato hex."),
    llave: str = typer.Argument(..., help="Llave secreta usada durante la encriptación."),
):
    """
    Desencripta un hex string y muestra el texto original.

    Extrae el IV, reconstruye el cifrador AES-256-CBC con la llave derivada
    y remueve el padding PKCS#7.
    """
    try:
        resultado = desencriptar(texto_encriptado, llave)
        console.print(
            Panel(f"[bold cyan]{resultado}[/]", title="Texto Desencriptado", expand=False)
        )
    except ValueError:
        console.print("[bold red]Error:[/] llave incorrecta o texto encriptado inválido.")
        raise typer.Exit(code=1)
    except UnicodeDecodeError:
        console.print("[bold red]Error:[/] el texto desencriptado no es UTF-8 válido.")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
