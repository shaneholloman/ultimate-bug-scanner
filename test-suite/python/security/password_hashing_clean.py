from django.contrib.auth.hashers import make_password
from passlib.context import CryptContext
from passlib.hash import argon2, bcrypt
from werkzeug.security import generate_password_hash

import passlib.hash as passlib_hash
import werkzeug.security as werkzeug_security


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


def werkzeug_scrypt(password):
    return generate_password_hash(password, method="scrypt")


def werkzeug_pbkdf2_alias(password):
    return werkzeug_security.generate_password_hash(password, "pbkdf2:sha256")


strong_context = CryptContext(schemes=["argon2", "bcrypt", "pbkdf2_sha256"])


def passlib_argon(password):
    return argon2.hash(password)


def passlib_bcrypt(password):
    return bcrypt.hash(password)


def passlib_module_hash(password):
    return passlib_hash.pbkdf2_sha256.hash(password)


def django_default_hasher(password):
    return make_password(password, hasher="pbkdf2_sha256")
