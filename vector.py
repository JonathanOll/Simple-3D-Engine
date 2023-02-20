from math import tan, radians, cos, sin, sqrt
from options import screen_width, screen_height

class Vector:
    def __init__(self, *args):
        self.coords = list(args) if type(args[0]) != list else list(args[0])
    
    @staticmethod
    def zeros(length):
        return Vector([0] * length)

    @property
    def length(self):
        return len(self.coords)
    
    @property
    def norm(self):
        res = 0
        for i in range(self.length):
            res += self[i] ** 2
        return sqrt(res)
    
    def normalize(self):
        self = self * (1 / (self.norm if self.norm != 0 else 1))
        return self
    
    def dot(self, other):
        res = 0
        for i in range(self.length):
            res += self[i] * other[i]
        return res

    def __repr__(self):
        return "(" + ", ".join(str(self[i]) for i in range(self.length)) + ")"
   
    def __setitem__(self, index, value):
        self.coords[index] = value
    
    def __getitem__(self, index):
        assert index < self.length  # ne pas accéder à une coordonée inexistante 

        return self.coords[index]
    
    def __add__(self, other):
        v = Vector.zeros(self.length)
        for i in range(self.length):
            v[i] = self[i] + other[i]
        return v

    def __iadd__(self, other):
        for i in range(self.length):
            self[i] += other[i]
        return self
    
    def __imul__(self, n):
        self = self * n
        return self

    def __mul__(self, n):
        if type(n) in (float, int):
            v = Vector.zeros(self.length)
            for i in range(self.length):
                v[i] = self[i] * n
            return v
        elif type(n) == Matrix:
            res = Vector.zeros(self.length)
            for i in range(self.length):
                current = 0
                for k in range(res.length):
                    current += self[k] * n[k][i]
                res[i] = current
            return res
    
    def __rmul__(self, n):
        return self * n

    def __sub__(self, other):
        return self + (-other)
    
    def __isub__(self, other):
        self = self + (-other)
        return self

    def __neg__(self):
        v = Vector.zeros(self.length)
        for i in range(self.length):
            v[i] = -self[i]
        return v
    


class Matrix:
    def __init__(self, *args):
        args = list(args[0]) if type(args[0]) != list else args
        self.values = [Vector(args[i]) for i in range(len(args))]
    
    @staticmethod
    def zeros(width, height):
        return Matrix([0] * width for i in range(height))
    
    @staticmethod
    def projection(fov, near, far):
        ratio = screen_width/screen_height
        return Matrix([1/(ratio*tan(radians(fov/2))), 0, 0, 0], [0, 1/tan(radians(fov/2)), 0, 0], [0, 0, (far + near)/(near - far), (2 * far * near)/(near - far)], [0, 0, 1, 0])

    @staticmethod
    def rotationx(angle):
        angle = radians(angle)
        return Matrix([1, 0, 0, 0], [0, cos(angle), -sin(angle), 0], [0, sin(angle), cos(angle), 0], [0, 0, 0, 1])
    
    @staticmethod
    def rotationy(angle):
        angle = radians(angle)
        return Matrix([cos(angle), 0, sin(angle), 0], [0, 1, 0, 0], [-sin(angle), 0, cos(angle), 0], [0, 0, 0, 1])

    @staticmethod
    def rotationz(angle):
        angle = radians(angle)
        return Matrix([cos(angle), -sin(angle), 0, 0], [sin(angle), cos(angle), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1])

    @property
    def dimension(self):
        return (len(self.values), self.values[0].length)
    
    @property
    def height(self):
        return len(self.values)
    
    @property
    def width(self):
        return self.values[0].length

    def __repr__(self):
        return "[ [" + "] , \n  [".join(", ".join(str(self[i][j]) for j in range(self.dimension[1])) for i in range(self.dimension[0])) + "] ]"

    def __getitem__(self, index):
        assert index < self.dimension[0]  # ne pas accéder à une coordonée inexistante 

        return self.values[index]
    
    def __setitem__(self, index, value):
        self.values[index] = value
    
    def __mul__(self, other):
        if type(other) == Matrix:
            res = Matrix.zeros(self.width, self.height)
            for i in range(self.height):
                for j in range(self.width):
                    current = 0
                    for k in range(res.width):
                        current += self[i][k] * other[k][j]
                    res[i][j] = current
            return res
        elif type(other) == int:
            for vec in self.values:
                vec *= other
            return self
    
    def __imul__(self, other):
        self = self * other
        return self
    
    def __add__(self, other):
        res = Matrix.zeros(self.width, self.height)
        for i in range(self.height):
            for j in range(self.width):
                res[i][j] = self[i][j] + other[i][j]
        return res
    
    def __iadd__(self, other):
        self = self + other
        return self