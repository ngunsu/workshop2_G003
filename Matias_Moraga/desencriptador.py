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
	Desencripta un hex string producido por encriptador.py y muestra el texto original.

	Extrae el IV de los primeros 16 bytes, reconstruye el cifrador AES-256-CBC
	con la llave derivada y remueve el padding PKCS#7 para recuperar el texto plano.

	Parameters
	----------
	texto_encriptado : str
		Cadena hexadecimal generada por encriptador.py.
	llave : str
		Contraseña secreta idéntica a la usada durante la encriptación.
	"""
	try:
		resultado = desencriptar(texto_encriptado, llave)
		console.print(
			Panel(f"[bold cyan]{resultado}[/]", title="Texto Desencriptado", expand=False)
		)
	except Exception:
		console.print("[bold red]Error:[/] llave incorrecta o texto encriptado inválido.")
		raise typer.Exit(code=1)


if __name__ == "__main__":
	app()
