import secrets
from random import SystemRandom
from secrets import token_urlsafe


ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"

reset_token = token_urlsafe(32)
session_id = secrets.token_hex(32)
otp_code = secrets.randbelow(900000) + 100000
api_key = secrets.token_bytes(32).hex()
csrf_nonce = "".join(secrets.choice(ALPHABET) for _ in range(16))

system_rng = SystemRandom()
public_sample = system_rng.randrange(10**12)
public_direct = SystemRandom().choice(ALPHABET)


def make_invite_token():
    return token_urlsafe(24)
