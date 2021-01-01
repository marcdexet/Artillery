import numpy as np
import pygame as pg
from pygame.sprite import Sprite

from artillery.compute import move


class Canon(Sprite):

    def __init__(self, pos=(0, 0), size=(200, 200)):
        super(Canon, self).__init__()
        self.original_image = pg.image.load('sprites/canon_centered.png')
        rec = self.original_image.get_rect()
        self.original_vector = pg.Vector2(1.,0.)
        self.vector = self.original_vector
        pg.draw.line(surface=self.original_image, color=(255, 0, 255), start_pos=rec.midleft, end_pos=rec.midright, width=1)
        pg.draw.line(surface=self.original_image, color=(255, 0, 255), start_pos=rec.midtop, end_pos=rec.midbottom, width=1)

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        self.angle = 0
        self.required_angle = 0

    def set_required_elevation_to(self, required_elevation):
        self.required_angle = required_elevation

    def update(self):
        if self.angle != self.required_angle:
            orientation = 1 if (self.angle - self.required_angle < 0 ) else -1
            self.angle += orientation
            self.image = pg.transform.rotate(self.original_image, self.angle)
            self.vector = self.original_vector.rotate(self.angle)
            self.rect = self.image.get_rect(center=self.pos)

class Target(Sprite):

    def __init__(self, pos=(0, 0), size=(20,5)):
        super(Target, self).__init__()
        self.image = pg.Surface(size=size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos


class Ball(Sprite):

    def __init__(self,pos=(0, 0), size=(5,5)):
        super(Ball, self).__init__()
        self.ctx = None
        self.image = pg.Surface(size=size)
        self.rect = pg.draw.circle(self.image, pg.Color("red"), pos, 5)
        self.rect.center = pos
        self.pos = pos
        self.speed = pg.Vector2(0,0)
        self._base_altitude = self.pos[1]

    def set_initial_speed(self, speed, ctx):
        self.speed = speed
        self.ctx = ctx

    def update(self, *args, **kwargs) -> None:
        self.speed += pg.Vector2(0., self.ctx.g_per_tick)
        self.pos += self.speed
        self.rect = self.image.get_rect(center=self.pos)
        if self.pos[1] > self._base_altitude:
            self.kill()
