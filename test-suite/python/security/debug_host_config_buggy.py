class App:
    def __init__(self):
        self.config = {}

    def run(self, **kwargs):
        self.kwargs = kwargs


app = App()


class Settings:
    pass


settings = Settings()

DEBUG = True
FLASK_DEBUG = True
ALLOWED_HOSTS = ["*"]
settings.DEBUG = 1

app.debug = True
app.config["DEBUG"] = "true"
app.config["ALLOWED_HOSTS"] = [".example.com", "*.internal.example"]

app.config.update(DEBUG=True, ALLOWED_HOSTS=["*"])
app.config.from_mapping(FLASK_DEBUG=True)

app.run(debug="yes")
app.run(use_debugger="on")
