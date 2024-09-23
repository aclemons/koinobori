from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from koinobori.lambdas import api


def build() -> FastAPI:
    app = FastAPI(
        title="koinobori API",
        description="WIP: 🎏",
        version=api.__version__,
        debug=False,
    )

    def ping() -> str:
        return "🎏"

    app.get("/v1/ping", response_class=PlainTextResponse)(ping)

    return app
