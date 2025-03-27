import random
from typing import Tuple

import pygame

from src.engine.logger import info, warn
from src.engine.renderer import Renderer
from src.engine.state.state import State
from src.engine.ui.button import Button
from src.engine.ui.textButton import TextButton
from src.pokemons.attacks.explosion import Explosion
from src.pokemons.classes.attack import Attack
from src.pokemons.classes.pokermon import Pokermon
from src.pokemons.pokemons.all import *


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

class MoveButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, move: Attack | None, index:int, pp: int, max_pp: int):
        super().__init__(x, y, width, height)

        self.width = width
        self.height = height
        self.move = move
        self.index = index
        self.pp = pp
        self.max_pp = max_pp

    def draw(self, renderer: Renderer):
        if self.move:
            r = renderer.draw_rect((255, 255, 255) if self.pp > 0 else (125, 125, 125), self.x,
                                   renderer.screen.get_height() - 125, 100, 100)
            renderer.draw_text_centered(type(self.move).__name__, r, start=48, color=(0, 0, 0), y_offset=-20)
            renderer.draw_text_centered(f"{self.pp}/{self.max_pp} PP", r, start=24, color=(0, 0, 0), y_offset=20)
        else:
            r = renderer.draw_rect((100, 100, 100), self.x, renderer.screen.get_height() - 125, 100, 100)
            renderer.draw_text_centered("-", r, color=(75, 75, 75))

class FightState(State):
    def __init__(self, speler_mon:Pokermon, ai_mon: Pokermon, renderer: Renderer):
        super().__init__()

        self.speler = speler_mon
        self.speler.x = 150
        self.speler.y = renderer.screen.get_height() - self.speler.image.get_height() - 150

        self.ai = ai_mon
        self.ai.x = renderer.screen.get_width() - self.ai.image.get_width() - 100
        self.ai.y = 200 - self.ai.image.get_height()

        self.staat = 0

        self.background_color = (200, 200, 200)

        self.staat = 0
        self.speler_aanval: Attack|None = None
        self.ai_aanval: Attack|None = None

        self.buttons_made = False

        menuButton = TextButton(
            750,
            renderer.screen.get_height() - 125,
            100,
            100,
            (255, 255, 255),
            "Menu",
            (0, 0, 0),
            48
        )

        x = 250
        menuButton.set_on_click(lambda btn : self.toggle_menu())

        self.buttons = [menuButton]

        for i in range(0, 4):
            move = speler_mon.moves[i] if i < len(speler_mon.moves) else None

            if move:
                btn = MoveButton(x, renderer.screen.get_height() - 125, 100, 100, move[0], i, move[1], move[2])
                btn.set_on_click(self.move_click)
            else:
                btn = MoveButton(x, renderer.screen.get_height() - 125, 100, 100, None, i, 0, 0)

            self.buttons.append(btn)
            x += 125

    def transition_cue(self):
        self.ai.hp = self.ai.max_hp

        for move in self.speler.moves:
            move[1] = move[2]


    def update(self, inputManager, stateMachine):
        self.stateMachine = stateMachine
        if self.staat == 0:
            if inputManager.is_key_held(pygame.K_p):
                self.speler.hp -= 1
                if self.speler.hp < 0:
                    self.speler.hp = 0
            if inputManager.is_key_held(pygame.K_o):
                self.speler.hp += 1
                if self.speler.hp > self.speler.max_hp:
                    self.speler.hp = self.speler.max_hp
            if inputManager.is_key_down(pygame.K_r):
                stateMachine.start_transitie(FightState(self.speler, self.ai, self.renderer), 1.5)
                warn("Gevecht reset triggered")

    def draw(self, renderer):
        self.renderer = renderer

        self.speler.draw(renderer)
        self.ai.draw(renderer)


        # speler stuff
        mon_name_rect = renderer.draw_rect((10, 10, 10, 0), 20, renderer.screen.get_height() - 130, 155, 30)
        mon_health_rect = renderer.draw_rect((10, 10, 10, 0), 20, renderer.screen.get_height() - 47, 155, 30)

        renderer.draw_rect((150, 150, 150), 0, renderer.screen.get_height()-150, renderer.screen.get_width(), 150, 0)

        renderer.draw_text_centered(self.speler.name, mon_name_rect, alignment="left")

        length, color = get_health_bar(self.speler.hp, self.speler.max_hp, 155)

        renderer.draw_rect(color, 15, renderer.screen.get_height()-75, length, 20)
        renderer.draw_image("assets/healthbar.png", 15, renderer.screen.get_height()-80, 5)

        renderer.draw_text_centered(f"{self.speler.hp}/{self.speler.max_hp}", mon_health_rect, alignment="left", size=32)

        # ai stuff
        ai_health_rect = renderer.draw_rect((0, 0, 0, 0), self.ai.x - 255 + 150, 105, 80, 30)
        ai_name_rect = renderer.draw_rect((150, 150, 150), self.ai.x - 275, 50, 255, 100, 10)

        renderer.draw_text_centered(self.ai.name, ai_name_rect, start=48, y_offset=-15, alignment="left", x_offset=10)

        ai_length, ai_color = get_health_bar(self.ai.hp, self.ai.max_hp, 155)

        renderer.draw_rect(ai_color, ai_name_rect.x+10, ai_name_rect.y+ai_name_rect.height-40, ai_length, 20)
        renderer.draw_image("assets/healthbar.png", ai_name_rect.x+10, ai_name_rect.y+ai_name_rect.height-45, 5)


        renderer.draw_text_centered(f"{self.ai.hp}/{self.ai.max_hp}", ai_health_rect, start=48, alignment="left", color=(255, 255, 255))

    def move_click(self, btn:Button|MoveButton):
        if not isinstance(btn, MoveButton):
            return

        stateMachine = self.stateMachine

        from src.states.mainMenuState import MainMenuState
        if self.speler.speed > self.ai.speed:
            info(btn.move.name)

            if self.speler.moves[btn.index][1] <= 0:
                info("Geen PP!")
                return

            self.speler.moves[btn.index][1] -= 1

            if isinstance(self.speler.moves[btn.index][1], Explosion):
                self.speler.hp = 0

            self.ai.hp -= btn.move.calculate_damage(self.speler, self.ai, True)
            if self.ai.hp <= 0:
                info("speler wint")
                self.ai.hp = 0
                stateMachine.start_transitie(MainMenuState(self.renderer, self.stateMachine), 2.5)
                return

            move = random.choice(self.ai.moves)

            dmg = move[0].calculate_damage(self.ai, self.speler, True)

            self.speler.hp -= dmg

            if self.speler.hp <= 0:
                self.speler.hp = 0
                warn("Speler is dood")
                stateMachine.start_transitie(MainMenuState(self.renderer, self.stateMachine), 2.5)
                return
        else:
            warn("AI Moved eerst")

            move = random.choice(self.ai.moves)

            dmg = move[0].calculate_damage(self.ai, self.speler, True)

            self.speler.hp -= dmg

            if self.speler.hp <= 0:
                self.speler.hp = 0
                warn("Speler is dood")
                stateMachine.start_transitie(MainMenuState(self.renderer, self.stateMachine), 2.5)
                return

            info(btn.move.name)

            if self.speler.moves[btn.index][1] <= 0:
                info("Geen PP!")
                return

            self.speler.moves[btn.index][1] -= 1

            self.ai.hp -= btn.move.calculate_damage(self.speler, self.ai, True)
            if self.ai.hp <= 0:
                info("speler wint")
                self.ai.hp = 0
                stateMachine.start_transitie(MainMenuState(self.renderer, self.stateMachine), 2.5)
                return

    @staticmethod
    def random_battle(renderer:Renderer):
        mons = get_all()

        speler = random.choice(mons)
        mons.remove(speler)
        speler = speler()
        ai = random.choice(mons)()

        return FightState(speler, ai, renderer)