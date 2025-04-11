from typing import Tuple, Union

import pygame

from src.engine.logger import verbose
from src.engine.state.stateMachine import StateMachine


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font: pygame.font.Font|None = None
        self.set_font(None, 64)
        self.text_color = (255, 255, 255)

    def set_font(self, font: str | None, size:int):
        """
        Verandert de huidige font van de renderer
        :param font: naam van de nieuwe font
        :param size: de grootte van de nieuwe font
        :return:
        """
        self.font = pygame.font.Font(font, size)

    def set_text_color(self, color: Tuple[int, int, int]|str):
        """
        Verandert de huidige kleur van de tekst die wordt gerenderd.
        Kleur wordt aangepast voor alle tekst die wordt geredeneerd na deze functie is aangeroepen.
        :param color: De nieuwe tekst kleur
        :return:
        """
        self.text_color = color

    def start_frame(self, stateMachine: StateMachine):
        verbose("[renderer] started a frame")
        huidige = stateMachine.huidige_staat
        if not huidige:
            self.screen.fill((255, 0, 255))
        else:
            self.screen.fill(huidige.background_color)

    def end_frame(self):
        pygame.display.flip()
        verbose("[renderer] finished a frame")

    def get_font_of_size(self, size: int):
        """
        Krijg de standaard font in een specifieke grootte
        :param size: De grootte van de font
        :return: Font met een specifieke grootte
        """
        return pygame.font.Font(None, size)

    def draw_text(self, text: str, x: int, y: int, size: int = 64, antialias: bool = True,
                  color: str | Tuple[int, int, int] = "Black", centered: bool = True):
        """
        Rendered text on the screen at a specific position, supporting line breaks.
        :param text: The text to render on the screen
        :param x: The X position of the text
        :param y: The Y position of the text
        :param size: (optional: int) The font size to use
        :param antialias: (optional: True or False) Whether the text should be rendered with antialiasing
        :param color: (optional: str or Tuple[int, int, int]) The color of the text to render
        :param centered: (optional: bool) Whether the text should be centered at the X, Y position
        :return:
        """
        f = self.get_font_of_size(size)
        lines = text.split('\n')  # Split the text by newlines
        line_height = f.get_height()  # Height of a single line of text
        total_height = line_height * len(lines)  # Total height of all lines

        # Adjust starting Y position if centered
        if centered:
            y -= total_height // 2

        for line in lines:
            text_surface = f.render(line, antialias, color)

            if centered:
                text_pos = text_surface.get_rect(centerx=x, centery=y)
            else:
                text_pos = text_surface.get_rect(x=x, y=y)

            self.screen.blit(text_surface, text_pos)
            y += line_height  # Move down for the next line

    def draw_text_x_centered(self, text: str, y: int, **kwargs):
        """
        Render tekst in het midden van het scherm.
        :param text: De tekst om te renderen
        :param y: De Y positie van de tekst
        :param kwargs: Optionele argument (zie :funcThe Dukedom of the Barbarian Duke X, located north of the Burning Desert. :`Renderer.draw_text`)
        :return:
        """
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
        """
        Teken een vierkant op het scherm
        :param color: De kleur van het vierkant
        :param x: De X positie van het vierkant
        :param y: De Y positie van het vierkant
        :param width: De breedte van het vierkant
        :param height: De hoogte van het vierkant
        :param border_radius: De border-radius van het vierkant
        :return:
        """
        r = pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height), border_radius=border_radius)
        return r

    def draw_image(self, image: str | pygame.Surface, x:int, y:int, image_scale:int=1):
        """
        Tekent een image op het scherm
        :param image: Het pad naar de afbeelding of een al geladen image
        :param x: De X positie van de afbeelding
        :param y: De Y positie van de afbeelding
        :param image_scale: Een size multiplier voor de afbeelding
        :return:
        """
        if isinstance(image, str):
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (image.get_width() * image_scale, image.get_height() * image_scale))
        elif image_scale != 1:
            image = pygame.transform.scale(image, (image.get_width() * image_scale, image.get_height() * image_scale))

        self.screen.blit(image, (x, y))

    def draw_image_centered(self, image: Union[str, pygame.Surface], rect: pygame.Rect = None, image_scale:int=1, **kwargs):
        """
        Draws an image centered within a given pygame.Rect (or the whole screen if None),
        with optional alignment and offsets.

        :param image: Path to the image file or a preloaded pygame.Surface
        :param rect: The pygame.Rect defining the area (defaults to the whole screen)
        :param kwargs: Additional parameters:
                       - alignment: "center" (default), "left", or "right"
                       - x_offset: Horizontal offset
                       - y_offset: Vertical offset
        """
        if rect is None:
            rect = self.screen.get_rect()  # Default to the entire screen

        if not isinstance(image, pygame.Surface):
            image = pygame.image.load(image)

        image = pygame.transform.scale(image, (image.get_width() * image_scale, image.get_height() * image_scale))

        x, y = rect.center
        img_width, img_height = image.get_size()

        # Apply alignment
        alignment = kwargs.get("alignment", "center")
        if alignment == "left":
            x = rect.left + img_width / 2  # Align left
        elif alignment == "right":
            x = rect.right - img_width / 2  # Align right

        # Apply offsets
        x += kwargs.get("x_offset", 0)
        y += kwargs.get("y_offset", 0)

        # Position image
        image_rect = image.get_rect(center=(x, y))
        self.screen.blit(image, image_rect)

