from src.engine.state.state import State


class StateMachine:
    huidige_staat: State|None = None

    def __init__(self):
        pass

    def update(self):
        if self.huidige_staat is not None:
            self.huidige_staat.update()
            if self.huidige_staat.do_process_buttons:
                self.huidige_staat.process_buttons()

    def draw(self):
        if self.huidige_staat is not None:
            self.huidige_staat.draw()