import jinja2
from jinja2 import Environment, Template, select_autoescape
from jinja2.sandbox import SandboxedEnvironment


env = jinja2.Environment(autoescape=False)
direct_env = Environment(autoescape=False)
template = Template("<p>{{ name }}</p>", autoescape=False)
sandbox = SandboxedEnvironment(autoescape=lambda name: False)
autoescape = select_autoescape(default=False)
string_autoescape = select_autoescape(default_for_string=False)

jinja_options = {"autoescape": False}
app.jinja_env.autoescape = False
app.jinja_options["autoescape"] = False
app.jinja_options.update(autoescape=False)
app.jinja_options.update({"autoescape": False})
