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
    try:
        resultado = desencriptar(texto_encriptado, llave)
        console.print(
            Panel(f"[bold cyan]{resultado}[bold cyan]", title="Texto Desencriptado", expand=False)
        )
    except Exception:
        console.print("[bold red]Error:[bold red] llave incorrecta o texto encriptado inválido.")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
