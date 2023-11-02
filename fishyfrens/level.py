import time
import enum
import random
import logging
logger = logging.getLogger()

from gamelib.globals import *

from fishyfrens.view.camera import camera
# from fishyfrens.actor.player import player
from fishyfrens.actor.agent import Agent, AgentType, BehaviorType
from fishyfrens.actor.singletons import player, level




def safeXY():
    # how far away from the edge of the playfield should agents be spawned
    SAFE_BUFFER = 100

    # return a random x,y coordinate that is not within the player's view
    while True: # TODO: this is a bad way to do this... but it works for now
        # TODO: use min and max instead
        x = random.randint(SAFE_BUFFER, camera().playfield_width - SAFE_BUFFER)
        y = random.randint(SAFE_BUFFER, camera().playfield_height - SAFE_BUFFER)
        if player().position.distance_to(pygame.Vector2(x, y)) > 200:
            return x, y



class Storyline(enum.Enum):
    OCEAN_FREETIME = enum.auto()
    THE_BIG_FISH = enum.auto()
    FREN_RESCUE = enum.auto()
    DEEP_OCEAN = enum.auto()


# ###################################
# # THE MIGHTY SINGLETON!
# ###################################
# _l = None

# def create_levels(storyline: Storyline, starting_level: int = 0):
#     """ creates the level singleton to your specifications
#     """
#     global _l
#     if _l is not None:
#         raise Exception("Player instance already exists")
#     _l = LevelVariables(storyline=storyline, starting_level=starting_level)
#     return _l

# def level():
#     """ returns the level singleton - use this for all access
#     """
#     # global _l # not needed as we are only accessing, not modifying it
#     if _l is None:
#         raise Exception("Player has not been created yet")
#     return _l
# ###################################




class LevelVariables:

    MAX_LEVELS = 2
    LEVEL_SCORE_PROGRESSION = [0, 100, 150] # level zero is unpasssable

    def __init__(self, gameplay_view, storyline: Storyline, starting_level):  # NOTE: level zero is the first level!
        self.gameplay_view = gameplay_view
        self.storyline = storyline
        self.current_level = starting_level
        self.level_start_time = time.time()
        #TODO: I set to None so that bugs can be found
        self.winning_score = None # level 0 is unpassable
        self.starting_score = 0

        self.life_suck_rate = None
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


    def set_level(self, next_level=False, set_level=None):
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
            self.level_setup()



    # def level_setup(self, gameplay_view):
    def level_setup(self):
        if self.current_level == 0:
            print("Setting playfield for level zero!")

            camera().resize(SCREEN_WIDTH * 1.5,
                            SCREEN_HEIGHT * 1.5
            )

            self.starting_score = self.gameplay_view.score
            self.winning_score = 0 # level 0 is unpassable


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
            self.gameplay_view.actor_group = pygame.sprite.Group() # KILL ALL AGENTS (wipe the board clean)

            camera().resize(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 6)
            self.starting_score = self.gameplay_view.score
            self.winning_score = self.starting_score + 10

            self.max_agents = 900

            self.show_vignette = False
            self.hide_out_of_sight = True
            self.depth_gradient = True

        elif self.current_level == 2:
            self.gameplay_view.actor_group = pygame.sprite.Group() # KILL ALL AGENTS (wipe the board clean)

            camera().resize(SCREEN_WIDTH * 4, SCREEN_HEIGHT * 4)
            self.starting_score = self.gameplay_view.score
            self.winning_score = self.starting_score + 10

            self.max_agents = 1200

            self.show_vignette = True
            self.hide_out_of_sight = True
            self.depth_gradient = True
        else:
            raise NotImplementedError(f"Level {self.level} not implemented")



    def spawn_krill(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.KRILL)
        agent.target = player()
        agent.hide_out_of_sight = hide_out_of_sight
        self.gameplay_view.actor_group.add(agent)



    def spawn_fren(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.FRENFISH)
        agent.target = player()
        agent.hide_out_of_sight = hide_out_of_sight
        self.gameplay_view.actor_group.add(agent)



    def spawn_fish(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.FISH)
        agent.target = player()
        agent.hide_out_of_sight = hide_out_of_sight
        self.gameplay_view.actor_group.add(agent)



    def spawn_kraken(self, hide_out_of_sight: bool = False):
        agent = Agent(AgentType.KRAKEN)
        agent.target = player()
        agent.hide_out_of_sight = hide_out_of_sight
        self.gameplay_view.actor_group.add(agent)



#####################################################
    # def level_agent_handler(self, gameplay_view):
    def level_agent_handler(self):
        #####################################################
        #################  LEVEL ONE  #######################
        #####################################################
        if self.current_level == 0:
            self.testing_level_agent_generator()
            # if time.time() > level().last_krill_spawn_time + level().agent_spawn_interval:
            #     level().last_krill_spawn_time = time.time()
            #     self.spawn_krill()

            # if time.time() > level().last_fish_spawn_time + level().agent_spawn_interval * 3: # 3:1 ratio krill to fish
            #     level().last_fish_spawn_time = time.time()
            #     self.spawn_fish()
        #####################################################
        #################  LEVEL TWO  #######################
        #####################################################
        elif self.current_level == 1:
            while len(self.gameplay_view.actor_group) < self.max_agents:
                random_number = random.uniform(0, 1)

                if random_number < 0.5:
                    self.spawn_krill( self.hide_out_of_sight )
                else:
                    self.spawn_fish( self.hide_out_of_sight )

        #####################################################
        #################  LEVEL THREE  #####################
        #####################################################
        elif self.current_level == 2:
            while len(self.gameplay_view.actor_group) < self.max_agents:
                random_number = random.uniform(0, 1)
                if random_number < 15/32:
                    # print("This branch runs with a 7/16 probability.")
                    self.spawn_krill( self.hide_out_of_sight )
                elif random_number < 15/32 + 16/32:
                    # print("This branch runs with a 8/16 (or 1/2) probability.")
                    self.spawn_fish( self.hide_out_of_sight )
                else:
                    # print("This branch runs with a 1/16 probability.")
                    self.spawn_kraken( self.hide_out_of_sight )



        # TODO - all levels have the same collision handler FOR NOW
        self.gameplay_view.handle_collisions()



    def testing_level_agent_generator(self):
        if self.gameplay_view.clicked:
            self.gameplay_view.clicked = False

            for i in range(4):
                x, y = self.gameplay_view.clicked_pos + camera().offset + pygame.Vector2(random.randint(-100, 100), random.randint(-100, 100))
                agent = Agent(AgentType.KRILL)
                agent.target = player()
                agent.max_sight = 200
                agent.position = pygame.Vector2(x, y)
                # agent.behavior_type = BehaviorType.FLOCK
                self.gameplay_view.actor_group.add(agent)
