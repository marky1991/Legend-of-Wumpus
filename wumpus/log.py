import functools, logging
import os
from datetime import datetime
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

from . import log_dir

def init(filename=None):
    today = datetime.today().date().isoformat()
    global logger
    if filename is None:
        filename="log_" + today
    print("initing", filename, __file__, __name__)
    logger = logging.getLogger()
    new_handler = logging.FileHandler(str(log_dir / (filename + ".log")), "a+")
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.addHandler(new_handler)

def log(*args, func=None):
    print("logging", args, func)
    msg = u", ".join(map(str, args))
    func(msg)

def debug(*args):
    log(*args, func=logger.debug)
def error(*args):
    log(*args, func=logger.error)
warning = 4
#warning = functools.partial(log, func=logger.warning)
#There are of course more levels, but I don't need them right now


