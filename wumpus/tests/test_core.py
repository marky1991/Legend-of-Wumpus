from functools import wraps
import random, nose
from nose.tools import nottest
from ..core import Player, Game, Unit, Terrain, Cell, Map
from ..events import bytify

class Test_Unit_Level_All(Unit):
    def __init__(self):
        super().__init__()
        for stat in self.growth_rates:
            self.growth_rates[stat] = 100

        for stat in self.stats:
            setattr(self, stat, 10)
class Test_Unit_Level_None(Unit):
    def __init__(self):
        super().__init__()
        for stat in self.growth_rates:
            self.growth_rates[stat] = 0

        for stat in self.stats:
            setattr(self, stat, 10)
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

class test_game:
    def setup(self):
        self.game = Game()
        self.player = Player("marky1991")
    def test_add_player(self):
        raise nose.SkipTest
        self.game.add_player(self.player)
        assert len(self.game.players) == 1
        assert list(self.game.players)[0] == self.player
class test_unit:
    def setup(self):
        self.good_unit = Test_Unit_Level_All()
        self.bad_unit = Test_Unit_Level_None()
    def test_create(self):
        for field in vars(self.good_unit):
            if field in ("growth_rates", "weapon_skill"):
                continue
            val = getattr(self.good_unit, field)
            assert 0 <= val and val <= 10, ("Vas was not in range 0_10. Val: ", val, ". Fieldname: ", field)

    def test_level_up_all(self):
        for stat in type(self.good_unit).stats:
            assert getattr(self.good_unit, stat) == 10, (getattr(self.good_unit, stat), stat)
        print("all were 10")
        self.good_unit.level_up()
        print(vars(self.good_unit))
        
        for stat in type(self.good_unit).stats:
            assert getattr(self.good_unit, stat) == 11, (getattr(self.good_unit, stat), stat)

    def test_level_up_none(self): 
        for stat in type(self.bad_unit).stats:
            assert getattr(self.bad_unit, stat) == 10, (getattr(self.bad_unit, stat), stat)

        self.bad_unit.level_up()
        
        for stat in type(self.bad_unit).stats:
            assert getattr(self.bad_unit, stat) == 10, (getattr(self.bad_unit, stat), stat)


class test_map:
    def setup(self):
        self.map = Map()
        self.big_map = Map(100, 200)
    def test_dims(self):
        assert self.map.grid.rows == self.map.grid.columns == 50
        assert self.big_map.grid.rows == 200
        assert self.big_map.grid.columns == 100
    def test_jsonify(self):
        expected = {"grid": self.map.grid.jsonify()}
        assert self.map.jsonify() == expected, (
                    self.map.jsonify(), "!=", expected)
    def test_debytify(self):
        assert Map.debytify(bytify(self.map)) == self.map

class test_cell:
    def setup(self):
        self.cell = Cell()
    def test_has_terrain(self):
        #Translation will be done in the view. Will have to add something to
        #the model to support this, but this will be some property, not the core
        #description
        assert self.cell.terrain.description == "NOT SET", self.cell.terrain.description
    def test_object(self):
        #I don't really think I'll need a method for putting stuff in a location
        #I'll just do direct attribute assignment. Not going to test that attr
        #assignment works
        assert self.cell.object is None
class test_terrain:
    def test_defaults(self):
        terrain = Terrain()
        assert terrain.movement_cost == 1
        assert terrain.defense_multiplier == 1.0
        assert terrain.attack_multiplier == 1.0
        assert terrain.description == "NOT SET"
