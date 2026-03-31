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
    return hashlib.sha256(llave.encode()).digest()


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
    ct = cipher.encrypt(pad(texto.encode("utf-8"), AES.block_size))
    return (iv + ct).hex()


def desencriptar(texto_encriptado: str, llave: str) -> str:
    """
    Desencripta un hex string producido por :func:`encriptar`.

    Extrae el IV de los primeros 16 bytes del hex decodificado, reconstruye
    el cifrador AES-CBC y remueve el padding PKCS#7 para recuperar el texto
    original.

    Parameters
    ----------
    texto_encriptado : str
        Cadena hexadecimal generada por :func:`encriptar`, con formato
        ``<iv_hex><ciphertext_hex>``.
    llave : str
        Llave secreta en texto plano; debe ser idéntica a la usada durante
        la encriptación.

    Returns
    -------
    str
        Texto plano original decodificado en UTF-8.

    Raises
    ------
    ValueError
        Si ``texto_encriptado`` no es un hex string válido o el padding
        resultante es incorrecto (llave equivocada).
    UnicodeDecodeError
        Si los bytes desencriptados no pueden interpretarse como UTF-8.

    Examples
    --------
    >>> from aes_utils import encriptar, desencriptar
    >>> texto = "mensaje secreto"
    >>> desencriptar(encriptar(texto, "llave"), "llave") == texto
    True
    """
    key = _derive_key(llave)
    data = bytes.fromhex(texto_encriptado)
    iv, ct = data[:16], data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode("utf-8")
