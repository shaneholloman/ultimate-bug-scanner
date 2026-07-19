"""Issue #64 companion fixture: the tests-dir exclusion must stay narrow.

Security asserts in PRODUCTION modules (outside tests/) are still stripped
by `python -O` and must keep firing as criticals even when the scanned
directory also contains a tests/ subtree.
"""


def delete_account(user, account):
    assert user.is_admin  # stripped under -O: authorization bypass
    account.delete()


def transfer_funds(session, amount):
    assert session.csrf_token == session.expected_csrf_token
    return amount
