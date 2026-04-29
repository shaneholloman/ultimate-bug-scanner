import jwt
from jose import jwt as jose_jwt
from jwt import decode as decode_jwt


def decode_rs256(token: str, public_key: str):
    return jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience="api",
        issuer="https://issuer.example.com/",
    )


def decode_with_expiration(token: str, key: str):
    return jwt.decode(token, key, algorithms=["HS256"], options={"verify_exp": True})


def jose_decode(token: str, key: str):
    return jose_jwt.decode(token, key, algorithms=["HS256"], audience="api")


def aliased_decode(token: str, key: str):
    return decode_jwt(token, key, algorithms=["HS256"], options={"verify_signature": True})
