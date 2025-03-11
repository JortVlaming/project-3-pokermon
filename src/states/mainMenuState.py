from src.engine.state.state import State
from src.engine.ui.textButton import TextButton
from src.states.testState import TestState


class MainMenuState(State):
    def __init__(self):
        super().__init__()

        from src.engine.globals import Globals
        txt = "Play"
        w = Globals.renderer.get_text_width(txt)
        startButton = TextButton(int(Globals.renderer.screen.get_width()/2-w/2), Globals.renderer.screen.get_height()-120, 100, 60, "White", txt, text_color="Black")

        startButton.set_on_click(lambda button : Globals.stateMachine.start_transitie(TestState(), 1.5))

        self.buttons.append(startButton)