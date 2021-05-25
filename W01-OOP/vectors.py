class V2:
    """
    A class to represent two-dimensional vectors

    Attributes:
        x (float): the first coordinate
        y (float): the second coordinate
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return 'V2[' + str(self.x) + ', ' + str(self.y) + ']'

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def __add__(self, other):
        return print(V2(self.x + other.x, self.y + other.y))

    def __mul__(self, a):
        return print(V2(self.x * a, self.y * a))

# Test instances
v = V2(1.1, 2.2)
a = V2(1.0, 2.0)
b = V2(2.2, 3.3)