from wumpus.server import Server
from circuits import Debugger

s = Server("0.0.0.0", 50551) + Debugger()
s.run()
