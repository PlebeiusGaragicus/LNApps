import os
import platform

MY_DIR = os.path.dirname(os.path.abspath(__file__))


## CONTROL
AFK_TIMEOUT = 300  # 5 minutes (set to zero to diable)
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
# BORDER_WIDTH = 6

# PLAYFIELD_WIDTH = None
# PLAYFIELD_HEIGHT = None
### 1/2x
# PLAYFIELD_WIDTH = 720
# PLAYFIELD_HEIGHT = 449

# 1479
# WIDTH + overpan // 3

### 1x - 16L9 - MacOS 15 inch Air - Display size: 1440 x 898 (720 x 449)
# PLAYFIELD_WIDTH = 1440
# PLAYFIELD_HEIGHT = 900

### 2x
# PLAYFIELD_WIDTH = 2890
# PLAYFIELD_HEIGHT = 1800

# PLAYFIELD_WIDTH = 2000
# PLAYFIELD_HEIGHT = 2000
# PLAYFIELD_WIDTH = 3000
# PLAYFIELD_HEIGHT = 3000
# PLAYFIELD_WIDTH = 5000
# PLAYFIELD_HEIGHT = 5000


## GAMEPLAY - all variables are set for level 1
## NOTE: These are not set in gameplay.level_setup()
