import enum

class BehaviorType:
    NONE = 0x00000000
    SEEK = 0x00000002
    FLEE = 0x00000004
    ARRIVE = 0x00000008
    WANDER = 0x00000010
    COHESION = 0x00000020
    SEPARATION = 0x00000040
    ALIGNMENT = 0x00000080
    OBSTACLE_AVOIDANCE = 0x00000100
    WALL_AVOIDANCE = 0x00000200
    FOLLOW_PATH = 0x00000400
    PURSUIT = 0x00000800
    EVADE = 0x00001000
    INTERPOSE = 0x00002000
    HIDE = 0x00004000
    FLOCK = 0x00008000
    OFFSET_PURSUIT = 0x00010000


# TODO: turn these into proper classes.  Inherit from the Agent class and override methods.  Create a collide_with_player() function as well.
class AgentType(enum.Enum):
    KRILL = enum.auto()
    FISH = enum.auto() # basically your food
    FRENFISH = enum.auto() # just the generic boring fish pngs

    ENEMY = enum.auto()
    KRAKEN = enum.auto()


class BoundaryBehaviour(enum.Enum):
    Bounce = enum.auto()
    Wrap = enum.auto()


# how far away from the edge of the playfield should agents be spawned
SAFE_BUFFER = 100 # TODO: move this into a SafeXY() function

# how far off screen to draw agents - arbitrary number that needs a better solution overall
VIEW_OPTO_PIXEL_DISTANCE = -150

