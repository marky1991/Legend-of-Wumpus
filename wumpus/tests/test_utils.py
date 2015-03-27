from functools import wraps
import random
from nose.tools import nottest

from wumpus.utils import *

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

class testUtils:
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
