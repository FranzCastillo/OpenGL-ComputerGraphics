import math

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
    obj.model.position = glm.vec3(0.0, -0.4, -1.5)
    renderer.scene.append(obj.model)
    renderer.target = obj.model.position

    isRunning = True

    radius = 3
    angle = 0
    speed = 0.1

    while isRunning:
        deltaTime = clock.tick(60) / 1000.0
        renderer.elapsedTime += deltaTime
        keys = pygame.key.get_pressed()

        if keys[K_a]:
            angle += speed
        if keys[K_d]:
            angle -= speed
        if keys[K_w]:
            if renderer.cameraPosition.y < 1.0:
                renderer.cameraPosition.y += speed
        if keys[K_s]:
            if renderer.cameraPosition.y > -1.0:
                renderer.cameraPosition.y -= speed
        if keys[K_SPACE]:
            radius += speed
        if keys[K_LSHIFT]:
            radius -= speed

        renderer.cameraPosition.x = obj.model.position.x + radius * math.sin(angle)
        renderer.cameraPosition.z = obj.model.position.z + radius * math.cos(angle)


        # Handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isRunning = False
                if event.key == pygame.K_f:
                    renderer.toggleFilledMode()
                # Handle Shaders
                if event.key == K_0:
                    renderer.setShader(vertex_shader, fragment_shader)
                if event.key == K_1:
                    renderer.setShader(vertex_shader, tvStatic_fragment_shader)
                if event.key == K_2:
                    renderer.setShader(vertex_shader, random_normal_map_fragment_shader)
                if event.key == K_3:
                    renderer.setShader(vertex_shader, rainbow_fragment_shader)
                if event.key == K_4:
                    renderer.setShader(vertex_shader, ripple_fragment_shader)
                if event.key == K_5:
                    renderer.setShader(vertex_shader, fire_fragment_shader)
                if event.key == K_6:
                    renderer.setShader(vertex_shader, grayscale_fragment_shader)
                if event.key == K_7:
                    renderer.setShader(vertex_shader, blur_fragment_shader)
                if event.key == K_8:
                    renderer.setShader(glitch_vertex_shader, glitch_fragment_shader)
                if event.key == K_9:
                    renderer.setShader(heart_vertex_shader, heart_fragment_shader)

        renderer.updateViewMatrix()
        renderer.render()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
