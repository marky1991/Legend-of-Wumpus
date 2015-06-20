__all__ = ["units", "client", "server"]

import pathlib, os

log_roots = [pathlib.Path(__file__).parent.parent,
             pathlib.Path(os.path.expanduser("~")),
             pathlib.Path("/tmp")]

for root in log_roots:
    log_dir = root / "logs"
    try:
        os.makedirs(str(log_dir))
    except os.error as e:
        if e.errno == 13:
            #Permission denied
            log_dir = None
        elif e.errno == 17:
             #Path already existed
             break
        else:
             raise e
    #Stop as soon as we can log *somewhere*
    break

from .log import debug, error, warning


