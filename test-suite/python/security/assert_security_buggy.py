from flask import request, session


def require_admin(current_user):
    assert current_user.is_admin
    return "ok"


def validate_csrf(form):
    assert form.get("csrf_token") in session["csrf_tokens"]


def require_account_owner(account, current_user):
    assert account.owner_id == current_user.id


def authorize_delete(user, document):
    assert document.can_delete(user)


def require_scope(check_scope, current_scope):
    assert check_scope(scope=current_scope)


def verify_api_key(headers):
    assert headers.get("X-Api-Key")


def require_bearer_token():
    assert request.headers.get("Authorization", "").startswith("Bearer ")
