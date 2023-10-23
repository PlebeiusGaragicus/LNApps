import time

# These can be anything, just make sure they're unique
KEY_UP = "up"
KEY_DOWN = "down"
KEY_LEFT = "left"
KEY_RIGHT = "right"


class CooldownKey():
    def __init__(self, key, cooldown_seconds):
        self.key = key
        self.cooldown_seconds = cooldown_seconds
        self.pressed = False
        self.last_pressed_time = None
    
    def reset(self):
        self.pressed = False
        self.last_pressed_time = None

    def run(self, key: int = None):
        """
            This needs to be run in the on_update() function AND the on_key_press() function
        """

        # for the on_key_press() function
        if key is not None:
            if key == self.key:
                self.pressed = True
                return False
            else:
                return False
        
        # for the on_update() function
        else:
            if self.pressed is True:
                if self.last_pressed_time is None or time.time() > self.last_pressed_time + self.cooldown_seconds:
                    self.last_pressed_time = time.time()
                    return True
                else:
                    return False
            else:
                return False

    def on_key_release(self, key: int):
        if key == self.key:
            self.pressed = False
            return True
        else:
            return False
