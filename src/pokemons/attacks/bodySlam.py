from src.pokemons.classes.attack import Attack


class BodySlam(Attack):
    def __init__(self):
        super().__init__("Body Slam", 80)