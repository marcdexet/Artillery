from dataclasses import dataclass
from enum import Enum

import numpy as np


class Const:
    G = 9.81

@dataclass
class Context:
    g_per_tick: float = Const.G/100
    bounce_dispersion: float = 0.01


def move(p: np.ndarray, ctx: Context):
    p[1, :] += (0., ctx.g_per_tick)
    p[0, :] += p[1, :]


def compute(p: np.ndarray, ctx: Context, stop_fn= None, bounce_fn=None, nmax: int = 1000000):
    if stop_fn is None:
        def stop_fn(p):
            p[0][1] < 0

    for i in range(nmax):
        move(p, ctx)
        if bounce_fn and bounce_fn(p):
            bounce(p, ctx)
        yield p
        if stop_fn(p):
            break


def bounce(p: np.ndarray, ctx: Context):
    coef: float = 1 - ctx.bounce_dispersion
    p[1, :] *= (coef, -coef)


def new_ball(ctx: Context):
    return np.zeros((2, 2)).astype(float)


