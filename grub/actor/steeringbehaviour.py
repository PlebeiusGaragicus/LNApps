import logging
logger = logging.getLogger()

import pygame

from gamelib.colors import Colors
from gamelib.globals import APP_SCREEN

from grub.view.camera import CAMERA

NULL_VECTOR = pygame.Vector2(0, 0)

class BehaviorType:
    NONE = 0x00000000
    SEEK = 0x00000002
    FLEE = 0x00000004
    ARRIVE = 0x00000008
    WANDER = 0x00000010
    COHESION = 0x00000020
    SEPARATION = 0x00000040
    ALIGNMENT = 0x00000080
    OBSTACLE_AVOIDANCE = 0x00000100
    WALL_AVOIDANCE = 0x00000200
    FOLLOW_PATH = 0x00000400
    PURSUIT = 0x00000800
    EVADE = 0x00001000
    INTERPOSE = 0x00002000
    HIDE = 0x00004000
    FLOCK = 0x00008000
    OFFSET_PURSUIT = 0x00010000


class SteeringBehaviour:
    mass: int = None
    position: pygame.Vector2 = None
    max_speed: int = None
    max_force: int = None
    velocity: pygame.Vector2 = None
    heading: pygame.Vector2 = None

    def __init__(self,
                 mass: int,
                 position:
                 pygame.Vector2,
                 max_speed: int,
                 max_force: int,
                 velocity: pygame.Vector2,
                 heading: pygame.Vector2,
                 behavior_type: BehaviorType = BehaviorType.NONE):
        self.mass = mass
        self.position = position
        self.max_speed = max_speed
        self.max_force = max_force
        self.velocity = velocity
        self.heading = heading
        self.behavior_type = behavior_type

        self.deceleration_tweaker = 1.4

        self.vel_coef = 1.0

        # these are for drawing the vectors and are not needed.  Helpful for debugging
        self.desired_velocity = NULL_VECTOR

    def set_velocity_coefficients(self, vel_coef: float) -> None:
        self.vel_coef = vel_coef


    def update_steering(self):
        if self.behavior_type & BehaviorType.SEEK:
            steering_force = self.seek()
            self.velocity += steering_force

        if self.behavior_type & BehaviorType.FLEE:
            steering_force = self.flee()
            self.velocity += steering_force

        # cap velocity
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.velocity *= self.vel_coef
        self.position += self.velocity


    def draw_vectors(self):
        self.draw_vector(self.desired_velocity, color=Colors.GREEN)
        self.draw_vector(self.velocity, color=Colors.RED)


    def draw_vector(self, vec, color: pygame.Color = Colors.RED, magnitude = 8):
        player_center = self.position + self.size // 2
        player_center += -CAMERA.offset
        pygame.draw.line(APP_SCREEN, color, player_center, player_center + vec * magnitude, 3)


    def set_target(self, target: pygame.Vector2) -> None:
        self.target = target

    # def seek(self, target: pygame.Vector2) -> pygame.Vector2:
    def seek(self) -> pygame.Vector2:
        """ returns a 'steering force' """
        if self.target is None:
            logger.warning(f"{__class__.__name__} self.target is None")
            return pygame.Vector2(0, 0)

        self.desired_velocity = (self.target.position - self.position).normalize() * self.max_speed
        distance = self.position.distance_to(self.target.position)
        if distance > 0:
            # deceleration_tweaker = 1.4
            speed = distance / (self.deceleration_tweaker)
            speed = min(speed, self.max_speed)
            self.desired_velocity *= speed / distance

        steering_force = self.desired_velocity - self.velocity

        # limit by max force
        steering_force = steering_force.normalize() * self.max_force
        return steering_force


    def flee(self) -> pygame.Vector2:
        """ returns a 'steering force' """
        # steering_force = -self.seek()
        # self.desired_velocity = -self.desired_velocity
        # return steering_force
        if self.target is None:
            logger.warning(f"{__class__.__name__} self.target is None")
            return pygame.Vector2(0, 0)

        self.desired_velocity = (self.target.position - self.position).normalize() * self.max_speed
        # attenuate desired velocity - the farther the target is, the less we want to flee
        distance = self.position.distance_to(self.target.position)
        if distance > 0:
            # deceleration_tweaker = 1.4
            speed = distance / (self.deceleration_tweaker)
            speed = min(speed, self.max_speed)
            self.desired_velocity *= speed / -distance

        steering_force = self.desired_velocity - self.velocity

        # limit by max force
        steering_force = steering_force.normalize() * self.max_force
        return steering_force










    def arrive(self, target: pygame.Vector2, deceleration: int) -> pygame.Vector2:
        desired_velocity = (target - self.position).normalize() * self.max_speed
        distance = target.distance_to(self.position)
        if distance > 0:
            deceleration_tweaker = 0.3
            speed = distance / (deceleration * deceleration_tweaker)
            speed = min(speed, self.max_speed)
            desired_velocity *= speed / distance
        steering_force = desired_velocity - self.velocity
        return steering_force

    def pursue(self, target: pygame.Vector2) -> pygame.Vector2:
        return self.seek(target)

    def evade(self, target: pygame.Vector2) -> pygame.Vector2:
        return self.flee(target)

    def wander(self) -> pygame.Vector2:
        pass

    def obstacle_avoidance(self) -> pygame.Vector2:
        pass

    def wall_avoidance(self) -> pygame.Vector2:
        pass

    def interpose(self) -> pygame.Vector2:
        pass

    def hide(self) -> pygame.Vector2:
        pass

    def follow_path(self) -> pygame.Vector2:
        pass

    def offset_pursuit(self) -> pygame.Vector2:
        pass

    def flock(self) -> pygame.Vector2:
        pass

    def cohesion(self) -> pygame.Vector2:
        pass

    def separation(self) -> pygame.Vector2:
        pass

    def alignment(self) -> pygame.Vector2:
        pass

    def calculate(self) -> pygame.Vector2:
        pass

    def render(self) -> None:
        pass

    def set_path(self, path: pygame.Vector2) -> None:
        pass

    def set_obstacles(self, obstacles: pygame.Vector2) -> None:
        pass

    def set_walls(self, walls: pygame.Vector2) -> None:
        pass

    def set_neighbors(self, neighbors: pygame.Vector2) -> None:
        pass

    def set_leader(self, leader: pygame.Vector2) -> None:
        pass

    def set_offset(self, offset: pygame.Vector2) -> None:
        pass