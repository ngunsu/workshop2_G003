"""
Pruebas unitarias para la funcion encriptar de aes_utils.py
"""

# Se elimino import pytest porque no se esta utilizando en las pruebas

from aes_utils import encriptar


def test_encriptar_retorna_hex():
    """
    Verifica que la función encriptar retorne un string en formato
    hexadecimal válido que pueda convertirse a bytes sin error.
    """
    resultado = encriptar("hola", "llave")
    assert isinstance(resultado, str)
    bytes.fromhex(resultado)


def test_encriptar_longitud_minima():
    """
    IV (16 bytes) + al menos un bloque (16 bytes) → 64 chars hex mínimo
    """
    resultado = encriptar("a", "llave")
    assert len(resultado) >= 64


def test_encriptar_diferente_cada_vez():
    """
    El IV aleatorio hace que cada llamada produzca un resultado distinto
    """
    r1 = encriptar("mismo texto", "misma llave")
    r2 = encriptar("mismo texto", "misma llave")
    assert r1 != r2

    # se cambio == a != para verificar que cada encriptacion con el mismo texto y llave produce resultados diferentes.


def test_encriptar_texto_largo():
    """
    Valida que encriptar textos largos siga retornando un string en formato
    hexadecimal valido y sin errores al convertirlo a bytes
    """
    texto = "A" * 1000
    resultado = encriptar(texto, "llave_larga_segura")
    assert isinstance(resultado, str)
    bytes.fromhex(resultado)


# Se cambiaron los comentarios explicativos de las funciones ya hechos de # a """ """
