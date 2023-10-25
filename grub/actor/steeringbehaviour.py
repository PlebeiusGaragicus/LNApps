import pygame

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
                 target: object = None):
        self.mass = mass
        self.position = position
        self.max_speed = max_speed
        self.max_force = max_force
        self.velocity = velocity
        self.heading = heading

    # def update(self):
        # pass

    # def seek(self, target: pygame.Vector2) -> pygame.Vector2:
    def seek(self) -> pygame.Vector2:
        if self.target is None:
            return pygame.Vector2(0, 0)

        target = self.target.position
        desired_velocity = (target - self.position).normalize() * self.max_speed
        steering_force = desired_velocity - self.velocity
        return steering_force

    def flee(self, target: pygame.Vector2) -> pygame.Vector2:
        desired_velocity = (self.position - target).normalize() * self.max_speed
        steering_force = desired_velocity - self.velocity
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

    def set_target(self, target: pygame.Vector2) -> None:
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