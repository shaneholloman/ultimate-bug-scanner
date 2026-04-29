import jwt
from jose import jwt as jose_jwt
from jwt import decode as decode_jwt


def decode_without_signature(token: str):
    return jwt.decode(token, options={"verify_signature": False})


def decode_without_expiration(token: str, key: str):
    return jwt.decode(token, key, algorithms=["HS256"], options={"verify_exp": False})


def decode_without_verify(token: str, key: str):
    return jose_jwt.decode(token, key, algorithms=["HS256"], verify=False)


def decode_none_algorithm(token: str):
    return decode_jwt(token, None, ["none"])
