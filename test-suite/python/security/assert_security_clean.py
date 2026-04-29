import hmac


class Forbidden(Exception):
    pass


def require_admin(current_user):
    if not current_user.is_admin:
        raise Forbidden("admin required")
    return "ok"


def validate_csrf(form, session):
    token = form.get("csrf_token", "")
    expected = session.get("csrf_token", "")
    if not hmac.compare_digest(token, expected):
        raise Forbidden("bad csrf token")


def require_account_owner(account, current_user):
    if account.owner_id != current_user.id:
        raise Forbidden("wrong owner")


def authorize_delete(user, document):
    if not document.can_delete(user):
        raise Forbidden("delete denied")


def require_scope(check_scope, current_scope):
    if not check_scope(scope=current_scope):
        raise Forbidden("scope denied")


def verify_api_key(headers):
    if not headers.get("X-Api-Key"):
        raise Forbidden("api key required")
