# from image import ResourceImage


import os
import math
from enum import Enum, auto
import arcade

MY_DIR = os.path.dirname(os.path.realpath(__file__))


class SlideMode(Enum):
    LINEAR = auto()
    DECAY = auto()


class ResourceImage():
    def __init__(self, img_name, x, y, alpha: int = 255):
        try:
            # self.texture = arcade.load_texture( os.path.join(MY_DIR, "resources/img", img_name + ".png") )
            self.texture = arcade.load_texture( os.path.join(MY_DIR, "resources/img", img_name) )
        except FileNotFoundError:
            self.texture = arcade.load_texture( os.path.join(MY_DIR, "missing.jpg") )
 
        self.position = [x, y]
        self.alpha = alpha
        self.angle = 0

    def draw(self):
        arcade.draw_texture_rectangle(center_x=self.position[0], center_y=self.position[1],
                                      width=self.texture.width, height=self.texture.height,
                                      texture=self.texture, angle=self.angle, alpha=self.alpha)
        # arcade.draw_scaled_texture_rectangle()





class SlideObject:
    def __init__(self, image_name, start_x, start_y, target_x, target_y, slide_duration, mode):
        self.image: ResourceImage = ResourceImage(image_name, start_x, start_y)
        self.target_position = [target_x, target_y]
        self.total_distance = ((target_x - start_x)**2 + (target_y - start_y)**2)**0.5
        self.distance_remaining = self.total_distance
        self.slide_duration = slide_duration
        self.time_elapsed = 0
        self.mode = mode

    def draw(self):
        self.image.draw()
        print(self.image.position)

    def update(self, delta_time):
        self.time_elapsed += delta_time
        time_remaining = self.slide_duration - self.time_elapsed
        
        if self.mode == SlideMode.LINEAR:
            if time_remaining <= 0:
                self.image.position = self.target_position
            else:
                fraction_of_time_passed = delta_time / self.slide_duration
                delta_x = (self.target_position[0] - self.image.position[0]) * fraction_of_time_passed
                delta_y = (self.target_position[1] - self.image.position[1]) * fraction_of_time_passed
                self.image.position[0] += delta_x
                self.image.position[1] += delta_y
        elif self.mode == SlideMode.DECAY:
            if time_remaining <= 0:
                self.image.position = self.target_position
            else:
                speed = self.distance_remaining / time_remaining
                move_distance = speed * delta_time
                direction_x = (self.target_position[0] - self.image.position[0]) / self.distance_remaining
                direction_y = (self.target_position[1] - self.image.position[1]) / self.distance_remaining
                delta_x = direction_x * move_distance
                delta_y = direction_y * move_distance
                self.image.position[0] += delta_x
                self.image.position[1] += delta_y
                self.distance_remaining -= move_distance

        # To avoid minor floating point inaccuracies causing perpetual movement
        if self.time_elapsed >= self.slide_duration:
            self.image.position = self.target_position




# class SlideObject:
#     def __init__(self, image_name, start_x, start_y, target_x, target_y, slide_speed, mode=SlideMode.LINEAR):
#         """
#         :param image_path: Path to the image file.
#         :param start_x: Initial x position.
#         :param start_y: Initial y position.
#         :param target_x: Target x position to slide to.
#         :param target_y: Target y position to slide to.
#         :param slide_speed: Pixels per frame the object should move.
#         """
#         self.image: ResourceImage = ResourceImage( image_name, start_x, start_y )
#         self.target_position = [target_x, target_y]
#         self.slide_speed = slide_speed
#         self.mode = mode

#     def draw(self):
#         """Draw the slide object."""
#         # arcade.draw_texture_rectangle(self.position[0], self.position[1],
#         #                               self.texture.width, self.texture.height,
#         #                               self.texture)
#         self.image.draw()

#     def update(self, delta_time):
#         """Update the slide object."""

#         if self.mode == SlideMode.LINEAR:
#             # Calculate vector to target position
#             vector_x = self.target_position[0] - self.image.position[0]
#             vector_y = self.target_position[1] - self.image.position[1]

#             # Calculate distance to target position
#             distance = (vector_x ** 2 + vector_y ** 2) ** 0.5

#             # If we are not at the target position yet, move towards it
#             if distance > 0:
#                 # Calculate how much we should move this frame
#                 move_x = vector_x / distance * self.slide_speed * delta_time
#                 move_y = vector_y / distance * self.slide_speed * delta_time

#                 # If we would move past the target position, move to the target position instead
#                 if abs(move_x) > abs(vector_x):
#                     move_x = vector_x
#                 if abs(move_y) > abs(vector_y):
#                     move_y = vector_y

#                 # Move the object
#                 self.image.position[0] += move_x
#                 self.image.position[1] += move_y

#                 # If we are at the target position, stop moving
#                 if self.image.position[0] == self.target_position[0] and self.image.position[1] == self.target_position[1]:
#                     self.slide_speed = 0
#         elif self.mode == SlideMode.DECAY:
#             distance_to_target = ((self.target_position[0] - self.image.position[0]) ** 2 + 
#                                 (self.target_position[1] - self.image.position[1]) ** 2) ** 0.5
#             decay_constant = 0.1  # Adjust this value for sharper or smoother decay
#             self.slide_speed = self.slide_speed * math.exp(-decay_constant * distance_to_target)
