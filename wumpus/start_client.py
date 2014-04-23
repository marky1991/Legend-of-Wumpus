from wumpus.client import Client
from circuits import Debugger
from circuits.net.events import connect

c = Client() + Debugger()
c.connect("192.168.1.104", 50551)
c.run()

