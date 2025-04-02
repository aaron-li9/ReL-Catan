import numpy as np
import pygame
import random


class Vector:

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.vector = point2 - point1
        self.midpoint = (point1 + point2) / 2
        self.magnitude = np.linalg.norm(self.vector)
        self.unit = self.vector / self.magnitude
        self.normal = np.array([self.unit[1], -self.unit[0]])

    @classmethod
    def from_points(cls, x1, y1, x2, y2):
        return cls(np.array([x1, y1]), np.array([x2, y2]))

    def get_midpoint(self):
        return self.midpoint

    def get_vector(self):
        return self.vector

    def get_unit(self):
        return self.unit

    def get_normal(self):
        return self.normal
