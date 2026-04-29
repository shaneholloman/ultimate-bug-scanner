from django.utils.safestring import SafeString, mark_safe
from flask import request
from markupsafe import Markup


def django_mark_safe_direct():
    return mark_safe(request.args["bio"])


def django_mark_safe_fstring(django_request):
    display_name = django_request.GET["name"]
    return mark_safe(f"<strong>{display_name}</strong>")


def django_safe_string_alias():
    title = request.form["title"]
    return SafeString("<h1>" + title + "</h1>")


def markupsafe_markup_direct():
    comment = request.values["comment"]
    return Markup(comment)


def markupsafe_markup_format():
    name = request.args["name"]
    return Markup("<span>{}</span>".format(name))


def flask_markup_qualified(flask_request):
    import markupsafe

    return markupsafe.Markup(flask_request.form["html"])


def tainted_assignment_then_mark_safe():
    fragment = request.headers["X-Preview"]
    return mark_safe(fragment)


def stdin_markup():
    html = input("html> ")
    return Markup(html)
