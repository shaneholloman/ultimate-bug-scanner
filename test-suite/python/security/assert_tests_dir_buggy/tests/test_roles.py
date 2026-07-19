"""Asserts under tests/ remain the expected pytest idiom (not findings),
even in a directory that also contains buggy production asserts."""


def test_role(user):
    assert user.role == "admin"
