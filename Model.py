import glm
import pygame
from OpenGL.GL import *
from numpy import array, float32


class Model(object):
    def __init__(self, data):
        self.vertexBuffer = array(data, dtype=float32)
        self.VBO = glGenBuffers(1)  # Vertex Buffer Object
        self.VAO = glGenVertexArrays(1)  # Vertex Array Object
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotation = glm.vec3(0.0, 0.0, 0.0)
        self.scale = glm.vec3(1.0, 1.0, 1.0)
        self.textureSurface = None
        self.textureData = None
        self.textureBuffer = None

    def loadTexture(self, path):
        self.textureSurface = pygame.image.load(path)
        self.textureData = pygame.image.tostring(self.textureSurface, "RGB", True)
        self.textureBuffer = glGenTextures(1)

    def getModelMatrix(self):
        identity = glm.mat4(1.0)
        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1.0, 0.0, 0.0))
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0.0, 1.0, 0.0))
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0.0, 0.0, 1.0))
        translateMatrix = glm.translate(identity, self.position)
        rotateMatrix = pitch * yaw * roll
        scaleMatrix = glm.scale(identity, self.scale)
        return translateMatrix * rotateMatrix * scaleMatrix

    def render(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        glBufferData(GL_ARRAY_BUFFER, self.vertexBuffer.nbytes, self.vertexBuffer, GL_STATIC_DRAW)

        # Positions: Attribute number, size, type, normalized, stride, offset
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Texture Coordinates:
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)

        # Texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureBuffer)
        glTexImage2D(
            GL_TEXTURE_2D,  # Texture Type
            0,  # Position
            GL_RGB,  # Internal Format
            self.textureSurface.get_width(),  # Width
            self.textureSurface.get_height(),  # Height
            0,  # Border
            GL_RGB,  # Format
            GL_UNSIGNED_BYTE,  # Type
            self.textureData  # Data
        )
        glGenerateTextureMipmap(self.textureBuffer)

        # Normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(4 * 5))
        glEnableVertexAttribArray(2)

        # Draw
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertexBuffer) // 8)
