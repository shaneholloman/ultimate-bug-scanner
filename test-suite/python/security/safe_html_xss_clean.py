import html

import bleach
import markupsafe
from django.utils.html import conditional_escape
from django.utils.safestring import SafeString, mark_safe
from flask import request
from markupsafe import Markup, escape


def django_mark_safe_literal():
    return mark_safe("<strong>trusted</strong>")


def django_mark_safe_escaped(django_request):
    display_name = html.escape(django_request.GET["name"])
    return mark_safe(f"<strong>{display_name}</strong>")


def django_safe_string_conditional_escape():
    title = conditional_escape(request.form["title"])
    return SafeString("<h1>" + title + "</h1>")


def markupsafe_markup_bleach_clean():
    comment = bleach.clean(request.values["comment"], tags=["b", "i"], strip=True)
    return Markup(comment)


def markupsafe_markup_escape_format():
    name = escape(request.args["name"])
    return Markup("<span>{}</span>".format(name))


def qualified_markupsafe_escape(flask_request):
    safe_html = markupsafe.escape(flask_request.form["html"])
    return markupsafe.Markup(safe_html)


def plain_template_context_is_not_marked_safe():
    return {"preview": request.headers["X-Preview"]}


def escaped_input_markup():
    html_fragment = html.escape(input("html> "))
    return Markup(html_fragment)
