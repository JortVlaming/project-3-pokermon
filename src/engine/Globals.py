import pygame


class Globals:
    window:pygame.Surface = None

    @classmethod
    def set_window(cls, window):
        cls.window = window

    @classmethod
    def get_window(cls):
        return cls.window