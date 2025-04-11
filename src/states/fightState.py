from typing import Tuple, List

import pygame

from src.engine.inputManager import InputManager
from src.engine.renderer import Renderer
from src.engine.state.state import State
from src.engine.state.stateMachine import StateMachine
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
        self.move = move
        self.index = index
        self.pp = pp
        self.max_pp = max_pp
        self.width = width
        self.height = height

    def draw(self, renderer: Renderer):
        r = renderer.draw_rect(
            (255, 255, 255) if self.move and self.pp > 0 else (100, 100, 100),
            self.x, self.y, self.width, self.height
        )
        if self.move:
            renderer.draw_text_centered(type(self.move).__name__, r, start=48, color=(0, 0, 0), y_offset=-20)
            renderer.draw_text_centered(f"{self.pp}/{self.max_pp} PP", r, start=24, color=(0, 0, 0), y_offset=20)
        else:
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
        r = renderer.draw_rect((75, 75, 75), self.x, self.y, self.width, self.height)
        if self.pokermon is None:
            renderer.draw_text_centered("-", r, color=(50, 50, 50))
        elif self.active:
            renderer.draw_text_centered("Active", r, y_offset=-20, color=(0, 0, 0), start=20)
            renderer.draw_text_centered(self.pokermon.name, r, y_offset=0, color=(0, 0, 0), start=16)
            renderer.draw_text_centered(f"{self.pokermon.hp}/{self.pokermon.max_hp}", r, y_offset=20, color=(0, 0, 0), start=16)
        else:
            color = (200, 200, 255) if self.pokermon.hp > 0 else (150, 150, 150)
            r = renderer.draw_rect(color, self.x, self.y, self.width, self.height)
            renderer.draw_text_centered(self.pokermon.name, r, y_offset=-20, color=(0, 0, 0), start=16)
            renderer.draw_text_centered(f"{self.pokermon.hp}/{self.pokermon.max_hp}", r, y_offset=20, color=(0, 0, 0), start=16)


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
        self.awaiting_continue = False
        self.log_text = ""
        self.log_display_index = 0
        self.typewriter_speed = 2  # characters per frame

        self.background_color = (200, 200, 200)

        self.active_speler.x = 150
        self.active_speler.y = renderer.screen.get_height() - self.active_speler.image.get_height() - 150

        self.ai.x = renderer.screen.get_width() - self.ai.image.get_width() - 100
        self.ai.y = 200 - self.ai.image.get_height()
        self.next_transition_state = None
        self.next_transition_speed = None

        self.auto_switch(initial=True)
        self.make_buttons()


    @property
    def active_speler(self) -> Pokermon:
        return self.speler_team[self.current_speler_index]

    def make_buttons(self):
        self.buttons = []
        menuButton = TextButton(750, self.renderer.screen.get_height() - 125, 100, 100, (255, 255, 255), "Switch", (0, 0, 0), 40)
        menuButton.set_on_click(lambda btn: self.toggle_switch_mode())
        self.buttons.append(menuButton)

        x = 250
        for i in range(4):
            if self.switching:
                mon = self.speler_team[i] if i < len(self.speler_team) else None
                is_active = (i == self.current_speler_index)
                btn = SwitchButton(x, self.renderer.screen.get_height() - 125, 100, 100, i, mon, is_active)
                if mon and mon.hp > 0 and not is_active:
                    btn.set_on_click(self.switch_click)
            else:
                move = self.active_speler.moves[i] if i < len(self.active_speler.moves) else None
                if move:
                    btn = MoveButton(x, self.renderer.screen.get_height() - 125, 100, 100, move[0], i, move[1], move[2])
                    btn.set_on_click(self.move_click)
                else:
                    btn = MoveButton(x, self.renderer.screen.get_height() - 125, 100, 100, None, i, 0, 0)
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
        self.set_log(f"{self.active_speler.name} is ready to fight!")

    def auto_switch(self, initial=False):
        for i, mon in enumerate(self.speler_team):
            if mon.hp > 0:
                self.current_speler_index = i
                self.active_speler.x = 150
                self.active_speler.y = self.renderer.screen.get_height() - self.active_speler.image.get_height() - 150
                self.make_buttons()
                if not initial:
                    self.set_log(f"{mon.name} steps in!")
                return True
        return False

    def set_log(self, text: str):
        self.log_text = text
        self.log_display_index = 0
        self.awaiting_continue = True

    def handle_combat(self, btn: MoveButton):
        log_lines = []

        if self.active_speler.speed >= self.ai.speed:
            if self.active_speler.moves[btn.index][1] <= 0:
                self.set_log("No PP left!")
                return

            self.active_speler.moves[btn.index][1] -= 1
            dmg = btn.move.calculate_damage(self.active_speler, self.ai, True)
            self.ai.hp -= dmg
            log_lines.append(f"{self.active_speler.name} used {type(btn.move).__name__}! It dealt {dmg} damage.")

            if isinstance(btn.move, Explosion):
                self.active_speler.hp = 0
                log_lines.append(f"{self.active_speler.name} fainted from explosion!")

            if self.ai.hp <= 0:
                self.ai.hp = 0
                log_lines.append("Enemy fainted! You win!")
                self.set_log("\n".join(log_lines))
                self.next_transition_state = self.random_battle_wt(self.renderer, self.speler_team)
                self.next_transition_speed = 1
                return

            move = random.choice(self.ai.moves)
            dmg = move[0].calculate_damage(self.ai, self.active_speler, True)
            self.active_speler.hp -= dmg
            log_lines.append(f"{self.ai.name} used {type(move[0]).__name__}! It dealt {dmg} damage.")
        else:
            move = random.choice(self.ai.moves)
            dmg = move[0].calculate_damage(self.ai, self.active_speler, True)
            self.active_speler.hp -= dmg
            log_lines.append(f"{self.ai.name} used {type(move[0]).__name__}! It dealt {dmg} damage.")

            if self.active_speler.hp <= 0:
                self.active_speler.hp = 0
                log_lines.append(f"{self.active_speler.name} fainted!")
                if self.auto_switch():
                    self.set_log("\n".join(log_lines))
                    return
                else:
                    log_lines.append("No Pokémon left! You lost.")
                    self.set_log("\n".join(log_lines))
                    self.next_transition_state = self.random_battle_wt(self.renderer, self.speler_team)
                    self.next_transition_speed = 1
                    return

            if self.active_speler.moves[btn.index][1] <= 0:
                self.set_log("No PP left!")
                return

            self.active_speler.moves[btn.index][1] -= 1
            dmg = btn.move.calculate_damage(self.active_speler, self.ai, True)
            self.ai.hp -= dmg
            log_lines.append(f"{self.active_speler.name} used {type(btn.move).__name__}! It dealt {dmg} damage.")

        if self.active_speler.hp <= 0:
            self.active_speler.hp = 0
            log_lines.append(f"{self.active_speler.name} fainted!")
            if not self.auto_switch():
                log_lines.append("No Pokémon left! You lost.")
                self.set_log("\n".join(log_lines))
                self.next_transition_state = self.random_battle_wt(self.renderer, self.speler_team)
                self.next_transition_speed = 1
                return

        if self.ai.hp <= 0:
            self.ai.hp = 0
            log_lines.append("Enemy fainted! You win!")
            self.set_log("\n".join(log_lines))
            self.next_transition_state = self.random_battle_wt(self.renderer, self.speler_team)
            self.next_transition_speed = 1
            return

        self.set_log("\n".join(log_lines))

    def move_click(self, btn: Button | MoveButton):
        if not isinstance(btn, MoveButton) or self.awaiting_continue:
            return
        self.handle_combat(btn)

    def update(self, inputManager: "InputManager", stateMachine: "StateMachine"):
        self.stateMachine = stateMachine
        if self.awaiting_continue:
            if inputManager.is_key_down(pygame.K_SPACE):
                if self.log_display_index < len(self.log_text):
                    self.log_display_index = len(self.log_text)
                    return
                self.awaiting_continue = False
                self.log_text = ""
                self.make_buttons()
                if self.next_transition_state:
                    stateMachine.start_transitie(self.next_transition_state, self.next_transition_speed or 1)

    def draw(self, renderer):
        self.renderer = renderer

        # Player HP box
        name_rect = renderer.draw_rect((10, 10, 10, 0), 20, renderer.screen.get_height() - 130, 155, 30)
        hp_rect = renderer.draw_rect((10, 10, 10, 0), 20, renderer.screen.get_height() - 47, 155, 30)

        renderer.draw_image_centered("assets/grass.png")
        self.active_speler.draw(renderer)
        self.ai.draw(renderer)

        renderer.draw_text_centered(self.active_speler.name, name_rect, alignment="left")
        length, color = get_health_bar(self.active_speler.hp, self.active_speler.max_hp, 155)
        renderer.draw_rect(color, 15, renderer.screen.get_height() - 75, length, 20)
        renderer.draw_image("assets/healthbar.png", 15, renderer.screen.get_height() - 80, 5)
        renderer.draw_text_centered(f"{self.active_speler.hp}/{self.active_speler.max_hp}", hp_rect, alignment="left", size=32)

        # AI HP box
        ai_health_rect = renderer.draw_rect((0, 0, 0, 0), self.ai.x - 255 + 150, 105, 80, 30)
        ai_name_rect = renderer.draw_rect((0, 0, 150), self.ai.x - 275, 50, 255, 100, 10)

        renderer.draw_text_centered(self.ai.name, ai_name_rect, start=48, y_offset=-15, alignment="left", x_offset=10)
        ai_length, ai_color = get_health_bar(self.ai.hp, self.ai.max_hp, 155)
        renderer.draw_rect(ai_color, ai_name_rect.x + 10, ai_name_rect.y + ai_name_rect.height - 40, ai_length, 20)
        renderer.draw_image("assets/healthbar.png", ai_name_rect.x + 10, ai_name_rect.y + ai_name_rect.height - 45, 5)
        renderer.draw_text_centered(f"{self.ai.hp}/{self.ai.max_hp}", ai_health_rect, start=48, alignment="left", color=(255, 255, 255))

        for btn in self.buttons:
            btn.draw(renderer)

        # Combat log with typewriter effect
        if self.log_text:
            self.ready_for_transition = False
            box = renderer.draw_rect((25, 25, 25), 50, 50, renderer.screen.get_width() - 100, 100)
            if self.log_display_index < len(self.log_text):
                self.log_display_index += self.typewriter_speed
            shown_text = self.log_text[:int(self.log_display_index)]
            renderer.draw_text(shown_text, 60, 60, size=24, color=(255, 255, 255), centered=False)

    @staticmethod
    def random_battle(renderer: Renderer):
        mons = get_all()
        speler_team = random.sample(mons, 4)
        speler_team = [mon() for mon in speler_team]
        for mon in speler_team:
            mons.remove(type(mon))
        ai = random.choice(mons)()
        return FightState(speler_team, ai, renderer)

    @staticmethod
    def random_battle_wt(renderer: Renderer, speler_team: List[Pokermon]):
        mons = get_all()
        for mon in speler_team:
            if type(mon) in mons:
                mons.remove(type(mon))
        ai = random.choice(mons)()
        return FightState(speler_team, ai, renderer)