from django.views.decorators.csrf import csrf_exempt
from flask_wtf.csrf import CSRFProtect


WTF_CSRF_ENABLED = False
WTF_CSRF_CHECK_DEFAULT = False
CSRF_EXEMPT = True

app.config["WTF_CSRF_ENABLED"] = False
app.config.update(WTF_CSRF_CHECK_DEFAULT=False)
app.config.from_mapping({"WTF_CSRF_ENABLED": False})
settings.CSRF_ENABLED = False


@csrf_exempt
def webhook(request):
    return handle_webhook(request.body)


csrf = CSRFProtect(app)


@csrf.exempt
def legacy_form():
    return "updated"


csrf.exempt(admin_post)
disabled_csrf = CSRFProtect(app, enabled=False)
