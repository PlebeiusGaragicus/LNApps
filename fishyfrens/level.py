import time
import logging
logger = logging.getLogger()

from gamelib.globals import *

from fishyfrens import config


MAX_LEVELS = 2
LEVEL_SCORE_PROGRESSION = [1, 99, 200]


class Level:
    def __init__(self, starting_level = 0):  # NOTE: level zero is the first level!
        self.current_level = starting_level
        self.level_start_time = time.time()

        self.life_suck_rate: int = None
        self.max_agents: int = None
        self.agent_spawn_interval: int = None # seconds

        self.show_vignette: bool = None
        self.hide_out_of_sight: bool = None
        self.top_color = None
        self.bottom_color = None
        self.depth_gradient = None

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
            config.PLAYFIELD_WIDTH = SCREEN_WIDTH
            config.PLAYFIELD_HEIGHT = SCREEN_HEIGHT

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

            config.PLAYFIELD_WIDTH = SCREEN_WIDTH // 2
            config.PLAYFIELD_HEIGHT = SCREEN_HEIGHT * 6

            self.max_agents = 900

            self.show_vignette = False
            self.hide_out_of_sight = True
            self.depth_gradient = True

        elif self.current_level == 2:
            gameplay_view.actor_group = pygame.sprite.Group() # KILL ALL AGENTS (wipe the board clean)

            config.PLAYFIELD_WIDTH = SCREEN_WIDTH * 4
            config.PLAYFIELD_HEIGHT = SCREEN_HEIGHT * 4

            self.max_agents = 1200

            self.show_vignette = True
            self.hide_out_of_sight = True
            self.depth_gradient = True
        else:
            raise NotImplementedError(f"Level {self.level} not implemented")


# LEVEL = Level()
