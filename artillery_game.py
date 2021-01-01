from typing import Tuple

import pygame as pg
import numpy as np
from artillery.compute import Context, compute, new_ball, move
from artillery.pieces import Canon, Target

RED = (150, 150, 150)


def init_game() -> Tuple[pg.Surface, pg.time.Clock]:
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1600, 600))
    font = pg.font.Font(None, 25)
    return screen, clock, font


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
    screen, clock, font = init_game()
    ball = None
    ctx = Context()
    delta_angle = 1.
    FONT_COLOR = (255,255,255)
    def stop_fn(p):
        p[0][1] < 0

    canon = Canon(pos=(40,screen.get_height() - 20),size=(50, 50))
    target = Target(pos=(1000, screen.get_height() - 20))
    all_sprites = pg.sprite.Group(canon)
    all_sprites.add(target)
    required_angle = 0
    spring = 10.
    coef_spring = 1.

    while not done:

        draw_landscape(screen)
        #canon = draw_canon(screen)

        if ball is not None:
            if not stop_fn(ball):
                move(ball, ctx)

            draw_ball(screen, ball)

        all_sprites.update()
        all_sprites.draw(screen)

        text_angle = font.render(str("Angle: %.2f " % canon.required_angle), True, FONT_COLOR)
        screen.blit(text_angle, (10, 10))
        text_spring = font.render(str("Force: %.2f " % spring), True, FONT_COLOR)
        screen.blit(text_spring, (10, 40))
        text_coef = font.render(str("Coef.: %.2f " % coef_spring), True, FONT_COLOR)
        screen.blit(text_coef, (10, 70))
        pg.display.flip()

        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
            elif e.type == pg.KEYDOWN:
                modifying_angle = 0
                modif_spring = 0
                if e.key == pg.K_n:
                    ball = new_ball(ctx=ctx)
                    ball[0, :] = canon.rect.center
                    x, y = canon.vector
                    ball[1, :] = np.array([x, -y]) * spring
                    print(f'VEC={canon.vector}, l={canon.vector.length()}, BALL={ball}')
                elif e.key == pg.K_a:
                    modifying_angle += delta_angle
                elif e.key == pg.K_z:
                    modifying_angle -= delta_angle
                elif e.key == pg.K_q:
                    modifying_angle += delta_angle * 5
                elif e.key == pg.K_s:
                    modifying_angle -= delta_angle * 5
                elif e.key == pg.K_w:
                    modif_spring += 1 * coef_spring
                elif e.key == pg.K_x:
                    modif_spring -= 1 * coef_spring
                elif e.key == pg.K_c:
                    coef_spring *= 10
                elif e.key == pg.K_v:
                    coef_spring /= 10
                if modifying_angle:
                    required_angle += modifying_angle
                    canon.set_required_elevation_to(required_angle)
                if modif_spring:
                    spring += modif_spring
        clock.tick(40)


if __name__ == '__main__':
    run_game()
