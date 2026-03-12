errores iniciales que hay que arreglar mostrados en terminal con pytest -v:

(.venv) PS C:\Users\Usuario\Desktop\Israel_González> pytest -v
========================================================== test session starts ===========================================================
platform win32 -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\Usuario\Desktop\Israel_González\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Usuario\Desktop\Israel_González
configfile: pyproject.toml
collected 9 items                                                                                                                         

test_desencriptador.py::test_roundtrip_basico FAILED                                                                                [ 11%]
test_desencriptador.py::test_roundtrip_caracteres_especiales FAILED                                                                 [ 22%] 
test_desencriptador.py::test_llave_incorrecta_falla PASSED                                                                          [ 33%] 
test_desencriptador.py::test_hex_invalido_falla PASSED                                                                              [ 44%] 
test_desencriptador.py::test_roundtrip_texto_largo FAILED                                                                           [ 55%]
test_encriptador.py::test_encriptar_retorna_hex PASSED                                                                              [ 66%] 
test_encriptador.py::test_encriptar_longitud_minima FAILED                                                                          [ 77%] 
test_encriptador.py::test_encriptar_diferente_cada_vez FAILED                                                                       [ 88%] 
test_encriptador.py::test_encriptar_texto_largo PASSED                                                                              [100%] 

================================================================ FAILURES ================================================================ 
_________________________________________________________ test_roundtrip_basico __________________________________________________________ 

    def test_roundtrip_basico():
        texto = "Este es un mensaje secreto"
        llave = "mi_llave_secreta"
>       assert desencriptar(encriptar(texto, llave), llave) == texto
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

test_desencriptador.py:8:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  
aes_utils.py:107: in desencriptar
    return unpad(cipher.decrypt(ct), AES.block_size * 2).decode()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  

padded_data = b'je secreto\x06\x06\x06\x06\x06\x06', block_size = 32, style = 'pkcs7'

    def unpad(padded_data, block_size, style='pkcs7'):
        """Remove standard padding.

        Args:
          padded_data (byte string):
            A piece of data with padding that needs to be stripped.
          block_size (integer):
            The block boundary to use for padding. The input length
            must be a multiple of :data:`block_size`.
          style (string):
            Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.
        Return:
            byte string : data without padding.
        Raises:
          ValueError: if the padding is incorrect.
        """

        pdata_len = len(padded_data)

        if pdata_len == 0:
            raise ValueError("Zero-length input cannot be unpadded")

        if pdata_len % block_size:
>           raise ValueError("Input data is not padded")
E           ValueError: Input data is not padded

.venv\Lib\site-packages\Crypto\Util\Padding.py:92: ValueError
__________________________________________________ test_roundtrip_caracteres_especiales __________________________________________________ 

    def test_roundtrip_caracteres_especiales():
        texto = "¡Hola! Ñoño 123 @#$"
        llave = "llave_con_ñ"
>       assert desencriptar(encriptar(texto, llave), llave) == texto
                            ^^^^^^^^^^^^^^^^^^^^^^^

test_desencriptador.py:14:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  

texto = '¡Hola! Ñoño 123 @#$', llave = 'llave_con_ñ'

    def encriptar(texto: str, llave: str) -> str:
        """
        Encripta texto plano usando AES-256 en modo CBC.

        Genera un IV aleatorio de 16 bytes por cada llamada, lo antepone al
        ciphertext y devuelve la concatenación IV+ciphertext codificada en
        hexadecimal. El padding PKCS#7 se aplica automáticamente para alinear
        el texto al tamaño de bloque de AES.

        Parameters
        ----------
        texto : str
            Texto plano a encriptar, codificado en UTF-8.
        llave : str
            Llave secreta en texto plano; se deriva internamente a 32 bytes
            mediante SHA-256.

        Returns
        -------
        str
            Cadena hexadecimal con formato ``<iv_hex><ciphertext_hex>``,
            donde los primeros 32 caracteres (16 bytes) corresponden al IV.

        Examples
        --------
        >>> resultado = encriptar("hola mundo", "mi_llave")
        >>> isinstance(resultado, str)
        True
        >>> len(resultado) >= 64  # IV (32 hex) + al menos un bloque (32 hex)
        True
        """
        key = _derive_key(llave)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
>       ct = cipher.encrypt(pad(texto.encode("ascii"), AES.block_size))
                                ^^^^^^^^^^^^^^^^^^^^^
E       UnicodeEncodeError: 'ascii' codec can't encode character '\xa1' in position 0: ordinal not in range(128)

aes_utils.py:62: UnicodeEncodeError
_______________________________________________________ test_roundtrip_texto_largo _______________________________________________________ 

    def test_roundtrip_texto_largo():
        texto = "Mensaje " * 100
        llave = "super_secreta"
>       assert desencriptar(encriptar(texto, llave), llave) == texto
E       AssertionError: assert 'Mensaje Mens...saje Mensaje ' == 'Mensaje Mens...saje Mensaje '
E
E         - Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensaje Mensa...
E
E         ...Full output truncated (3 lines hidden), use '-vv' to show

test_desencriptador.py:31: AssertionError
_____________________________________________________ test_encriptar_longitud_minima _____________________________________________________ 

    def test_encriptar_longitud_minima():
        # IV (16 bytes) + al menos un bloque (16 bytes) → 64 chars hex mínimo
        resultado = encriptar("a", "llave")
>       assert len(resultado) >= 64
E       AssertionError: assert 32 >= 64
E        +  where 32 = len('6f45a1d13f09e762a09be6ab09beab4d')

test_encriptador.py:14: AssertionError
___________________________________________________ test_encriptar_diferente_cada_vez ____________________________________________________ 

    def test_encriptar_diferente_cada_vez():
        # El IV aleatorio hace que cada llamada produzca un resultado distinto
        r1 = encriptar("mismo texto", "misma llave")
        r2 = encriptar("mismo texto", "misma llave")
>       assert r1 == r2
E       AssertionError: assert '203ecbc2924f...8e33cd42f9ce9' == 'd9bac027a854...6aab416dca362'
E
E         - d9bac027a8549bef3746aab416dca362
E         + 203ecbc2924f4d7bb268e33cd42f9ce9

test_encriptador.py:21: AssertionError
======================================================== short test summary info ========================================================= 
FAILED test_desencriptador.py::test_roundtrip_basico - ValueError: Input data is not padded
FAILED test_desencriptador.py::test_roundtrip_caracteres_especiales - UnicodeEncodeError: 'ascii' codec can't encode character '\xa1' in position 0: ordinal not in range(128)
FAILED test_desencriptador.py::test_roundtrip_texto_largo - AssertionError: assert 'Mensaje Mens...saje Mensaje ' == 'Mensaje Mens...saje Mensaje '
FAILED test_encriptador.py::test_encriptar_longitud_minima - AssertionError: assert 32 >= 64
FAILED test_encriptador.py::test_encriptar_diferente_cada_vez - AssertionError: assert '203ecbc2924f...8e33cd42f9ce9' == 'd9bac027a854...6aab416dca362'
====================================================== 5 failed, 4 passed in 0.49s ======================================================= 
(.venv) PS C:\Users\Usuario\Desktop\Israel_González> 

-------------------------------------------------------------------------------------------------------------
ya con todos los errores arreglados:

(.venv) PS C:\Users\Usuario\Desktop\Israel_González> pytest -v
================================================== test session starts ===================================================
platform win32 -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\Usuario\Desktop\Israel_González\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Usuario\Desktop\Israel_González
configfile: pyproject.toml
collected 9 items                                                                                                         

test_desencriptador.py::test_roundtrip_basico PASSED                                                                [ 11%] 
test_desencriptador.py::test_roundtrip_caracteres_especiales PASSED                                                 [ 22%] 
test_desencriptador.py::test_llave_incorrecta_falla PASSED                                                          [ 33%] 
test_desencriptador.py::test_hex_invalido_falla PASSED                                                              [ 44%] 
test_desencriptador.py::test_roundtrip_texto_largo PASSED                                                           [ 55%] 
test_encriptador.py::test_encriptar_retorna_hex PASSED                                                              [ 66%] 
test_encriptador.py::test_encriptar_longitud_minima PASSED                                                          [ 77%] 
test_encriptador.py::test_encriptar_diferente_cada_vez PASSED                                                       [ 88%] 
test_encriptador.py::test_encriptar_texto_largo PASSED                                                              [100%] 

=================================================== 9 passed in 0.04s ==================================================== 
(.venv) PS C:\Users\Usuario\Desktop\Israel_González> 


ahora arreglar todos los errores de los linter con ruff y ya estamos todos listo:

(.venv) PS C:\Users\Usuario\Desktop\Israel_González> python.exe -m ruff check 
F401 [*] `pytest` imported but unused
 --> test_encriptador.py:1:8
  |
1 | import pytest
  |        ^^^^^^
2 | from aes_utils import encriptar
  |
help: Remove unused import: `pytest`

Found 1 error.
[*] 1 fixable with the `--fix` option.
(.venv) PS C:\Users\Usuario\Desktop\Israel_González> python.exe -m ruff check 
All checks passed!
(.venv) PS C:\Users\Usuario\Desktop\Israel_González> python.exe -m ruff check 
All checks passed!