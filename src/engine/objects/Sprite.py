from typing import Callable

import pygame

from src.engine.Globals import Globals
from src.engine.objects.GameObject import GameObject


class Sprite(GameObject):
    def __init__(self, x:int, y:int, image:str):
        super().__init__(x, y)

        self.image = pygame.image.load(image)
        self.update_callback: None | Callable[[Sprite, list, dict], None] = None

    def set_update(self, function: None|Callable[["Square", list, dict], None]):
        self.update_callback = function

    def update(self, *args, **kwargs):
        if self.update_callback is not None:
            self.update_callback(self, list(args), dict(kwargs))

    def draw(self, *args, **kwargs):
        Globals.get_window().blit(self.image, (self.x, self.y))