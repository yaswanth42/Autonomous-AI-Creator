import logging
import sys

import io

def setup_logging():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s"))

    root_logger = logging.getLogger("AutoPersonaAI")
    root_logger.setLevel(logging.INFO)
    if not root_logger.handlers:
        root_logger.addHandler(handler)
    return root_logger

logger = setup_logging()
