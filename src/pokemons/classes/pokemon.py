from src.engine.objects.Sprite import Sprite


class Pokemon(Sprite):
    name:str = ""
    hp:int = 0
    max_hp:int = 0
    speed:int = 0
    attack:int = 0
    defense:int = 0
    #       [(class, pp, max)]
    moves = []

    def __init__(self, x:int, y:int, image:str):
        super().__init__(x, y, image)
