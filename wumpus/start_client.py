from wumpus.client import Client
from circuits import Debugger
from circuits.net.events import connect

c = Client() + Debugger()
c.connect("0.0.0.0", 50551)
c.run()
