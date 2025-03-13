from src.engine.state.state import State
from src.engine.ui.textButton import TextButton
from src.pokemons.pokemons.froggo import Froggo
from src.states.fightState import FightState
from src.states.reviewModeState import ReviewModeState


class MainMenuState(State):
    def __init__(self):
        super().__init__()

        from src.engine.globals import Globals
        txt = "Play"
        w = Globals.renderer.get_text_width(txt)
        startButton = TextButton(int(Globals.renderer.screen.get_width()/2-w/2), Globals.renderer.screen.get_height()-120, w+20, 60, "White", txt, text_color="Black")
        txt = "Review"
        w = Globals.renderer.get_text_width(txt)
        reviewButton = TextButton(10, Globals.renderer.screen.get_height()-70, w+20, 60, "White", txt, text_color="Black")

        startButton.set_on_click(lambda button : Globals.stateMachine.start_transitie(FightState(Froggo(0,0), Froggo(0,0)), 1.5))
        reviewButton.set_on_click(lambda button : Globals.stateMachine.start_transitie(ReviewModeState()))

        self.buttons.append(startButton)
        self.buttons.append(reviewButton)
        self.background_color = (0, 205, 205)

    def draw(self):
        from src.engine.globals import Globals
        Globals.renderer.draw_text_x_centered("Pokermon", 120, color="Black", size=96)