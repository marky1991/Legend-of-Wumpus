#!/usr/bin/env python3
from wumpus.client import Client
from circuits import Debugger
from circuits.net.events import connect 
import sys

c = Client()# + Debugger()
#c.connect("marky1991.com", 50551)
try:
    c.go()
except KeyboardInterrupt:
    pass
finally:
    c.stop()
