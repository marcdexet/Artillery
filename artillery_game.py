from typing import Tuple

import pygame as pg

from artillery.compute import Context, compute, new_ball, move
from artillery.pieces import Canon

RED = (150, 150, 150)


def init_game() -> Tuple[pg.Surface, pg.time.Clock]:
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((800, 800))
    return screen, clock


def draw_landscape(screen):
    screen.fill((53, 81, 92))


def draw_canon(screen):
    canon = pg.Rect((10, screen.get_height() - 20), (10, 2))
    pg.draw.rect(screen, RED, rect=canon)
    return canon


def draw_ball(screen, ball):
    x, y = ball[0, :]
    pg.draw.circle(screen, RED, (x, y), 5)


def run_game():
    done = False
    screen, clock = init_game()
    ball = None
    ctx = Context()

    def stop_fn(p):
        p[0][1] < 0

    canon = Canon(pos=(40,740),size=(50, 50))
    all_sprites = pg.sprite.Group(canon)
    required_angle = 0

    while not done:

        draw_landscape(screen)
        #canon = draw_canon(screen)

        if ball is not None:
            if not stop_fn(ball):
                move(ball, ctx)

            draw_ball(screen, ball)

        all_sprites.update()
        all_sprites.draw(screen)
#        screen.blit(canon.image, canon.rect)
        pg.display.flip()

        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_n:
                    ball = new_ball(ctx=ctx)
                    ball[0, :] = ( canon.x, canon.y)
                    ball[1, :] = [5., -5.]
                elif e.key == pg.K_a:
                    required_angle += 10
                    print(f'Required {required_angle}')
                    canon.set_required_elevation_to(required_angle)
                elif e.key == pg.K_z:
                    required_angle -= 10
                    print(f'Required {required_angle}')
                    canon.set_required_elevation_to(required_angle)
        clock.tick(40)


if __name__ == '__main__':
    run_game()
