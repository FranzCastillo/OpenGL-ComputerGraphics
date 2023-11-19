from Model import Model
import glm


class OBJ:
    def __init__(self, modelPath, texturePath):
        self.vertices = []
        self.texture_coordinates = []
        self.normals = []
        self.faces = []
        self.initial_radius = 2.0
        self.closest = 2.0
        self.furthest = 5.0
        self.top = 1.0
        self.bottom = -1.0
        self.center = glm.vec3(0.0, 0.0, 0.0)
        self.original_position = glm.vec3(0.0, 0.0, 0.0)
        with open(modelPath) as file:
            for line in file:
                if line.startswith("v "):
                    self.vertices.append(list(map(float, line.split()[1:])))
                elif line.startswith("vt "):
                    self.texture_coordinates.append(list(map(float, line.split()[1:])))
                elif line.startswith("vn "):
                    self.normals.append(list(map(float, line.split()[1:])))
                elif line.startswith("f "):
                    face = []
                    for vertex in line.split()[1:]:
                        indices = list(map(int, vertex.split("/")))
                        face.append(indices)
                    self.faces.append(face)

        self.data = self._transformData()
        self.model = Model(self.data)
        self.model.loadTexture(texturePath)

    def _transformData(self):
        data = []
        for face in self.faces:
            if len(face) == 3:
                for vertex in face:
                    # Vertex
                    data.append(self.vertices[vertex[0] - 1][0])
                    data.append(self.vertices[vertex[0] - 1][1])
                    data.append(self.vertices[vertex[0] - 1][2])
                    # Texture Coordinates
                    data.append(self.texture_coordinates[vertex[1] - 1][0])
                    data.append(self.texture_coordinates[vertex[1] - 1][1])
                    # Normals
                    data.append(self.normals[vertex[2] - 1][0])
                    data.append(self.normals[vertex[2] - 1][1])
                    data.append(self.normals[vertex[2] - 1][2])
            elif len(face) == 4:
                for i in range(3):
                    # Vertex
                    data.append(self.vertices[face[i][0] - 1][0])
                    data.append(self.vertices[face[i][0] - 1][1])
                    data.append(self.vertices[face[i][0] - 1][2])
                    # Texture Coordinates
                    data.append(self.texture_coordinates[face[i][1] - 1][0])
                    data.append(self.texture_coordinates[face[i][1] - 1][1])
                    # Normals
                    data.append(self.normals[face[i][2] - 1][0])
                    data.append(self.normals[face[i][2] - 1][1])
                    data.append(self.normals[face[i][2] - 1][2])
                for i in [0, 2, 3]:
                    # Vertex
                    data.append(self.vertices[face[i][0] - 1][0])
                    data.append(self.vertices[face[i][0] - 1][1])
                    data.append(self.vertices[face[i][0] - 1][2])
                    # Texture Coordinates
                    data.append(self.texture_coordinates[face[i][1] - 1][0])
                    data.append(self.texture_coordinates[face[i][1] - 1][1])
                    # Normals
                    data.append(self.normals[face[i][2] - 1][0])
                    data.append(self.normals[face[i][2] - 1][1])
                    data.append(self.normals[face[i][2] - 1][2])
        return data