import html

from django.template import Context, Template
from flask import render_template, render_template_string, request
import jinja2


def fixed_flask_template_string():
    name = html.escape(request.args["name"])
    return render_template_string("<p>{{ name }}</p>", name=name)


def fixed_file_template():
    name = html.escape(request.args["name"])
    return render_template("profile.html", name=name)


def fixed_jinja_environment():
    env = jinja2.Environment(autoescape=True)
    template = env.from_string("<p>{{ name|e }}</p>")
    return template.render(name=request.args["name"])


def fixed_django_template(django_request):
    template = Template("Hello {{ name }}")
    return template.render(Context({"name": django_request.GET["name"]}))


def selected_template_from_allowlist(name):
    templates = {
        "summary": "<p>{{ total }}</p>",
        "empty": "<p>No results</p>",
    }
    source = templates.get(name)
    if source is None:
        raise ValueError("unsupported template")
    return render_template_string(source, total=0)
