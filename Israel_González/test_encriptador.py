from aes_utils import encriptar


def test_encriptar_retorna_hex():
    resultado = encriptar("hola", "llave")
    assert isinstance(resultado, str)
    bytes.fromhex(resultado)  # no debe lanzar excepción


def test_encriptar_longitud_minima():
    # IV (16 bytes) + al menos un bloque (16 bytes) → 64 chars hex mínimo
    resultado = encriptar("a", "llave")
    assert len(resultado) >= 64


def test_encriptar_diferente_cada_vez():
    # El IV aleatorio hace que cada llamada produzca un resultado distinto
    r1 = encriptar("mismo texto", "misma llave")
    r2 = encriptar("mismo texto", "misma llave")
    assert r1 != r2


def test_encriptar_texto_largo():
    texto = "A" * 1000
    resultado = encriptar(texto, "llave_larga_segura")
    assert isinstance(resultado, str)
    bytes.fromhex(resultado)
