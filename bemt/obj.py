
import numpy as np

class OBJ:
    def __init__(self, sectionPath):
        # Load section
        self.section = np.loadtxt(sectionPath, skiprows=1)

        # Move section back by c/4
        for i in range(len(self.section)):
            self.section[i][0] -= 0.25

        # Init arrays
        self.vertices = []
        self.indices = []
        self.centerPoints = []
        self.vps = len(self.section)

    def add(self, x, twist, chord):
        # Create rotation/scale matrix
        trad = -np.deg2rad(twist)
        sect = np.zeros((self.vps, 2))
        A = np.array([
            [ np.cos(trad), -np.sin(trad) ],
            [ np.sin(trad),  np.cos(trad) ]
        ]) * chord

        # Create modified section
        for i in range(self.vps):
            sect[i] = np.dot(A, self.section[i])

        # Compute and save center point
        c = np.array([ 0.596, 0.0422 ])
        ct = np.dot(A, c)
        self.centerPoints.append([ x, ct[0], ct[1] ])

        # Append to vertices
        for i in range(self.vps):
            self.vertices.append([ x, sect[i][0], sect[i][1] ])

        # If not first, create indices
        nvert = len(self.vertices)
        if  nvert > self.vps:
            for i in range(self.vps):
                a1 = nvert - (2*self.vps) + i
                a2 = nvert - (2*self.vps) + ((i + 1) % self.vps)
                b1 = nvert - self.vps + i
                b2 = nvert - self.vps + ((i + 1) % self.vps)
                self.indices.append([ a1, a2, b1 ])
                self.indices.append([ a2, b1, b2 ])

    def closeEnds(self):
        nvert = len(self.vertices)

        # Add center points
        ch = len(self.vertices)
        self.vertices.append(self.centerPoints[0])
        ct = len(self.vertices)
        self.vertices.append(self.centerPoints[len(self.centerPoints)-1])

        # Create hub face
        for i in range(self.vps):
            a1 = i
            a2 = (i + 1) % self.vps
            self.indices.append([ ch, a1, a2 ])

        # Create tip face
        for i in range(self.vps):
            a1 = nvert - self.vps + i
            a2 = nvert - self.vps + ((i + 1) % self.vps)
            self.indices.append([ ct, a1, a2 ])

    def save(self, path):
        # Open OBJ file
        file = open(path, 'w')

        # Write vertices
        for v in self.vertices:
            vv = np.array(v)*1e3
            file.write('v %lf %lf %lf\n' % (vv[0], vv[1], vv[2]))

        # Write indices
        for i in self.indices:
            file.write('f %d %d %d\n' % (i[0]+1, i[1]+1, i[2]+1))

        # Close OBJ file
        file.close()