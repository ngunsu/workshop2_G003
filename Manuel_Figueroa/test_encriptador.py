import pytest
from aes_utils import encriptar


def test_encriptar_retorna_hex():
    resultado = encriptar("hola", "llave")
    assert isinstance(resultado, str)
    bytes.fromhex(resultado)  # no debe lanzar excepción


def test_encriptar_longitud_minima():
    resultado = encriptar("a", "llave")
    assert len(resultado) >= 64  # IV (32 hex) + al menos un bloque (32 hex)


def test_encriptar_diferente_cada_vez():
    r1 = encriptar("mismo texto", "misma llave")
    r2 = encriptar("mismo texto", "misma llave")
    assert r1 != r2  # debe ser distinto por el IV aleatorio


def test_encriptar_texto_largo():
    texto = "A" * 1000
    resultado = encriptar(texto, "llave_larga_segura")
    assert isinstance(resultado, str)
    bytes.fromhex(resultado)