class Response:
    def set_cookie(self, name, value, **kwargs):
        self.cookie = (name, value, kwargs)

    def set_signed_cookie(self, name, value, **kwargs):
        self.signed_cookie = (name, value, kwargs)


class App:
    def __init__(self):
        self.config = {}


app = App()
response = Response()


SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = "None"

app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = False
app.config["SESSION_COOKIE_SAMESITE"] = None

app.config.update(
    SESSION_COOKIE_SECURE=False,
    CSRF_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE="None",
)

app.config.from_mapping(
    SESSION_COOKIE_HTTPONLY=False,
    SESSION_COOKIE_SAMESITE=False,
)

response.set_cookie("sid", "value", secure=False, httponly=True, samesite="Lax")
response.set_cookie("prefs", "value", secure=True, httponly=False, samesite="Lax")
response.set_cookie("oauth_state", "value", httponly=True, samesite="None")
response.set_signed_cookie("signed", "value", secure=False, httponly=False)
