import asyncio
import os
import signal
import sys
from typing import TYPE_CHECKING

from alembic import command
from alembic.config import CommandLine, Config

from koinobori.utils.logging import init_logging

if TYPE_CHECKING:
    from mangum.types import LambdaContext, LambdaEvent


def main(argv: list[str]) -> None:
    command_line = CommandLine()

    options = command_line.parser.parse_args(argv or None)
    if not hasattr(options, "cmd"):
        command_line.parser.error("too few arguments")

    cfg = Config(ini_section=options.name, cmd_opts=options)
    cfg.set_main_option("script_location", "koinobori.lambdas.migrations:migrations")

    command_line.run_cmd(cfg, options)


if (
    any(
        os.environ.get(env_var) == f"{__name__}.lambda_handler"
        for env_var in ["_HANDLER", "ORIG_HANDLER"]
    )
    or __name__ == "__main__"
):
    init_logging(mode="json")

    def shutdown() -> None:
        pass  # nothing to do for now

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, shutdown)

    def lambda_handler(_event: "LambdaEvent", _context: "LambdaContext") -> dict:
        config = Config()
        config.set_main_option(
            "script_location",
            "koinobori.lambdas.migrations:migrations",
        )

        command.upgrade(config, revision="heads")

        return {}

    if __name__ == "__main__":
        main(sys.argv[1:])
