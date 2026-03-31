import pytest
from aes_utils import encriptar, desencriptar


def test_roundtrip_basico():
    texto = "Este es un mensaje secreto"
    llave = "mi_llave_secreta"
    assert desencriptar(encriptar(texto, llave), llave) == texto


def test_roundtrip_caracteres_especiales():
    texto = "¡Hola! Ñoño 123 @#$"
    llave = "llave_con_ñ"
    assert desencriptar(encriptar(texto, llave), llave) == texto


def test_llave_incorrecta_falla():
    encriptado = encriptar("secreto", "llave_correcta")
    with pytest.raises((ValueError, UnicodeDecodeError)):
        desencriptar(encriptado, "llave_incorrecta")


def test_hex_invalido_falla():
    with pytest.raises(ValueError):
        desencriptar("no_es_hex_valido", "llave")


def test_roundtrip_texto_largo():
    texto = "Mensaje " * 100
    llave = "super_secreta"
    assert desencriptar(encriptar(texto, llave), llave) == texto
