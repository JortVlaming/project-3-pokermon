import pygame

from src.engine.inputManager import InputManager
from src.engine.renderer import Renderer
from src.engine.state.stateMachine import StateMachine


class Globals:
    window:pygame.Surface = None
    renderer:Renderer = None
    inputManager:InputManager = None
    stateMachine:StateMachine = None

    @classmethod
    def set_window(cls, window: pygame.Surface):
        cls.window = window

    @classmethod
    def get_window(cls) -> pygame.Surface:
        return cls.window

    @classmethod
    def set_renderer(cls, renderer: Renderer):
        cls.renderer = renderer

    @classmethod
    def get_renderer(cls) -> Renderer:
        return cls.renderer