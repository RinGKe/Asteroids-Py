import sys

import pygame

from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    POWER_UP_MULTI,
    POWER_UP_TIME,
    SHIELD_PULSE_RECHARGE_AMOUNT,
    SHOT_RADIUS,
)
from logger import log_event
from shield_pulse import Shield_Pulse
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.shot_timer = 0
        self.dead = False
        self.end_timer = 0
        self.shield = True
        self.kill_counter = 0
        self.left_shot = True
        self.power_up = 0
        self.power_multi = 1

    def destroy_shield(self):
        if self.shield:
            self.shield = False
            x, y = self.position
            Shield_Pulse(x, y, self.radius)

    def gain_power_up(self):
        self.power_up += POWER_UP_TIME

    def triangle(self):
        radius = float(self.radius)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        back = pygame.Vector2(0, 1).rotate(self.rotation + 90) * radius / 1.25
        front = pygame.Vector2(0, 1).rotate(self.rotation + 90) * radius / 5
        a = self.position + forward * radius + front
        b = self.position + forward * radius - front
        c = self.position - forward * radius - back
        d = self.position - forward * radius * 0.7
        e = self.position - forward * radius + back
        return [a, b, c, d, e]

    def color(self, source):
        if source == "player":
            if self.power_up > 0:
                return "blue"
            return "white"
        elif source == "shot":
            if self.power_up > 0:
                return "blue"
            return "green"
        else:
            return "white"

    def draw(self, surface):
        if self.shield:
            pygame.draw.polygon(surface, self.color("player"), self.triangle())
        elif self.dead:
            return None
        else:
            pygame.draw.polygon(
                surface, self.color("player"), self.triangle(), width=LINE_WIDTH
            )

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        if dt > 0:
            self.position += self.forward_vect * PLAYER_SPEED * dt * self.power_multi
        else:
            self.position += self.forward_vect * PLAYER_SPEED * dt * 0.5

    def shoot(self):
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * float(self.radius) / 3
        l_x, l_y = (
            self.position + self.forward_vect * (float(self.radius) * 0.35) + right
        )
        r_x, r_y = (
            self.position + self.forward_vect * (float(self.radius) * 0.35) - right
        )
        if self.left_shot:
            self.left_shot = False
            l_shot = Shot(l_x, l_y, SHOT_RADIUS, self.color("shot"))
            l_shot.velocity = self.forward_vect * PLAYER_SHOOT_SPEED
        else:
            self.left_shot = True
            r_shot = Shot(r_x, r_y, SHOT_RADIUS, self.color("shot"))
            r_shot.velocity = self.forward_vect * PLAYER_SHOOT_SPEED

    def add_kill_count(self):
        self.kill_counter += 1 * self.power_multi
        if not self.shield:
            if self.kill_counter % SHIELD_PULSE_RECHARGE_AMOUNT == 0:
                self.shield = True

    def death(self):
        if not self.dead:
            log_event("player_hit")
            print("|------------------------------------")
            print("|-------------GAME OVER!-------------")
            print(f"|-------------{self.kill_counter} POINTS!------------")
            print("|------------------------------------")
            self.dead = True

    def update(self, dt):
        self.forward_vect = pygame.Vector2(0, 1).rotate(self.rotation)
        self.shot_timer -= dt
        rev_dt = dt * -1
        if self.dead:
            self.end_timer += dt
            if self.end_timer >= 2:
                sys.exit()
        else:
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
                    self.shot_timer = PLAYER_SHOOT_COOLDOWN / self.power_multi
                    self.shoot()

            if self.power_up > 0:
                self.power_up -= dt
                self.power_multi = POWER_UP_MULTI
            else:
                self.power_multi = 1
