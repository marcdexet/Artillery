from typing import Tuple

import pygame as pg
import numpy as np
from artillery.compute import Context, compute, new_ball, move
from artillery.pieces import Canon, Target, Ball

LANDSCAPE_COLOR = pg.Color("aliceblue")
TARGET_COLOR = pg.Color("firebrick4")
RED = (150, 150, 150)
FONT_COLOR = (255, 255, 255)
BASELINE = 20


def init_game() -> Tuple[pg.Surface, pg.time.Clock]:
    pg.init()
    pg.key.set_repeat(50,100)
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1600, 600))
    font = pg.font.Font(None, 25)
    return screen, clock, font


def draw_landscape(screen, canon_pos):
    screen.fill(LANDSCAPE_COLOR)
    w, h = screen.get_size()
    wc, hc = canon_pos
    coef = 50
    for x in range(0, h // coef + 1):
        pg.draw.line(screen, pg.Color("darkblue"),(wc, coef*x - BASELINE), (w, coef*x - BASELINE))

    delta_x = wc
    for x in range(0, w // coef):
        pg.draw.line(screen, pg.Color("grey"),(coef*x + wc, 0), (coef*x + wc, hc))


def print_texts(screen, font, canon, spring, coef_spring, score, nb_try):
    xstart, _ = canon.pos
    pg.draw.rect(screen,pg.Color("black"),(xstart-2, 8, 300, 142))
    base = 10
    screen.blit(font.render(str("Angle: %.2f" % canon.required_angle), True, FONT_COLOR), (xstart, base))
    base += 30
    screen.blit(font.render(str("Force: %.2f" % spring), True, FONT_COLOR), (xstart, base))
    base += 30
    screen.blit(font.render(str("Coef.: %.2f" % coef_spring), True, FONT_COLOR), (xstart, base))
    base += 30
    screen.blit(font.render(str("Score: %s " % score), True, FONT_COLOR), (xstart, base))
    base += 30
    screen.blit(font.render(str("Tries: %s " % nb_try), True, FONT_COLOR), (xstart, base))



def run_game():
    done = False
    screen, clock, font = init_game()
    ball = None
    ctx = Context()
    delta_angle = 1.

    canon = Canon(pos=(40,screen.get_height() - BASELINE),size=(50, 50))
    target = Target(pos=(1000, screen.get_height() - BASELINE))
    all_sprites = pg.sprite.Group(canon)
    all_sprites.add(target)
    required_angle = 0
    spring = 10.
    coef_spring = 1.
    score = 0
    nb_try = 5
    while not done:

        draw_landscape(screen, canon.pos)

        all_sprites.update()
        all_sprites.draw(screen)

        if ball:
            if pg.sprite.collide_rect(ball, target):
                print("COLLIDE")
                ball = None
                score += 1
                target.kill()
                width, height = screen.get_size()
                target = Target(pos=(np.random.randint(width //8, width - BASELINE), height - BASELINE))
                all_sprites.add(target)
                nb_try = 5
            elif ball.is_out():
                nb_try -= 1
                ball.kill()
                ball = None

        if nb_try <= 0:
            w, h = screen.get_size()
            screen.blit(font.render("The END ! (press M to restart)", True, FONT_COLOR), (w // 2, h // 2))

        print_texts(screen=screen, font=font, canon=canon, spring=spring, coef_spring=coef_spring, score=score, nb_try=nb_try)

        pg.display.flip()

        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and keys[pg.K_ESCAPE]):
                done = 1
                break
            elif e.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                modes = pg.key.get_mods()
                if modes & pg.KMOD_SHIFT:
                    print("SHIFT")
                modifying_angle = 0
                modif_spring = 0
                if keys[pg.K_SPACE] and ball is None:
                    ball = Ball(pos=canon.rect.center)
                    x, y = canon.vector
                    ball.set_initial_speed(np.array([x, -y]) * spring, ctx)
                    all_sprites.add(ball)
                    print(f'VEC={canon.vector}, l={canon.vector.length()}, BALL={ball}')
                elif keys[pg.K_a] or keys[pg.K_LEFT] and not modes & pg.KMOD_SHIFT:
                    modifying_angle += delta_angle
                elif keys[pg.K_z] or keys[pg.K_RIGHT] and not modes & pg.KMOD_SHIFT:
                    modifying_angle -= delta_angle
                elif keys[pg.K_q] or keys[pg.K_LEFT] and modes & pg.KMOD_SHIFT:
                    modifying_angle += delta_angle * 5
                elif keys[pg.K_s] or keys[pg.K_RIGHT] and modes & pg.KMOD_SHIFT:
                    modifying_angle -= delta_angle * 5
                elif keys[pg.K_w] or keys[pg.K_UP]:
                    modif_spring += 1 * coef_spring
                elif keys[pg.K_x] or keys[pg.K_DOWN]:
                    modif_spring -= 1 * coef_spring
                elif keys[pg.K_c] or keys[pg.K_PAGEUP]:
                    coef_spring *= 10
                elif keys[pg.K_v] or keys[pg.K_PAGEDOWN]:
                    coef_spring /= 10

                elif keys[pg.K_m]:
                    nb_try = 5
                    score = 0
                if modifying_angle:
                    required_angle += modifying_angle
                    canon.set_required_elevation_to(required_angle)
                if modif_spring:
                    spring += modif_spring
        clock.tick(40)


if __name__ == '__main__':
    run_game()
