import asyncio
import os
import signal
from types import FrameType

from alembic import command
from alembic.config import Config
from mangum.types import LambdaContext, LambdaEvent

from koinobori.utils.logging import init_logging

if any(
    os.environ.get(env_var) == f"{__name__}.lambda_handler"
    for env_var in ["_HANDLER", "ORIG_HANDLER"]
):
    init_logging(mode="json")

    def shutdown(_signum: int, _frame: FrameType | None) -> None:
        pass  # nothing to do for now

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, shutdown)

    def lambda_handler(_event: LambdaEvent, _context: LambdaContext) -> dict:
        config = Config()
        config.set_main_option(
            "script_location", "koinobori.lambdas.migrations:migrations",
        )

        command.upgrade(config, revision="heads")

        return {}
