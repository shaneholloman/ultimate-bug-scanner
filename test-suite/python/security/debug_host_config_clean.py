class App:
    def __init__(self):
        self.config = {}

    def run(self, **kwargs):
        self.kwargs = kwargs


app = App()


class Settings:
    pass


settings = Settings()

DEBUG = False
FLASK_DEBUG = False
ALLOWED_HOSTS = ["app.example.com", "api.example.com"]
settings.DEBUG = 0

app.debug = False
app.config["DEBUG"] = False
app.config["ALLOWED_HOSTS"] = ["admin.example.com"]

app.config.update(DEBUG=False, ALLOWED_HOSTS=["api.example.com"])
app.config.from_mapping(FLASK_DEBUG=False)

app.run(debug=False)
app.run(use_debugger=False)
