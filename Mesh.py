from Triangle import Triangle, Vector3D

class Mesh:
    def __init__(self, tris: list[Triangle] = []):
        self.tris = tris
        self.loadedFromFile = False
        self.filename = None
    
    def __str__(self):
        return f"Mesh({self.tris})"

    def loadFromObj(self, filename: str):
        try:
            f = open(filename, "r")
        except IOError:
            return False
        
        verts = []
        with f as reader:
            for line in reader:
                line = line.rstrip('\n')
                l = line.split(' ')
                
                if l[0] == 'v':
                    verts.append(Vector3D(float(l[1]), float(l[2]), float(l[3])))

                if l[0] == 'f':
                    self.tris.append(Triangle(verts[int(l[1]) - 1], verts[int(l[2]) - 1], verts[int(l[3]) - 1]))

        f.close()  

        self.filename = filename
        self.loadedFromFile = True
        return True
