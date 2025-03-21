import pygame

from src.engine.globals import Globals
from src.engine.logger import info, debug
from src.engine.objects.sprite import Sprite
from src.engine.objects.square import Square
from src.engine.state.state import State
from src.engine.ui.button import Button
from src.engine.ui.imageButton import ImageButton
from src.engine.ui.textButton import TextButton
from src.pokemons.pokemons.froggo import Froggo


class TestState(State):
    square = Square(100, 100, "Blue", 100, 100)
    sprite = Sprite(300, 300, "assets/test.jpg")

    froggo = Froggo()
    froggo.x = 100
    froggo.y = 400

    render_test = Square(0, 300, "Yellow", 0, 25)
    test_width = 0
    test_mode = 5

    def test_on_click(btn: Button):
        info("BUTTON CLICK")

    test_button = TextButton(400, 200, 100, 100, "Yellow", "Test")
    test_button.set_on_click(test_on_click)

    test_button2 = ImageButton(550, 200, "assets/cards/ruit/ruitA.png", 4)
    test_button2.set_on_click(test_on_click)

    buttons = [test_button, test_button2]

    def update(self):
        self.test_width += self.test_mode
        if self.test_width >= 800 and self.test_mode == 5:
            self.test_mode = -5
        elif self.test_width <= 0 and self.test_mode == -5:
            self.test_mode = 5

        if Globals.inputManager.is_key_down(pygame.K_SPACE):
            info("SPACE BAR PRESSED")
        if Globals.inputManager.is_key_held(pygame.K_SPACE):
            info("SPACE BAR HELD")

    def draw(self):
        Globals.renderer.draw_text_x_centered("Hello pokermon!", 50)

        self.square.draw()
        self.sprite.draw()

        self.render_test.set_width(self.test_width)
        self.render_test.draw()

        self.froggo.draw()