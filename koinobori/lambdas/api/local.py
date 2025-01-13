from typing import TYPE_CHECKING

from koinobori.lambdas.api.builder import build
from koinobori.utils.log_setup import init_logging

if TYPE_CHECKING:
    from fastapi import FastAPI


def uvicorn_app() -> "FastAPI":
    init_logging(mode="console")

    return build()


if __name__ == "__main__":
    import uvicorn
    from uvicorn.config import LOG_LEVELS

    init_logging(mode="console")

    uvicorn.run(
        "koinobori.lambdas.api.local:uvicorn_app",
        factory=True,
        host="127.0.0.1",
        log_config=None,
        log_level=LOG_LEVELS["info"],
        port=8000,
        reload=True,
        reload_dirs=["koinobori"],
    )
