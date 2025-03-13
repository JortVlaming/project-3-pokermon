from typing import Tuple

import pygame

from src.engine.globals import Globals
from src.engine.state.state import State
from src.pokemons.classes.attack import Attack
from src.pokemons.classes.pokermon import Pokermon


def get_health_bar(base: int, max_value: int, scale: int) -> Tuple[int, Tuple[int, int, int]]:
    if max_value <= 0:
        raise ValueError("max_value must be greater than 0")

    percentage = base / max_value
    bar_length = round(percentage * scale)
    bar_length = max(0, min(bar_length, scale))

    if percentage <= 0.33:
        color = (255, 0, 0)  # Red
    elif percentage <= 0.66:
        color = (255, 165, 0)  # Orange
    else:
        color = (0, 255, 0)  # Green

    return bar_length, color


class FightState(State):
    def __init__(self, speler_mon:Pokermon, ai_mon: Pokermon):
        super().__init__()

        self.speler = speler_mon
        self.speler.x = 150
        self.speler.y = Globals.renderer.screen.get_height() - self.speler.image.get_height() - 150

        self.ai = ai_mon
        self.ai.x = Globals.renderer.screen.get_width() - self.ai.image.get_width() - 100
        self.ai.y = 200 - self.ai.image.get_height()

        self.staat = 0

        self.buttons = []
        self.background_color = (200, 200, 200)

        self.staat = 0
        self.speler_aanval: Attack|None = None
        self.ai_aanval: Attack|None = None


    def update(self):
        if self.staat == 0:
            if Globals.inputManager.is_key_held(pygame.K_p):
                self.speler.hp -= 1
                if self.speler.hp < 0:
                    self.speler.hp = 0
            if Globals.inputManager.is_key_held(pygame.K_o):
                self.speler.hp += 1
                if self.speler.hp > self.speler.max_hp:
                    self.speler.hp = self.speler.max_hp

    def draw(self):
        self.speler.draw()
        self.ai.draw()

        renderer = Globals.renderer

        renderer.draw_rect((150, 150, 150), 0, renderer.screen.get_height()-150, renderer.screen.get_width(), 150, 0)

        renderer.draw_text(self.speler.name, 20, renderer.screen.get_height()-130)

        length, color = get_health_bar(self.speler.hp, self.speler.max_hp, 31*5)

        renderer.draw_rect(color, 15, renderer.screen.get_height()-75, length, 20)
        renderer.draw_image("assets/healthbar.png", 15, renderer.screen.get_height()-80, 5)

        renderer.draw_text(f"{self.speler.hp}/{self.speler.max_hp}", 15, renderer.screen.get_height()-50, size=32)