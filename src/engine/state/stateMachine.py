from src.engine.inputManager import InputManager
from src.engine.logger import info


class StateMachine:
    from src.engine.state.state import State
    huidige_staat: State | None = None
    transitie_staat: State | None = None
    transitie_tijd = 0.5  # Tijd van de transitie in seconden
    transitie_timer = 0
    transitie_opaciteit = 0  # 0 = volledig zichtbaar, 255 = volledig zwart
    transitie_snelheid = 255 / (transitie_tijd * 60)  # FPS-afhankelijke snelheid
    transitie = False
    transitie_stand = 0

    def __init__(self):
        pass

    def start_transitie(self, nieuwe_staat: State, tijd: float = 0.5):
        """Start een fade-out, wissel de staat, en start een fade-in."""
        self.transitie = True
        self.transitie_staat = nieuwe_staat
        if self.transitie_staat.background_color == "inherit":
            self.transitie_staat.background_color = self.huidige_staat.background_color
        self.transitie_tijd = tijd
        self.transitie_snelheid = 255 / (tijd * 60)  # Aangepaste snelheid
        self.transitie_opaciteit = 0
        self.huidige_staat.do_process_buttons = False
        info(f"Started transition from {type(self.huidige_staat).__name__} to {type(nieuwe_staat).__name__}")

    def update(self, inputManager: InputManager):
        if self.transitie:
            # Fade-out fase
            if self.transitie_opaciteit < 255 and self.huidige_staat is not None and self.transitie_stand == 0:
                self.transitie_opaciteit += self.transitie_snelheid
            # Wissel van staat als volledig zwart
            elif self.transitie_staat is not None and self.transitie_stand == 0:
                self.huidige_staat.do_process_buttons = True
                self.transitie_staat.do_process_buttons = False
                self.huidige_staat = self.transitie_staat
                self.transitie_staat = None
                self.transitie_opaciteit = 255  # Begin fade-in
                self.transitie_stand = 1
                self.huidige_staat.transition_cue()
            # Fade-in fase
            elif self.transitie_opaciteit > 0 and self.transitie_stand == 1:
                self.transitie_opaciteit -= self.transitie_snelheid
            else:
                self.transitie = False  # Transitie voltooid
                self.huidige_staat.do_process_buttons = True
                self.transitie_stand = 0
                info("Finished transition to " + type(self.huidige_staat).__name__)

        if self.huidige_staat is not None and not self.transitie:
            self.huidige_staat.update(inputManager, self)
            if self.huidige_staat.do_process_buttons:
                self.huidige_staat.process_buttons(inputManager)

    def draw(self, renderer):
        if self.huidige_staat is not None:
            self.huidige_staat.draw(renderer)
            for btn in self.huidige_staat.buttons:
                if btn.do_render:
                    btn.draw(renderer)

        if self.transitie_opaciteit > 0:
            # Teken een zwart vlak met de juiste transparantie
            import pygame
            scherm = pygame.display.get_surface()
            overlay = pygame.Surface(scherm.get_size(), pygame.SRCALPHA)
            if self.transitie_opaciteit > 255:
                self.transitie_opaciteit = 255
            overlay.fill((0, 0, 0, int(self.transitie_opaciteit)))
            scherm.blit(overlay, (0, 0))
