import circuits
from . import events
from circuits.node import Node
import itertools
from .network_node import Network_Node

class Server(Network_Node, circuits.core.Component):
    def __init__(self, host="0.0.0.0", port=50551):
        super().__init__(host=host, port=port)
        #This maps user_id to client
        self.clients = {}
        self.id_generator = itertools.count()
        self.node = Node((self.host, self.port))
        self.node.register(self)
        
    def connect(*args):
        print("Hey")
        pass
