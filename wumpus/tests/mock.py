from unittest.mock import MagicMock

from wumpus.server import Server
from wumpus.client import Client
from wumpus.core import Player

#Yeah, it's a function (factory) that's pretending to be a class.
#Deal with it
def FakeServer():
    return MagicMock(spec=Server)

def FakeClient():
    return MagicMock(spec=Client)

