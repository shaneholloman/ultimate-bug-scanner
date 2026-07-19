"""Production module with explicit security checks (no asserts)."""


def require_admin(user):
    if not user.is_admin:
        raise PermissionError("admin required")
    return True
