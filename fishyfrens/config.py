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

### 1/2x
PLAYFIELD_WIDTH = 720
PLAYFIELD_HEIGHT = 449

# 1479
# WIDTH + overpan // 3

### 1x - 16L9 - MacOS 15 inch Air - Display size: 1440 x 898 (720 x 449)
# PLAYFIELD_WIDTH = 1440
# PLAYFIELD_HEIGHT = 900

### 2x
PLAYFIELD_WIDTH = 2890
PLAYFIELD_HEIGHT = 1800

# PLAYFIELD_WIDTH = 2000
# PLAYFIELD_HEIGHT = 2000
# PLAYFIELD_WIDTH = 3000
# PLAYFIELD_HEIGHT = 3000
PLAYFIELD_WIDTH = 5000
PLAYFIELD_HEIGHT = 5000


## GAMEPLAY - all variables are set for level 1
LIFE_SUCK_RATE = 1
AGENT_SPAWN_INTERVAL_SECONDS = 0.05
# MAX_AGENTS = 900 # 80 FPS MacOS
# MAX_AGENTS = 2000 # 80 FPS MacOS (after optimization!!!)
# MAX_AGENTS = 4000 # Very playable on MacOS - can lag when screen crowded & with vectors/mask drawn
# MAX_AGENTS = 1500 # 53 FPS MacOS / ~35-45 on arcade
# MAX_AGENTS = 1000 # 70-80 FPS MacOS / 
# MAX_AGENTS = 5000 # 40-50 FPS MacOS / SHIT on arcade
MAX_AGENTS = 900


## PLAYER
PLAYER_STARTING_POS = (20, 20)
PLAYER_WALL_BOUNCE_ATTENUATION = 0.60
PLAYER_TOP_SPEED = 6
PLAYER_ACCELERATION = 0.5
# PLAYER_ACCELERATION = 0.5
# PLAYER_ACCELERATION = 2.5

## AGENTS
# AGENT_WALL_BOUNCE_ATTENUATION = 0.89
# AGENT_WALL_BOUNCE_ATTENUATION = 3.5
AGENT_WALL_BOUNCE_ATTENUATION = 2.1

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
