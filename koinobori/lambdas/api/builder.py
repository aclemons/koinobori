from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


def build() -> FastAPI:
    app = FastAPI()

    @app.get("/v1/ping", response_class=PlainTextResponse)
    def ping() -> str:
        return "🎏"

    return app
