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
# ---- extra life (both stages) and protection charm ----
def heart(n):
    im, d = canvas(128, 128)
    for col, o in (((120, 16, 24), 0), ((226, 40, 52), 5)):
        E(d, 12+o, 16+o, 58-2*o, 58-2*o, col); E(d, 58+o, 16+o, 58-2*o, 58-2*o, col); P(d, [(14+o, 56), (114-o, 56), (64, 116-o)], col)
    E(d, 28, 30, 20, 16, (255, 170, 170)); P(d, [(64, 44), (70, 60), (86, 60), (73, 70), (78, 86), (64, 76), (50, 86), (55, 70), (42, 60), (58, 60)], g.GOLD)
    save(im, out(n, 'item_life.png'), 128, 128)
heart(1); heart(2)
im, d = canvas(128, 128)   # stage 1: gold star
pts = [(64 + (56 if i % 2 == 0 else 24)*math.cos(-math.pi/2 + i*math.pi/5), 66 + (56 if i % 2 == 0 else 24)*math.sin(-math.pi/2 + i*math.pi/5)) for i in range(10)]
P(d, [(x, y+4) for x, y in pts], g.GOLD_D); P(d, pts, g.GOLD); P(d, [(64 + (x-64)*0.6, 66 + (y-66)*0.6) for x, y in pts], g.GOLD_L)
E(d, 50, 56, 8, 14, (30, 30, 30)); E(d, 70, 56, 8, 14, (30, 30, 30))
save(im, out(1, 'item_star.png'), 128, 128)
im, d = canvas(128, 128)   # stage 2: "um sabaa oyoun" seven-eyes blue charm
R(d, 60, 0, 8, 22, g.GOLD, 3); E(d, 10, 16, 108, 108, (14, 60, 130)); E(d, 14, 20, 100, 100, (30, 110, 200)); E(d, 22, 26, 40, 30, (110, 180, 240))
for i in range(7):
    if i < 6: a = i*math.pi/3; cx, cy = 64 + 30*math.cos(a), 70 + 30*math.sin(a)
    else: cx, cy = 64, 70
    E(d, cx-11, cy-11, 22, 22, (255, 255, 255)); E(d, cx-6, cy-6, 12, 12, (14, 40, 90))
save(im, out(2, 'item_star.png'), 128, 128)
