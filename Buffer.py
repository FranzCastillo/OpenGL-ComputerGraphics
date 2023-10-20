from OpenGL.GL import *
from numpy import array, float32


class Buffer(object):
    def __init__(self, data):
        self.vertexBuffer = array(data, dtype=float32)
        self.VBO = glGenBuffers(1)  # Vertex Buffer Object
        self.VAO = glGenVertexArrays(1)  # Vertex Array Object

    def render(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Attribute number, size, type, normalized, stride, pointer
        glBufferData(GL_ARRAY_BUFFER, self.vertexBuffer.nbytes, self.vertexBuffer, GL_STATIC_DRAW)

        # Positions: Attribute number, size, type, normalized, stride, offset
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4*6, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Colors: Attribute number, size, type, normalized, stride, offset
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4*6, ctypes.c_void_p(4*3))
        glEnableVertexAttribArray(1)

        # Draw
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertexBuffer) // 6)

