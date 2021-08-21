from Mesh import Mesh, Triangle, Vector3D
import utils

import sys, time, pygame
from numpy import identity

# Pygame init
pygame.init()
pygame.display.set_caption('2D to 3D')
size = width, height = 1280, 720
black = 0, 0, 0
screen = pygame.display.set_mode(size)
debugTriangles = False
theta = 0

# Load OBJ file (export with Triangles)
meshFromFile = Mesh()
res = meshFromFile.loadFromObj("cube.obj")

if not res:
    exit('Error while loading OBJ file')

# Projection variables
near = 0.1
far = 1000.0
fov = 90.0
aspectRatio = height / width
projectionMatrix = utils.getMatrixProjection(fov, aspectRatio, near, far)

# Camera
camera = Vector3D()
lookDir = Vector3D()
yaw = 0.0

# Pygame main loop
while 1:
    elapsedTime = pygame.time.Clock().tick(30) / 1000
    #theta = pygame.time.get_ticks() / 1000

    for event in pygame.event.get():
        # Quit properly
        if event.type == pygame.QUIT: sys.exit()

        # Controls
        if event.type == pygame.KEYDOWN:
            # Toggle Triangle debugging
            if event.key == pygame.K_t:
                debugTriangles = not debugTriangles

            # Camera bottom
            if event.key == pygame.K_UP:
                camera.setY(camera.y + (1.0))
            
            # Camera up
            if event.key == pygame.K_DOWN:
                camera.setY(camera.y - (1.0))
            
            # Camera left
            if event.key == pygame.K_LEFT:
                camera.setX(camera.x + (1.0))

            # Camera Right
            if event.key == pygame.K_RIGHT:
                camera.setX(camera.x - (1.0))
            
    # Still Controls
    keys_pressed = pygame.key.get_pressed()
    forward = lookDir * 0.10
    
    # Go forward
    if keys_pressed[pygame.K_z]:
        camera = camera + forward

    # Go backward
    if keys_pressed[pygame.K_s]:
        camera = camera - forward

    # Rotate camera left
    if keys_pressed[pygame.K_q]:
        yaw -= 1.0 * elapsedTime

    # Rotate camera right
    if keys_pressed[pygame.K_d]:
        yaw += 1.0 * elapsedTime

    # Reset screen
    screen.fill(black)
    
    # Rotation variables
    rotationXMatrix = utils.getMatrixRotationX(theta * 0.5)
    rotationZMatrix = utils.getMatrixRotationZ(theta)

    # World transform
    matTrans = utils.getMatrixTranslation(0.0, 0.0, 3.0)
    matWorld = identity(4)
    matWorld = rotationZMatrix * rotationXMatrix
    matWorld = matWorld * matTrans

    # Camera
    up = Vector3D(0, 1, 0)
    target = Vector3D(0, 0, 1)
    matCameraRot = utils.getMatrixRotationY(yaw)
    lookDir = target * matCameraRot
    target = camera + lookDir

    matCamera = utils.getMatrixPointAt(camera, target, up)
    matView = utils.getMatrixQuickInverse(matCamera)

    # Draw the cube
    vecTriangles = []
    for tri in meshFromFile.tris:
        # Transform
        triTransformed = Triangle()

        triTransformed.p1 = tri.p1 * matWorld
        triTransformed.p2 = tri.p2 * matWorld
        triTransformed.p3 = tri.p3 * matWorld

        # Surface normal
        normal = Vector3D()
        line1 = Vector3D()
        line2 = Vector3D()

        line1 = triTransformed.p2 - triTransformed.p1
        line2 = triTransformed.p3 - triTransformed.p1

        normal = line1.cross(line2)
        normal = normal.getNormaliseVec()

        # Camera Ray
        cameraRay = triTransformed.p1 - camera

        if normal.dot(cameraRay) < 0.0:
            # Illumination
            ligthDirection = Vector3D(0.0, 0.0, -1.0)
            ligthDirection = ligthDirection.getNormaliseVec()

            dp = max(0.1, ligthDirection.dot(normal))
            triTransformed.setColor(dp)

            # Camera 
            triViewed = Triangle()
            triViewed.p1 = triTransformed.p1 * matView
            triViewed.p2 = triTransformed.p2 * matView
            triViewed.p3 = triTransformed.p3 * matView
            triViewed.color = triTransformed.color

            # Clipping
            clipped = utils.getTriangleClipAgainstPlane(Vector3D(0, 0, 0.1), Vector3D(0, 0, 1.0), triViewed)

            for triClipped in clipped:
                # Projection
                triProjected = Triangle()
                triProjected.p1 = triClipped.p1 * projectionMatrix
                triProjected.p2 = triClipped.p2 * projectionMatrix
                triProjected.p3 = triClipped.p3 * projectionMatrix
                triProjected.color = triClipped.color

                if triProjected.p1.w != 0:
                    triProjected.p1 = triProjected.p1 / triProjected.p1.w
                
                if triProjected.p2.w != 0:
                    triProjected.p2 = triProjected.p2 / triProjected.p2.w
                
                if triProjected.p3.w != 0:
                    triProjected.p3 = triProjected.p3 / triProjected.p3.w

                # Invert X/Y
                triProjected.p1.setX(triProjected.p1.x * -1.0)
                triProjected.p2.setX(triProjected.p2.x * -1.0)
                triProjected.p3.setX(triProjected.p3.x * -1.0)

                triProjected.p1.setY(triProjected.p1.y * -1.0)
                triProjected.p2.setY(triProjected.p2.y * -1.0)
                triProjected.p3.setY(triProjected.p3.y * -1.0)

                # Scale the triangle
                offsetView = Vector3D(1, 1, 0)
                triProjected.p1 = triProjected.p1 + offsetView
                triProjected.p2 = triProjected.p2 + offsetView
                triProjected.p3 = triProjected.p3 + offsetView

                triProjected.p1.setX(triProjected.p1.x * (0.5 * (width)))
                triProjected.p1.setY(triProjected.p1.y * (0.5 * (height)))

                triProjected.p2.setX(triProjected.p2.x * (0.5 * (width)))
                triProjected.p2.setY(triProjected.p2.y * (0.5 * (height)))

                triProjected.p3.setX(triProjected.p3.x * (0.5 * (width)))
                triProjected.p3.setY(triProjected.p3.y * (0.5 * (height)))

                # Store
                vecTriangles.append(triProjected)
    
    # Sort back to front
    vecTriangles.sort()

    for triToRaster in vecTriangles:
        clipped = []
        listTriangles = []
        
        listTriangles.append(triToRaster)
        nNewTriangles = 1

        for p in range(4):
            nTrisToAdd = 0
            while nNewTriangles > 0:
                test = listTriangles[0]
                listTriangles.pop(0)
                nNewTriangles -= 1

                if p == 0:
                    clipped = utils.getTriangleClipAgainstPlane(Vector3D(0, 0, 0), Vector3D(0, 1.0, 0), test)
                elif p == 1:
                    clipped = utils.getTriangleClipAgainstPlane(Vector3D(0, height - 1, 0), Vector3D(0, -1.0, 0), test)
                elif p == 2:
                    clipped = utils.getTriangleClipAgainstPlane(Vector3D(0, 0, 0), Vector3D(1.0, 0, 0), test)
                elif p == 3:
                    clipped = utils.getTriangleClipAgainstPlane(Vector3D(width - 1, 0, 0), Vector3D(-1.0, 0, 0), test)
            
                listTriangles.extend(clipped)

            nNewTriangles = len(listTriangles)


        for t in listTriangles:
            # Draw projected triangles
            color = [255, 0, 255] if t.color is None else t.color

            pygame.draw.polygon(
                screen, 
                color, 
                [
                    (t.p1.x, t.p1.y), 
                    (t.p2.x, t.p2.y), 
                    (t.p3.x, t.p3.y)
                ]
            )

            if debugTriangles:
                pygame.draw.polygon(
                    screen, 
                    (255, 0, 0), 
                    [
                        (t.p1.x, t.p1.y), 
                        (t.p2.x, t.p2.y), 
                        (t.p3.x, t.p3.y)
                    ],
                    3
                )

    #time.sleep(0.01)
    pygame.display.flip()