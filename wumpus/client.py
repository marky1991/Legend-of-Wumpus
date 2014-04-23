from circuits import Debugger
from circuits.net.events import connect

import circuits
from circuits.node import Node, remote

class Client(circuits.core.BaseComponent):
    def __init__(self, host="0.0.0.0", port=50552):
        super().__init__()
        self.node = Node((host, port))
        self.node.register(self)
    def connect(self, host="0.0.0.0", port=50551):
        self.node.add("server", host, port)
        self.fire(remote(connect(("0.0.0.0", 50551)), "server"))
    @circuits.handler("read")
    def read(self, socket, data):
        event = events.parse(data)
        old_events = new_events = event.handle()
        #old = new = [BBevent]
        while new_events:
            #new = [bb] -> [blow, candle]
            #old = [BBEvent] -> [blow, candle]
            old_events = list(new_events)
            #old = bb -> [blow, candle]
            #new = []
            new_events = []
            for event in old_events:
                #old = [bb] -> [blow, candle]
                #new = [blow_up, c=andle_on] -> []
                new_events.extend(event.handle())
                self.broadcast(event)


