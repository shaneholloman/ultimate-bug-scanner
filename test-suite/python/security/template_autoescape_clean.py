import jinja2
from jinja2 import Environment, select_autoescape
from jinja2.sandbox import SandboxedEnvironment


env = jinja2.Environment(autoescape=True)
direct_env = Environment(autoescape=select_autoescape(["html", "xml"]))
sandbox = SandboxedEnvironment(autoescape=lambda name: bool(name and name.endswith((".html", ".xml"))))

jinja_options = {"autoescape": True}
app.jinja_env.autoescape = True
app.jinja_options["autoescape"] = True
app.jinja_options.update(autoescape=True)
app.jinja_options.update({"autoescape": True})
