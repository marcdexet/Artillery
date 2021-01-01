import pygame as pg
from pygame.sprite import Sprite


class Canon(Sprite):

    def __init__(self, pos=(0, 0), size=(200, 200)):
        super(Canon, self).__init__()
        self.original_image = pg.image.load('sprites/canon.png')
        rec = self.original_image.get_rect()
        self.pivot = pg.Vector2(rec.width * 2 / 5, rec.height / 2)
        self.original_vector = pg.Vector2(rec.width * (2 / 5 - 1 / 2), 0.)

        pg.draw.line(surface=self.original_image, color=(255, 0, 255), start_pos=rec.midleft, end_pos=rec.midright, width=1)
        pg.draw.line(surface=self.original_image, color=(255, 0, 255), start_pos=rec.midtop, end_pos=rec.midbottom, width=1)
        pg.draw.line(surface=self.original_image, color=(125, 125, 255), start_pos=(self.pivot[0], 0), end_pos=(self.pivot[0], rec.bottom), width=1)

        self.image = self.original_image
        self.vector = self.original_vector
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pg.Vector2(pos)
        self.angle = 0
        self.required_angle = 0

    def set_required_elevation_to(self, required_elevation):
        self.required_angle = required_elevation

    def update(self):
        if self.angle != self.required_angle:
            orientation = 1 if (self.angle - self.required_angle < 0 ) else -1
            self.angle += orientation
            rotated = self.original_vector.rotate(self.angle)
            offset = rotated - self.original_vector
            self.image = pg.transform.rotate(self.original_image, self.angle)
            print(f'ROTATE=({rotated}, len={rotated.length()}), OFFSET=({offset}, len={offset.length()}), ORIG={self.original_image.get_rect().center}, ROTATED={self.image.get_rect().center}')
            self.rect = self.image.get_rect(center=self.pos + offset  - self.original_vector)