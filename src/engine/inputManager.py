from typing import Dict

import pygame.event


class InputManager:
    keys: Dict[int, bool] = {}
    keysLast: Dict[int, bool] = {}

    buttons: Dict[int, bool] = {}
    buttonsLast: Dict[int, bool] = {}

    def __init__(self):
        pass

    def update(self):
        self.keysLast = self.keys.copy()
        self.buttonsLast = self.buttons.copy()

    def process_event(self, event: pygame.event.Event):
        if event.type != pygame.KEYDOWN and event.type != pygame.KEYUP\
                and event.type != pygame.MOUSEBUTTONDOWN and event.type != pygame.MOUSEBUTTONUP:
            return

        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = False
            self.keysLast[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.buttons[event.button] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.buttons[event.button] = False
            self.buttonsLast[event.button] = False

    def is_key_down(self, key: int) -> bool:
        try:
            return self.keys[key] and not self.keysLast[key]
        except (IndexError, KeyError):
            if key not in self.keys:
                return False
            if key not in self.keysLast:
                return self.keys[key]
            return False

    def is_key_held(self, key: int) -> bool:
        try:
            return self.keys[key] and self.keysLast[key]
        except (IndexError, KeyError):
            return False

    def is_button_down(self, button: int) -> bool:
        try:
            return self.buttons[button] and not self.buttonsLast[button]
        except (IndexError, KeyError):
            if button not in self.buttons:
                return False
            if button not in self.buttonsLast:
                return self.buttons[button]
            return False

    def is_button_held(self, button: int) -> bool:
        try:
            return self.buttons[button] and self.buttonsLast[button]
        except (IndexError, KeyError):
            return False