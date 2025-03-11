from src.engine.state.state import State


class StateMachine:
    huidige_staat: State|None = None

    def __init__(self):
        pass

    def update(self):
        if self.huidige_staat is not None:
            self.huidige_staat.update()
    def draw(self):
        if self.huidige_staat is not None:
            self.huidige_staat.draw()