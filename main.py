import math
import os

import pygame
import glm
from pygame.locals import *

from Renderer import Renderer
from Shaders import *
from OBJ import OBJ


def getModels():
    models = []

    obj = OBJ("Models/Pumpkin/pumpkin.obj", "Models/Pumpkin/pumpkin.png")
    obj.original_position = glm.vec3(0.0, 0.0, 0.0)
    obj.model.scale = glm.vec3(2, 2, 2)
    obj.center = glm.vec3(0.0, 1.0, 0.0)
    obj.top = 2.5
    obj.bottom = -2.5
    models.append(obj)

    obj = OBJ("Models/Duck/duck.obj", "Models/Duck/duck.jpg")
    obj.original_position = glm.vec3(0, -3, 0)
    obj.model.scale = glm.vec3(0.05, 0.05, 0.05)
    obj.model.rotation = glm.vec3(-90, 0, 0)
    obj.center = glm.vec3(0, 1.0, 0)
    models.append(obj)

    obj = OBJ("Models/Death/death.obj", "Models/Death/death.jpg")
    obj.original_position = glm.vec3(0, 0, 0)
    obj.model.scale = glm.vec3(0.01, 0.01, 0.01)
    obj.center = glm.vec3(0, 0.5, 0)
    obj.top = 2
    models.append(obj)

    obj = OBJ("Models/Bender/robo.obj", "Models/Bender/robo.png")
    obj.original_position = glm.vec3(0, 0, 0)
    obj.model.scale = glm.vec3(1.2, 1.2, 1.2)
    obj.center = glm.vec3(0, 0.5, 0)
    obj.top = 3
    obj.bottom = -3
    models.append(obj)

    return models


def getModel(renderer, models, index):
    index = index % len(models)
    obj = models[index]
    obj.model.position = obj.original_position
    renderer.scene.clear()
    renderer.scene.append(obj.model)
    renderer.target = obj.model.position + obj.center
    return obj


def main():
    width = 960
    height = 540

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    renderer = Renderer(screen)
    renderer.setShader(vertex_shader, fragment_shader)

    model_index = 0
    models = getModels()
    obj = models[0]
    renderer.scene.append(obj.model)

    renderer.target = obj.model.position

    isRunning = True

    radius = 5
    angle = 0
    speed = 0.1

    is_clicking = False
    last_mouse_pos = None

    playingMusic = True
    audio_files = ["pumpkin.mp3", "duck.mp3", "death.mp3", "bender.mp3"]
    sounds = [pygame.mixer.Sound(os.path.join('Audio', file)) for file in audio_files]
    audio_index = 0
    sounds[audio_index].play()

    while isRunning:
        deltaTime = clock.tick(60) / 1000.0
        renderer.elapsedTime += deltaTime
        keys = pygame.key.get_pressed()

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
                if event.key == K_RIGHT:
                    model_index += 1
                    obj = getModel(renderer, models, model_index)

                    if playingMusic:
                        sounds[audio_index].stop()
                        audio_index = (audio_index + 1) % len(sounds)
                        sounds[audio_index].play()
                if event.key == K_LEFT:
                    model_index -= 1
                    obj = getModel(renderer, models, model_index)

                    if playingMusic:
                        sounds[audio_index].stop()
                        audio_index = (audio_index - 1) % len(sounds)
                        sounds[audio_index].play()
                if event.key == K_m:
                    playingMusic = not playingMusic
                    if playingMusic:
                        sounds[audio_index].play()
                    else:
                        sounds[audio_index].stop()
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_clicking = True
                    last_mouse_pos = pygame.mouse.get_pos()
                # Adjust the radius with the mouse wheel
                elif event.button == 4:
                    radius -= speed
                    if radius < obj.closest:
                        radius = obj.closest
                elif event.button == 5:
                    radius += speed
                    if radius > obj.furthest:
                        radius = obj.furthest
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_clicking = False
                    last_mouse_pos = None
            elif event.type == pygame.MOUSEMOTION:
                if is_clicking:
                    mouse_pos = pygame.mouse.get_pos()

                    x = last_mouse_pos[0] - mouse_pos[0]
                    angle += x * 0.01

                    y = last_mouse_pos[1] - mouse_pos[1]
                    renderer.cameraPosition.y -= y * 0.01
                    if renderer.cameraPosition.y > obj.top:
                        renderer.cameraPosition.y = obj.top
                    if renderer.cameraPosition.y < obj.bottom:
                        renderer.cameraPosition.y = obj.bottom

                    last_mouse_pos = mouse_pos
        renderer.updateViewMatrix()
        renderer.render()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
