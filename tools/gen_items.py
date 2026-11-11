"""Power-up art: item_grow, item_weapon, shot for each stage (128x128 each)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
import gen_stage1 as g
R, E, P, canvas, save = g.R, g.E, g.P, g.canvas, g.save
def out(n, name): return os.path.join(g.OUT, f'stage{n}', name)
# ---- stage 1: golden apple / ball ----
im, d = canvas(128, 128)
E(d, 14, 30, 60, 84, (176, 28, 28)); E(d, 54, 30, 60, 84, (176, 28, 28)); E(d, 18, 32, 56, 78, (226, 52, 44)); E(d, 54, 32, 56, 78, (226, 52, 44))
E(d, 28, 44, 20, 30, (255, 150, 130)); R(d, 60, 10, 8, 30, (96, 62, 36), 4); E(d, 66, 8, 40, 20, (62, 158, 74)); E(d, 74, 12, 22, 8, (120, 205, 120))
save(im, out(1, 'item_grow.png'), 128, 128)
def ball(path, size=128):
    im, d = canvas(128, 128)
    E(d, 10, 10, 108, 108, (24, 24, 28)); E(d, 14, 14, 100, 100, (240, 240, 240))
    for a in range(5):
        an = -math.pi/2 + a*2*math.pi/5; cx, cy = 64 + 40*math.cos(an), 64 + 40*math.sin(an)
        P(d, [(cx + 15*math.cos(an + k*2*math.pi/5), cy + 15*math.sin(an + k*2*math.pi/5)) for k in range(5)], (24, 24, 28))
    P(d, [(64 + 17*math.cos(-math.pi/2 + k*2*math.pi/5 + math.pi/5), 64 + 17*math.sin(-math.pi/2 + k*2*math.pi/5 + math.pi/5)) for k in range(5)], g.GOLD)
    E(d, 30, 24, 26, 16, (255, 255, 255)); save(im, path, 128, 128)
ball(out(1, 'item_weapon.png')); ball(out(1, 'shot.png'))
# ---- stage 2: tea istikan / sling (misyada) / pebble ----
im, d = canvas(128, 128)
E(d, 10, 96, 108, 24, (212, 175, 55)); E(d, 18, 98, 92, 16, (255, 244, 200))
P(d, [(38, 22), (90, 22), (84, 56), (92, 104), (36, 104), (44, 56)], (236, 244, 248)); P(d, [(42, 40), (86, 40), (82, 58), (88, 100), (40, 100), (46, 58)], (150, 52, 20))
E(d, 38, 16, 52, 14, (236, 244, 248)); E(d, 42, 34, 44, 12, (190, 76, 30)); R(d, 38, 60, 52, 5, (212, 175, 55)); R(d, 48, 44, 6, 50, (220, 130, 80), 3)
for x, y in ((52, 2), (70, 0)): E(d, x, y, 8, 16, (255, 255, 255, 150))
save(im, out(2, 'item_grow.png'), 128, 128)
im, d = canvas(128, 128)
W, WD = (122, 74, 34), (84, 48, 20)
R(d, 54, 62, 20, 62, WD, 8); R(d, 58, 64, 8, 56, W, 4)
P(d, [(54, 76), (22, 20), (38, 14), (68, 66)], WD); P(d, [(74, 76), (106, 20), (90, 14), (60, 66)], WD); P(d, [(56, 72), (28, 22), (34, 20), (62, 66)], W)
d.line([(30*g.SS, 18*g.SS), (64*g.SS, 44*g.SS), (98*g.SS, 18*g.SS)], fill=(30, 20, 14), width=6*g.SS); R(d, 52, 36, 24, 16, (138, 31, 31), 4)
save(im, out(2, 'item_weapon.png'), 128, 128)
im, d = canvas(128, 128)
P(d, [(22, 70), (36, 30), (76, 16), (108, 44), (104, 88), (68, 112), (32, 100)], (96, 88, 80)); P(d, [(30, 68), (42, 36), (76, 24), (98, 46), (70, 60)], (150, 142, 130)); E(d, 48, 36, 22, 12, (196, 190, 180))
save(im, out(2, 'shot.png'), 128, 128)
