from wumpus.client import Client
from circuits import Debugger
from circuits.net.events import connect

c = Client() + Debugger()
c.connect("marky1991.com", 50551)
c.run()
