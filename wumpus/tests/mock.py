from unittest.mock import MagicMock
from socket import socket

from wumpus.server import Server
from wumpus.client import Client
from wumpus.core import Player, Game

example_server = Server("0.0.0.0")
example_server.shutdown()
example_client = Client()
example_client.shutdown()
example_socket = socket()
example_socket.close()

#It's a function (factory) that's pretending to be a class.
def FakeServer():
    server = MagicMock(spec=example_server)
    server.game = Game()
    server.running = False
    return server

def FakeClient():
    client = MagicMock(spec=example_client)
    client.game = Game()
    client.running = False
    return client

def FakeSocket():
    return MagicMock(spec=example_socket)
