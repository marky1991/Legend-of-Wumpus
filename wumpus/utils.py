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

class Node:
    def __init__(self, data):
        self.data = data
        self.x = None
        self.y = None
        self.left = self.right = self.up = self.down = None

class Grid:
    def __init__(self, columns=50, rows=50):
        """Represents an m x n grid of nodes. 
        
        Internally implemented as a list of lists. (Sparseness
        was considered, but for my usecase, it will always be fully
        populated, so it was unnecessary complexity)"""
        self.nodes = [[None for y in rows] for x in columns]
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
            left = self.nodes[x-1][y]
            node.left = left
            if left:
                left.right = node

        if x < (len(self.nodes) - 1):
            right = self.nodes[x+1][y]
            node.right = right
            if right:
                node.left = node
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
        self.nodes[x][y] = node            

def get_git_password():
    f = open("../password.txt")
    line = f.readline().strip()
    return line
