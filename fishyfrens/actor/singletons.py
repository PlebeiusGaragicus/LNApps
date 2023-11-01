# from fishyfrens.actor.player import Player
# from fishyfrens.level import LevelVariables, Storyline


_p = None

def create_player(name):
    global _p
    if _p is not None:
        raise Exception("Player instance already exists")

    from fishyfrens.actor.player import Player
    _p = Player(name)
    return _p

def player():
    # global _p # not needed as we are only accessing, not modifying it
    if _p is None:
        raise Exception("Player has not been created yet")
    return _p





_l = None

# def create_levels(storyline: Storyline, starting_level: int = 0):
def create_levels(gameplay_view, storyline, starting_level: int = 0):
    """ creates the level singleton to your specifications
    """
    global _l
    if _l is not None:
        raise Exception("Player instance already exists")
    from fishyfrens.level import LevelVariables, Storyline
    _l = LevelVariables(gameplay_view=gameplay_view, storyline=storyline, starting_level=starting_level)
    return _l

def level():
    """ returns the level singleton - use this for all access
    """
    # global _l # not needed as we are only accessing, not modifying it
    if _l is None:
        raise Exception("Player has not been created yet")
    return _l
