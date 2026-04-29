from flask_cors import CORS, cross_origin
from fastapi.middleware.cors import CORSMiddleware


class App:
    def add_middleware(self, middleware, **kwargs):
        self.middleware = (middleware, kwargs)


app = App()


CORS(app, origins="*", supports_credentials=True)

CORS(app, supports_credentials=True)

CORS(
    app,
    resources={r"/*": {"origins": "*", "supports_credentials": True}},
)

CORS(
    app,
    resources={r"/admin/*": {"origins": "*"}},
    supports_credentials=True,
)

CORS(app, resources={r"/reports/*": {"supports_credentials": True}})


@cross_origin(origins="*", supports_credentials=True)
def dashboard():
    return "private dashboard"


@cross_origin(supports_credentials=True)
def settings():
    return "private settings"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
)


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
