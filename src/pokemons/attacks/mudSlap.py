from src.pokemons.classes.attack import Attack


class MudSlap(Attack):
    def __init__(self):
        super().__init__("Mud Slap", 20)