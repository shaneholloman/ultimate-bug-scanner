"""Issue #64 regression: pytest-style security asserts inside tests/ are the
expected idiom and must not be flagged as stripped-by--O criticals."""
import os


def test_path_env():
    assert os.environ.get("PATH") == "/usr/bin"


def test_admin_role(user):
    assert user.role == "admin"


def test_session_scope(session):
    assert session.scope == "read-only"
