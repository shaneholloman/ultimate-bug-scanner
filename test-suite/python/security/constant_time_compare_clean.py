import hmac
import secrets

from flask import request, session


def webhook_signature_check(payload, signing_secret):
    expected_signature = hmac.new(signing_secret, payload, "sha256").hexdigest()
    provided_signature = request.headers["X-Signature"]
    return hmac.compare_digest(provided_signature, expected_signature)


def api_key_check(request_api_key, stored_api_key):
    return secrets.compare_digest(request_api_key, stored_api_key)


def csrf_token_check(csrf_token):
    return hmac.compare_digest(csrf_token, session["csrf_token"])


def password_reset_check(token, user):
    return secrets.compare_digest(token, user.reset_token)


def status_check(status, expected_status):
    return status == expected_status


def token_length_check(token):
    return len(token) == 32


def public_identifier_check(user_id, expected_id):
    return user_id == expected_id
