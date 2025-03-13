import time

import pygame

from src.engine.globals import Globals
from src.engine.inputManager import InputManager
from src.engine.logger import *
from src.engine.renderer import Renderer
from src.engine.state.stateMachine import StateMachine
from src.states.mainMenuState import MainMenuState
from src.states.testState import TestState

info("Hello pokermon!")

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokermon")
Globals.set_window(screen)

renderer = Renderer(screen)

Globals.set_renderer(renderer)

UPDATE_CAP = 1.0/60.0

running = True

font = pygame.font.Font(None, 64)

inputManager = InputManager()
Globals.inputManager = inputManager

stateMachine = StateMachine()
Globals.stateMachine = stateMachine

mainMenuState = MainMenuState()

stateMachine.huidige_staat = mainMenuState

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

                inputManager.process_event(event)

            stateMachine.update()

            if frameTime >= 1.0:
                frameTime = 0
                fps = frames
                frames = 0
                debug("FPS:", fps)

        if should_render:
            renderer.start_frame()

            stateMachine.draw()

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