import asyncio
import os
import signal
from typing import TYPE_CHECKING, Any

from mangum import Mangum

from koinobori.lambdas.api.builder import build
from koinobori.utils.log_setup import init_logging

if TYPE_CHECKING:
    from mangum.types import LambdaContext, LambdaEvent

if any(
    os.environ.get(env_var) == f"{__name__}.lambda_handler"
    for env_var in ["_HANDLER", "ORIG_HANDLER"]
):
    init_logging(mode="json")

    app = build()

    def shutdown() -> None:
        pass  # nothing to do for now

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, shutdown)

    mangum_handler = Mangum(app, lifespan="off")

    def lambda_handler(event: LambdaEvent, context: LambdaContext) -> dict[str, Any]:
        return mangum_handler(event, context)
