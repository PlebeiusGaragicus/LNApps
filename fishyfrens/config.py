import platform

## CONTROL
AFK_TIMEOUT = 300 # 5 minutes (set to zero to diable)
HOLD_TO_QUIT_SECONDS = 1.5
COOLDOWN_DIRECTIONAL_SECONDS = 0.05
# COOLDOWN_DIRECTIONAL_SECONDS = 0.1

## DISPLAY / UI
# NOTE: only for MacOS... need to test on rpi
# this is because of the menu bar / camera cutout on the macbook air
TOP_BAR_HEIGHT = 0
if platform.system() == "Darwin":
    TOP_BAR_HEIGHT = 34

FPS = 80
BORDER_WIDTH = 6
# PLAYFIELD_WIDTH = 4000
# PLAYFIELD_HEIGHT = 4000
PLAYFIELD_WIDTH = 3000
PLAYFIELD_HEIGHT = 3000
# PLAYFIELD_WIDTH = 2000
# PLAYFIELD_HEIGHT = 2000


## GAMEPLAY - all variables are set for level 1
LIFE_SUCK_RATE = 1
AGENT_SPAWN_INTERVAL_SECONDS = 0.05
# MAX_AGENTS = 900 # 80 FPS MacOS
# MAX_AGENTS = 2000 # 46 FPS MacOS
# MAX_AGENTS = 1500 # 53 FPS MacOS
MAX_AGENTS = 1000 # 70-80 FPS MacOS


## PLAYER
PLAYER_STARTING_POS = (20, 20)
WALL_BOUNCE_ATTENUATION = 0.40
PLAYER_TOP_SPEED = 3
PLAYER_ACCELERATION = 0.5

## DEBUG / TESTING
# These need to be in their own file so that I can reference them via debug.DRAW_MASKS so that I can change them at runtime
# DRAW_MASKS = False
# DRAW_VECTORS = True
# DRAW_RECTS = True







#NOTE: This would create a circular import
# from .view.camera import Camera
# CAMERA: Camera = None

# from .actor.player import Player
# PLAYER: Player = None
