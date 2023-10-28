import pygame
import glm
from pygame.locals import *

from Renderer import Renderer
from Model import Model
from Shaders import *

def main():
    width = 960
    height = 540

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    renderer = Renderer(screen)
    renderer.setShader(vertex_shader, fragment_shader)
    # x, y, z, U, V
    triangleData = [
        -0.5, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
        0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,

        -0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
        0.5, 0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0,
        0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
    ]
    triangleModel = Model(triangleData)
    triangleModel.loadTexture("Textures/text.jpg")
    triangleModel.position.z = -5
    triangleModel.scale = glm.vec3(3, 3, 3)
    renderer.scene.append(triangleModel)

    isRunning = True
    while isRunning:
        deltaTime = clock.tick(60) / 1000.0
        renderer.elapsedTime += deltaTime
        keys = pygame.key.get_pressed()

        if keys[K_RIGHT]:
            renderer.clearColor[0] += deltaTime
        if keys[K_LEFT]:
            renderer.clearColor[0] -= deltaTime
        if keys[K_UP]:
            renderer.clearColor[1] += deltaTime
        if keys[K_DOWN]:
            renderer.clearColor[1] -= deltaTime
        if keys[K_SPACE]:
            renderer.clearColor[2] += deltaTime
        if keys[K_LSHIFT]:
            renderer.clearColor[2] -= deltaTime

        if keys[K_d]:
            triangleModel.rotation.y += deltaTime * 50
        if keys[K_a]:
            triangleModel.rotation.y -= deltaTime * 50
        if keys[K_w]:
            triangleModel.rotation.x += deltaTime * 50
        if keys[K_s]:
            triangleModel.rotation.x -= deltaTime * 50


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


if __name__ == "__main__":
    main()
