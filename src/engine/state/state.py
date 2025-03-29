from typing import Tuple, List

import pygame

from src.engine.inputManager import InputManager
from src.engine.ui.button import Button


class State:
    buttons: List["Button"] = []
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
                if btn.is_in_bounds(mX, mY) and btn.do_clicks and btn.do_render:
                    btn.click()