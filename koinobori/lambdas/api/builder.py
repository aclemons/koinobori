from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import PlainTextResponse
from starlette.responses import HTMLResponse

from koinobori.lambdas import api


def build() -> FastAPI:
    app = FastAPI(
        docs_url=None,
        title="koinobori API",
        description="WIP: 🎏",
        version=api.__version__,
        debug=False,
    )

    app.openapi_version = "3.1.0"

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.0.0-alpha.13/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.0.0-alpha.13/swagger-ui.css",
        )

    @app.get("/v1/ping", response_class=PlainTextResponse)
    def ping() -> str:
        return "🎏"

    return app
