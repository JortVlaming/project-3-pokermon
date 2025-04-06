from src.engine.blackjack import BlackjackState
from src.engine.inputManager import InputManager
from src.engine.logger import warn
from src.engine.renderer import Renderer
from src.engine.slots import SlotsState
from src.engine.state.state import State
from src.engine.ui.textButton import TextButton
from src.states.choosePokermonState import ChoosePokermonState
from src.states.fightState import FightState


class ChooseState(State):
    def __init__(self):
        """
        Constructor meant for the main menu and static methods to use
        """
        super().__init__()

        self.points = 5
        self.background_color = "gray"

        from src.main import SCREEN_WIDTH, SCREEN_HEIGHT

        fight_button_width, fight_button_height = 200, 320
        fight_button = TextButton(
            SCREEN_WIDTH/2-fight_button_width/2,
            SCREEN_HEIGHT/2-fight_button_height/2,
            fight_button_width,
            fight_button_height,
            "White",
            "Choose Pokermon",
            "black",
            text_size=32
        )

        fight_button.set_on_click(lambda btn : self.switch_state(ChoosePokermonState(self.points), 1))
        #fight_button.set_on_click(lambda btn : self.switch_state(FightState.random_battle(self.renderer), 1))

        slots_button_width, slots_button_height = 200, 320
        slots_button = TextButton(
            SCREEN_WIDTH / 2 - slots_button_width / 2 + slots_button_width * 1.33,
            SCREEN_HEIGHT / 2 - slots_button_height / 2,
            slots_button_width,
            slots_button_height,
            "White",
            "Slots",
            "black"
        )

        slots_button.set_on_click(lambda btn: self.start_slots())

        blackjack_button_width, blackjack_button_height = 200, 320
        blackjack_button = TextButton(
            SCREEN_WIDTH / 2 - blackjack_button_width / 2 - blackjack_button_width * 1.33,
            SCREEN_HEIGHT / 2 - blackjack_button_height / 2,
            blackjack_button_width,
            blackjack_button_height,
            "white",
            "Blackjack",
            "black",
            text_size=60
        )

        blackjack_button.set_on_click(lambda btn: self.switch_state(BlackjackState(self.points), 1))

        s = "Reset run"
        self.reset_button = TextButton(
            SCREEN_WIDTH / 2 - 110,
            SCREEN_HEIGHT - 75,
            220,
            70,
            "Red",
            s,
            text_color="White"
        )

        self.reset_button.set_on_click(lambda btn : self.reset_run())

        self.buttons = [fight_button, slots_button, blackjack_button]
        self.stateMachine = None
        self.renderer = None

    def switch_state(self, state: State, time: int | float):
        if self.stateMachine is None:
            warn("[ChooseState] No state machine defined to switch with!")
            return
        if self.renderer is None:
            warn("[ChooseState] No renderer defined to switch with!")
            return
        self.stateMachine.start_transitie(state, time)

    def start_slots(self):
        s = SlotsState()
        s.balance = self.points
        self.switch_state(s, 1)

    def reset_run(self):
        self.switch_state(ChooseState(), 1)

    @staticmethod
    def from_slots(balance: int) -> 'ChooseState':
        s = ChooseState()
        s.points = balance
        return s

    @staticmethod
    def from_blackjack(balance: int) -> 'ChooseState':
        s = ChooseState()
        s.points = balance
        return s

    def update(self, input_manager:InputManager, state_machine):
        self.stateMachine = state_machine

    def draw(self, renderer: Renderer):
        self.renderer = renderer

        if self.points > 0:
            if len(self.buttons) == 4:
                self.buttons.pop()
                self.buttons[0].do_clicks = True
                self.buttons[1].do_clicks = True
                self.buttons[2].do_clicks = True
            renderer.draw_text_x_centered(f"Current points: {self.points}", renderer.screen.get_height()-50, size=48)
        else:
            if len(self.buttons) < 4:
                self.buttons.append(self.reset_button)
                self.buttons[0].do_clicks = False
                self.buttons[1].do_clicks = False
                self.buttons[2].do_clicks = False

            renderer.draw_text_x_centered("You do not have any points to play with!", renderer.screen.get_height()-100, size=48)