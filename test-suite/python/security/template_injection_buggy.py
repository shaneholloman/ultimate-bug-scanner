from django.template import Context, Template as DjangoTemplate
from flask import render_template_string, request
import jinja2
from mako.template import Template as MakoTemplate


def flask_template_string():
    template = request.args["template"]
    return render_template_string(template)


def flask_template_keyword():
    return render_template_string(source=request.form["source"])


def jinja_environment_from_string():
    env = jinja2.Environment(autoescape=True)
    source = request.get_json()["template"]
    return env.from_string(source).render()


def jinja_template_constructor():
    template = request.json["template"]
    return jinja2.Template(template).render()


def django_template_constructor(django_request):
    source = django_request.POST["template"]
    return DjangoTemplate(source).render(Context({}))


def mako_template_text():
    source = input("template: ")
    return MakoTemplate(text=source).render()
