import time
import enum
import logging
logger = logging.getLogger()

from gamelib.globals import *
# from fishyfrens import config

from fishyfrens.view.camera import camera

class Storyline(enum.Enum):
    OCEAN_FREETIME = enum.auto()
    THE_BIG_FISH = enum.auto()
    FREN_RESCUE = enum.auto()
    DEEP_OCEAN = enum.auto()


class LevelVariables:

    MAX_LEVELS = 2
    LEVEL_SCORE_PROGRESSION = [1, 99, 200]

    def __init__(self, storyline: Storyline, starting_level):  # NOTE: level zero is the first level!
        self.storyline = storyline
        self.current_level = starting_level
        self.level_start_time = time.time()

        self.life_suck_rate = 1
        # self.life_suck_rate: int = None
        self.max_agents: int = None
        # self.agent_spawn_interval: int = None # seconds
        self.agent_spawn_interval = 0.1 # seconds
        self.last_krill_spawn_time = time.time()
        self.last_fish_spawn_time = time.time()

        # self.show_vignette: bool = None
        self.show_vignette = False
        # self.hide_out_of_sight: bool = None
        self.hide_out_of_sight = False
        self.top_color = None
        self.bottom_color = None
        # self.depth_gradient = None
        self.depth_gradient = False

        # self.level_setup(self)


    def set_level(self, gameplay_view, next_level=False, set_level=None):
        if set_level is not None:
            self.current_level = set_level
        elif next_level:
            self.current_level += 1
        else:
            self.current_level = 0

        logger.debug(f"level: {self.current_level}")

        if self.current_level > LevelVariables.MAX_LEVELS:
            raise NotImplementedError("YOU WIN THE GAME!!!")
        else:
            self.level_setup(gameplay_view)



    def level_setup(self, gameplay_view):
        if self.current_level == 0:
            print("Setting playfield for level zero!")

            camera().resize(SCREEN_WIDTH, SCREEN_HEIGHT)

            # self.max_agents = 100
            self.agent_spawn_interval = 0.1 # seconds
            self.last_krill_spawn_time = time.time()
            self.last_fish_spawn_time = time.time()

            self.life_suck_rate = 1

            self.show_vignette = False
            self.hide_out_of_sight = False
            self.depth_gradient = False

        elif self.current_level == 1:

            # TODO: add a marquee to the queue.  This way we can explain gameplay/level to player
            # TODO: trigger a "yay sound effect"
            gameplay_view.actor_group = pygame.sprite.Group() # KILL ALL AGENTS (wipe the board clean)

            camera().resize(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 6)

            self.max_agents = 900

            self.show_vignette = False
            self.hide_out_of_sight = True
            self.depth_gradient = True

        elif self.current_level == 2:
            gameplay_view.actor_group = pygame.sprite.Group() # KILL ALL AGENTS (wipe the board clean)

            camera().resize(SCREEN_WIDTH * 4, SCREEN_HEIGHT * 4)

            self.max_agents = 1200

            self.show_vignette = True
            self.hide_out_of_sight = True
            self.depth_gradient = True
        else:
            raise NotImplementedError(f"Level {self.level} not implemented")



# _l = None

# def level() -> LevelVariables:
#     global _l
#     if _l is None:
#         _l = LevelVariables()
#     return _l



_l = None

def create_levels(storyline: Storyline, starting_level: int = 0):
    global _l
    if _l is not None:
        raise Exception("Player instance already exists")
    _l = LevelVariables(storyline=storyline, starting_level=starting_level)
    return _l

def level():
    # global _l # not needed as we are only accessing, not modifying it
    if _l is None:
        raise Exception("Player has not been created yet")
    return _l
