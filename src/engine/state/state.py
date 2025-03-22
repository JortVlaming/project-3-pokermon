from typing import Tuple

import pygame

from src.engine.inputManager import InputManager


class State:
    buttons = []
    do_process_buttons = True
    background_color: Tuple[int, int, int]|str = (255,0,255)
    
    def __init__(self):
        pass

    def update(self, inputManager:InputManager, stateMachine):
        pass

    def draw(self, renderer):
        pass

    def transition_cue(self):
        pass
    
    def process_buttons(self, inputManager: InputManager):
        if inputManager.is_button_down(pygame.BUTTON_LEFT):
            mX, mY = pygame.mouse.get_pos()
            for btn in self.buttons:
                if btn.is_in_bounds(mX, mY):
                    btn.click()