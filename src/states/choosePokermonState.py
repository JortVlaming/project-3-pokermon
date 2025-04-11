from src.engine.inputManager import InputManager
from src.engine.state.state import State
from src.engine.ui.button import Button
from src.engine.ui.textButton import TextButton
from src.pokemons.classes.pokermon import Pokermon
from src.pokemons.pokemons.all import get_all, get_random
from src.states.fightState import FightState


class PokermonButton(Button):
    def __init__(self, pokermon: Pokermon, x: int, y: int):
        super().__init__(x, y, pokermon.image.get_width(), pokermon.image.get_height())
        self.pokermon = pokermon
        self.x = x
        self.y = y
        self.selected = False

    def draw(self, renderer: "Renderer"):
        # Draw the Pokémon image
        renderer.draw_image(self.pokermon.image, self.pokermon.x, self.pokermon.y, 0.75)

        # Draw cost square with color change
        cost_square_color = (0, 255, 0) if self.selected else (255, 255, 255)  # Green if selected
        r = renderer.draw_rect(cost_square_color, self.pokermon.x + self.pokermon.image.get_width() - 100,
                               self.pokermon.y + self.pokermon.image.get_height() - 50, 50, 50)
        renderer.draw_text_centered(str(self.pokermon.cost), r, color=(0, 0, 0))


class StartButton(TextButton):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 250, 50, "White", "Start Battle", "Black")
        self.enabled = False

    def set_enabled(self, enabled: bool):
        self.enabled = enabled
        self.color = "White" if enabled else "Gray"

    def on_click(self, state_machine):
        if self.enabled and state_machine.selected_pokemons:
            state_machine.start_transitie(
                FightState(state_machine.selected_pokemons, get_random()(), state_machine.renderer))


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
        self.selected_pokemons = []
        self.max_pokemons = 4

        # Create Pokémon selection buttons
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

        # Add start button (TextButton)
        self.start_button = StartButton(325, 500)
        self.start_button.set_on_click(lambda btn : self.start_battle(self.stateMachine))
        self.buttons.append(self.start_button)

    def update(self, inputManager: InputManager, stateMachine):
        self.stateMachine = stateMachine

    def draw(self, renderer):
        self.renderer = renderer
        renderer.draw_text_x_centered("Current points: " + str(self.balance), 500)

        # Enable or disable the start button based on the selection of Pokémon
        self.start_button.set_enabled(len(self.selected_pokemons) > 0)

    def choose_pokermon(self, btn: Button | PokermonButton):
        if not isinstance(btn, PokermonButton):
            return

        # Toggle selection: If already selected, deselect and refund the points
        if btn.selected:
            self.selected_pokemons.remove(btn.pokermon)
            self.balance += btn.pokermon.cost
            btn.selected = False
        else:
            # Check if the player has enough points
            if self.balance >= btn.pokermon.cost and len(self.selected_pokemons) < self.max_pokemons:
                self.selected_pokemons.append(btn.pokermon)
                self.balance -= btn.pokermon.cost
                btn.selected = True

    def start_battle(self, state_machine):
        if len(self.selected_pokemons) > 0:
            state_machine.start_transitie(FightState(self.selected_pokemons, get_random()(), self.renderer))
