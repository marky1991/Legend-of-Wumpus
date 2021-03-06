from functools import wraps
import itertools
import random
from nose.tools import nottest
from ..utils import Lazy_Coord, Node, not_set, Grid, bytify, jsonify

@nottest
def unary_test(function):
    @wraps(function)
    def wrapper(self):
        coords = [(Lazy_Coord(obj, "x"), Lazy_Coord(obj, "y")) for obj in self.objects]
        for coord in coords:
            for component in coord:
                function(self, component)
    return wrapper

@nottest
def binary_test(function):
    @wraps(function)
    def wrapper(self):
        coords = [(Lazy_Coord(obj, "x"), Lazy_Coord(obj, "y")) for obj in self.objects]
        for coord in coords:
            function(self, *coord)
    return wrapper


class Dummy_Object:
    def __init__(self,x=0, y=0):
        self.x = x
        self.y = y

class test_lazy_coords:
    def setup(self):
        self.origin = Dummy_Object(0, 0)
        self.one_one = Dummy_Object(1, 1)
        self.one_zero = Dummy_Object(1, 0)
        self.zero_one = Dummy_Object(0, 1)
        self.objects = [self.origin, self.one_one, self.one_zero, self.zero_one]

    @unary_test
    def test_identity(self, component):
        assert component * 1 == component, ("Multiplication identity failed:", component)
        assert component + 0 == component, ("Additive Identity failed:", component)
        assert component == component, ("Regular identity failed.", component)
        assert component - 0 == component, ("Subtractive identity failed:", component)
        assert component / 1 == component, ("Divisive identity failed:", component)
        assert component ** 1 == component, ("Exponential identity failed:", component)

    @binary_test
    def test_associativity(self, x, y):
        dummy = Dummy_Object(random.randint(2,100), random.randint(2,100))
        z = Lazy_Coord(dummy, "x")
        assert (x + y) + z == x + (y + z), ("Additive associativity failed:", (x,y,z))
        #Subtraction is not associative
        assert (x * y) * z == x * (y * z), ("Multiplicative associativity failed:", (x,y,z))
        #Division is not associative either
        #Finally, neither is exponentiation

    @binary_test
    def test_commutativity(self, x, y):
        assert x + y == y + x, ("Additive associativity failed:", (x,y))
        #Subtraction is not commutative
        assert x * y == y * x, ("Multiplicative associativity failed:", (x,y))
        #Division is not commutative either
        #Finally, neither is exponentiation
        
    @binary_test
    def test_distributativity(self, x, y):
        #Off the top of my head, I don't immediately know what function pairs
        #are distributive on each other for real numbers. Just going to do the 
        #easy examples from wikipedia.
        dummy = Dummy_Object(random.randint(2,100), random.randint(2,100))
        z = Lazy_Coord(dummy, "x")
        assert x * (y + z) == (x * y) + (x * z), (
                    "Distributativity of addition over multiplication failed:", (x,y, z))
        assert max([x, min([y, z])]) == min([max([x, y]), max([x, z])]), (
                    "Distributativity of max over min failed:", (x, y, z))
        assert min([x, max([y, z])]) == max([min([x, y]), min([x, z])]), (
                    "Distributativity of min over max failed:", (x, y, z))
        assert x + max([y, z]) == max([x+y, x+z]), (
                    "Distributativity of addition over max failed:", (x, y, z))
        assert x + min([y, z]) == min([x+y, x+z]), (
                    "Distributativity of addition over min failed:", (x, y, z))
   
    def test_value(self):
        dummy = Dummy_Object(3, 7)
        x = Lazy_Coord(dummy, "x")
        y = Lazy_Coord(dummy, "y")
        z = Lazy_Coord(dummy, "y") + 4

        assert float(x) == 3.0, ("Basic value checking failed: ", (float(x), 3.0))
        assert int(y) == 7, ("Int value checking failed: ", (int(y), 7))
        assert float(z) == 11, ("Lazy + Scalar failed: ", (float(z), 11))
        assert float(x - 3) == 0, ("Lazy - scalar failed: ", (float(x - 3), 0))
        assert float(x * 4) == 12, ("Lazy * scalar failed: ", (float(x * 3), 12))
        assert float(z / 22) == .5, ("Lazy / scalar failed: ", (float(z / 22), .5))
        assert float(y ** 3) == 7**3, ("Lazy ** scalar failed: ", (float(y**3), 7**3)) 
        assert float(x + y) == (7 + 3), ("Lazy + Lazy failed: ", (float(x + y), (7 + 3)))
        assert float(y - x) == 4, ("Lazy - Lazy failed: ", (float(y - x), 4))
        assert float(x * y) == 21, ("Lazy * lazy failed: ", (float(x * y), 21))
        assert float(x / y) == 3/7, ("Lazy / Lazy failed: ", (float(x / y), 3/7))
        assert float(y ** x) == 7**3, ("Lazy ** lazy failed: ", (float(y ** x), 7**3))

class test_grid_and_node:
    def setup(self):
        self.node1 = Node("hello")
        self.node2 = Node(500)
        self.grid = Grid(5, 10)
    def test_node_eq(self):
        assert self.node1 == self.node1
        assert self.node2 != self.node1
    def test_node_data(self):
        assert self.node1.data == "hello", ("node1 data was not 'hello', but instead", self.node1.data)
        assert self.node2.data == 500, ("node2 data was not 500, but instead", self.node2.data)
    def test_node_neq(self):
        assert self.node2 != self.node1
    def test_set(self):
        self.grid[1, 4] = 750
        node_count = 0
        for column in self.grid.nodes:
            for item in column:
                if item.data is not not_set:
                    node_count = node_count + 1
        assert node_count == 1, ("len of nodes != 1, actually equals", node_count)
        assert self.grid.nodes[1][4].data == 750
    def test_node_jsonify(self):
        expected = {"data": "hello",
                    "data_class": "builtins.str",
                    "x": None,
                    "y": None}
        assert self.node1.jsonify() == expected
    def test_node_dejsonify(self):
        json_dict = {"data": "hello",
                    "data_class": "builtins.str",
                    "x": None,
                    "y": None}
        assert Node.dejsonify(json_dict).data == "hello"
        assert Node.dejsonify(json_dict).x == None
        assert Node.dejsonify(json_dict).y == None
    def test_node_serialization(self):
        assert Node.dejsonify(self.node1.jsonify()).data == self.node1.data
    def test_get(self): 
        self.grid[1, 4] = "test"
        assert self.grid[1,4].data == "test", ("node is not test", self.grid[1,4].data, "test")
        assert self.grid[1,1].data == not_set, (("self.grid[1,1] is not not_set, but instead", self.grid[1,1]))
        assert self.grid[0, 0].data == not_set
    def test_x_y(self):
        self.grid[1,2] = "bmah"
        node = self.grid[1,2]
        assert node.x == 1, ("node1.x, ", node.x, "!=", 1)
        assert node.y == 2, ("node1.y, ", node.y, "!=", 2)
    def test_up_down_left_right(self): 
        self.grid[2,4] = "potato"
        potato = self.grid[2,4]
        self.grid[3,3] = "mark"
        mark = self.grid[3, 3]
        assert {not_set} == {potato.left.data, potato.right.data,
                               potato.up.data, potato.down.data}
        assert {not_set} == {mark.left.data, mark.right.data,
                             mark.up.data, mark.down.data}
        self.grid[3,4] = "cheese"
        cheese = self.grid[3, 4]
        assert potato.right == cheese
        assert cheese.left == potato, ("cheese left != potato", cheese.left, potato)
        assert mark.up == cheese, ("mark.up is not cheese, but instead", mark.up.data if mark and mark.up else "WAS NONE")
        assert cheese.down == mark
    def test_grid_jsonify(self):
        expected = {"nodes": [[Node() for _ in range(10)] for _ in range(5)]}
        expected_nodes = expected["nodes"]
        json_nodes = self.grid.jsonify()["nodes"]
        for node1, node2 in zip(itertools.chain.from_iterable(expected_nodes),
                         itertools.chain.from_iterable(json_nodes)):
            assert node1.data == node2.data
    def test_grid_dejsonify(self):
        json_dict = {"nodes": [[jsonify(Node()) for _ in range(self.grid.rows)] for _ in range(self.grid.columns)]}
        assert Grid.dejsonify(json_dict) == self.grid, (Grid.dejsonify(json_dict), self.grid)


                                                    
def test_bytify_returns_bytes():
    sample = 5
    assert hasattr(bytify(sample), "decode"), (bytify(sample), type(bytify(sample)))
