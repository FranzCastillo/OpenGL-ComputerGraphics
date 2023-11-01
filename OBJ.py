from Model import Model


class OBJ:
    def __init__(self, modelPath, texturePath):
        self.vertices = []
        self.texture_coordinates = []
        self.normals = []
        self.faces = []
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
            for vertexInfo in face:
                vertexId, textureID, normalId = vertexInfo
                vertex = self.vertices[vertexId - 1]
                normals = self.normals[normalId - 1]
                uv = self.texture_coordinates[textureID - 1]
                data.extend(vertex + uv + normals)
        return data
