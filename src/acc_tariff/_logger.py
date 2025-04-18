import logging
import os
import sys

logger = logging.getLogger("acc_tariff")


def __setup_logging():
    strm_handle = logging.StreamHandler(stream=sys.stdout)
    strm_handle.setFormatter(logging.Formatter(fmt="[MIGA] %(message)s"))
    logger.addHandler(strm_handle)
    logger.setLevel(os.environ.get("TARIFF_LOG_LEVEL", "INFO").upper())


__setup_logging()
del __setup_logging
