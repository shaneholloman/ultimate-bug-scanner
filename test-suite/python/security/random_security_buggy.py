import random
from random import choices, randint


ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"

reset_token = "".join(random.choice(ALPHABET) for _ in range(32))
session_id = random.getrandbits(128)
otp_code = randint(100000, 999999)
api_key = random.randbytes(32).hex()

rng = random.Random()
csrf_nonce = "".join(rng.choice(ALPHABET) for _ in range(16))


def make_invite_token():
    return "".join(choices(ALPHABET, k=24))


def issue_cookie(response):
    response.set_cookie("session", str(random.randrange(10**12)))
