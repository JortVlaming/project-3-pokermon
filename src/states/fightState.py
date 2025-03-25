import random
from typing import Tuple

import pygame

from src.engine.logger import info, warn
from src.engine.renderer import Renderer
from src.engine.state.state import State
from src.engine.ui.button import Button
from src.pokemons.attacks.explosion import Explosion
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

class MoveButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, move: Attack, index:int):
        super().__init__(x, y, width, height)

        self.width = width
        self.height = height
        self.move = move
        self.index = index

    def draw(self, renderer: Renderer):
        pass

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

        self.buttons = []
        self.background_color = (200, 200, 200)

        self.staat = 0
        self.speler_aanval: Attack|None = None
        self.ai_aanval: Attack|None = None

        self.buttons_made = False

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
                stateMachine.start_transitie(FightState(self.speler, self.ai), 1.5)
                warn("Gevecht reset triggered")

    def draw(self, renderer):
        self.renderer = renderer

        self.speler.draw(renderer)
        self.ai.draw(renderer)

        # speler stuff
        mon_name_rect = renderer.draw_rect((10,10,10,0),20, renderer.screen.get_height()-130, 31*5, 30)
        mon_health_rect = renderer.draw_rect((10,10,10,0),20, renderer.screen.get_height()-47, 31*5, 30)

        renderer.draw_rect((150, 150, 150), 0, renderer.screen.get_height()-150, renderer.screen.get_width(), 150, 0)


        renderer.draw_text_centered(self.speler.name, mon_name_rect, alignment="left")

        length, color = get_health_bar(self.speler.hp, self.speler.max_hp, 31*5)

        renderer.draw_rect(color, 15, renderer.screen.get_height()-75, length, 20)
        renderer.draw_image("assets/healthbar.png", 15, renderer.screen.get_height()-80, 5)

        renderer.draw_text_centered(f"{self.speler.hp}/{self.speler.max_hp}", mon_health_rect, alignment="left", size=32)

        # ai stuff
        r2 = renderer.draw_rect((0,0,0,0), self.ai.x-255+150, 50+100-45, 80, 30)
        r = renderer.draw_rect((150, 150, 150), self.ai.x-275, 50, 255, 100, 10)

        renderer.draw_text_centered(self.ai.name, r, start=48, y_offset=-15, alignment="left", x_offset=10)

        ai_length, ai_color = get_health_bar(self.ai.hp, self.ai.max_hp, 31 * 5)

        renderer.draw_rect(ai_color, r.x+10, r.y+r.height-40, ai_length, 20)
        renderer.draw_image("assets/healthbar.png", r.x+10, r.y+r.height-45, 5)


        renderer.draw_text_centered(f"{self.ai.hp}/{self.ai.max_hp}", r2, start=48, alignment="left", color=(255, 255, 255))

        x = 250

        for i in range(0, 4):
            move = self.speler.moves[i] if i < len(self.speler.moves) else None

            if move:
                r = renderer.draw_rect((255, 255, 255) if move[1] > 0 else (125, 125, 125), x, renderer.screen.get_height()-125, 100, 100)
                renderer.draw_text_centered(type(move[0]).__name__, r, start=48, color=(0,0,0), y_offset=-20)
                renderer.draw_text_centered(f"{move[1]}/{move[2]} PP", r, start=24, color=(0,0,0), y_offset=20)
            else:
                r = renderer.draw_rect((100, 100, 100), x, renderer.screen.get_height()-125, 100, 100)
                renderer.draw_text_centered("-", r, color=(75, 75, 75))

            if not self.buttons_made and move:
                b = MoveButton(x, renderer.screen.get_height() - 125, 100, 100, move[0], i)
                b.set_on_click(self.move_click)
                self.buttons.append(b)

            x += 125

        self.buttons_made = True

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
