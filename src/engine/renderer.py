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

    def draw_text_centered(self, text: str, rect: pygame.Rect = None, **kwargs):
        """
        Draws text centered within a given pygame.Rect (or the whole screen if None),
        automatically scaling it to fit.

        :param text: The text to render
        :param rect: The pygame.Rect defining the area (defaults to the whole screen)
        :param kwargs: Additional parameters (e.g., font, color)
        """
        if rect is None:
            rect = self.screen.get_rect()  # Default to the entire screen

        font = kwargs.get("font", pygame.font.Font(None, 36))  # Default font
        max_width, max_height = rect.width, rect.height
        text_width, text_height = 0, 0

        font_size = kwargs.get("start", 72)
        while 10 < font_size:
            test_font = pygame.font.Font(None, font_size)
            text_width, text_height = test_font.size(text)
            if text_width <= max_width and text_height <= max_height:
                font = test_font
                break
            font_size -= 1

        text_surface = font.render(text, True, kwargs.get("color", (255, 255, 255)))
        x, y = rect.center
        y += kwargs.get("y_offset", 0)
        if kwargs.get("alignment", "center") == "left":
            x = rect.x+text_width/2
        elif kwargs.get("alignment", "center") == "right":
            x = rect.x + rect.width-text_width
        x += kwargs.get("x_offset", 0)
        text_rect = text_surface.get_rect(center=(x,y))

        self.screen.blit(text_surface, text_rect)

    def get_text_width(self, txt:str) -> int:
        return self.font.render(txt, False, (0, 0, 0, 0)).get_width()

    def draw_rect(self, color: str | Tuple[int, int, int] | Tuple[int, int, int, int], x:int, y:int, width: int, height: int, border_radius:int=0):
        r = pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height), border_radius=border_radius)
        return r

    def draw_image(self, image: str | pygame.Surface, x:int, y:int, image_scale:int=1):
        if isinstance(image, str):
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (image.get_width() * image_scale, image.get_height() * image_scale))
        else:
            image = pygame.transform.scale(image, (image.get_width() * image_scale, image.get_height() * image_scale))

        self.screen.blit(image, (x, y))
