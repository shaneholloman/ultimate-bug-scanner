import hmac

from flask import request, session


def webhook_signature_check(payload, signing_secret):
    expected_signature = hmac.new(signing_secret, payload, "sha256").hexdigest()
    provided_signature = request.headers["X-Signature"]
    return provided_signature == expected_signature


def api_key_check(request_api_key, stored_api_key):
    if request_api_key != stored_api_key:
        return False
    return True


def csrf_token_check(csrf_token):
    assert csrf_token == session["csrf_token"]


def password_reset_check(token, user):
    return token == user.reset_token


def webhook_digest_check(payload, provided_sig):
    digest = calculate_webhook_digest(payload)
    if digest == provided_sig:
        return "accepted"
    return "rejected"


def bearer_token_check(headers, expected_token):
    return headers["Authorization"] == expected_token


def calculate_webhook_digest(payload):
    return hmac.new(b"key", payload, "sha256").hexdigest()
