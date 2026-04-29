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


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"

app.config.update(
    SESSION_COOKIE_SECURE=True,
    CSRF_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="None",
)

app.config.from_mapping(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="None",
)

response.set_cookie("sid", "value", secure=True, httponly=True, samesite="Lax")
response.set_cookie("oauth_state", "value", secure=True, httponly=True, samesite="None")
response.set_signed_cookie("signed", "value", secure=True, httponly=True, samesite="Strict")
