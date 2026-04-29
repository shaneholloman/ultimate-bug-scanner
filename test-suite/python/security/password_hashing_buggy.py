from django.contrib.auth.hashers import make_password
from passlib.context import CryptContext
from passlib.hash import md5_crypt, plaintext as plaintext_hash
from werkzeug.security import generate_password_hash

import passlib.hash as passlib_hash
import werkzeug.security as werkzeug_security


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
    "django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher",
]


def werkzeug_plaintext(password):
    return generate_password_hash(password, method="plain")


def werkzeug_md5_alias(password):
    return werkzeug_security.generate_password_hash(password, "md5")


def werkzeug_pbkdf2_sha1(password):
    return generate_password_hash(password, method="pbkdf2:sha1")


weak_context = CryptContext(schemes=["plaintext", "md5_crypt"])


def passlib_plaintext(password):
    return plaintext_hash.hash(password)


def passlib_md5(password):
    return md5_crypt.hash(password)


def passlib_module_hash(password):
    return passlib_hash.des_crypt.hash(password)


def django_weak_hasher(password):
    return make_password(password, hasher="unsalted_md5")
