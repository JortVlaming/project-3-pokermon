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
        color = (255, 0, 0)
    elif percentage <= 0.66:
        color = (255, 165, 0)
    else:
        color = (0, 255, 0)

    return bar_length, color

class MoveButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, move: Attack | None, index: int, pp: int, max_pp: int):
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

class SwitchButton(Button):
    def __init__(self, x, y, width, height, mon_index: int, pokermon: Pokermon | None, active: bool = False):
        super().__init__(x, y, width, height)
        self.mon_index = mon_index
        self.pokermon = pokermon
        self.active = active
        self.width = width
        self.height = height

    def draw(self, renderer: Renderer):
        if self.pokermon is None:
            r = renderer.draw_rect((75, 75, 75), self.x, self.y, self.width, self.height)
            renderer.draw_text_centered("-", r, color=(50, 50, 50))
        elif self.active:
            r = renderer.draw_rect((125, 125, 125), self.x, self.y, self.width, self.height)
            renderer.draw_text_centered("Active", r, y_offset=-15, color=(0, 0, 0), start=20)
            renderer.draw_text_centered(self.pokermon.name, r, y_offset=15, color=(0, 0, 0), start=16)
        else:
            color = (200, 200, 255) if self.pokermon.hp > 0 else (150, 150, 150)
            r = renderer.draw_rect(color, self.x, self.y, self.width, self.height)
            renderer.draw_text_centered(self.pokermon.name, r, y_offset=-20, color=(0, 0, 0), start=20)
            renderer.draw_text_centered(f"{self.pokermon.hp}/{self.pokermon.max_hp}", r, y_offset=20, color=(0, 0, 0), start=20)


class FightState(State):
    def __init__(self, speler_team: list[Pokermon], ai_mon: Pokermon, renderer: Renderer):
        super().__init__()

        self.speler_team = speler_team
        self.current_speler_index = 0
        self.ai = ai_mon
        self.renderer = renderer

        self.staat = 0
        self.speler_aanval: Attack | None = None
        self.ai_aanval: Attack | None = None
        self.switching = False

        self.background_color = (200, 200, 200)

        self.active_speler.x = 150
        self.active_speler.y = renderer.screen.get_height() - self.active_speler.image.get_height() - 150

        self.ai.x = renderer.screen.get_width() - self.ai.image.get_width() - 100
        self.ai.y = 200 - self.ai.image.get_height()

        self.buttons_made = False
        self.make_buttons()

    @property
    def active_speler(self) -> Pokermon:
        return self.speler_team[self.current_speler_index]

    def make_buttons(self):
        self.buttons = []

        menuButton = TextButton(
            750,
            self.renderer.screen.get_height() - 125,
            100,
            100,
            (255, 255, 255),
            "Switch",
            (0, 0, 0),
            40
        )
        menuButton.set_on_click(lambda btn: self.toggle_switch_mode())
        self.buttons.append(menuButton)

        if not self.switching:
            x = 250
            for i in range(0, 4):
                move = self.active_speler.moves[i] if i < len(self.active_speler.moves) else None

                if move:
                    btn = MoveButton(x, self.renderer.screen.get_height() - 125, 100, 100, move[0], i, move[1], move[2])
                    btn.set_on_click(self.move_click)
                else:
                    btn = MoveButton(x, self.renderer.screen.get_height() - 125, 100, 100, None, i, 0, 0)

                self.buttons.append(btn)
                x += 125
        else:
            x = 250
            for i in range(4):
                if i >= len(self.speler_team):
                    mon = None
                else:
                    mon = self.speler_team[i]

                is_active = (i == self.current_speler_index)
                btn = SwitchButton(x, self.renderer.screen.get_height() - 125, 100, 100, i, mon, is_active)

                if mon is not None and mon.hp > 0 and not is_active:
                    btn.set_on_click(self.switch_click)

                self.buttons.append(btn)
                x += 125

    def toggle_switch_mode(self):
        self.switching = not self.switching
        self.make_buttons()

    def switch_click(self, btn: Button):
        if not isinstance(btn, SwitchButton):
            return
        self.current_speler_index = btn.mon_index
        self.active_speler.x = 150
        self.active_speler.y = self.renderer.screen.get_height() - self.active_speler.image.get_height() - 150
        self.switching = False
        self.make_buttons()

    def transition_cue(self):
        self.ai.hp = self.ai.max_hp
        for mon in self.speler_team:
            for move in mon.moves:
                move[1] = move[2]

    def update(self, inputManager, stateMachine):
        self.stateMachine = stateMachine

    def draw(self, renderer):
        self.renderer = renderer
        mon_name_rect = renderer.draw_rect((10, 10, 10, 0), 20, renderer.screen.get_height() - 130, 155, 30)
        mon_health_rect = renderer.draw_rect((10, 10, 10, 0), 20, renderer.screen.get_height() - 47, 155, 30)

        renderer.draw_image_centered("assets/grass.png")

        self.active_speler.draw(renderer)
        self.ai.draw(renderer)

        renderer.draw_text_centered(self.active_speler.name, mon_name_rect, alignment="left")

        length, color = get_health_bar(self.active_speler.hp, self.active_speler.max_hp, 155)

        renderer.draw_rect(color, 15, renderer.screen.get_height() - 75, length, 20)
        renderer.draw_image("assets/healthbar.png", 15, renderer.screen.get_height() - 80, 5)

        renderer.draw_text_centered(f"{self.active_speler.hp}/{self.active_speler.max_hp}", mon_health_rect, alignment="left", size=32)

        ai_health_rect = renderer.draw_rect((0, 0, 0, 0), self.ai.x - 255 + 150, 105, 80, 30)
        ai_name_rect = renderer.draw_rect((0, 0, 150), self.ai.x - 275, 50, 255, 100, 10)

        renderer.draw_text_centered(self.ai.name, ai_name_rect, start=48, y_offset=-15, alignment="left", x_offset=10)

        ai_length, ai_color = get_health_bar(self.ai.hp, self.ai.max_hp, 155)

        renderer.draw_rect(ai_color, ai_name_rect.x + 10, ai_name_rect.y + ai_name_rect.height - 40, ai_length, 20)
        renderer.draw_image("assets/healthbar.png", ai_name_rect.x + 10, ai_name_rect.y + ai_name_rect.height - 45, 5)

        renderer.draw_text_centered(f"{self.ai.hp}/{self.ai.max_hp}", ai_health_rect, start=48, alignment="left", color=(255, 255, 255))

        for btn in self.buttons:
            btn.draw(renderer)

    def move_click(self, btn: Button | MoveButton):
        if not isinstance(btn, MoveButton):
            return

        stateMachine = self.stateMachine

        from src.states.mainMenuState import MainMenuState
        if self.active_speler.speed > self.ai.speed:
            if self.active_speler.moves[btn.index][1] <= 0:
                info("Geen PP!")
                return

            self.active_speler.moves[btn.index][1] -= 1

            if isinstance(self.active_speler.moves[btn.index][0], Explosion):
                self.active_speler.hp = 0

            self.ai.hp -= btn.move.calculate_damage(self.active_speler, self.ai, True)
            if self.ai.hp <= 0:
                info("speler wint")
                self.ai.hp = 0
                stateMachine.start_transitie(MainMenuState(self.renderer, self.stateMachine), 2.5)
                return

            move = random.choice(self.ai.moves)
            dmg = move[0].calculate_damage(self.ai, self.active_speler, True)
            self.active_speler.hp -= dmg

            if self.active_speler.hp <= 0:
                self.active_speler.hp = 0
                warn("Speler is dood")
                stateMachine.start_transitie(MainMenuState(self.renderer, self.stateMachine), 2.5)
                return
        else:
            move = random.choice(self.ai.moves)
            dmg = move[0].calculate_damage(self.ai, self.active_speler, True)
            self.active_speler.hp -= dmg

            if self.active_speler.hp <= 0:
                self.active_speler.hp = 0
                warn("Speler is dood")
                stateMachine.start_transitie(MainMenuState(self.renderer, self.stateMachine), 2.5)
                return

            if self.active_speler.moves[btn.index][1] <= 0:
                info("Geen PP!")
                return

            self.active_speler.moves[btn.index][1] -= 1
            self.ai.hp -= btn.move.calculate_damage(self.active_speler, self.ai, True)
            if self.ai.hp <= 0:
                info("speler wint")
                self.ai.hp = 0
                stateMachine.start_transitie(MainMenuState(self.renderer, self.stateMachine), 2.5)
                return

    @staticmethod
    def random_battle(renderer: Renderer):
        mons = get_all()
        speler_team = random.sample(mons, 4)
        speler_team = [mon() for mon in speler_team]

        for mon in speler_team:
            mons.remove(type(mon))

        ai = random.choice(mons)()
        return FightState(speler_team, ai, renderer)
