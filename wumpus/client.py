from circuits import Debugger
from circuits.net.events import connect, write

import circuits
from circuits.node import Node, remote
from .network_node import Network_Node
from .events import Join_Event
from .core import Player

class Client(Network_Node, circuits.core.BaseComponent):
    def __init__(self, host="0.0.0.0", port=50552):
        super().__init__()
        self.node = Node((self.host, self.port))
        self.node.register(self)
        self.player = Player()
    def connect(self, host="0.0.0.0", port=50551):
        self.node.add("server", host, port)
    @circuits.handler("connected")
    def connected(self, host, port):
        #self.fire(remote(write(Join_Event(self.player).bytify()), "server"))
        print("About to casue problems probably")
        self.fire(write(Join_Event(self.player).bytify().encode("utf-8")))
        print("Finisehd")

