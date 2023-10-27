import pygame

import steeringbehaviour

class FriendFish(steeringbehaviour):
    def __init__(self, world, image, position, name='FriendFish', mass=1, max_force=1, max_speed=1, max_turn_rate=1, scale=1):
        super().__init__(world, image, position, name, mass, max_force, max_speed, max_turn_rate, scale)
        self.steering_behaviours = ['seek', 'flee', 'arrive', 'wander', 'pursuit', 'evade', 'follow_path']
        self.steering_behaviour = 'seek'
        self.target = None
        self.path = None
        self.path_index = 0
        self.path_loop = False
        self.path_threshold = 20


    def update(self, delta):
        super().update(delta)
        if self.path:
            if self.path_index >= len(self.path):
                if self.path_loop:
                    self.path_index = 0
                else:
                    self.path = None
                    return
            self.target = self.path[self.path_index]
            if self.position.distance_to(self.target) < self.path_threshold:
                self.path_index += 1


    def render(self, surface):
        super().render(surface)
        if self.path:
            for i in range(len(self.path) - 1):
                pygame.draw.line(surface, (0, 0, 255), self.path[i], self.path[i + 1], 1)


    def set_path(self, path, loop=False, threshold=20):
        self.path
        self.path_index = 0
        self.path_loop = loop
        self.path_threshold = threshold
