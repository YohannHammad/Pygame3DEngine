from copy import deepcopy
from Mesh import Vector3D
from Triangle import Triangle

from math import tan, pi, cos, sin
from numpy import matrix as mx

def getMatrixRotationX(angleRad: float):
    return mx([
        [1, 0, 0, 0],
        [0, cos(angleRad), sin(angleRad), 0],
        [0, -sin(angleRad), cos(angleRad), 0],
        [0, 0, 0, 1]
    ])

def getMatrixRotationY(angleRad: float):
    return mx([
        [cos(angleRad), 0, sin(angleRad), 0],
        [0, 1, 0, 0],
        [-sin(angleRad), 0, cos(angleRad), 0],
        [0, 0, 0, 1]
    ])

def getMatrixRotationZ(angleRad: float):
    return mx([
        [cos(angleRad), sin(angleRad), 0, 0],
        [-sin(angleRad), cos(angleRad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def getMatrixTranslation(x: float, y: float, z: float):
    return mx([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1]
    ])

def getMatrixProjection(fovDegrees: float, aspectRatio: float, near: float, far: float):
    fovRad = 1.0 / tan(fovDegrees * 0.5 / 180.0 * pi)
    return mx([
        [aspectRatio * fovRad, 0, 0, 0],
        [0, fovRad, 0, 0],
        [0, 0, far / (far - near), 1.0],
        [0, 0, (-far * near) / (far - near), 0.0]
    ])

def getMatrixPointAt(pos: Vector3D, target: Vector3D, up: Vector3D):
    # Forward direction
    newForward = target - pos
    newForward = newForward.getNormaliseVec()

    # Up direction
    a = newForward * up.dot(newForward)
    newUp = up - a
    newUp = newUp.getNormaliseVec()

    # Right direction
    newRight = newUp.cross(newForward)

    # Dimensioning + Translation Matrix
    return mx([
        [newRight.x, newRight.y, newRight.z, 0],
        [newUp.x, newUp.y, newUp.z, 0],
        [newForward.x, newForward.y, newForward.z, 0],
        [pos.x, pos.y, pos.z, 1.0]
    ])

def getMatrixQuickInverse(m: mx): # Only for Rotation/Translation Matrices
    matrix = mx([
        [m[0, 0], m[1, 0], m[2, 0], 0],
        [m[0, 1], m[1, 1], m[2, 1], 0],
        [m[0, 2], m[1, 2], m[2, 2], 0],
        [0, 0, 0, 1]
    ])

    matrix[3, 0] = -(m[3, 0] * matrix[0, 0] + m[3, 1] * matrix[1, 0] + m[3, 2] * matrix[2, 0])
    matrix[3, 1] = -(m[3, 0] * matrix[0, 1] + m[3, 1] * matrix[1, 1] + m[3, 2] * matrix[2, 1])
    matrix[3, 2] = -(m[3, 0] * matrix[0, 2] + m[3, 1] * matrix[1, 2] + m[3, 2] * matrix[2, 2])
    return matrix

def getVectorIntersectPlane(planeP: Vector3D, planeN: Vector3D, lineStart: Vector3D, lineEnd: Vector3D):
    planeN = planeN.getNormaliseVec()
    planeD = -planeN.dot(planeP)
    ad = lineStart.dot(planeN)
    bd = lineEnd.dot(planeN)
    t = (-planeD - ad) / (bd - ad)
    lineStartToEnd = lineEnd - lineStart
    lineToIntersect = lineStartToEnd * t
    return lineStart + lineToIntersect

def getTriangleClipAgainstPlane(planeP: Vector3D, planeN: Vector3D, inTri: Triangle()):
    planeN = planeN.getNormaliseVec()
    
    def getDist(p: Vector3D):
        n = p.getNormaliseVec()
        return (planeN.x * p.x + planeN.y * p.y + planeN.z * p.z - planeN.dot(planeP))
    
    outTri1 = Triangle() 
    outTri2 = Triangle()

    insidePoints = []
    outsidePoints = []
    
    d1 = getDist(inTri.p1)
    d2 = getDist(inTri.p2)
    d3 = getDist(inTri.p3)

    if d1 >= 0:
        insidePoints.append(inTri.p1)
    else:
        outsidePoints.append(inTri.p1)
    
    if d2 >= 0:
        insidePoints.append(inTri.p2)
    else:
        outsidePoints.append(inTri.p2)
    
    if d3 >= 0:
        insidePoints.append(inTri.p3)
    else:
        outsidePoints.append(inTri.p3)


    if len(insidePoints) == 0:
        return []
    
    if len(insidePoints) == 3:
        return [inTri] 

    if len(insidePoints) == 1 and len(outsidePoints) == 2:
        outTri1.color = inTri.color
        
        outTri1.p1 = insidePoints[0]

        outTri1.p2 = getVectorIntersectPlane(planeP, planeN, insidePoints[0], outsidePoints[0])
        outTri1.p3 = getVectorIntersectPlane(planeP, planeN, insidePoints[0], outsidePoints[1])
        return [outTri1]

    if len(insidePoints) == 2 and len(outsidePoints) == 1:
        outTri1.color = inTri.color
        outTri2.color = inTri.color

        outTri1.p1 = insidePoints[0]
        outTri1.p2 = insidePoints[1]
        outTri1.p3 = getVectorIntersectPlane(planeP, planeN, insidePoints[0], outsidePoints[0])

        outTri2.p1 = insidePoints[1]
        outTri2.p2 = outTri1.p3
        outTri2.p3 = getVectorIntersectPlane(planeP, planeN, insidePoints[1], outsidePoints[0])
        return [outTri1, outTri2]