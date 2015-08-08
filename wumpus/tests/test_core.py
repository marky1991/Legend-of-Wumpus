from functools import wraps
import random
from nose.tools import nottest
from ..core import Player
from ..events import bytify

class test_player:
    def setup(self):
        self.player1 = Player("marky1991")
        self.player2 = Player("txgangsta")
        self.player3 = Player("marky1991")
    def test_name(self):
        assert self.player1.name == "marky1991"
        assert self.player2.name == "txgangsta"
    def test_default_team(self):
        assert self.player1.team is None

    def test_jsonify(self):
        expected = {"name": self.player1.name,
                   "team": self.player1.team}
        assert self.player1.jsonify() == expected, (
                    self.player1.jsonify(), "!=", expected)
    def test_debytify(self):
        assert Player.debytify(bytify(self.player1)) == self.player1
    def test_eq(self):
        assert self.player1 != self.player2
        assert self.player1 == self.player3
    def test_hash(self):
        dict = {self.player1: "hi",
                self.player2: "ho",
                self.player3: "chair"}

        assert len(dict) == 2
        assert dict[self.player1] == dict[self.player3]
        assert dict[self.player1] != dict[self.player2]
        assert hash(self.player1) == hash(self.player3)
        assert hash(self.player2) != hash(self.player1)
