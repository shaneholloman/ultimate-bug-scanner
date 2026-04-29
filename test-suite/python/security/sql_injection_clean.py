from flask import request
from sqlalchemy import text

import pandas as pd


def sqlite_parameterized_query(conn):
    username = request.args["user"]
    query = "SELECT * FROM users WHERE username = ?"
    return conn.execute(query, (username,))


def sqlite_named_parameters(cursor):
    account_id = request.args["account_id"]
    return cursor.execute(
        "SELECT * FROM accounts WHERE id = :account_id",
        {"account_id": account_id},
    )


def sqlalchemy_text_bind_params(session):
    tenant = request.args["tenant"]
    statement = text("SELECT * FROM invoices WHERE tenant_id = :tenant")
    # ubs:ignore - tenant is passed as a SQLAlchemy bind parameter, not interpolated into SQL
    return session.execute(statement, {"tenant": tenant})


def django_raw_params(User):
    email = request.GET["email"]
    return User.objects.raw("SELECT * FROM auth_user WHERE email = %s", [email])


def django_extra_params(User):
    username = request.GET["username"]
    return User.objects.extra(where=["username = %s"], params=[username])


def pandas_read_sql_params(conn):
    event_id = request.args["event_id"]
    return pd.read_sql_query(
        "SELECT * FROM events WHERE id = ?",
        conn,
        params=(event_id,),
    )
