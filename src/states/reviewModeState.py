import random

from src.engine.globals import Globals
from src.engine.renderer import Renderer
from src.engine.state.state import State
from src.engine.ui.textButton import TextButton
from src.pokemons.pokemons.eagle import Eagle
from src.pokemons.pokemons.froggo import Froggo
from src.pokemons.pokemons.racoon import Racoon
from src.pokemons.pokemons.spider import Spider
from src.pokemons.pokemons.turtles import Turtles
from src.states.fightState import FightState


class ReviewModeState(State):
    def __init__(self):
        super().__init__()

        txt = "Next"
        w = Globals.renderer.get_text_width(txt)
        self.nextButton = TextButton(int(Globals.renderer.screen.get_width()/2-w/2), Globals.renderer.screen.get_height()-50, w, 45, (150, 150, 150), txt)
        self.nextButton.set_on_click(self.next)

        self.buttons = [self.nextButton]
        self.background_color = (200, 200, 200)
        self.review_deel = 1

    def next(self, _):
        self.review_deel+=1
        if self.review_deel == 6:
            txt = "Show fight"
            w = Globals.renderer.get_text_width(txt)
            self.nextButton = TextButton(int(Globals.renderer.screen.get_width() / 2 - w / 2),
                                         Globals.renderer.screen.get_height() - 50, w, 45, (150, 150, 150), txt)
            mons = [Eagle(0,0), Froggo(0,0), Racoon(0,0), Spider(0,0), Turtles(0,0)]
            speler = random.choice(mons)
            mons.remove(speler)
            ai = random.choice(mons)
            self.nextButton.set_on_click(lambda button : Globals.stateMachine.start_transitie(FightState(speler, ai)))
            self.buttons = [self.nextButton]

    def draw(self):
        renderer = Globals.renderer
        renderer.draw_text_x_centered("Review mode activated", 40, color="Black")
        if self.review_deel == 1:
            self.draw_cards(renderer, "harten", "hart")
        elif self.review_deel == 2:
            self.draw_cards(renderer, "klaver", "klaver")
        elif self.review_deel == 3:
            self.draw_cards(renderer, "ruit", "ruit")
        elif self.review_deel == 4:
            self.draw_cards(renderer, "schoppen", "schop")
        elif self.review_deel == 5:
            self.draw_mons(renderer)
        elif self.review_deel == 6:
            self.draw_turtles(renderer)

    def draw_cards(self, renderer, dir:str, type: str):
        _x = 45
        x = _x
        y = 90
        gap = 140
        scale = 4
        i = 1
        renderer.draw_image(f"assets/cards/{dir}/{type}{i}.png", x, y, scale)
        x += gap
        i += 1
        renderer.draw_image(f"assets/cards/{dir}/{type}{i}.png", x, y, scale)
        x += gap
        i += 1
        renderer.draw_image(f"assets/cards/{dir}/{type}{i}.png", x, y, scale)
        x += gap
        i += 1
        renderer.draw_image(f"assets/cards/{dir}/{type}{i}.png", x, y, scale)
        x += gap
        i += 1
        renderer.draw_image(f"assets/cards/{dir}/{type}{i}.png", x, y, scale)
        x += gap
        i += 1
        y += 140
        x = _x
        renderer.draw_image(f"assets/cards/{dir}/{type}{i}.png", x, y, scale)
        x += gap
        i += 1
        renderer.draw_image(f"assets/cards/{dir}/{type}{i}.png", x, y, scale)
        x += gap
        i += 1
        renderer.draw_image(f"assets/cards/{dir}/{type}{i}.png", x, y, scale)
        x += gap
        i += 1
        renderer.draw_image(f"assets/cards/{dir}/{type}{i}.png", x, y, scale)
        x += gap
        i += 1
        renderer.draw_image(f"assets/cards/{dir}/{type}{i}.png", x, y, scale)
        x += gap
        i += 1
        y += 140
        x = _x + gap / 2
        renderer.draw_image(f"assets/cards/{dir}/{type}A.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/cards/{dir}/{type}J.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/cards/{dir}/{type}K.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/cards/{dir}/{type}Q.png", x, y, scale)
        x += gap

    def draw_mons(self, renderer):
        _x = 45
        x = _x
        y = 60
        gap = 270
        scale = 2.5
        renderer.draw_image(f"assets/AREND.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/Evil_frog.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/Foxie.png", x, y, scale)
        x += gap

        y += gap/4*3
        x = _x

        renderer.draw_image(f"assets/Racoon.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/snek.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/spoeder.png", x, y, scale)

    def draw_turtles(self, renderer):
        _x = 45
        x = _x
        y = 60
        gap = 270
        scale = 2.5
        renderer.draw_image(f"assets/Donnatello.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/Leonardo.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/lama.png", x, y, scale)

        y += gap / 4 * 3
        x = _x

        renderer.draw_image(f"assets/Michelangelo.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/Raphael.png", x, y, scale)
        x += gap
        renderer.draw_image(f"assets/Energyzwordedwopper.png", x, y, scale)