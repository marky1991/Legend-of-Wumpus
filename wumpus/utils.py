import itertools, importlib
from collections.abc import Mapping
import json

class Lazy_Coord(float):

    """Implements a lazily_evaluated value. Effectively implements a blob
    of lazy getattrs that can be done arithmetic on. Not actually used at this
    point. (But it works too well to rip out without me feeling sad. : ( )
    
    TODO: Does this really need to be  a float subclass? It should work
    regardless of what the type that self.function returns. I think I
    can generalize to Lazy_Object if I implement the magic methods needed
    for non-numerics."""
    
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)#*args, **kwargs)
    #Note : To implement thuis, just make sure to calculate the current value
    #when doing __mul__, __add__, etc.
    def __init__(self, obj, field_name):
        super().__init__()
        self.object = obj
        self.field_name = field_name
        self.function = lambda: getattr(self.object, self.field_name) 

    def __add__(self, other):
        sum = Lazy_Coord(self.object, self.field_name)
        sum.function = lambda: self.function() + (other.function() if hasattr(other, "function") else other)
        return sum
    __radd__ = __add__

    def __sub__(self, other):
        difference = Lazy_Coord(self.object, self.field_name)
        difference.function = lambda: self.function() - (other.function() if hasattr(other, "function") else other) 
        return difference

    def __mul__(self, other):
        product = Lazy_Coord(self.object, self.field_name)
        product.function = lambda: self.function() * (other.function() if hasattr(other, "function") else other)
        return product

    def __truediv__(self, other):
        quotient = Lazy_Coord(self.object, self.field_name)
        quotient.function = lambda: self.function() / (other.function() if hasattr(other, "function") else other)
        return quotient

    def __floordiv__(self, other):
        quotient = Lazy_Coord(self.object, self.field_name)
        quotient.function = lambda: self.function() // (other.function() if hasattr(other, "function") else other)
        return quotient

    def __pow__(self, other, mod=None):
        #Not exactly the technical term...
        raised_thing = Lazy_Coord(self.object, self.field_name)
        if mod is None:
            raised_thing.function = lambda: self.function() ** (other.function() if hasattr(other, "function") else other)
        else:
            raised_thing.function = lambda: self.function() ** (other.function() if hasattr(other, "function") else other) % mod
        return raised_thing



    def __float__(self):
        #Haha. I can't believe I forgot to add the mechanism for a lazy number to be converted to a real number.
        return float(self.function())

    def __int__(self):
        return int(self.function())

class Unset_Sentinel:
    def __repr__(self):
        return type(self).__name__
    def __str__(self):
        return type(self).__name__
    def __hash__(self):
        return id(self)
    def jsonify(self):
        return {"": None}
    @classmethod
    def dejsonify(cls, json_dict):
        return not_set
not_set = Unset_Sentinel()
class Node:
    def __init__(self, data=not_set, x=None, y=None):
        self.data = data
        self.x = x
        self.y = y
        self.left = self.right = self.up = self.down = None
    def __str__(self):
        return "Node({data})".format(data=str(self.data))
    __repr__ = __str__
    def jsonify(self):
        cls = type(self.data)
        return {"data": self.data,
                "data_class": cls.__module__ + "." + cls.__qualname__,
                "x": self.x,
                "y": self.y}
    @classmethod
    def dejsonify(cls, json_dict):
        x = json_dict["x"]
        y = json_dict["y"]
        *module_pieces, data_cls = json_dict["data_class"].split(".")
        data_cls_module = importlib.import_module(".".join(module_pieces))
        data_cls = getattr(data_cls_module, data_cls)
        if hasattr(data_cls, "dejsonify"):
            data = data_cls.dejsonify(json_dict["data"])
        elif data_cls in [str, int, float, bool]:
            data = json_dict["data"]
        me = cls(data=data, x=x, y=y)
        return me
    def __eq__(self, other):
        return self is other
        fields = ["data", "x", "y", "left", "right", "up", "down"]
        try:
            return all((getattr(self, field) == getattr(other, field) for field in fields))
        except AttributeError:
            return False

class Grid:
    def __init__(self, columns=50, rows=50, nodes=None):
        """Represents an m x n grid of nodes. 
        
        Internally implemented as a list of lists. (Sparseness
        was considered, but for my usecase, it will always be fully
        populated, so it was unnecessary complexity)"""
        if nodes is None:
            self.nodes = []
            for x in range(columns):
                self.nodes.append([])
                for y in range(rows):
                    node = Node()
                    if x > 0:
                        left = self.nodes[x-1][y]
                        node.left = left
                        left.right = node

                    if y > 0:
                        down = self.nodes[x][y-1]
                        node.down = down
                        down.up = node
                    node.x = x
                    node.y = y
                    self.nodes[x].append(node)
        else:
            self.nodes = nodes

    def __getitem__(self, indices):
        #For now, only supporting grid[1,2] syntax 
        #(I.e. no ellipses or ranges please)
        x, y = indices
        return self.nodes[x][y]
    def __setitem__(self, indices, data):
        x, y = indices
        if x < 0:
            x = len(self.nodes) + x
        if y < 0:
            y = len(self.nodes[x]) + y
        #The main behavior requirements considered for the 
        #current design:
            #O(1) lookup (Not strictly needed, but nice)
            #O(1) neighbor lookup (Radial damage, etc)
            #O(n) insertion
            #(Deletion's performance is irrelevant as I never intend to 
            #remove from the data structure) (For completeness: all subclasses must
            #have O(n) worst case performance here)

        #I currently have O(1) for all of these, given that I dropped the sparseness
        #design. A sparse list of lists would work with these complexity
        #requirements

        #Memory requirements are O(n), where n = number of nodes
        #(reminder: Constant factors don't matter for O-notation)
        
        #The current design seems to meet these requirements (it exceeds them in fact),
        #so I'm not spending further time thinking about it

        node = Node(data)
        if x > 0:
            print(x, y, len(self.nodes))
            print(len(self.nodes[x-1]))
            left = self.nodes[x-1][y]
            node.left = left
            if left:
                left.right = node

        if x < (len(self.nodes) - 1):
            right = self.nodes[x+1][y]
            node.right = right
            if right:
                right.left = node
        if y > 0:
            down = self.nodes[x][y-1]
            node.down = down
            if down:
                down.up = node
        if y < (len(self.nodes[x]) - 1):
            up = self.nodes[x][y+1]
            node.up = up
            if up:
                up.down = node
        node.x = x
        node.y = y
        self.nodes[x][y] = node
    def __iter__(self):
        return itertools.chain(*self.nodes)
    @property
    def columns(self):
        return len(self.nodes)
    
    @property
    def rows(self):
        #Assuming a consistently-sized matrix
        return len(self.nodes[0] if self.nodes else [])
    def jsonify(self):
        return {"nodes": self.nodes}
    @classmethod
    def dejsonify(cls, json_dict):
        nodes = []
        for col in json_dict["nodes"]:
            column = []
            for row in col:
                node = Node.dejsonify(row)
                column.append(node)
            nodes.append(column)

        me = Grid(nodes=nodes)
        return me
    def __str__(self):
        return "Grid(columns={cols}, rows={rows})".format(cols=len(self.nodes),
                                                          rows=len(self.nodes[0]) if self.nodes else 0)
    __repr__ = __str__

    def __eq__(self, other):
        for node1, node2 in zip(self, other):
            if node1.data != node2.data:
                print(node1.data, node2.data)
                return False
        return True

def get_git_password():
    f = open("../password.txt")
    line = f.readline().strip()
    return line

def jsonify(arg):
    """Woo recursion!"""
    if hasattr(arg, "jsonify"):
        return jsonify(arg.jsonify())

    known_types = [str, int, float, bool, type(None)]
    if type(arg) in known_types:
        return arg
    #If it's a mapping
    if isinstance(arg, Mapping):
        def wrap(item):
            return type(arg)(item)
        return wrap({jsonify(key): jsonify(value) for (key, value) in arg.items()})
    if hasattr(arg, "__iter__"):
        def wrap(item):
            return type(arg)([item])
        if len(arg) > 1:
            head, *tail = arg

            #Python doesn't do tail-call optimization anyway
            #tail is already an iterable due to the star
            #(even if it's a single element)
            return wrap(jsonify(head)) + jsonify(tail)
        elif len(arg) == 1:
            return wrap(jsonify(arg[0]))
        else:
            return wrap([])
    raise ValueError("Unbytify-able object: {obj}".format(obj=arg))

def bytify(arg):
    return json.dumps(jsonify(arg)).encode("utf-8")

def debytify(byte_string):
    string = byte_string.decode("utf-8")
    dictionary = json.loads(string)
    #This might raise exceptions, but that's fine. (There's no way to elegantly
    #handle them here.)
    module_name, cls_name = dictionary["name"].rsplit(".", 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, cls_name)
    json_dict = json.loads(string)
    return cls.dejsonify(json_dict)

