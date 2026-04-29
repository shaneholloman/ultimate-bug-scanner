from django_auth_ldap.config import LDAPSearch
from flask import request


def ldap3_search_filter(conn):
    username = request.args["username"]
    search_filter = f"(uid={username})"
    return conn.search("ou=people,dc=example,dc=com", search_filter)


def ldap3_keyword_filter(conn):
    group = request.form["group"]
    return conn.search(
        search_base="ou=groups,dc=example,dc=com",
        search_filter=f"(&(objectClass=groupOfNames)(cn={group}))",
    )


def python_ldap_search(connection, flask_request):
    email = flask_request.args["email"]
    ldap_filter = "(mail=%s)" % email
    return connection.search_s("ou=people,dc=example,dc=com", 2, ldap_filter)


def python_ldap_ext_search(connection):
    department = request.values["department"]
    return connection.search_ext_s(
        "ou=people,dc=example,dc=com",
        2,
        "(&(objectClass=person)(department={}))".format(department),
    )


def ldap3_paged_search(connection):
    surname = request.args["surname"]
    search_filter = f"(sn={surname})"
    return connection.extend.standard.paged_search("ou=people,dc=example,dc=com", search_filter)


def django_auth_ldap_search(django_request):
    username = django_request.GET["username"]
    return LDAPSearch("ou=people,dc=example,dc=com", 2, f"(uid={username})")


def ldap_bind_dn(connection):
    username = request.args["username"]
    dn = f"uid={username},ou=people,dc=example,dc=com"
    return connection.simple_bind_s(dn, "placeholder-password")


def ldap_modify_dn(connection, django_request):
    username = django_request.POST["username"]
    user_dn = "uid=" + username + ",ou=people,dc=example,dc=com"
    return connection.modify_s(user_dn, [])
