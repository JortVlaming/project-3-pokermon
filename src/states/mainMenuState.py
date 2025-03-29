from src.engine.renderer import Renderer
from src.engine.state.state import State
from src.engine.state.stateMachine import StateMachine
from src.engine.ui.textButton import TextButton
from src.states.chooseState import ChooseState


class MainMenuState(State):
    def __init__(self, renderer: Renderer, stateMachine: StateMachine):
        super().__init__()

        txt = "Play"
        w = renderer.get_text_width(txt)
        startButton = TextButton(int(renderer.screen.get_width()/2-w/2), renderer.screen.get_height()-120, w+20, 60, "White", txt, text_color="Black")

        startButton.set_on_click(lambda button : stateMachine.start_transitie(ChooseState(), 1.5))
#        startButton.set_on_click(lambda button : stateMachine.start_transitie(SlotsState()))

        self.buttons.append(startButton)
        self.background_color = (0, 205, 205)

    def draw(self, renderer):
        renderer.draw_text_x_centered("Pokermon", 120, color="Black", size=96)