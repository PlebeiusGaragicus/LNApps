import logging
logger = logging.getLogger()

import pygame
import numpy as np

from gamelib.colors import Colors
from gamelib.globals import APP_SCREEN

from fishyfrens.actor import BehaviorType, NULL_VECTOR

from fishyfrens.view.camera import camera




class Boid:
    def __init__(self,
                 mass: int,
                 position: pygame.Vector2,
                 max_speed: int,
                 max_force: int,
                 velocity: pygame.Vector2,
                 decay_rate: float,
                 max_sight: int,
                 behavior_type: BehaviorType):

        self.mass: int = mass
        self.position: pygame.Vector2 = position
        self.max_speed: int = max_speed
        self.max_force: int = max_force
        self.velocity: pygame.Vector2 = velocity

        # This is for drawing the vectors and are not needed.  Helpful for debugging
        self.desired_velocity = NULL_VECTOR
        self.steering_force = NULL_VECTOR

        self.decay_rate: float = decay_rate
        self.behavior_type: BehaviorType = behavior_type
        self.vel_coef = 1
        # self.vel_coef = 0.999
        self.max_sight = max_sight



###########################################
    def draw_vectors(self):
        # self.draw_vector(self.desired_velocity, color=Colors.GREEN)
        # self.draw_vector(self.steering_force, color=Colors.BLUE)
        self.draw_vector(self.velocity, color=Colors.RED)



###########################################
    def draw_vector(self, vec, color: pygame.Color = Colors.RED, magnitude = 20):
        player_center = self.position + self.size // 2
        player_center += -camera().offset
        pygame.draw.line(APP_SCREEN, color, player_center, player_center + vec * magnitude, 3)




###########################################
    def update_steering(self):
        self.velocity *= self.vel_coef

        if self.behavior_type is not None:
            if self.behavior_type & BehaviorType.SEEK:
                self.steering_force = self.seek()
                self.velocity += self.steering_force

            if self.behavior_type & BehaviorType.FLEE:
                self.steering_force = self.flee()
                self.velocity += self.steering_force
            
            # if self.behavior_type & BehaviorType.ARRIVE:
            #     self.steering_force = self.arrive()
            #     self.velocity += self.steering_force

            if self.behavior_type & BehaviorType.FLOCK:
                self.steering_force = self.flock()
                self.velocity += self.steering_force

        # cap velocity
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        # steering_force /= self.mass  # Assuming mass is not zero
        self.velocity += self.steering_force
        self.position += self.velocity


###########################################
    def seek(self) -> pygame.Vector2:
        if self.target is None:
            return pygame.Vector2(0, 0)
        
        distance = self.position.distance_to(self.target.position)
        if distance > self.max_sight:
            return NULL_VECTOR

        self.desired_velocity = (self.target.position - self.position).normalize() * self.max_speed
        steering_force = self.desired_velocity - self.velocity
        steering_force = steering_force.normalize() * self.max_force

        # Invert the decay factor for the seeker
        decay_factor = 1 - np.exp(-self.decay_rate * (1 - distance / self.max_sight))
        steering_force *= decay_factor

        return steering_force


###########################################
    def flee(self) -> pygame.Vector2:
        if self.target is None:
            return pygame.Vector2(0, 0)
        
        distance = self.position.distance_to(self.target.position)
        if distance > self.max_sight:
            return NULL_VECTOR

        self.desired_velocity = (self.position - self.target.position).normalize() * self.max_speed
        steering_force = self.desired_velocity - self.velocity
        steering_force = steering_force.normalize() * self.max_force

        # Standard decay for flee
        decay_factor = np.exp(-self.decay_rate * distance / self.max_sight)
        steering_force *= decay_factor

        return steering_force


###########################################
    def flock(self) -> pygame.Vector2:
        return NULL_VECTOR
