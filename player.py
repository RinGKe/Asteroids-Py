import pygame

from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SHOT_RADIUS,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.shot_timer = 0

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
        self.position += self.forward_vect * PLAYER_SPEED * dt

    def shoot(self):
        a, b = self.position
        for_x, for_y = self.forward_vect * float(self.radius)
        x = a + for_x
        y = b + for_y
        shot = Shot(x, y, SHOT_RADIUS)
        shot.velocity = self.forward_vect * PLAYER_SHOOT_SPEED

    def update(self, dt):
        self.forward_vect = pygame.Vector2(0, 1).rotate(self.rotation)
        self.shot_timer -= dt
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
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        if keys[pygame.K_SPACE]:
            if self.shot_timer <= 0:
                self.shot_timer = PLAYER_SHOOT_COOLDOWN
                self.shoot()
