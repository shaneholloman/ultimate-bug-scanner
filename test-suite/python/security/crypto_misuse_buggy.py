from Crypto.Cipher import AES, ARC4, DES
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

STATIC_IV = b"\x00" * 16
STATIC_NONCE = b"fixednonce12"


def pycryptodome_ecb_mode(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)


def pycryptodome_static_cbc_iv(key, data):
    cipher = AES.new(key, AES.MODE_CBC, STATIC_IV)
    return cipher.encrypt(data)


def cryptography_ecb_mode(key):
    return Cipher(algorithms.AES(key), modes.ECB())


def cryptography_static_gcm_nonce(key):
    return Cipher(algorithms.AES(key), modes.GCM(b"000000000000"))


def legacy_des_cipher(key):
    return DES.new(key, DES.MODE_CBC, iv=STATIC_IV)


def legacy_arc4_cipher(key):
    return ARC4.new(key)


def hazmat_arc4_cipher(key):
    return algorithms.ARC4(key)


def aead_static_nonce(key, data):
    aead = AESGCM(key)
    return aead.encrypt(STATIC_NONCE, data, None)
