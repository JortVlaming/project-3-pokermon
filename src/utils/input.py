from src.engine.logger import warn


def int_input(*args) -> int:
    r = " ".join(args)

    res: str|int|None = None

    while res is None:
        res = input(r)

        if not res:
            warn("Please input a value")

        if not res.isnumeric():
            warn("That is not a number!")
            res = None
        else:
            res = int(res)

    return res