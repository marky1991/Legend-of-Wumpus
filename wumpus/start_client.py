#!/usr/bin/env python3
import wumpus

from wumpus import log
from wumpus.client import Client
from circuits import Debugger
from circuits.net.events import connect 
import sys
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
log.init(filename="client_" + now)

c = Client()# + Debugger()
#c.connect("marky1991.com", 50551)
try:
    c.go()
except KeyboardInterrupt:
    pass
finally:
    c.stop()
