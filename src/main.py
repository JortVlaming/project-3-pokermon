import time

import pygame

from logger import *
from src.renderer import Renderer

info("Hello pokermon!")

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

renderer = Renderer(screen)
renderer.set_background_color("Red")

UPDATE_CAP = 1.0/60.0

running = True

font = pygame.font.Font(None, 64)

def update():
    # TODO: update game
    pass

def render():
    # TODO: render game
    renderer.draw_text_x_centered("Hello pokermon!", 50)

def run():
    global running

    should_render = False
    lastTime = time.time_ns() / 1_000_000_000.0
    unprocessedTime = 0

    frameTime = 0
    frames = 0

    while running:
        firstTime = time.time_ns() / 1_000_000_000.0
        passedTime = firstTime - lastTime
        lastTime = firstTime

        unprocessedTime += passedTime
        frameTime += passedTime

        while unprocessedTime >= UPDATE_CAP:
            unprocessedTime -= UPDATE_CAP
            should_render = True

            verbose("UPDATE")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            update()

            if frameTime >= 1.0:
                frameTime = 0
                fps = frames
                frames = 0
                debug("FPS:", fps)

        if should_render:
            verbose("RENDER")

            renderer.start_frame()

            render()

            renderer.end_frame()

            frames += 1

            should_render = False

            pygame.display.flip()
        else:
            time.sleep(1.0/1000.0)

set_level(LogLevel.VERBOSE)

run()