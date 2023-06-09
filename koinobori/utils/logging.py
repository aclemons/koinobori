import logging
from typing import Literal

import structlog


def init_logging(mode: Literal["console", "json"] = "console") -> None:
    structlog.configure(
        processors=[structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
    ]

    if mode == "console":
        processors += [
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.dev.ConsoleRenderer(
                exception_formatter=structlog.dev.rich_traceback,
            ),
        ]
    elif mode == "json":
        processors += [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        msg = f"Unknown mode {mode}"
        raise ValueError(msg)

    formatter = structlog.stdlib.ProcessorFormatter(processors=processors)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
