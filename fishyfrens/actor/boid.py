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

        self.target = None
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

        steering = pygame.Vector2(0, 0)
        if self.behavior_type & BehaviorType.SEEK:
            steering += self.seek()

        if self.behavior_type & BehaviorType.FLEE:
            flee_force = self.flee()
            steering += flee_force + flee_force + flee_force + flee_force

        if self.behavior_type & BehaviorType.FLOCK:
            steering += self.flock( all_actors )

        self.steering_force = steering

        # normalize steering force
        if self.steering_force.magnitude() > self.max_force:
            self.steering_force = self.steering_force.normalize() * self.max_force

        # steering_force /= self.mass  # Assuming mass is not zero
        self.velocity += self.steering_force

        # cap velocity
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

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


    def align(self, neighbors: pygame.sprite.Group) -> pygame.Vector2:
        print("aligning with neighbors", len(neighbors))
        average = pygame.Vector2(0, 0)
        print("neighbors: ", len(neighbors))
        for a in neighbors:
            average += a.velocity

        average /= max(len(neighbors), 1)
        return average.normalize() * self.max_force if average != NULL_VECTOR else NULL_VECTOR


    def separate(self, neighbors: pygame.sprite.Group) -> pygame.Vector2:
        return NULL_VECTOR

    def cohere(self, neighbors: pygame.sprite.Group) -> pygame.Vector2:
        return NULL_VECTOR

###########################################
    def flock(self, all_actors: pygame.sprite.Group) -> pygame.Vector2:
        # get actors within sight

        neighbors: pygame.sprite.Group = pygame.sprite.Group()
        for a in all_actors:
            if a != self:
                distance = self.position.distance_to(a.position)
                # if self.position.distance_to(a.position) < self.max_sight // 3:
                # print(distance)
                if distance < self.max_sight // 2:
                    neighbors.add(a)


        if len(neighbors) == 0:
            print("no neighbors")
            return NULL_VECTOR
        else:
            return self.align( neighbors ) + self.separate( neighbors ) + self.cohere( neighbors )
        # return self.align( all_actors ) + self.separate( all_actors ) + self.cohere( all_actors )
