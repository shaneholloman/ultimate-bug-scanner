import os
import secrets

from Crypto.Cipher import AES
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305


def pycryptodome_gcm_random_nonce(key, data):
    nonce = secrets.token_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.encrypt(data)


def pycryptodome_cbc_random_iv(key, data):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(data)


def cryptography_cbc_random_iv(key):
    iv = os.urandom(16)
    return Cipher(algorithms.AES(key), modes.CBC(iv))


def cryptography_ctr_random_nonce(key):
    counter = secrets.token_bytes(16)
    return Cipher(algorithms.AES(key), modes.CTR(counter))


def aead_random_nonce(key, data):
    nonce = os.urandom(12)
    return AESGCM(key).encrypt(nonce, data, None)


def tracked_aead_random_nonce(key, data):
    aead = ChaCha20Poly1305(key)
    nonce = secrets.token_bytes(12)
    return aead.encrypt(nonce, data, None)
