from typing import Tuple

import pygame

from src.engine.logger import verbose


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font: pygame.font.Font|None = None
        self.set_font(None, 64)
        self.text_color = (255, 255, 255)

    def set_font(self, font, size):
        self.font = pygame.font.Font(font, size)

    def set_text_color(self, color: Tuple[int, int, int]|str):
        self.text_color = color

    def start_frame(self):
        verbose("[renderer] started a frame")
        from src.engine.globals import Globals
        huidige = Globals.stateMachine.huidige_staat
        if not huidige:
            self.screen.fill((255, 0, 255))
        else:
            self.screen.fill(huidige.background_color)

    def end_frame(self):
        pygame.display.flip()
        verbose("[renderer] finished a frame")

    def get_font_of_size(self, size: int):
        return pygame.font.Font(None, size)

    def draw_text(self, text: str, x: int, y: int, **kwargs):
        f = self.font
        if "size" in kwargs:
            if isinstance(kwargs["size"], int):
                f = self.get_font_of_size(kwargs["size"])
        text_surface = f.render(text, kwargs["antialias"] if "antialias" in kwargs else True, kwargs["color"] if "color" in kwargs else self.text_color)
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

    def draw_rect(self, color: str | Tuple[int, int, int], x:int, y:int, width: int, height: int, border_radius:int=0):
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height), border_radius=border_radius)

    def draw_image(self, image: str | pygame.Surface, x:int, y:int, image_scale:int=1):
        if isinstance(image, str):
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (image.get_width() * image_scale, image.get_height() * image_scale))
        else:
            image = pygame.transform.scale(image, (image.get_width() * image_scale, image.get_height() * image_scale))

        self.screen.blit(image, (x, y))
