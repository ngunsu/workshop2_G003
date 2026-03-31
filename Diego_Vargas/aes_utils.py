import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def _derive_key(llave: str) -> bytes:
    """
    Deriva una llave AES de 32 bytes a partir de una cadena de texto.

    Aplica SHA-256 sobre la cadena codificada en UTF-8, produciendo siempre
    una salida de longitud fija adecuada para AES-256.

    Parameters
    ----------
    llave : str
        Cadena de texto arbitraria que actúa como contraseña.

    Returns
    -------
    bytes
        Digest SHA-256 de 32 bytes listo para usarse como llave AES-256.
    """
    return hashlib.sha256(llave.encode("utf-8")).digest()


def encriptar(texto: str, llave: str) -> str:
    """
    Encripta texto plano usando AES-256 en modo CBC.

    Genera un IV aleatorio de 16 bytes por cada llamada, lo antepone al
    ciphertext y devuelve la concatenación IV+ciphertext codificada en
    hexadecimal. El padding PKCS#7 se aplica automáticamente.

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
        Cadena hexadecimal con formato ``<iv_hex><ciphertext_hex>``.
    """
    key = _derive_key(llave)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(texto.encode("utf-8"), AES.block_size))
    return (iv + ct).hex()


def desencriptar(texto_encriptado: str, llave: str) -> str:
    """
    Desencripta un hex string producido por :func:`encriptar`.

    Extrae el IV de los primeros 16 bytes, reconstruye el cifrador AES-CBC
    y remueve el padding PKCS#7 para recuperar el texto original.

    Parameters
    ----------
    texto_encriptado : str
        Cadena hexadecimal generada por :func:`encriptar`.
    llave : str
        Llave secreta en texto plano idéntica a la usada al encriptar.

    Returns
    -------
    str
        Texto plano original decodificado en UTF-8.
    """
    key = _derive_key(llave)
    data = bytes.fromhex(texto_encriptado)
    iv, ct = data[:16], data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode("utf-8")
