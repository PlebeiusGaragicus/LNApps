import time
import logging
logger = logging.getLogger()

from gamelib.globals import *

from fishyfrens import config

# from fishyfrens.view.camera import CAMERA
# from fishyfrens.globals import CAMERA

MAX_LEVELS = 1
LEVEL_SCORE_PROGRESSION = [5, 99, 200]

class Level:
    def __init__(self, starting_level = 0):  # NOTE: level zero is the first level!
        self.current_level = starting_level
        self.level_start_time = time.time()

        self.life_suck_rate: int = None
        self.max_agents: int = None
        self.agent_spawn_interval: int = None # seconds

        self.show_vignette: bool = None
        self.hide_out_of_sight: bool = None

        self.last_krill_spawn_time = None
        self.last_shark_spawn_time = None

        self.level_setup(self)


    def next_level(self, gameplay_view):
        self.current_level += 1
        logger.debug(f"level: {self.current_level}")

        if self.current_level > MAX_LEVELS:
            raise NotImplementedError("YOU WIN THE GAME!!!")
        else:
            self.level_setup(gameplay_view)



    def level_setup(self, gameplay_view):
        if self.current_level == 0:
            print("Setting playfield for level zero!")
            # global PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT
            config.PLAYFIELD_WIDTH = 500
            config.PLAYFIELD_HEIGHT = 500

            self.life_suck_rate = 1
            self.max_agents = 100
            self.hide_out_of_sight = False

            self.show_vignette = False

        elif self.current_level == 1:

            # TODO: add a marquee to the queue.  This way we can explain gameplay/level to player
            # TODO: trigger a "yay sound effect"
            gameplay_view.actor_group = pygame.sprite.Group() # KILL ALL AGENTS (wipe the board clean)

            # config.PLAYFIELD_WIDTH = 1440
            # config.PLAYFIELD_HEIGHT = 900
            config.PLAYFIELD_WIDTH = 500
            config.PLAYFIELD_HEIGHT = 2000

            self.agent_spawn_interval = 1 # seconds
            self.last_krill_spawn_time = time.time()
            self.last_fish_spawn_time = time.time()
            self.show_vignette = True
        else:
            raise NotImplementedError(f"Level {self.level} not implemented")


# LEVEL = Level()
