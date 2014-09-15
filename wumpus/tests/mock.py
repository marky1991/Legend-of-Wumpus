from unittest.mock import MagicMock
from socket import socket

from wumpus.server import Server
from wumpus.client import Client
from wumpus.core import Player

example_server = Server("0.0.0.0")
example_server.shutdown()
example_client = Client()
example_client.shutdown()
example_socket = socket()
example_socket.close()

#It's a function (factory) that's pretending to be a class.
def FakeServer():
    return MagicMock(spec=example_server)

def FakeClient():
    return MagicMock(spec=example_client)

def FakeSocket():
    return MagicMock(spec=example_socket)
