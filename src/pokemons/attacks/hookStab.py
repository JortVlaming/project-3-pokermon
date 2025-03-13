from src.pokemons.classes.attack import Attack


class HookStab(Attack):
    def __init__(self):
        super().__init__("Hook Stab", 100)