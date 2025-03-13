from src.engine.globals import Globals
from src.engine.state.state import State
from src.pokemons.classes.attack import Attack
from src.pokemons.classes.pokermon import Pokermon

class FightState(State):
    def __init__(self, speler_mon:Pokermon, ai_mon: Pokermon):
        super().__init__()

        self.speler = speler_mon
        self.speler.x = 150
        self.speler.y = Globals.renderer.screen.get_height() - self.speler.image.get_height() - 150

        self.ai = ai_mon
        self.ai.x = Globals.renderer.screen.get_width() - self.ai.image.get_width() - 100
        self.ai.y = 200 - self.ai.image.get_height()

        self.staat = 0

        self.buttons = []
        self.background_color = (200, 200, 200)

        self.staat = 0
        self.speler_aanval: Attack|None = None
        self.ai_aanval: Attack|None = None


    def update(self):
        if self.staat == 0:
            pass

    def draw(self):
        self.speler.draw()
        self.ai.draw()

        renderer = Globals.renderer

        renderer.draw_rect((150, 150, 150), 0, renderer.screen.get_height()-150, renderer.screen.get_width(), 150, 0)

        renderer.draw_text(self.speler.name, 20, renderer.screen.get_height()-130)