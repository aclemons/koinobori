from fastapi import FastAPI


def build() -> FastAPI:
    app = FastAPI()

    @app.get("/v1/ping")
    def ping():
        return "pong"

    return app
