import json, subprocess
import platform
import importlib

from wumpus.core import Player
from wumpus.utils import get_git_password, jsonify, bytify, debytify

class Event:
    #Determines whether the server will forward the event on to other clients or
#not.
    broadcast = False
    listeners = set()
    def __init__(self, *args, **kwargs):
        self.args = args or []
        self.kwargs = kwargs or {}
    def handle(self, listener):
        """Handles the event. Can return an arbitrary (Currently finite only)
number of events. Listener is the networking actor (i.e. either client or server) that
is handling the event."""
        return
    def __iter__(self):
        """Allows you to iterate over an event, allowing you to treat a single
event as
an event_tuple instead of being forced to explicitly put it in a tuple. I'm
pretty sure this is a good idea, but I could maybe be wrong.
(It's convenient, but a bit of a hack...Need to think about it further.)"""
        return iter((self,))
    @property
    def name(self):
        cls = self.__class__
        return cls.__module__ + "." + cls.__name__
    def jsonify(self):
        return {"name": self.name,
                "args": self.args,
                "kwargs": self.kwargs}
    @classmethod
    def dejsonify(cls, json_dict):
        return cls(*json_dict["args"], **json_dict["kwargs"])
    def __eq__(self, other):
        return self.args == other.args and self.kwargs == other.kwargs and self.name == other.name

class Join_Event(Event):
    broadcast = True    
    listeners = set()
    def __init__(self, player, *args, **kwargs):
        self.player = player
        super().__init__(player)
    def handle(self, listener):
        from wumpus.views import View
        #TODO: You know, add the client to the client list.
        #This is breaking OOP guidelines, but I don't see the point
        #in adding a trivial method right now. Will improve design
        #if it ends up being needed.
        listener.game.players.add(self.player)
        if not listener.is_server:
            if self.player == listener.player:
                listener.view = View()
                listener.view.post_init()
    
    @classmethod
    def dejsonify(cls, json_dict):
        player_dict = json_dict["args"][0]
        name, team = player_dict["name"], player_dict["team"]
        player = Player(name)
        player.team = team
        return cls(player)

class Update_Code_Event(Event):
    """Teehee. This event probably represents a fairly bad security hole. It allows clients
to force the server to update its code. (Pull from the repo). 

    Given that ultimately I'd like to be able
to test this by running it on different boxes, this will become necessary for proper testing and not
painstakingly-slow development.
   
Note: This needs to be broadcasted so that the clients know to disconnect and then reconnect.
 
A better solution for this problem would be to allow ssh connections into the server I'm connecting
to, but that wouldn't play nice/easily with windows. (I would like to use windows as the server
to ensure that there won't be OS-related issues down the line.) Plus, to be completely honest, this
allows me to be even lazier than I would have to be to do it the Right Way. 

(The fact that I have to write such a large docstring to defend my decision does suggest otherwise...)"""

    broadcast = True
    listeners = set()
    def __init__(self, *args, **kwargs):
        super().__init__()
    def handle(self, listener):
        #Let's not do this for now
        #Need to figure out how this interacts with no-ff
        #(If at all)
        return
        print("Hello from updet")
        password = get_git_password()
        cmd = ("git", "pull")
        pull_shell = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE, shell=False,
                                        universal_newlines=True)
        stdout, stderr = pull_shell.communicate(input=password)
        error_code = True
        print(stdout, stderr, pull_shell)
        if error_code:
            raise Exception("Returned {err_code} from git pull".format(err_code=error_code))
        else:
            print("Finished")
            Restart_Event().handle(listener)

class Shutdown_Event(Event):
    """Shuts the server down. To be handled server-side only."""
    listeners = set()
    def __init__(self, *args, **kwargs):
        super().__init__()
    def handle(self, server):
        print("Got a shutfown")
        server.shutdown()

class Restart_Event(Event):
    """Restarts the server. Broadcast so clients can know to reconnect"""
    broadcast = True
    listeners = set()
    def __init__(self, *args, **kwargs):
        super().__init__()
    def handle(self, server):
        print("Restarting")
        server.restart()

