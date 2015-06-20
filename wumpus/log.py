import functools, logging
import os
from datetime import datetime
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("wumpus")

from . import log_dir

def init(filename=None):
    today = datetime.today().date().isoformat()
    global logger
    if filename is None:
        filename="log_" + today
    logger = logging.getLogger("wumpus")
    new_handler = logging.FileHandler(str(log_dir / (filename + ".log")), "a+")

    formatter = logging.Formatter("%(asctime)s: %(message)s")
    new_handler.setFormatter(formatter)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.addHandler(new_handler)

def log(*args, func=None):
    msg = u", ".join(map(str, args))
    func(msg)

def debug(*args):
    log(*args, func=logger.debug)
def error(*args):
    log(*args, func=logger.error)
def warning(*args):
    log(*args, func=logger.warning)
#There are of course more levels, but I don't need them right now


