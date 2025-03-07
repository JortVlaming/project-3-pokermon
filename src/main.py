import time

import pygame

from src.engine.globals import Globals
from src.engine.inputManager import InputManager
from src.engine.logger import *
from src.engine.objects.sprite import Sprite
from src.engine.objects.square import Square
from src.engine.renderer import Renderer
from src.engine.ui.imageButton import ImageButton
from src.engine.ui.textButton import TextButton
from src.engine.ui.button import Button
from src.pokemons.pokemons.froggo import Froggo

info("Hello pokermon!")

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
Globals.set_window(screen)

renderer = Renderer(screen)
renderer.set_background_color((0, 205, 205))

Globals.set_renderer(renderer)

UPDATE_CAP = 1.0/60.0

running = True

font = pygame.font.Font(None, 64)
square = Square(100, 100, "Blue", 100, 100)
sprite = Sprite(300, 300, "assets/test.jpg")

froggo = Froggo(100,400)

render_test = Square(0, 300, "Yellow", 0, 25)
test_width = 0
test_mode = 5

def test_on_click(btn: Button):
    info("BUTTON CLICK")

test_button = TextButton(400, 200, 100, 100, "Yellow", "Test")
test_button.set_on_click(test_on_click)

test_button2 = ImageButton(550, 200, "assets/cards/ruit/ruitA.png", 4)
test_button2.set_on_click(test_on_click)

buttons = [test_button, test_button2]

inputManager = InputManager()

def update():
    global test_width, test_mode
    # TODO: update game
    test_width += test_mode
    if test_width >= 800 and test_mode == 5:
        test_mode = -5
    elif test_width <= 0 and test_mode == -5:
        test_mode = 5

    if inputManager.is_key_down(pygame.K_SPACE):
        info("SPACE BAR PRESSED")
    if inputManager.is_key_held(pygame.K_SPACE):
        info("SPACE BAR HELD")

def render():
    # TODO: render game
    renderer.draw_text_x_centered("Hello pokermon!", 50)
    square.draw()
    sprite.draw()

    render_test.set_width(test_width)
    render_test.draw()

    froggo.draw()

    for btn in buttons:
        btn.draw()

def run():
    global running

    should_render = False
    lastTime = time.time_ns() / 1_000_000_000.0
    unprocessedTime = 0

    frameTime = 0
    frames = 0

    startTime = time.time()

    while running:
        firstTime = time.time_ns() / 1_000_000_000.0
        passedTime = firstTime - lastTime
        lastTime = firstTime

        unprocessedTime += passedTime
        frameTime += passedTime

        while unprocessedTime >= UPDATE_CAP:
            unprocessedTime -= UPDATE_CAP
            should_render = True

            inputManager.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in buttons:
                        if btn.is_in_bounds(pos[0], pos[1]):
                            btn.click()

                inputManager.process_event(event)

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

    endTime = time.time()

    info(f"Runtime of game: {round(endTime - startTime, 2)}s")

if __name__ == "__main__":
    set_level(LogLevel.DEBUG)

    run()