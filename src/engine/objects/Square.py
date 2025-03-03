from typing import Tuple, Callable

import pygame

from src.engine.objects.GameObject import GameObject
from src.engine.Globals import Globals


class Square(GameObject):
    def __init__(self, x:int, y:int, color: Tuple[int, int, int]|str, width: int, height: int):
        super().__init__(x, y)

        self.color = color
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.update_callback: None | Callable[[Square, list, dict], None] = None

    def set_update(self, function: None|Callable[["Square", list, dict], None]):
        self.update_callback = function

    def update(self, *args, **kwargs):
        if self.update_callback is not None:
            self.update_callback(self, list(args), dict(kwargs))

    def draw(self, *args, **kwargs):
        Globals.get_window().blit(self.image, (self.x, self.y))
