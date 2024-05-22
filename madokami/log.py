import sys
import inspect
import logging
from typing import TYPE_CHECKING
import logging

import loguru

if TYPE_CHECKING:
    # avoid sphinx autodoc resolve annotation failed
    # because loguru module do not have `Logger` class actually
    from loguru import Logger, Record

# logger = logging.getLogger("nonebot")
logger: "Logger" = loguru.logger

# default_handler = logging.StreamHandler(sys.stdout)
# default_handler.setFormatter(
#     logging.Formatter("[%(asctime)s %(name)s] %(levelname)s: %(message)s"))
# logger.addHandler(default_handler)


class MessageStorageHandler(logging.Handler):
    def __init__(self):
        self.logs = []
        super().__init__()

    def emit(self, record: logging.LogRecord):
        self.logs.append(record.getMessage())

    def get_messages(self, limit: int = 1000, level: str = 'ALL') -> list[str]:
        if len(self.logs) > limit:
            return self.logs[-limit:]
        return self.logs


# https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
class LoguruHandler(logging.Handler):  # pragma: no cover
    """logging 与 loguru 之间的桥梁，将 logging 的日志转发到 loguru。"""

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def default_filter(record: "Record"):
    """默认的日志过滤器，根据 `config.log_level` 配置改变日志等级。"""
    log_level = record["extra"].get("nonebot_log_level", "INFO")
    levelno = logger.level(log_level).no if isinstance(log_level, str) else log_level
    return record["level"].no >= levelno


default_format: str = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    # "<c>{function}:{line}</c>| "
    "{message}"
)
"""默认日志格式"""

logger.remove()
logger_id = logger.add(
    sys.stdout,
    level=0,
    diagnose=False,
    filter=default_filter,
    format=default_format,
)
"""默认日志处理器 id"""

logger.add(
    "data/logs/{time:YYYY-MM-DD}.log",
    level=0,
    rotation="10 MB",
    compression="zip"
)

# logger.add(
#     LoguruHandler(),
#     level=0,
#     format=default_format,
#     serialize=False
# )

message_storage_handler = MessageStorageHandler()

logger.add(
    message_storage_handler,
    level=0,
    format=default_format,
    serialize=False
)