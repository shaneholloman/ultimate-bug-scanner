from flask_cors import CORS, cross_origin
from starlette.middleware.cors import CORSMiddleware


class App:
    def add_middleware(self, middleware, **kwargs):
        self.middleware = (middleware, kwargs)


app = App()


CORS(
    app,
    origins=["https://app.example.com", "https://admin.example.com"],
    supports_credentials=True,
)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["https://app.example.com"],
            "supports_credentials": True,
        }
    },
)


@cross_origin(origins=["https://app.example.com"], supports_credentials=True)
def dashboard():
    return "private dashboard"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
)


CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ["https://app.example.com"]
CORS_ALLOW_CREDENTIALS = True
