import pygame
from vector import *

class Triangle:
    def __init__(self, points):
        self.points = points
    
    def draw(self, screen, color=(255, 255, 255)):
        p = []
        for i in self.points:
            p.append((i[0], i[1]))
        pygame.draw.polygon(screen, color, p)
    
    def normal(self):
        l1 = self.points[1] - self.points[0]
        l2 = self.points[2] - self.points[0]
        return Vector(l1[1] * l2[2] - l1[2] * l2[1], l1[2] * l2[0] - l1[0] * l2[2], l1[0] * l2[1] - l1[1] * l2[0]).normalize()
    
    def __rmul__(self, other):
        return self * other

    def __mul__(self, other):
        t = Triangle(self.points)
        for i in range(3):
            t.points[i] = self.points[i] * other
        return t
    
    def __add__(self, other):
        t = Triangle(self.points)
        for i in range(3):
            t.points[i] = self.points[i] + other
        return t
    
    def __sub__(self, other):
        t = Triangle(self.points)
        for i in range(3):
            t.points[i] = self.points[i] - other
        return t


class Mesh:
    def __init__(self, triangles):
        self.triangles = triangles
    
    def draw(self, screen, color=(255, 255, 255)):
        for triangle in self.triangles:
            triangle.draw(screen, color)

    def __setitem__(self, index, value):
        self.triangles[index] = value
    
    def __getitem__(self, index):
        return self.triangles[index]

    def __mul__(self, n):
        m = Mesh(self.triangles)
        for triangle in m.triangles:
            triangle *= n
        return m
    
    def __rmul__(self, n):
        return self * n
    
    def __imul__(self, other):
        self = self * other
        return self