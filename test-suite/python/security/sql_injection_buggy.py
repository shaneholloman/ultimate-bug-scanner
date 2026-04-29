from flask import request
from sqlalchemy import text

import pandas as pd


def sqlite_concatenated_query(conn):
    username = request.args["user"]
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return conn.execute(query)


def sqlite_fstring_query(cursor):
    account_id = request.args["account_id"]
    return cursor.execute(f"SELECT * FROM accounts WHERE id = {account_id}")


def sqlite_percent_query(cursor):
    email = request.args["email"]
    sql = "SELECT * FROM users WHERE email = '%s'" % email
    return cursor.execute(sql)


def sqlalchemy_text_query(session):
    tenant = request.args["tenant"]
    statement = text(f"SELECT * FROM invoices WHERE tenant_id = {tenant}")
    return session.execute(statement)


def django_raw_query(User):
    email = request.GET["email"]
    return User.objects.raw("SELECT * FROM auth_user WHERE email = '{}'".format(email))


def django_extra_where(User):
    username = request.GET["username"]
    return User.objects.extra(where=[f"username = '{username}'"])


def pandas_read_sql(conn):
    event_id = request.args["event_id"]
    query = f"SELECT * FROM events WHERE id = {event_id}"
    return pd.read_sql_query(query, conn)
