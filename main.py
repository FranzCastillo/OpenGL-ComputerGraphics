import pygame
import glm
from pygame.locals import *

from Renderer import Renderer
from Shaders import *
from OBJ import OBJ

def main():
    width = 960
    height = 540

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    renderer = Renderer(screen)
    renderer.setShader(vertex_shader, fragment_shader)
    obj = OBJ("Models/Pumpkin/pumpkin.obj", "Models/Pumpkin/pumpkin.png")
    obj.model.position = glm.vec3(0.0, -0.3, -1.0)
    renderer.scene.append(obj.model)

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
            obj.model.rotation.y += deltaTime * 50
        if keys[K_a]:
            obj.model.rotation.y -= deltaTime * 50
        if keys[K_w]:
            obj.model.rotation.x += deltaTime * 50
        if keys[K_s]:
            obj.model.rotation.x -= deltaTime * 50


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
