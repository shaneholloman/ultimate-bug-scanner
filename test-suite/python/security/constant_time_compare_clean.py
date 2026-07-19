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


# Issue #64 regressions: non-secret comparisons that must stay clean.
def orm_column_filter(session, Token, user_uuid):
    # SQLAlchemy ORM expression: the receiver class name (Token) must not
    # make a non-secret column comparison look timing-sensitive.
    return session.query(Token).filter(Token.user_id == user_uuid).all()


def token_budget_check(total_tokens):
    # Comparing a count against a number can never leak secret material.
    if total_tokens == 0:
        return "empty"
    return "has budget"
