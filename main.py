import pygame
from OpenGL.GL import *

from Renderer import Renderer
from Buffer import Buffer
from Shaders import *

width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)
# x, y, z, r, g, b
triangle = [
    -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
    0.0, 0.5, 0.0, 0.0, 1.0, 0.0,
    0.5, -0.5, 0.0, 0.0, 0.0, 1.0,
]
renderer.scene.append(Buffer(triangle))

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        renderer.clearColor[0] += deltaTime
    if keys[pygame.K_LEFT]:
        renderer.clearColor[0] -= deltaTime
    if keys[pygame.K_UP]:
        renderer.clearColor[1] += deltaTime
    if keys[pygame.K_DOWN]:
        renderer.clearColor[1] -= deltaTime
    if keys[pygame.K_SPACE]:
        renderer.clearColor[2] += deltaTime
    if keys[pygame.K_LSHIFT]:
        renderer.clearColor[2] -= deltaTime

    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    renderer.render()
    pygame.display.flip()

pygame.quit()