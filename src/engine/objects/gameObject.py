from pygame.sprite import Sprite

class GameObject(Sprite):
    def __init__(self, x:int, y:int):
        super().__init__()
        self.x = x
        self.y = y

    def update(self, *args, **kwargs):
        pass

    def draw(self, *args, **kwargs):
        pass