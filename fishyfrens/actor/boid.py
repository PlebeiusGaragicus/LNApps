import logging
logger = logging.getLogger()

import pygame
import numpy as np

from gamelib.colors import Colors
from gamelib.globals import APP_SCREEN

from fishyfrens.actor import BehaviorType

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

        self.target = None
        self.mass: int = mass
        self.position: pygame.Vector2 = position
        self.max_speed: int = max_speed
        self.max_force: int = max_force
        self.velocity: pygame.Vector2 = velocity

        # This is for drawing the vectors and are not needed.  Helpful for debugging
        self.desired_velocity = pygame.Vector2(0, 0)
        self.steering_force = pygame.Vector2(0, 0)

        self.decay_rate: float = decay_rate
        self.behavior_type: BehaviorType = behavior_type
        self.vel_coef = 1
        # self.vel_coef = 0.999
        self.max_sight = max_sight



###########################################
    def draw_vectors(self):
        self.draw_vector(self.desired_velocity, color=Colors.GREEN)
        self.draw_vector(self.steering_force, color=Colors.BLUE)
        self.draw_vector(self.velocity, color=Colors.RED)

        # draw circle with radius max_sight // 3
        pygame.draw.circle(APP_SCREEN, Colors.RED, self.position, self.max_sight, 1)
        pygame.draw.circle(APP_SCREEN, Colors.GREEN, self.position, self.max_sight // 2, 1)



###########################################
    def draw_vector(self, vec, color: pygame.Color = Colors.RED, magnitude = 20):
        player_center = self.position + self.size // 2
        player_center += -camera().offset
        pygame.draw.line(APP_SCREEN, color, player_center, player_center + vec * magnitude, 3)




###########################################
    def update_steering(self, all_actors: pygame.sprite.Group):
        self.velocity *= self.vel_coef

        # steering = pygame.Vector2(0, 0)
        self.steering_force = pygame.Vector2(0, 0)

        if self.behavior_type & BehaviorType.SEEK:
            self.steering_force += self.seek()

        if self.behavior_type & BehaviorType.FLEE:
            flee_force = self.flee()
            # self.steering_force += flee_force + flee_force + flee_force + flee_force
            self.steering_force += flee_force * 4

        if self.behavior_type & BehaviorType.FLOCK:
            self.steering_force += self.flock( all_actors )

        # self.steering_force = steering

        # LIMIT STEERING FORCE TO MAX FORCE
        # if self.steering_force.magnitude() > self.max_force:
        #     self.steering_force = self.steering_force.normalize() * self.max_force

        if self.steering_force.magnitude() > 0:
            self.steering_force = self.steering_force.normalize() * self.max_force

        # steering_force /= self.mass  # Assuming mass is not zero
        self.velocity += self.steering_force

        # LIMIT VELOCITY TO MAX SPEED
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.position += self.velocity


###########################################
    def seek(self) -> pygame.Vector2:
        if self.target is None:
            return pygame.Vector2(0, 0)
        
        distance = self.position.distance_to(self.target.position)
        if distance > self.max_sight:
            return pygame.Vector2(0, 0)

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
            return pygame.Vector2(0, 0)

        self.desired_velocity = (self.position - self.target.position).normalize() * self.max_speed
        steering_force = self.desired_velocity - self.velocity
        steering_force = steering_force.normalize() * self.max_force

        # Standard decay for flee
        decay_factor = np.exp(-self.decay_rate * distance / self.max_sight)
        steering_force *= decay_factor

        return steering_force


    def align(self, neighbors: pygame.sprite.Group) -> pygame.Vector2:
        average = pygame.Vector2(0, 0)
        for a in neighbors:
            average += a.velocity

        average /= max(len(neighbors), 1)
        return average.normalize() * self.max_force if average != pygame.Vector2(0, 0) else pygame.Vector2(0, 0)


    def separate(self, neighbors: pygame.sprite.Group) -> pygame.Vector2:
        average = pygame.Vector2(0, 0)
        for a in neighbors:
            diff = self.position - a.position
            diff /= a.distance
            average += diff

        average /= max(len(neighbors), 1)
        # return average
        return average.normalize() * self.max_force if average != pygame.Vector2(0, 0) else pygame.Vector2(0, 0)



    def cohere(self, neighbors: pygame.sprite.Group) -> pygame.Vector2:
        average = pygame.Vector2(0, 0)
        for a in neighbors:
            average += a.position

        average /= max(len(neighbors), 1)
        # return average - self.position
        return average.normalize() * self.max_force if average != pygame.Vector2(0, 0) else pygame.Vector2(0, 0)


###########################################
    def flock(self, all_actors: pygame.sprite.Group) -> pygame.Vector2:
        # get actors within sight

        neighbors: pygame.sprite.Group = pygame.sprite.Group()
        for a in all_actors:
            if a != self:
                distance = self.position.distance_to(a.position)
                a.distance = distance
                if distance < self.max_sight // 2:
                    neighbors.add(a)


        if len(neighbors) == 0:
            return pygame.Vector2(0, 0)
        else:
            return self.align( neighbors ) * 1 + \
                    self.separate( neighbors ) * 0.5 + \
                        self.cohere( neighbors ) * 1.3

            # return self.cohere( neighbors )
            # return self.align( neighbors )
            # return self.seperate( neighbors )
