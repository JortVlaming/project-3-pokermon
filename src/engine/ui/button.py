from typing import Callable

from src.engine.logger import warn, error


class Button:
    def __init__(self, x:int, y:int, click_width: int, click_height: int):
        self.x = x
        self.y = y
        self.click_width = click_width
        self.click_height = click_height
        self.on_click: Callable[["Button"], None]|None = None
        self.do_clicks: bool = True
        self.do_render: bool = True

    def set_on_click(self, function: Callable[["Button"], None]|None):
        self.on_click = function

    def click(self):
        if self.on_click is not None:
            try:
                self.on_click(self)
            except AttributeError as e:
                error(e)
                warn("Button heeft lamdba naar niet bestaande functie!")

    def draw(self, renderer: "Renderer"):
        raise ValueError("How da hell this happen")

    def is_in_bounds(self, mouseX: int, mouseY: int) -> bool:
        return self.x <= mouseX <= self.x + self.click_width and self.y <= mouseY <= self.y + self.click_height