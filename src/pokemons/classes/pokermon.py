from src.engine.objects.sprite import Sprite


class Pokermon(Sprite):
    name:str = ""
    hp:int = 0
    max_hp:int = 0
    speed:int = 0
    attack:int = 0
    defense:int = 0
    #       [(class, pp, max)]
    moves = []

    def __init__(self, image: str):
        super().__init__(0, 0, image)
