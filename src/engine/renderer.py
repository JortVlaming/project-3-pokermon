from typing import Tuple

import pygame

from src.engine.logger import verbose


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font: pygame.font.Font|None = None
        self.set_font(None, 64)
        self.text_color = (255, 255, 255)
        self.background_color = (0, 0, 0)

    def set_font(self, font, size):
        self.font = pygame.font.Font(font, size)

    def set_text_color(self, color: Tuple[int, int, int]|str):
        self.text_color = color

    def set_background_color(self, color: Tuple[int, int, int]|str):
        self.background_color = color

    def start_frame(self):
        verbose("[renderer] started a frame")
        self.screen.fill(self.background_color)

    def end_frame(self):
        pygame.display.flip()
        verbose("[renderer] finished a frame")

    def draw_text(self, text: str, x: int, y: int, **kwargs):
        text_surface = self.font.render(text, kwargs["antialias"] if "antialias" in kwargs else True, kwargs["color"] if "color" in kwargs else self.text_color)
        if "centered" in kwargs:
            if kwargs["centered"]:
                text_pos = text_surface.get_rect(centerx=x, centery=y)
            else:
                text_pos = text_surface.get_rect(x=x, y=y)
        else:
            text_pos = text_surface.get_rect(x=x, y=y)
        self.screen.blit(text_surface, text_pos)

    def draw_text_x_centered(self, text: str, y: int, **kwargs):
        w, h = self.screen.get_size()
        x = int(w/2-len(text)/2)
        kwargs["centered"] = True
        self.draw_text(text, x, y, **kwargs)

    def get_text_width(self, txt:str) -> int:
        return self.font.render(txt, False, (0, 0, 0, 0)).get_width()