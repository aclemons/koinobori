import asyncio
import os
import signal
from types import FrameType

from mangum import Mangum
from mangum.types import LambdaContext, LambdaEvent

from koinobori.lambdas.api.builder import build
from koinobori.utils.logging import init_logging

if any(
    os.environ.get(env_var) == f"{__name__}.lambda_handler"
    for env_var in ["_HANDLER", "ORIG_HANDLER"]
):
    init_logging(mode="json")

    app = build()

    def shutdown(signum: int, frame: FrameType | None) -> None:
        pass  # nothing to do for now

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, shutdown)

    mangum_handler = Mangum(app, lifespan="off")

    def lambda_handler(event: LambdaEvent, context: LambdaContext) -> dict:
        return mangum_handler(event, context)
