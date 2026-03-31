import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def _derive_key(llave: str) -> bytes:
    return hashlib.sha256(llave.encode()).digest()


def encriptar(texto: str, llave: str) -> str:
    key = _derive_key(llave)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(texto.encode("utf-8"), AES.block_size))
    # Guardamos IV + ciphertext juntos
    return (iv + ct).hex()


def desencriptar(texto_encriptado: str, llave: str) -> str:
    key = _derive_key(llave)
    data = bytes.fromhex(texto_encriptado)
    iv, ct = data[:16], data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode("utf-8")
