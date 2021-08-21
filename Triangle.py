from Vector3D import Vector3D

from colorsys import  hls_to_rgb
from numpy import linspace, array, uint8

hue = 0.585
numcolors, scale = 32, 16
a = linspace(0, 1, num=numcolors, endpoint=True)
colorGrid = array([[hls_to_rgb(hue, lite, sat) for sat in a] for lite in a])
colorGrid = (0.5 + 255 * colorGrid).astype(uint8)
colorGrid.repeat(scale, axis=1).repeat(scale, axis=0)

class Triangle:
    def __init__(self, p1 = Vector3D(), p2 = Vector3D(), p3 = Vector3D(), color = None):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.color = color

    def __str__(self):
        return f"Triangle(p1: {self.p1}, p2: {self.p2}, p3: {self.p3})"

    def __repr__(self):
        return f"Triangle(p1: {self.p1}, p2: {self.p2}, p3: {self.p3})"

    def __lt__(self, other):
        z1 = (self.p1.z + self.p2.z + self.p3.z) / 3.0
        z2 = (other.p1.z + other.p2.z + other.p3.z) / 3.0
        return z1 > z2
    
    def setColor(self, illumination: int):
        self.color = colorGrid[round(numcolors * illumination) - 1][round(scale * illumination) - 1]
        return True