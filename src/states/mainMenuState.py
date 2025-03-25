import random

from src.engine.renderer import Renderer
from src.engine.slots import SlotsState
from src.engine.state.state import State
from src.engine.state.stateMachine import StateMachine
from src.engine.ui.textButton import TextButton
from src.pokemons.pokemons.eagle import Eagle
from src.pokemons.pokemons.froggo import Froggo
from src.pokemons.pokemons.racoon import Racoon
from src.pokemons.pokemons.spider import Spider
from src.pokemons.pokemons.turtles import Turtles
from src.states.fightState import FightState
from src.states.reviewModeState import ReviewModeState


class MainMenuState(State):
    def __init__(self, renderer: Renderer, stateMachine: StateMachine):
        super().__init__()

        txt = "Play"
        w = renderer.get_text_width(txt)
        startButton = TextButton(int(renderer.screen.get_width()/2-w/2), renderer.screen.get_height()-120, w+20, 60, "White", txt, text_color="Black")
        txt = "Review"
        w = renderer.get_text_width(txt)
        reviewButton = TextButton(10, renderer.screen.get_height()-70, w+20, 60, "White", txt, text_color="Black")

        mons = [Eagle(), Froggo(), Racoon(), Spider(), Turtles()]
        speler = random.choice(mons)
        mons.remove(speler)
        ai = random.choice(mons)
        startButton.set_on_click(lambda button : stateMachine.start_transitie(FightState(speler, ai, renderer), 1.5))
#        startButton.set_on_click(lambda button : stateMachine.start_transitie(SlotsState()))
        reviewButton.set_on_click(lambda button : stateMachine.start_transitie(ReviewModeState(renderer, stateMachine)))

        self.buttons.append(startButton)
        self.buttons.append(reviewButton)
        self.background_color = (0, 205, 205)

    def draw(self, renderer):
        renderer.draw_text_x_centered("Pokermon", 120, color="Black", size=96)