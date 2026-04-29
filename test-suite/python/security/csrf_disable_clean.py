from flask_wtf.csrf import CSRFProtect


WTF_CSRF_ENABLED = True
WTF_CSRF_CHECK_DEFAULT = True
CSRF_EXEMPT = False

app.config["WTF_CSRF_ENABLED"] = True
app.config.update(WTF_CSRF_CHECK_DEFAULT=True)
app.config.from_mapping({"WTF_CSRF_ENABLED": True})
settings.CSRF_ENABLED = True


def webhook(request):
    verify_signature(request.headers["X-Signature"], request.body)
    return handle_webhook(request.body)


csrf = CSRFProtect(app)


def legacy_form():
    csrf.protect()
    return "updated"
