import time

import pygame

from src.engine.Globals import Globals
from src.engine.logger import *
from src.engine.objects.Sprite import Sprite
from src.engine.objects.Square import Square
from src.engine.renderer import Renderer

info("Hello pokermon!")

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
Globals.set_window(screen)

renderer = Renderer(screen)
renderer.set_background_color((0, 205, 255))

UPDATE_CAP = 1.0/60.0

running = True

font = pygame.font.Font(None, 64)
square = Square(100, 100, "Blue", 100, 100)
sprite = Sprite(300, 300, "assets/test.jpg")

render_test = Square(0, 300, "Yellow", 0, 25)
test_width = 0
test_mode = 5

def update():
    global test_width, test_mode
    # TODO: update game
    test_width += test_mode
    if test_width >= 800 and test_mode == 5:
        test_mode = -5
    elif test_width <= 0 and test_mode == -5:
        test_mode = 5

def render():
    # TODO: render game
    renderer.draw_text_x_centered("Hello pokermon!", 50)
    square.draw()
    sprite.draw()

    render_test.set_width(test_width)
    render_test.draw()

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
            renderer.start_frame()

            render()

            renderer.end_frame()

            frames += 1

            should_render = False

            pygame.display.flip()
        else:
            time.sleep(1.0/1000.0)

set_level(LogLevel.DEBUG)

run()