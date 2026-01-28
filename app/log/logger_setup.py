"""Logging setup module."""

import logging
import sys


def setup_logging():
    "Configure logging to output JSON formatted logs to stdout."
    fmt = (
        '{"time":"%(asctime)s", "level":"%(levelname)s", '
        '"name":"%(name)s", "message":%(message)s}'
    )
    logging.basicConfig(
        format=fmt,
        stream=sys.stdout,
        level=logging.INFO,
    )

    # evita log duplicado
    logging.getLogger("uvicorn").handlers = logging.getLogger().handlers
    logging.getLogger("uvicorn.error").handlers = logging.getLogger().handlers
    logging.getLogger("uvicorn.access").handlers = logging.getLogger().handlers
