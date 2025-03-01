import time

from logger import *
import pygame
import threading

info("Hello pokermon!")

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

UPDATE_CAP = 1.0/60.0
game_thread = None

running = True

def update():
    # TODO: update game
    pass

def render():
    # TODO: render game
    pass

def run():
    global running

    should_render = False
    firstTime = 0
    lastTime = time.time_ns() / 1_000_000_000.0
    passedTime = 0
    unprocessedTime = 0

    frameTime = 0
    frames = 0
    fps = 0

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

            render()

            frames += 1

            should_render = False
            pass
        else:
            time.sleep(1.0/1000.0)

set_level(LogLevel.DEBUG)

game_thread = threading.Thread(target=run)
game_thread.start()
game_thread.join()