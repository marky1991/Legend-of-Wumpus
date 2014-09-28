import circuits
import sys
from itertools import count

from circuits.net.events import disconnect
from . import events
from circuits.node import Node
import itertools
from .client import Client
from .network_node import Network_Node

class Server(Network_Node, circuits.core.BaseComponent):
    def __init__(self, host="0.0.0.0", port=50551):
        super().__init__(host=host, port=port)
        #This maps user_id to client
        self.clients = {}
        #This is a temporary design. Ultimately this will be part of a client.
        #This is just here until clients are implemented
        self.sockets = set()
        self.id_generator = count()
        self.node = Node((self.host, self.port))
        self.node.register(self)
        self.id_generator = count() 
            
    @circuits.handler("connect")
    def connect(self, socket, host, port):
        self.sockets.add(socket)
        client = Client(host, port, socket=socket)
        self.clients[next(self.id_generator)] = client
    
    @circuits.handler("disconnect")
    def disconnect(self, socket):
        #This is an intentionally local event
        print("Updating code")
        events.Update_Code_Event().handle(self)

    def broadcast(self, event):
        for client in self.clients:
            self.fire(write(client.socket, bytify(event).encode("utf-8")))
    
    def cleanup(self):
        self.node.stop()
        self.stop()
    
    def shutdown(self):
        self.cleanup()
        #the fact that it tries to do this is gross.
        #Will need to replace the functionality somehow.
        #sys.exit(1)
    def restart(self):
        self.cleanup()
        #This is gross.
        #sys.exit(4)
