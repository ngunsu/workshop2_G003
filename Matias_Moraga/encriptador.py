import typer
from rich.console import Console
from rich.panel import Panel

from aes_utils import encriptar

app = typer.Typer(help="Encripta texto usando AES-256-CBC.")
console = Console()


@app.command()
def main(
	texto: str = typer.Argument(..., help="Texto plano a encriptar."),
	llave: str = typer.Argument(..., help="Llave secreta para la encriptación."),
):
	"""
	Encripta un texto usando AES-256-CBC y muestra el resultado en consola.

	Deriva la llave mediante SHA-256, genera un IV aleatorio y produce una
	cadena hexadecimal con formato ``<iv><ciphertext>``.

	Parameters
	----------
	texto : str
		Texto plano que se desea proteger.
	llave : str
		Contraseña secreta; se deriva internamente a 32 bytes con SHA-256.
	"""
	resultado = encriptar(texto, llave)
	console.print(Panel(f"[bold green]{resultado}[/]", title="Texto Encriptado", expand=False))


if __name__ == "__main__":
	app()
