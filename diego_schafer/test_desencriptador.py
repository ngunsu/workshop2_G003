"""
Pruebas unitarias para la función desencriptar de aes_utils.py
"""

import pytest
from aes_utils import encriptar, desencriptar


def test_roundtrip_basico():
    """
    Verifica que un texto basico se encripte y desencripte correctamente
    usando la misma llave.
    """
    texto = "Este es un mensaje secreto"
    llave = "mi_llave_secreta"
    assert desencriptar(encriptar(texto, llave), llave) == texto


def test_roundtrip_caracteres_especiales():
    """
    Comprueba que caracteres especiales y acentos se encripten y desencripten
    sin perdida de informacion.
    """
    texto = "¡Hola! Ñoño 123 @#$"
    llave = "llave_con_ñ"
    assert desencriptar(encriptar(texto, llave), llave) == texto


def test_llave_incorrecta_falla():
    """
    Valida que desencriptar con una llave incorrecta lance una excepcion.
    """
    encriptado = encriptar("secreto", "llave_correcta")
    with pytest.raises(Exception):
        desencriptar(encriptado, "llave_incorrecta")


def test_hex_invalido_falla():
    """
    Comprueba que desencriptar un string que no es hexadecimal valido
    lance una excepcion.
    """
    with pytest.raises(Exception):
        desencriptar("no_es_hex_valido", "llave")


def test_roundtrip_texto_largo():
    """
    Verifica que textos largos se encripten y desencripten correctamente
    manteniendo la integridad del contenido.
    """
    texto = "Mensaje " * 100
    llave = "super_secreta"
    assert desencriptar(encriptar(texto, llave), llave) == texto


# Se agregaron comentarios explicativos de """ """ para cada funcion.
