import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        self.scene = []
        self.clearColor = [0.0, 0.0, 0.0, 1.0]
        _, _, self.width, self.height = screen.get_rect()
        self.activeShader = None

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

    def setShader(self, vertex_shader=None, fragment_shader=None):
        if vertex_shader is None and fragment_shader is None:
            self.activeShader = None
        else:
            self.activeShader = compileProgram(
                compileShader(vertex_shader, GL_VERTEX_SHADER),
                compileShader(fragment_shader, GL_FRAGMENT_SHADER)
            )

    def render(self):
        glClearColor(*self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.activeShader is not None:
            glUseProgram(self.activeShader)

        for buffer in self.scene:
            buffer.render()