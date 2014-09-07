import json, subprocess
from collections.abc import Mapping
from utils import get_sudo_password

def bytify(arg):
    return json.dumps(_bytify(arg))

def _bytify(arg):
    """Woo recursion!"""
    print("Start")
    if hasattr(arg, "jsonify"):
        print("Jsonify")
        return _bytify(arg.jsonify())

    known_types = [str, int, float, bool, type(None)]
    if type(arg) in known_types:
        print("Simple")
        return arg
    #If it's a mapping
    if isinstance(arg, Mapping):
        print("It's a map!")
        def wrap(item):
            return type(arg)(item)
        return wrap({_bytify(key): _bytify(value) for (key, value) in arg.items()})
    if hasattr(arg, "__iter__"):
        print("Iter")
        def wrap(item):
            return type(arg)([item])
        if len(arg) > 1:
            head, *tail = arg

            #Python doesn't do tail-call optimization anyway
            return wrap(_bytify(head)) + wrap(_bytify(*tail))
        elif len(arg) == 1:
            return wrap(_bytify(arg[0]))
        else:
            return wrap([])
    print("Fail")
    raise ValueError("Unbytify-able object: {obj}".format(obj=arg))

def debytify(byte_string):
    print("Start")
    string = byte_string.decode("utf-8")
    print(string, "STRING")
    dictionary = json.loads(string)
    try:
        return locals()[dictionary["name"]].debytify(string)
    except KeyError:
        return Event()
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
    def bytify(self):
        return bytify(self.jsonify())
    @staticmethod
    def debytify(json_val):
        json_dict = json.loads(json_val)
        return Event(*json_dict["args"], **json_dict["kwargs"])

class Join_Event(Event):
    broadcast = True    
    listeners = set()
    def __init__(self, player):
        self.player = player
        super().__init__(args=(player,))
    def handle(self, listener):
        #TODO: You know, add the client to the client list.
        listener.players.append(self.player)
    def debytify(json_val):
        json_dict = json.loads(json_val)
        #Join_Event(5,6,7, name="mark", pw="bob")
        return Join_Event(*json_dict["args"], **json_dict["kwargs"])
        #def spam(*args): return args[0], args[2]
        #spam(5,6,7,8,9,10,11) -> (5,7)
        #def blah(*args, **kwargs): return args, kwargs
        #blah(1,2,3,4,5, (6,7,8), "walrus", name="sally", bob="boob", t=6) ->
        #((1,2,3,4,5, (6,7,8), "walrus"), {"name": "sally", "bob": "boob", "t":
        #6})

        #def add(a, b, c): return sum(a,b,c)
        #nums = [5,6,7]
        #add(nums[0], nums[1], nums[2])
        #add(*nums) == add(5,6,7) 

        #def ignore(*args): pass 

class Update_Code_Event(Event):
    """Teehee. This event probably represents a fairly bad security hole. It allows clients
to force the server to update its code. (Pull from the repo). 

    Given that ultimately I'd like to be able
to test this by running it on different boxes, this will become necessary for proper testing and not
painstakingly-slow development.
   
Note: This needs to be broadcasted so that the clients know to disconnect and then reconnect."""
    broadcast = True
    listeners = set()
    def __init__(self):
        super().__init__()
    def handle(self, listener):
        print("Hello from updet")
        #Sudo is required for some unknown reason.
        password = get_sudo_password()
        pull_shell = subprocess.Popen(("echo", password, "|", "sudo", "-S", "git", "pull"), shell=True)
        stdout, stderr = pull_shell.communicate()
        error_code = True
        print(stdout, stderr)
        if error_code:
            raise Exception("Returned {err_code} from git pull".format(err_code=error_code))
        else:
            print("Finished")
            Restart_Event().handle(listener)

class Shutdown_Event(Event):
    """Shuts the server down. To be handled server-side only."""
    listeners = set()
    def __init__(self):
        super().__init__()
    def handle(self, server):
        print("Got a shutfown")
        server.shutdown()

class Restart_Event(Event):
    """Restarts the server. Broadcast so clients can know to reconnect"""
    broadcast = True
    listeners = set()
    def __init__(self):
        super().__init__()
    def handle(self, server):
        print("Restarting")
        server.restart()
