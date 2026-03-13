import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def _derive_key(llave: str) -> bytes:
    """
    Deriva una llave AES de 32 bytes a partir de una cadena de texto.
    """
    return hashlib.sha256(llave.encode("utf-8")).digest()


def encriptar(texto: str, llave: str) -> str:
    """
    Encripta texto plano usando AES-256 en modo CBC.
    Devuelve IV + ciphertext en formato hexadecimal.
    """
    key = _derive_key(llave)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(texto.encode("utf-8"), AES.block_size))
    return (iv + ct).hex()


def desencriptar(texto_encriptado: str, llave: str) -> str:
    key = _derive_key(llave)
    data = bytes.fromhex(texto_encriptado)
    iv, ct = data[:16], data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)  # ✅ usar 16, no 32
    return pt.decode("utf-8")
