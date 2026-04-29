from django_auth_ldap.config import LDAPSearch
from flask import request
from ldap.dn import escape_dn_chars
from ldap.filter import escape_filter_chars


def ldap3_search_filter_clean(conn):
    username = escape_filter_chars(request.args["username"])
    search_filter = f"(uid={username})"
    return conn.search("ou=people,dc=example,dc=com", search_filter)


def ldap3_keyword_filter_clean(conn):
    group = escape_filter_chars(request.form["group"])
    return conn.search(
        search_base="ou=groups,dc=example,dc=com",
        search_filter=f"(&(objectClass=groupOfNames)(cn={group}))",
    )


def python_ldap_search_clean(connection, flask_request):
    email = escape_filter_chars(flask_request.args["email"])
    ldap_filter = "(mail=%s)" % email
    return connection.search_s("ou=people,dc=example,dc=com", 2, ldap_filter)


def python_ldap_ext_search_clean(connection):
    department = escape_filter_chars(request.values["department"])
    return connection.search_ext_s(
        "ou=people,dc=example,dc=com",
        2,
        "(&(objectClass=person)(department={}))".format(department),
    )


def ldap3_paged_search_clean(connection):
    surname = escape_filter_chars(request.args["surname"])
    search_filter = f"(sn={surname})"
    return connection.extend.standard.paged_search("ou=people,dc=example,dc=com", search_filter)


def django_auth_ldap_search_clean(django_request):
    username = escape_filter_chars(django_request.GET["username"])
    return LDAPSearch("ou=people,dc=example,dc=com", 2, f"(uid={username})")


def ldap_bind_dn_clean(connection):
    username = escape_dn_chars(request.args["username"])
    dn = f"uid={username},ou=people,dc=example,dc=com"
    return connection.simple_bind_s(dn, "placeholder-password")


def ldap_modify_dn_clean(connection, django_request):
    username = escape_dn_chars(django_request.POST["username"])
    user_dn = "uid=" + username + ",ou=people,dc=example,dc=com"
    return connection.modify_s(user_dn, [])
