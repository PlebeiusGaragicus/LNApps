SNEK_GREEN = (90, 255, 50)
SNEK_DEAD = (30, 90, 20)
FOOD_COLOR = (255, 99, 99)
SNAKE_COLOR = (190, 40, 119)

BORDER_WIDTH = 4
SCREEN_SIZE = (240, 240)
FOOD_SIZE = 6
FOOD_TOLERANCE = 40
SNAKE_INIT_SIZE = 9
SNAKE_STARTING_POS = (20, 20)
SNAKE_INIT_SPEED_X = -2
SNAKE_INIT_SPEED_Y = -4
TOP_SPEED = 5
TOP_TOTAL_SPEED = 8


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = FOOD_SIZE
    
    def draw(self, drawer):
        drawer.rectangle((self.x, self.y, self.x + self.size, self.y + self.size), fill=FOOD_COLOR)

    def is_eaten(self, snake):
        head = snake[0]
        return head[0] == self.x and head[1] == self.y
    
    def snake_is_close(self, snake):
        head = snake[0]
        return (head[0] - self.x) ** 2 + (head[1] - self.y) ** 2 < FOOD_TOLERANCE

