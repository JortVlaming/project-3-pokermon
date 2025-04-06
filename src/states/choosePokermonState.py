from src.engine.inputManager import InputManager
from src.engine.logger import info
from src.engine.state.state import State
from src.engine.ui.button import Button
from src.pokemons.classes.pokermon import Pokermon
from src.pokemons.pokemons.all import get_all, get_random
from src.states.fightState import FightState


class PokermonButton(Button):
    def __init__(self, pokermon: Pokermon, x: int, y: int):
        super().__init__(x, y, pokermon.image.get_width(), pokermon.image.get_height())
        self.pokermon = pokermon
        self.x = x
        self.y = y

    def draw(self, renderer: "Renderer"):
        renderer.draw_image(self.pokermon.image, self.pokermon.x, self.pokermon.y, 0.75)
        r = renderer.draw_rect((255, 255, 255), self.pokermon.x + self.pokermon.image.get_width() - 100, self.pokermon.y + self.pokermon.image.get_height() - 50, 50, 50)
        renderer.draw_text_centered(str(self.pokermon.cost), r, color=(0,0,0))

class ChoosePokermonState(State):
    def __init__(self, balance: int):
        super().__init__()
        self.balance = balance
        self.max_balance = balance

        self.background_color = "inherit"

        pokermonsClasses = get_all()

        pokermons = []

        for pokermonClass in pokermonsClasses:
            pokermons.append(pokermonClass())

        del pokermonsClasses

        start_x, start_y = 100, 100
        x, y = start_x, start_y
        space_X = 140
        space_y = 180

        self.buttons = []

        for i, pokermon in enumerate(pokermons):
            pokermon.x = x
            pokermon.y = y
            btn = PokermonButton(pokermon, x, y)
            btn.set_on_click(self.choose_pokermon)
            self.buttons.append(btn)
            x += space_X

            if i == 4:
                x = start_x
                y += space_y

    def update(self, inputManager:InputManager, stateMachine):
        self.stateMachine = stateMachine

    def draw(self, renderer):
        self.renderer = renderer
        renderer.draw_text_x_centered("Current points: " + str(self.balance), 500)

    def choose_pokermon(self, btn: Button|PokermonButton):
        if not isinstance(btn, PokermonButton):
            return

        if self.balance < btn.pokermon.cost:
            return

        self.stateMachine.start_transitie(FightState([type(btn.pokermon)()], get_random()(), self.renderer))
