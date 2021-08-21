from operator import length_hint
from numpy import matrix as mx
from numpy import cross
from math import sqrt

class Vector3D:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, w: float = 1):
        self.matrix = mx(f"{x}, {y}, {z}")
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return f"Vector3D(x: {self.x}, y: {self.y}, z: {self.z})"
    
    def __repr__(self):
        return f"Vector3D(x: {self.x}, y: {self.y}, z: {self.z})"

    def __add__(self, other):
        if not isinstance(other, Vector3D):
            return None

        result = self.matrix + other.matrix
        return Vector3D(result[0, 0], result[0, 1], result[0, 2])

    def __sub__(self, other):
        if not isinstance(other, Vector3D):
            return None

        result = self.matrix - other.matrix
        return Vector3D(result[0, 0], result[0, 1], result[0, 2])

    def __mul__(self, other):
        if not isinstance(other, (int, float, mx)):
            return None

        if isinstance(other, (int, float)):
            result = self.matrix * other
            return Vector3D(result[0, 0], result[0, 1], result[0, 2])
        else:
            return self.matrixMul(other)
    
    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            return None

        result = self.matrix / other
        return Vector3D(result[0, 0], result[0, 1], result[0, 2])

    def dot(self, other):
        if not isinstance(other, Vector3D):
            return None
        
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        if not isinstance(other, Vector3D):
            return None
        
        result = cross(self.matrix, other.matrix)
        return Vector3D(result[0, 0], result[0, 1], result[0, 2])

    def matrixMul(self, mx: mx):
        result = self.getSpecialMatrix().dot(mx)
        return Vector3D(result[0, 0], result[0, 1], result[0, 2], result[0, 3])

    def getLength(self):
        return sqrt(self.dot(self))

    def getNormaliseVec(self):
        l = self.getLength()

        if l == 0:
            return self

        return Vector3D(self.x / l, self.y / l, self.z / l)

    def setCoords(self, x, y, z):
        self.__init__(x, y, z)

    def setX(self, x):
        self.matrix[0, 0] = x
        self.x = x
        return self
    
    def setY(self, y):
        self.matrix[0, 1] = y
        self.y = y
        return self
    
    def setZ(self, z):
        self.matrix[0, 2] = z
        self.z = z
        return self

    def getSpecialMatrix(self):
        return mx(f"{self.x}, {self.y}, {self.z}, {self.w}")