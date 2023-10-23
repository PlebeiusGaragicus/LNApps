import sys
import random
import sfml as sf

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20

class Snake:
    def __init__(self):
        self.positions = [(5, 5)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head = self.positions[0]
        new_position = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.positions = [new_position] + self.positions

        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def grow_up(self):
        self.grow = True

    def collides_with_itself(self):
        return len(self.positions) != len(set(self.positions))

    def collides_with_bounds(self):
        head = self.positions[0]
        return (head[0] < 0 or head[0] >= WINDOW_WIDTH // BLOCK_SIZE or
                head[1] < 0 or head[1] >= WINDOW_HEIGHT // BLOCK_SIZE)

class Food:
    def __init__(self):
        self.position = (random.randint(0, (WINDOW_WIDTH // BLOCK_SIZE) - 1),
                         random.randint(0, (WINDOW_HEIGHT // BLOCK_SIZE) - 1))

    def reposition(self):
        self.position = (random.randint(0, (WINDOW_WIDTH // BLOCK_SIZE) - 1),
                         random.randint(0, (WINDOW_HEIGHT // BLOCK_SIZE) - 1))

def main():
    window = sf.RenderWindow(sf.VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Snake Game")
    clock = sf.Clock()
    snake = Snake()
    food = Food()

    while window.is_open:
        for event in window.events:
            if type(event) is sf.CloseEvent:
                window.close()
            if type(event) is sf.KeyEvent and event.released:
                if event.code == sf.Keyboard.UP:
                    snake.direction = (0, -1)
                elif event.code == sf.Keyboard.DOWN:
                    snake.direction = (0, 1)
                elif event.code == sf.Keyboard.LEFT:
                    snake.direction = (-1, 0)
                elif event.code == sf.Keyboard.RIGHT:
                    snake.direction = (1, 0)

        snake.move()

        if snake.positions[0] == food.position:
            snake.grow_up()
            food.reposition()

        if snake.collides_with_bounds() or snake.collides_with_itself():
            snake = Snake()  # Reset the snake

        window.clear()

        # Draw food
        food_shape = sf.RectangleShape()
        food_shape.position = (food.position[0] * BLOCK_SIZE, food.position[1] * BLOCK_SIZE)
        food_shape.size = (BLOCK_SIZE, BLOCK_SIZE)
        food_shape.fill_color = sf.Color.RED
        window.draw(food_shape)

        # Draw snake
        for position in snake.positions:
            snake_shape = sf.RectangleShape()
            snake_shape.position = (position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE)
            snake_shape.size = (BLOCK_SIZE, BLOCK_SIZE)
            snake_shape.fill_color = sf.Color.GREEN
            window.draw(snake_shape)

        window.display()

        sf.sleep(sf.milliseconds(150))

if __name__ == "__main__":
    main()
