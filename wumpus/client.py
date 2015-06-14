from hashlib import sha256

from circuits import Debugger
from circuits.net.events import connect, write
import circuits
from circuits.node import Node, remote

from .log import debug
from .network_node import Network_Node
from .events import Join_Event
from .core import Player
from .views import views

class Client(Network_Node, circuits.core.BaseComponent):
    def __init__(self, host="0.0.0.0", port=50552, socket=None):
        super().__init__()
        self.node = Node((self.host, self.port))
        self.node.register(self)
        self.socket = socket
        #This is the channel that the server's client is listening on.
        #The fact that I have to use this to talk exclusively to the server strongly
        #suggests that either circuits' API is all sorts of broken or I horribly misunderstand
        #it
        #This is GROOOOOSSSS
        self.server_channel = ""
        #Eventually, I'll need to grab player name somehow.
        self.player = Player()
    def connect(self, host="0.0.0.0", port=50551):
        self.node.add("server", host, port)
        self.server_channel = sha256("{0:s}:{1:d}".format(host, port).encode("utf-8")
                                    ).hexdigest()
    @circuits.handler("connected")
    def connected(self, host, port):
        #self.fire(remote(write(Join_Event(self.player).bytify()), "server"))
        self.fire(write(Join_Event(self.player).bytify().encode("utf-8")), self.server_channel)
        debug("Finished")
    def go(self):
        self.gui = views.GUI()
        debug("Made gui")
        self.gui.first_view_class = views.Login_View
        self.start()
        debug("Srtarting gui")
        self.gui.run()
        debug("Started")

    def update(self):
        self.game.update()
