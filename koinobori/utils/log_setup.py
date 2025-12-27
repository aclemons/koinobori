import contextlib
import json
import logging
import logging.config
from typing import TYPE_CHECKING, Any, Literal, cast

import orjson
import structlog

if TYPE_CHECKING:
    from structlog.typing import ExceptionRenderer, Processor


def init_logging(mode: Literal["console", "json"] = "console") -> None:
    structlog.configure(
        processors=[structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
    ]

    match mode:
        case "console":
            processors.append(structlog.processors.StackInfoRenderer())
            processors.append(structlog.dev.set_exc_info)

            untyped_formatter = structlog.dev.rich_traceback  # type: ignore[reportUnknownMemberType]
            formatter = cast("ExceptionRenderer", untyped_formatter)

            processors.append(
                structlog.dev.ConsoleRenderer(exception_formatter=formatter)
            )
        case "json":
            processors.append(structlog.processors.dict_tracebacks)

            def orjson_dumps(*args: Any, **kwargs: Any) -> str:
                kwargs["option"] = orjson.OPT_SORT_KEYS
                return orjson.dumps(*args, **kwargs).decode()

            def stdlib_dumps(*args: Any, **kwargs: Any) -> str:
                kwargs["sort_keys"] = True
                return json.dumps(*args, **kwargs)

            def safe_dumps(*args: Any, **kwargs: Any) -> str:
                with contextlib.suppress(Exception):
                    return orjson_dumps(*args, **kwargs)

                with contextlib.suppress(Exception):
                    return stdlib_dumps(*args, **kwargs)

                # safe fallback
                return repr(*args)

            processors.append(structlog.processors.JSONRenderer(serializer=safe_dumps))

    formatter = structlog.stdlib.ProcessorFormatter(processors=processors)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    add_handler(handler)


def add_handler(handler: logging.Handler) -> None:
    # clear logging configuration
    logging.config.dictConfig({"version": 1, "disable_existing_loggers": False})

    # clear all loggers set by anyone else
    for name in logging.root.manager.loggerDict:
        logger = logging.getLogger(name)
        if not isinstance(logger, logging.PlaceHolder):
            logger.setLevel(logging.NOTSET)
            logger.handlers = []
            logger.propagate = True

    # set our root handler
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # and finally apply our config
    logging_config: dict[str, Any] = {
        "loggers": {},
        "version": 1,
        "disable_existing_loggers": False,
        "incremental": True,
    }
    logging.config.dictConfig(logging_config)
