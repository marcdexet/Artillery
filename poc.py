import pygame as pg

class Subject(pg.sprite.Sprite):

    def __init__(self):
        super(Subject, self).__init__()
        self.image = pg.image.load('sprites/plane.png')
        self.rect = self.image.get_rect()

    def forward(self, surface: pg.Surface):
        r = self.rect
        self.rect.move_ip(2, 0)
        surface.blit(self.image, self.rect)


def run_main():
    done = False
    clock = pg.time.Clock()
    screen = pg.display.set_mode((800, 800))
    pg.init()

    s = Subject()
    while not done:

        screen.fill((20,20,20))
        s.forward(screen)
        pg.display.update()

        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break

        clock.tick(200)

if __name__ == '__main__':
    run_main()