import numpy as np

from artillery.compute import move, compute, Const, bounce, Context


def test_move():
    a = np.zeros((2, 2), dtype=float)
    ctx = Context(g_per_tick=Const.G/20)
    move(a, ctx)
    assert a[0][0] == 0.
    assert a[0][1] == -9.81/20


def test_compute():
    a = np.zeros((2, 2), dtype=float)
    a[1, :] += (20., 20.)
    ctx = Context()
    trajectory = [(p[0][0], p[0][1]) for p in compute(p=a, ctx=ctx, nmax=1000)]
    assert len(trajectory) > 100
    assert len({p for p in trajectory}) > 100


def test_bounce():
    a = np.zeros((2, 2), dtype=float)
    a[1, :] += (20., -20.)
    ctx = Context()
    bounce(a, ctx)
    assert a[1][0], a[1][1] == (18., 18.)
