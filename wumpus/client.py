from circuits import Debugger
from circuits.net.events import connect

import circuits
from circuits.node import Node, remote
from .network_node import Network_Node

class Client(Network_Node, circuits.core.BaseComponent):
    def __init__(self, host="0.0.0.0", port=50552):
        super().__init__()
        self.node = Node((self.host, self.port))
        self.node.register(self)
    def connect(self, host="0.0.0.0", port=50551):
        self.node.add("server", host, port)
        self.fire(remote(connect(("0.0.0.0", 50551)), "server"))
