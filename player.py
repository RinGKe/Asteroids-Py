import pygame

from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180

    def triangle(self):
        radius = float(self.radius)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * radius / 1.5
        a = self.position + forward * radius
        b = self.position - forward * radius - right
        c = self.position - forward * radius + right
        return [a, b, c]

    def draw(self, surface):
        pygame.draw.polygon(surface, "white", self.triangle())

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward_vect = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward_vect * PLAYER_SPEED * dt

    def update(self, dt):
        rev_dt = dt * -1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(rev_dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(rev_dt)
