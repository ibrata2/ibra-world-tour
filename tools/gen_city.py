"""Default art for stages 3-7 (Cairo, Moscow, Delhi, Beijing, New York). Every file is replaceable by a hand-made design."""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(__file__))
import gen_stage1 as g
from PIL import Image, ImageDraw, ImageFilter
R, E, P, canvas, save, noise, SS = g.R, g.E, g.P, g.canvas, g.save, g.noise, g.SS
GOLD, GOLD_L, GOLD_D = g.GOLD, g.GOLD_L, g.GOLD_D
W, H, GL = 4720, 1080, 940

def star(d, cx, cy, r, col, n=8, inner=0.5, ox=0, oy=0, rot=-math.pi / 2):
    P(d, [(cx + (r if i % 2 == 0 else r * inner) * math.cos(rot + i * math.pi / n), cy + (r if i % 2 == 0 else r * inner) * math.sin(rot + i * math.pi / n)) for i in range(2 * n)], col, ox, oy)
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def dk(c, k=0.7): return tuple(int(v * k) for v in c)
def lt(c, k=0.35): return tuple(int(v + (255 - v) * k) for v in c)

# ---------------- tiles ----------------
def tiles(S, c):
    for top in (True, False):
        im, d = canvas(128, 128, dk(c['g']) + (255,))
        if c['gstyle'] == 'asphalt':
            R(d, 0, 0, 128, 128, c['g'])
            if not top: R(d, 20, 58, 88, 10, c['gacc'], 3)
        else:
            rows, bw = (4, 64) if c['gstyle'] == 'brick' else (2, 64)
            bh = 128 // rows
            for row in range(rows):
                off = 0 if row % 2 == 0 else -bw // 2
                for col in range(4):
                    x, y = off + col * bw, row * bh
                    sh = [c['g'], lt(c['g'], .12), dk(c['g'], .9)][(row + col) % 3]
                    R(d, x + 2, y + 2, bw - 4, bh - 4, sh, 3); R(d, x + 4, y + 3, bw - 8, 5, lt(sh, .25), 2)
        if top:
            R(d, 0, 0, 128, 22, c['gtop']); R(d, 0, 0, 128, 7, lt(c['gtop'], .4)); R(d, 0, 22, 128, 4, dk(c['gtop'], .75))
            if c['gstyle'] == 'snow':
                for x in range(0, 128, 32): E(d, x - 4, 12, 40, 26, c['gtop'])
            else:
                for x in range(8, 128, 32): star(d, x + 8, 11, 6, c['gacc'], c.get('n', 8))
        noise(im, 8, 3); save(im, os.path.join(S, 'ground_top.png' if top else 'ground_fill.png'), 128, 128)
    im, d = canvas(128, 128, dk(c['br'], .55) + (255,))
    for row in range(4):
        off = 0 if row % 2 == 0 else -32
        for col in range(3):
            x, y = off + col * 64, row * 32
            R(d, x + 2, y + 2, 60, 28, c['br'], 3); R(d, x + 4, y + 3, 56, 6, lt(c['br'], .3), 2); R(d, x + 4, y + 23, 56, 5, dk(c['br'], .78), 2)
    noise(im, 8, 6); save(im, os.path.join(S, 'brick.png'), 128, 128)
    for used in (False, True):
        base = (112, 98, 84) if used else c['box']
        im, d = canvas(128, 128, dk(base, .55) + (255,))
        R(d, 4, 4, 120, 120, base, 10); R(d, 8, 8, 112, 12, lt(base, .35), 6); R(d, 8, 108, 112, 12, dk(base, .7), 6)
        m = (140, 130, 116) if used else GOLD
        for x, y in ((4, 4), (104, 4), (4, 104), (104, 104)): R(d, x, y, 20, 20, m, 5)
        if not used: star(d, 64, 68, 36, dk(base, .6), c.get('n', 8)); star(d, 64, 64, 34, GOLD_L, c.get('n', 8)); star(d, 64, 64, 16, c['gacc'], c.get('n', 8))
        noise(im, 6, 7); save(im, os.path.join(S, 'box_used.png' if used else 'box.png'), 128, 128)
    im, d = canvas(128, 128, dk(c['blk'], .55) + (255,))
    R(d, 4, 4, 120, 120, c['blk'], 6); P(d, [(4, 4), (124, 4), (106, 22), (22, 22)], lt(c['blk'], .35)); P(d, [(4, 124), (124, 124), (106, 106), (22, 106)], dk(c['blk'], .72))
    R(d, 22, 22, 84, 84, c['blk2'], 4); star(d, 64, 64, 30, lt(c['blk2'], .55), c.get('n', 8)); E(d, 56, 56, 16, 16, GOLD)
    noise(im, 7, 8); save(im, os.path.join(S, 'block.png'), 128, 128)
    for name, top in (('pipe_top.png', True), ('pipe_body.png', False)):
        im, d = canvas(256, 128); x0, w = (0, 256) if top else (18, 220); p = c['pipe']
        R(d, x0, 0, w, 128, dk(p, .55), 10 if top else 0); y0, hh = (6, 116) if top else (0, 128)
        R(d, x0 + 8, y0, w - 16, hh, p, 6 if top else 0); R(d, x0 + 28, y0, 26, hh, lt(p, .45)); R(d, x0 + 62, y0, 10, hh, lt(p, .2)); R(d, x0 + w - 62, y0, 42, hh, dk(p, .75))
        if top: R(d, 8, 100, 240, 18, dk(p, .55)); R(d, 8, 40, 240, 10, c['gacc'])
        save(im, os.path.join(S, name), 256, 128)

# ---------------- enemies (generic critter) ----------------
def critter(S, c):
    im, d = canvas(384, 128); B, F, k = c['e_body'], c['e_face'], c['e_kind']
    for i in range(3):
        ox = i * 128
        if i == 2: E(d, 8, 96, 112, 28, B, ox); E(d, 80, 100, 32, 18, F, ox); continue
        f = 0 if i == 0 else 12
        leg = (30, 30, 30) if k == 'panda' else dk(B, .65)
        E(d, 22 + f, 104, 28, 20, leg, ox); E(d, 72 - f, 104, 28, 20, leg, ox)
        if k in ('cat', 'monkey'):   # tail
            for j in range(6): E(d, 4 + j * 2, 84 - j * 12 + (j * j if k == 'monkey' else 0), 14, 14, dk(B, .8), ox)
        if k == 'rat': d.line([(14 * SS + ox * SS, 100 * SS), (0 * SS + ox * SS, 84 * SS), (6 * SS + ox * SS, 66 * SS)], fill=(230, 150, 160), width=5 * SS)
        if k == 'bird':
            E(d, 16, 50, 84, 62, B, ox); P(d, [(18, 70), (2, 58), (4, 86)], dk(B, .7), ox); E(d, 30, 62, 48, 30, dk(B, .8), ox)
        else: E(d, 12, 44, 92, 70, B, ox)
        E(d, 62, 40, 58, 58, B if k != 'monkey' else dk(B, .9), ox); E(d, 76, 56, 42, 40, F, ox)
        if k in ('cat', 'rat'): P(d, [(66, 50), (72, 22), (88, 44)], B, ox); P(d, [(96, 44), (110, 22), (114, 50)], B, ox)
        elif k == 'bird': P(d, [(116, 70), (128, 76), (114, 84)], (240, 170, 40), ox)
        else:
            ec = (30, 30, 30) if k == 'panda' else dk(B, .75)
            E(d, 60, 30, 24, 24, ec, ox); E(d, 100, 30, 24, 24, ec, ox)
        if k == 'panda': E(d, 84, 60, 20, 22, (30, 30, 30), ox)
        E(d, 88, 62, 14, 16, (255, 255, 255), ox); E(d, 94, 66, 8, 10, (20, 20, 20), ox); P(d, [(82, 58), (104, 64), (104, 60), (84, 52)], (40, 26, 20), ox)
        if k != 'bird': E(d, 110, 78, 12, 10, (40, 26, 20), ox)
    save(im, os.path.join(S, 'enemy1.png'), 384, 128)
    # water enemy: a fish, 2 swim frames + 1 defeated
    im, d = canvas(384, 128); fc = c['fish']
    for i in range(3):
        ox = i * 128; t = (0, 10, 0)[i]
        P(d, [(28, 64), (4, 34 + t), (4, 94 - t)], dk(fc, .75), ox); E(d, 20, 34, 96, 60, fc, ox); E(d, 36, 60, 70, 30, lt(fc, .4), ox)
        P(d, [(50, 38), (70, 14), (86, 38)], dk(fc, .75), ox)
        if i < 2: E(d, 86, 46, 18, 18, (255, 255, 255), ox); E(d, 93, 50, 9, 10, (20, 20, 20), ox); P(d, [(82, 42), (106, 50), (106, 46), (84, 38)], (40, 26, 20), ox)
        else: R(d, 86, 52, 16, 4, (20, 20, 20), 0, ox)
    save(im, os.path.join(S, 'enemy_water.png'), 384, 128)

# ---------------- hero ----------------
def hero(n, o):
    im, d = canvas(960, 256); SK, SKD, BD = g.SKIN, g.SKIN_D, g.BEARD
    for i, pose in enumerate(['idle', 'run1', 'run2', 'run3', 'jump']):
        ox = i * 192
        bl, blift, fl, flift, arm = {'idle': (74, 0, 100, 0, 0), 'run1': (58, 0, 116, 14, 18), 'run2': (84, 10, 92, 0, 0), 'run3': (116, 14, 58, 0, -18), 'jump': (60, 22, 118, 4, -30)}[pose]
        oy = (4 if pose == 'run2' else 0) + (-6 if pose == 'jump' else 0); sp = {'idle': 0, 'run1': 14, 'run2': 4, 'run3': 14, 'jump': 18}[pose]
        top, sl = o['top'], o.get('sleeve', o['top'])
        R(d, 66 - arm, 124 + oy, 24, 60, dk(sl, .8), 12, ox); E(d, 66 - arm, 170 + oy, 24, 24, SKD, ox)
        hem = o.get('hem', 0)   # 0 = short top, 1 = knee-length, 2 = full robe
        for lx, lift, col in ((bl, blift, dk(o['legs'], .8)), (fl, flift, o['legs'])):
            R(d, lx - 14, 176 + oy, 30, 56 - lift, col, 10, ox)
            R(d, lx - 16, 226 - lift, 46, 22, dk(o['shoes'], .6), 10, ox); R(d, lx - 16, 226 - lift, 46, 15, o['shoes'], 8, ox)
        if hem:
            hy = 214 if hem == 2 else 196
            P(d, [(58, 120 + oy), (134, 120 + oy), (140 + sp, hy + oy), (52 - sp, hy + oy)], top, ox)
        R(d, 58, 110 + oy, 76, 80 if not hem else 44, top, 18, ox)
        if o.get('stripes'):
            for sx in (74, 96, 118): R(d, sx, 116 + oy, 4, (96 if hem == 2 else 78 if hem else 70), o['stripes'], 0, ox)
        if o.get('belt'): R(d, 56, 156 + oy, 80, 14, o['belt'], 5, ox)
        if o.get('buttons'):
            for by in (124, 142, 160, 178): E(d, 92, by + oy, 9, 9, o['buttons'], ox); R(d, 84, by + 3 + oy, 26, 3, o['buttons'], 1, ox) if o.get('frog') else None
        if o.get('sash'): P(d, [(120, 112 + oy), (134, 118 + oy), (72, 196 + oy), (58, 188 + oy)], o['sash'], ox)
        if o.get('collar'): R(d, 56, 106 + oy, 80, 16, o['collar'], 8, ox)
        if o.get('open'): R(d, 82, 114 + oy, 28, 74, o['open'], 6, ox)
        # head
        E(d, 56, 34 + oy, 84, 84, SK, ox); E(d, 128, 74 + oy, 20, 18, SK, ox)
        P(d, [(60, 82 + oy), (140, 86 + oy), (134, 116 + oy), (104, 126 + oy), (72, 116 + oy)], BD, ox); E(d, 56, 62 + oy, 22, 46, BD, ox)
        R(d, 112, 90 + oy, 22, 5, SKD, 2, ox); E(d, 108, 62 + oy, 16, 20, (255, 255, 255), ox); E(d, 115, 66 + oy, 9, 13, (20, 20, 20), ox); R(d, 102, 54 + oy, 28, 6, BD, 3, ox)
        h, hc = o['hat'], o['hatc']
        if h == 'tarboosh': P(d, [(66, 56 + oy), (72, 6 + oy), (124, 6 + oy), (130, 56 + oy)], hc, ox); R(d, 72, 2 + oy, 52, 8, lt(hc, .2), 4, ox); R(d, 122, 4 + oy, 5, 44, (20, 20, 20), 2, ox); E(d, 118, 44 + oy, 12, 14, (20, 20, 20), ox)
        elif h == 'ushanka':
            E(d, 48, 8 + oy, 100, 62, hc, ox); R(d, 48, 40 + oy, 100, 20, lt(hc, .35), 8, ox); R(d, 46, 44 + oy, 28, 62, hc, 10, ox); E(d, 92, 20 + oy, 14, 14, (200, 30, 30), ox)
        elif h == 'pagri':
            E(d, 46, 4 + oy, 104, 62, hc, ox)
            for kk in range(4): P(d, [(50, 40 - kk * 9 + oy), (146, 26 - kk * 9 + oy), (146, 32 - kk * 9 + oy), (50, 46 - kk * 9 + oy)], dk(hc, .78), ox)
            E(d, 108, 22 + oy, 16, 16, GOLD, ox); P(d, [(60, 50 + oy), (44, 96 + oy), (58, 100 + oy), (70, 56 + oy)], hc, ox)
        elif h == 'douli': P(d, [(20, 58 + oy), (98, 4 + oy), (176, 58 + oy)], hc, ox); P(d, [(20, 58 + oy), (176, 58 + oy), (160, 64 + oy), (36, 64 + oy)], dk(hc, .75), ox); P(d, [(60, 34 + oy), (98, 8 + oy), (106, 14 + oy), (70, 40 + oy)], lt(hc, .3), ox)
        elif h == 'capback':
            d.pieslice([(ox + 52) * SS, (20 + oy) * SS, (ox + 142) * SS, (104 + oy) * SS], 180, 360, fill=hc); R(d, 20, 54 + oy, 50, 12, hc, 6, ox); R(d, 52, 56 + oy, 90, 8, dk(hc, .75), 0, ox)
        R(d, 96 + arm, 124 + oy, 24, 60, sl, 12, ox)
        if o.get('cuff'): R(d, 96 + arm, 146 + oy, 24, 8, o['cuff'], 0, ox)
        E(d, 96 + arm, 170 + oy, 26, 26, SK, ox)
    save(im, os.path.join(g.HERO, f'stage{n}.png'), 960, 256)

# ---------------- backgrounds ----------------
def sky(S, stops, sun=None, sil=None, band=None, stars=0, seed=1):
    im = Image.new('RGBA', (3840, H)); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for y in range(H):
        t = y / H
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1: d.line([(0, y), (3840, y)], fill=lerp(c0, c1, (t - t0) / (t1 - t0)) + (255,)); break
    for _ in range(stars): x, y = rnd.randrange(3840), rnd.randrange(620); d.rectangle([x, y, x + 3, y + 3], fill=(255, 255, 240, 255))
    if sun:
        x, y, r, col = sun; gl = Image.new('RGBA', im.size); gd = ImageDraw.Draw(gl); gd.ellipse([x - r * 2.6, y - r * 2.6, x + r * 2.6, y + r * 2.6], fill=col + (80,)); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(60))); d = ImageDraw.Draw(im); d.ellipse([x - r, y - r, x + r, y + r], fill=col + (255,))
    if sil: sil(d, rnd)
    if band:
        y0, c0, c1 = band
        for y in range(y0, H): d.line([(0, y), (3840, y)], fill=lerp(c0, c1, (y - y0) / (H - y0)) + (255,))
    im.convert('RGB').save(os.path.join(S, 'bg_far.jpg'), quality=92)

def haze(im, col, a):
    hz = Image.new('RGBA', im.size, col + (255,)); al = im.getchannel('A'); out = Image.blend(im, hz, a); out.putalpha(al); return out
def box(d, x0, y0, x1, y1, c): d.rectangle([x0, y0, x1, y1], fill=c + (255,))
def dome(d, x0, y0, x1, y1, c): d.pieslice([x0, y0, x1, y1], 180, 360, fill=c + (255,))
def tri(d, pts, c): d.polygon(pts, fill=c + (255,))
def wins(d, x0, y0, x1, y1, c, sx, sy, w, h, rnd, p=0.75):
    for x in range(int(x0), int(x1 - w), sx):
        for y in range(int(y0), int(y1 - h), sy):
            if rnd.random() < p: d.rectangle([x, y, x + w, y + h], fill=c + (255,))
def arch(d, x, w, h, c): box(d, x, GL - h + w / 2, x + w, GL, c); dome(d, x, GL - h, x + w, GL - h + w, c)

def mid_cairo(d, rnd):
    x = 30; S1, S2, WD, DK, LAMP = (214, 176, 118), (196, 152, 94), (112, 66, 30), (58, 34, 16), (255, 190, 80)
    while x < W - 300:
        k = rnd.random()
        if k < 0.6:
            bw, bh = rnd.randrange(190, 300), rnd.randrange(340, 540); c = rnd.choice([S1, S2, (224, 190, 134)])
            box(d, x, GL - bh, x + bw, GL, c); box(d, x - 8, GL - bh - 14, x + bw + 8, GL - bh, dk(c, .8))
            for cx in range(x, x + bw, 26): tri(d, [(cx, GL - bh - 14), (cx + 13, GL - bh - 34), (cx + 26, GL - bh - 14)], dk(c, .8))
            for i in range(max(1, bw // 110)):   # mashrabiya bays
                mx = x + 16 + i * 108; my = GL - bh + 70
                box(d, mx - 6, my, mx + 90, my + 130, WD); tri(d, [(mx - 6, my + 130), (mx + 90, my + 130), (mx + 78, my + 150), (mx + 6, my + 150)], DK)
                for gx in range(mx, mx + 84, 8): d.line([(gx, my + 12), (gx, my + 122)], fill=DK + (255,), width=3)
                for gy in range(my + 12, my + 124, 8): d.line([(mx, gy), (mx + 84, gy)], fill=DK + (255,), width=3)
                box(d, mx - 6, my, mx + 90, my + 10, lt(WD, .25))
            arch(d, x + bw / 2 - 34, 68, 150, DK); box(d, x + bw / 2 - 60, GL - 196, x + bw / 2 - 52, GL - 170, (40, 40, 40)); d.ellipse([x + bw / 2 - 70, GL - 176, x + bw / 2 - 42, GL - 140], fill=LAMP + (255,))
            x += bw + rnd.randrange(20, 60)
        elif k < 0.85:   # mamluk minaret + small dome
            box(d, x, GL - 300, x + 260, GL, S2); dome(d, x + 40, GL - 430, x + 220, GL - 170, (232, 210, 160))
            for i in range(9): d.arc([x + 40 + i * 8, GL - 430, x + 220 - i * 8, GL - 170], 180, 360, fill=dk(S2, .8) + (255,), width=3)
            for kx in range(3): arch(d, x + 30 + kx * 78, 46, 120, DK)
            mx = x + 290; box(d, mx, GL - 620, mx + 54, GL, S1)
            for by in (GL - 420, GL - 540): box(d, mx - 12, by, mx + 66, by + 18, WD)
            box(d, mx + 10, GL - 700, mx + 44, GL - 620, S1); dome(d, mx + 6, GL - 760, mx + 48, GL - 680, (232, 210, 160)); box(d, mx + 25, GL - 800, mx + 29, GL - 756, GOLD)
            for by in range(GL - 600, GL - 60, 60): box(d, mx, by, mx + 54, by + 8, (176, 96, 60))
            x += 400
        else:
            for px in (x + 30, x + 110): palm(d, px, rnd.randrange(300, 440))
            x += 180
def palm(d, x, s):
    for i in range(12): d.rectangle([x - 7, GL - s + i * s / 12, x + 7, GL - s + (i + 1) * s / 12], fill=(110, 70, 36, 255) if i % 2 else (132, 86, 44, 255))
    for a in range(-80, 261, 34):
        ar = math.radians(a); pts = [(x, GL - s)] + [(x + math.cos(ar) * t * 18, GL - s - math.sin(ar) * t * 18 + t * t * 2.2) for t in range(1, 7)]
        d.line(pts, fill=(40, 104, 56, 255), width=12); d.line(pts, fill=(58, 132, 70, 255), width=5)

def mid_moscow(d, rnd):
    RED, RD, WH, GR, SN = (166, 44, 34), (120, 28, 22), (240, 236, 228), (40, 110, 70), (255, 255, 255)
    box(d, 0, GL - 250, W, GL, RED); box(d, 0, GL - 250, W, GL - 236, lt(RED, .2))
    for x in range(0, W, 46):
        box(d, x, GL - 296, x + 28, GL - 250, RED); tri(d, [(x, GL - 296), (x + 7, GL - 312), (x + 14, GL - 296)], RED); tri(d, [(x + 14, GL - 296), (x + 21, GL - 312), (x + 28, GL - 296)], RED); box(d, x, GL - 300, x + 28, GL - 296, SN)
    for x in range(60, W, 140): arch(d, x, 40, 120, RD)
    x = 200
    while x < W - 500:
        k = rnd.random()
        if k < 0.45:   # tower with green spire and star
            box(d, x, GL - 520, x + 150, GL, dk(RED, .92)); box(d, x - 12, GL - 540, x + 162, GL - 516, WH)
            box(d, x + 25, GL - 660, x + 125, GL - 540, RED); tri(d, [(x + 15, GL - 660), (x + 75, GL - 860), (x + 135, GL - 660)], GR); tri(d, [(x + 15, GL - 660), (x + 60, GL - 810), (x + 45, GL - 660)], lt(GR, .25))
            pts = [(x + 75 + (26 if i % 2 == 0 else 11) * math.cos(-math.pi / 2 + i * math.pi / 5), GL - 884 + (26 if i % 2 == 0 else 11) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]; tri(d, pts, (220, 40, 40))
            d.ellipse([x + 40, GL - 500, x + 110, GL - 430], fill=WH + (255,), outline=(40, 30, 20, 255), width=5); d.line([(x + 75, GL - 465), (x + 75, GL - 492)], fill=(30, 20, 10, 255), width=4); d.line([(x + 75, GL - 465), (x + 94, GL - 458)], fill=(30, 20, 10, 255), width=4)
            for yy in (GL - 380, GL - 250): arch(d, x + 55, 40, GL - yy, RD) if False else box(d, x + 55, yy, x + 95, yy + 70, RD)
            x += 420
        elif k < 0.8:  # cathedral with onion domes
            cols = [(232, 176, 32), (58, 107, 192), (40, 140, 84), (200, 60, 50), (232, 176, 32)]
            for i, (dx, hh, r) in enumerate([(0, 300, 44), (90, 380, 52), (190, 470, 70), (310, 380, 52), (400, 300, 44)]):
                cx = x + dx + 40; box(d, cx - r * .6, GL - hh, cx + r * .6, GL, WH); box(d, cx - r * .6, GL - hh, cx - r * .25, GL, lt(WH, .5))
                for j in range(-r, r + 1):
                    w = math.sqrt(r * r - j * j); w = max(w, r * .55) if j > r * .45 else w
                    d.line([(cx - w, GL - hh - r + j), (cx + w, GL - hh - r + j)], fill=cols[i] + (255,))
                tri(d, [(cx - r * .5, GL - hh - r * 1.75), (cx, GL - hh - r * 2.7), (cx + r * .5, GL - hh - r * 1.75)], cols[i])
                for s in range(-2, 3): d.arc([cx - r + abs(s) * 9, GL - hh - 2 * r, cx + r - abs(s) * 9, GL - hh], 200, 340, fill=dk(cols[i], .75) + (255,), width=4)
                box(d, cx - 2, GL - hh - r * 2.7 - 40, cx + 2, GL - hh - r * 2.7, GOLD); box(d, cx - 12, GL - hh - r * 2.7 - 28, cx + 12, GL - hh - r * 2.7 - 24, GOLD)
                arch(d, cx - 14, 28, 110, (60, 50, 60)); d.ellipse([cx - r * .9, GL - hh - r * 1.9, cx - r * .2, GL - hh - r * 1.5], fill=SN + (255,))
            x += 620
        else:
            for px in (x, x + 110, x + 210):
                s = rnd.randrange(240, 360)
                box(d, px + 30, GL - 40, px + 44, GL, (90, 60, 40))
                for t in range(4): tri(d, [(px - 20 + t * 8, GL - 40 - t * s / 5), (px + 37, GL - 40 - (t + 1.8) * s / 5), (px + 94 - t * 8, GL - 40 - t * s / 5)], (36, 100 + t * 6, 66)); tri(d, [(px + 10 + t * 6, GL - 40 - (t + .9) * s / 5), (px + 37, GL - 40 - (t + 1.8) * s / 5), (px + 64 - t * 6, GL - 40 - (t + .9) * s / 5)], SN)
            x += 340

def mid_delhi(d, rnd):
    RS, RD2, WH, DKc = (176, 66, 46), (140, 46, 32), (244, 238, 226), (70, 22, 14)
    box(d, 0, GL - 300, W, GL, RS); box(d, 0, GL - 300, W, GL - 280, WH); box(d, 0, GL - 180, W, GL - 172, RD2)
    for x in range(0, W, 40): dome(d, x + 2, GL - 330, x + 38, GL - 270, RS)
    for x in range(40, W, 150): arch(d, x, 60, 150, RD2); arch(d, x + 10, 40, 130, DKc)
    def chhatri(cx, base, s=1.0):
        box(d, cx - 44 * s, base - 70 * s, cx - 36 * s, base, RS); box(d, cx + 36 * s, base - 70 * s, cx + 44 * s, base, RS); box(d, cx - 56 * s, base - 82 * s, cx + 56 * s, base - 70 * s, WH)
        dome(d, cx - 44 * s, base - 150 * s, cx + 44 * s, base - 14 * s, WH); box(d, cx - 2, base - 180 * s, cx + 2, base - 148 * s, GOLD)
    x = 250
    while x < W - 700:
        k = rnd.random()
        if k < 0.5:   # great gate
            box(d, x, GL - 560, x + 480, GL, RS); box(d, x, GL - 560, x + 480, GL - 540, WH); box(d, x + 40, GL - 500, x + 440, GL - 60, lt(RS, .1))
            arch(d, x + 150, 180, 440, DKc); d.arc([x + 138, GL - 452, x + 342, GL - 248], 180, 360, fill=WH + (255,), width=10)
            for sx in (x + 60, x + 360): arch(d, sx, 60, 200, DKc); arch(d, sx, 60, 380, DKc) if False else box(d, sx, GL - 420, sx + 60, GL - 320, DKc)
            for cx in (x + 20, x + 240, x + 460): chhatri(cx, GL - 560, 1.0 if cx != x + 240 else 1.3)
            for tx in (x - 40, x + 470): box(d, tx, GL - 640, tx + 50, GL, RD2); chhatri(tx + 25, GL - 640, 0.7)
            x += 760
        elif k < 0.8:  # white marble domes
            box(d, x, GL - 380, x + 420, GL, WH)
            for cx, r in ((x + 80, 70), (x + 210, 110), (x + 340, 70)):
                for j in range(-r, r + 1):
                    w = math.sqrt(r * r - j * j); w = max(w, r * .6) if j > r * .4 else w
                    d.line([(cx - w, GL - 380 - r + j), (cx + w, GL - 380 - r + j)], fill=WH + (255,))
                tri(d, [(cx - r * .3, GL - 380 - r * 1.9), (cx, GL - 380 - r * 2.5), (cx + r * .3, GL - 380 - r * 1.9)], WH); box(d, cx - 2, GL - 380 - r * 2.5 - 30, cx + 2, GL - 380 - r * 2.5, GOLD)
                d.arc([cx - r, GL - 380 - 2 * r, cx + r, GL - 380], 300, 350, fill=(210, 200, 186, 255), width=14)
            for i in range(5): arch(d, x + 24 + i * 80, 52, 220, (150, 60, 44))
            for tx in (x - 30, x + 420): box(d, tx, GL - 600, tx + 30, GL, WH); chhatri(tx + 15, GL - 600, 0.5)
            x += 560
        else:
            for px in (x, x + 150):
                s = rnd.randrange(240, 330); box(d, px + 50, GL - s * .5, px + 66, GL, (96, 62, 36))
                for dx, dy, r in ((0, 0, 1), (-.5, .2, .8), (.5, .2, .8), (0, -.35, .7)): d.ellipse([px + 58 + dx * s * .4 - r * s * .28, GL - s * .75 + dy * s * .4 - r * s * .26, px + 58 + dx * s * .4 + r * s * .28, GL - s * .75 + dy * s * .4 + r * s * .26], fill=(46, 120, 70, 255))
            x += 330

def mid_beijing(d, rnd):
    RED, RF, GRN, GD, WH, DKc = (190, 30, 40), (150, 20, 30), (40, 110, 92), (232, 186, 60), (236, 230, 216), (50, 20, 20)
    def roof(cx, y, w, col=GRN, t=26):
        tri(d, [(cx - w / 2 - 34, y), (cx - w / 2 + 10, y - t), (cx + w / 2 - 10, y - t), (cx + w / 2 + 34, y)], col); tri(d, [(cx - w / 2 - 34, y), (cx - w / 2 - 50, y - 16), (cx - w / 2 - 10, y - 8)], col); tri(d, [(cx + w / 2 + 34, y), (cx + w / 2 + 50, y - 16), (cx + w / 2 + 10, y - 8)], col)
        box(d, cx - w / 2 - 34, y, cx + w / 2 + 34, y + 8, GD)
        for rx in range(int(cx - w / 2), int(cx + w / 2), 14): d.line([(rx, y - t + 2), (rx - (cx - rx) * .12, y)], fill=dk(col, .75) + (255,), width=3)
    x = 120
    while x < W - 560:
        k = rnd.random()
        if k < 0.35:   # pagoda
            n = rnd.choice([4, 5, 6]); cx = x + 150; y = GL
            box(d, cx - 130, GL - 40, cx + 130, GL, WH)
            for i in range(n):
                w = 220 - i * 30; hh = 84 - i * 4; y -= hh if i else 40 + hh
                box(d, cx - w / 2 + 14, y, cx + w / 2 - 14, y + hh, RED); box(d, cx - w / 2 + 14, y + hh - 12, cx + w / 2 - 14, y + hh, RF)
                for wx in range(int(cx - w / 2 + 30), int(cx + w / 2 - 40), 36): box(d, wx, y + 22, wx + 20, y + hh - 22, GD if (wx // 36) % 2 else DKc)
                roof(cx, y, w - 28)
            box(d, cx - 3, y - 90, cx + 3, y - 24, GD); d.ellipse([cx - 9, y - 70, cx + 9, y - 52], fill=GD + (255,))
            x += 420
        elif k < 0.75:  # hall / gate
            w, hh = rnd.randrange(380, 520), rnd.randrange(240, 320); cx = x + w / 2
            box(d, x, GL - 90, x + w, GL, WH); box(d, x + 20, GL - hh, x + w - 20, GL - 90, RED)
            for px in range(x + 30, x + w - 30, 64): box(d, px, GL - hh, px + 14, GL - 90, RF)
            for px in range(x + 60, x + w - 80, 128): arch(d, px, 50, 190, DKc)
            box(d, x + 20, GL - hh - 30, x + w - 20, GL - hh, (40, 80, 150)); wins(d, x + 30, GL - hh - 24, x + w - 30, GL - hh, GD, 22, 40, 10, 12, rnd, 1)
            roof(cx, GL - hh - 30, w - 60, GD, 60); roof(cx, GL - hh - 110, w - 220, GD, 50); box(d, cx - (w - 240) / 2, GL - hh - 110, cx + (w - 240) / 2, GL - hh - 86, RED)
            x += w + 80
        else:
            for bx in range(x, x + 220, 26):   # bamboo
                s = rnd.randrange(300, 520)
                for j in range(0, s, 44): box(d, bx, GL - j - 42, bx + 9, GL - j, (70, 150, 80)); box(d, bx - 1, GL - j - 44, bx + 10, GL - j - 41, (40, 104, 56))
                for j in range(3): tri(d, [(bx + 4, GL - s + j * 40), (bx + 50, GL - s - 20 + j * 40), (bx + 30, GL - s + 10 + j * 40)], (84, 170, 90))
            x += 260
    for lx in range(100, W, 330):   # lantern strings
        d.line([(lx, GL - 430), (lx + 330, GL - 430)], fill=(60, 30, 30, 255), width=3)
        for j in range(1, 4): xx = lx + j * 82; box(d, xx - 1, GL - 430, xx + 1, GL - 414, (60, 30, 30)); d.ellipse([xx - 15, GL - 416, xx + 15, GL - 376], fill=(220, 40, 40, 255)); box(d, xx - 8, GL - 418, xx + 8, GL - 412, GD); box(d, xx - 2, GL - 378, xx + 2, GL - 360, GD)

def mid_nyc(d, rnd):
    x = 0; Y, B = (255, 206, 96), (150, 210, 255)
    while x < W - 120:
        k = rnd.random()
        if k < 0.6:   # tower
            bw, bh = rnd.randrange(170, 300), rnd.randrange(480, 860); c = rnd.choice([(52, 62, 96), (66, 74, 112), (44, 52, 84), (80, 76, 110)])
            box(d, x, GL - bh, x + bw, GL, c); box(d, x, GL - bh, x + 14, GL, lt(c, .15))
            if rnd.random() < .5: box(d, x + bw * .25, GL - bh - 60, x + bw * .75, GL - bh, c); box(d, x + bw * .5 - 3, GL - bh - 150, x + bw * .5 + 3, GL - bh - 60, (120, 126, 150))
            wins(d, x + 20, GL - bh + 24, x + bw - 10, GL - 120, rnd.choice([Y, Y, B]), 30, 44, 16, 24, rnd, .62)
            box(d, x + 10, GL - 96, x + bw - 10, GL, dk(c, .7)); box(d, x + 24, GL - 80, x + bw - 24, GL - 20, Y)
            if rnd.random() < .45:   # rooftop water tank
                tx = x + rnd.randrange(20, max(21, bw - 90))
                for lx in (tx + 6, tx + 54): box(d, lx, GL - bh - 40, lx + 5, GL - bh, (60, 44, 34))
                box(d, tx, GL - bh - 100, tx + 66, GL - bh - 40, (120, 80, 52)); tri(d, [(tx - 6, GL - bh - 100), (tx + 33, GL - bh - 136), (tx + 72, GL - bh - 100)], (90, 60, 40))
            x += bw + rnd.randrange(0, 24)
        else:   # brownstone with fire escape
            bw, bh = rnd.randrange(240, 320), rnd.randrange(330, 440); c = rnd.choice([(150, 78, 58), (124, 66, 52), (170, 100, 70)])
            box(d, x, GL - bh, x + bw, GL, c); box(d, x - 6, GL - bh - 16, x + bw + 6, GL - bh, dk(c, .7))
            for fy in range(GL - bh + 40, GL - 130, 96):
                for wx in range(x + 24, x + bw - 50, 70): box(d, wx, fy, wx + 40, fy + 58, (255, 220, 130) if rnd.random() < .6 else (40, 44, 66)); box(d, wx - 4, fy + 58, wx + 44, fy + 64, lt(c, .4))
                box(d, x + 14, fy + 70, x + bw - 14, fy + 76, (30, 30, 34))
                for rx in range(x + 14, x + bw - 14, 14): d.line([(rx, fy + 48), (rx, fy + 70)], fill=(30, 30, 34, 255), width=2)
                d.line([(x + 30, fy + 76), (x + 90, fy + 166)], fill=(30, 30, 34, 255), width=4)
            box(d, x + bw / 2 - 30, GL - 110, x + bw / 2 + 30, GL, (40, 26, 22)); box(d, x + 20, GL - 130, x + 110, GL - 96, (200, 40, 50)); box(d, x + 150, GL - 126, x + bw - 20, GL - 40, (255, 232, 170))
            x += bw + rnd.randrange(0, 20)

# ---------------- items ----------------
def items(S, n):
    def new(): return canvas(128, 128)
    def out(im, name): save(im, os.path.join(S, name), 128, 128)
    im, d = new()
    for col, o in (((120, 16, 24), 0), ((226, 40, 52), 5)): E(d, 12 + o, 16 + o, 58 - 2 * o, 58 - 2 * o, col); E(d, 58 + o, 16 + o, 58 - 2 * o, 58 - 2 * o, col); P(d, [(14 + o, 56), (114 - o, 56), (64, 116 - o)], col)
    E(d, 28, 30, 20, 16, (255, 170, 170)); star(d, 64, 62, 22, GOLD, 5, .45); out(im, 'item_life.png')
    if n == 3:   # Cairo: baladi bread / nabboot staff / gold scarab
        im, d = new(); E(d, 8, 30, 112, 76, (150, 96, 44)); E(d, 12, 32, 104, 66, (214, 164, 96)); E(d, 28, 40, 60, 30, (236, 200, 140))
        for x, y in ((40, 70), (70, 62), (88, 80), (56, 84)): E(d, x, y, 10, 7, (150, 96, 44))
        out(im, 'item_grow.png')
        for name in ('item_weapon.png', 'shot.png'):
            im, d = new(); P(d, [(14, 100), (26, 112), (112, 26), (100, 14)], (84, 48, 20)); P(d, [(18, 100), (24, 106), (106, 24), (100, 18)], (150, 96, 46)); E(d, 92, 8, 28, 28, (84, 48, 20)); R(d, 40, 76, 14, 6, GOLD); R(d, 70, 46, 14, 6, GOLD); out(im, name)
        im, d = new(); E(d, 22, 30, 84, 90, GOLD_D); E(d, 26, 32, 76, 82, GOLD); R(d, 62, 40, 4, 72, GOLD_D); E(d, 40, 10, 48, 36, (30, 110, 200)); E(d, 46, 14, 20, 12, (120, 190, 240))
        for y in (50, 70, 90): R(d, 8, y, 20, 6, GOLD_D, 3); R(d, 100, y, 20, 6, GOLD_D, 3)
        out(im, 'item_star.png')
    elif n == 4:   # Moscow: matryoshka / snowball / red-gold star
        im, d = new(); E(d, 36, 6, 56, 56, (200, 40, 50)); E(d, 20, 40, 88, 84, (200, 40, 50)); E(d, 46, 16, 36, 36, (250, 220, 190)); E(d, 54, 28, 6, 8, (30, 30, 30)); E(d, 68, 28, 6, 8, (30, 30, 30)); E(d, 36, 60, 56, 54, (250, 220, 120)); star(d, 64, 86, 18, (200, 40, 50), 6, .5); out(im, 'item_grow.png')
        for name in ('item_weapon.png', 'shot.png'):
            im, d = new(); E(d, 14, 14, 100, 100, (190, 210, 235)); E(d, 16, 14, 94, 92, (255, 255, 255)); E(d, 34, 28, 30, 20, (230, 242, 255)); E(d, 70, 74, 20, 14, (214, 228, 246)); out(im, name)
        im, d = new(); star(d, 64, 68, 58, GOLD_D, 5, .42); star(d, 64, 64, 56, GOLD, 5, .42); star(d, 64, 64, 40, (210, 36, 40), 5, .42); E(d, 54, 54, 8, 12, (255, 255, 255)); out(im, 'item_star.png')
    elif n == 5:   # Delhi: samosa / chakram disc / lotus
        im, d = new(); P(d, [(64, 10), (120, 110), (8, 110)], (150, 90, 30)); P(d, [(64, 22), (108, 104), (20, 104)], (222, 160, 70)); P(d, [(64, 34), (84, 74), (50, 70)], (244, 200, 120)); out(im, 'item_grow.png')
        for name in ('item_weapon.png', 'shot.png'):
            im, d = new(); E(d, 8, 8, 112, 112, (120, 126, 140)); E(d, 14, 14, 100, 100, (214, 220, 232)); E(d, 34, 34, 60, 60, (0, 0, 0, 0)); d.ellipse([34 * SS, 34 * SS, 94 * SS, 94 * SS], fill=(0, 0, 0, 0), outline=(120, 126, 140, 255), width=5 * SS)
            for a in range(8): an = a * math.pi / 4; P(d, [(64 + 52 * math.cos(an - .12), 64 + 52 * math.sin(an - .12)), (64 + 62 * math.cos(an), 64 + 62 * math.sin(an)), (64 + 52 * math.cos(an + .12), 64 + 52 * math.sin(an + .12))], (120, 126, 140))
            out(im, name)
        im, d = new()
        for a, col in ((-60, (236, 110, 160)), (60, (236, 110, 160)), (-30, (246, 150, 190)), (30, (246, 150, 190)), (0, (255, 190, 214))):
            an = math.radians(a - 90); cx, cy = 64 + 34 * math.cos(an), 80 + 34 * math.sin(an); P(d, [(64, 96), (cx - 16 * math.sin(an), cy + 16 * math.cos(an)), (64 + 70 * math.cos(an), 80 + 70 * math.sin(an)), (cx + 16 * math.sin(an), cy - 16 * math.cos(an))], col)
        E(d, 30, 92, 68, 22, (60, 150, 90)); E(d, 54, 70, 20, 20, GOLD); out(im, 'item_star.png')
    elif n == 6:   # Beijing: bao bun / firecracker / jade coin
        im, d = new(); E(d, 10, 30, 108, 86, (220, 210, 196)); E(d, 14, 30, 100, 78, (252, 248, 240))
        for a in range(-60, 61, 24): an = math.radians(a - 90); d.line([(64 * SS, 34 * SS), ((64 + 40 * math.cos(an)) * SS, (60 + 30 * math.sin(an) + 30) * SS)], fill=(214, 204, 190, 255), width=4 * SS)
        E(d, 56, 24, 16, 14, (236, 228, 214)); out(im, 'item_grow.png')
        for name in ('item_weapon.png', 'shot.png'):
            im, d = new(); P(d, [(30, 96), (50, 116), (104, 62), (84, 42)], (200, 30, 40)); P(d, [(34, 96), (42, 104), (96, 50), (88, 42)], (240, 80, 80)); R(d, 40, 86, 30, 6, GOLD); P(d, [(90, 46), (98, 54), (104, 48), (96, 40)], GOLD)
            d.line([(98 * SS, 44 * SS), (110 * SS, 26 * SS), (104 * SS, 16 * SS)], fill=(90, 70, 50, 255), width=4 * SS); star(d, 104, 14, 12, (255, 220, 80), 6, .4); out(im, name)
        im, d = new(); E(d, 10, 10, 108, 108, (20, 110, 80)); E(d, 14, 14, 100, 100, (60, 180, 130)); E(d, 22, 20, 44, 30, (150, 226, 190)); R(d, 46, 46, 36, 36, (20, 110, 80)); R(d, 52, 52, 24, 24, (0, 0, 0, 0)); d.rectangle([52 * SS, 52 * SS, 76 * SS, 76 * SS], fill=(0, 0, 0, 0)); R(d, 58, 0, 12, 14, (200, 30, 40), 3); out(im, 'item_star.png')
    elif n == 7:   # New York: pizza slice / baseball / gold badge star
        im, d = new(); P(d, [(8, 22), (120, 22), (64, 124)], (200, 130, 50)); P(d, [(18, 34), (110, 34), (64, 116)], (250, 200, 80))
        for x, y in ((46, 50), (76, 48), (62, 78), (52, 64)): E(d, x, y, 18, 18, (200, 40, 40))
        R(d, 6, 14, 116, 18, (176, 110, 40), 9); out(im, 'item_grow.png')
        for name in ('item_weapon.png', 'shot.png'):
            im, d = new(); E(d, 10, 10, 108, 108, (190, 190, 190)); E(d, 14, 12, 100, 100, (252, 250, 244))
            for sx, a0, a1 in ((-50, -50, 50), (114, 130, 230)): d.arc([sx * SS, 6 * SS, (sx + 64) * SS, 122 * SS], a0, a1, fill=(200, 40, 40, 255), width=4 * SS)
            out(im, name)
        im, d = new(); E(d, 6, 6, 116, 116, (30, 60, 130)); E(d, 12, 12, 104, 104, (50, 100, 190)); star(d, 64, 66, 46, GOLD_D, 5, .42); star(d, 64, 64, 44, GOLD, 5, .42); star(d, 64, 64, 22, GOLD_L, 5, .42); out(im, 'item_star.png')

def goal(S, c):
    im, d = canvas(640, 640); w, a, k = c['goal'], c['gacc'], c['gk']
    R(d, 40, 250, 560, 390, w); R(d, 40, 250, 560, 20, lt(w, .35)); R(d, 40, 270, 560, 22, a)
    for x in (40, 520): R(d, x, 150, 80, 110, dk(w, .9))
    if k == 'onion':
        for cx, r, col in ((80, 44, (58, 107, 192)), (320, 96, GOLD), (560, 44, (40, 140, 84))):
            base = 150 if cx != 320 else 250
            for j in range(-r, r + 1):
                ww = math.sqrt(r * r - j * j); ww = max(ww, r * .55) if j > r * .45 else ww
                ww = max(ww, 1.5); R(d, cx - ww, base - r + j, 2 * ww, 1.5, col)
            P(d, [(cx - r * .5, base - r * 1.75), (cx, base - r * 2.6), (cx + r * .5, base - r * 1.75)], col)
    elif k == 'pagoda':
        for i, (y, ww) in enumerate(((250, 600), (150, 420), (70, 260))):
            P(d, [(320 - ww / 2 - 20, y), (320 - ww / 2 + 30, y - 46), (320 + ww / 2 - 30, y - 46), (320 + ww / 2 + 20, y)], c['roof']); R(d, 320 - ww / 2 - 20, y, ww + 40, 10, GOLD)
            if i: R(d, 320 - ww / 2 + 50, y + 10, ww - 100, 100 if i == 1 else 80, w)
    elif k == 'flat':
        R(d, 120, 60, 400, 200, dk(w, .85)); R(d, 110, 44, 420, 22, lt(w, .3))
        for x in range(150, 500, 60):
            for y in range(84, 230, 50): R(d, x, y, 30, 34, (255, 220, 130))
        R(d, 300, 0, 8, 50, (150, 150, 160))
    else:
        for x in (40, 520): d.pieslice([x * SS, 100 * SS, (x + 80) * SS, 200 * SS], 180, 360, fill=a); R(d, x + 37, 76, 6, 30, GOLD)
        d.pieslice([200 * SS, 60 * SS, 440 * SS, 440 * SS], 180, 360, fill=c.get('dome', a)); R(d, 316, 20, 8, 50, GOLD); E(d, 308, 12, 24, 24, GOLD)
    R(d, 230, 400, 180, 240, (36, 22, 12)); d.pieslice([230 * SS, 310 * SS, 410 * SS, 490 * SS], 180, 360, fill=(36, 22, 12)); d.arc([222 * SS, 302 * SS, 418 * SS, 498 * SS], 180, 360, fill=a, width=8 * SS)
    for x in (90, 480): R(d, x, 360, 70, 120, (36, 22, 12), 30)
    save(im, os.path.join(S, 'goal.png'), 640, 640)

def far_sil(kind):
    def f(d, rnd):
        if kind == 'pyramids':
            for cx, h, c in ((900, 330, (196, 140, 70)), (1500, 430, (210, 152, 80)), (2050, 260, (184, 128, 64)), (3300, 380, (204, 146, 76))):
                d.polygon([(cx - h * 1.2, 900), (cx, 900 - h), (cx + h * 1.2, 900)], fill=c + (255,)); d.polygon([(cx, 900 - h), (cx + h * 1.2, 900), (cx + h * .25, 900)], fill=dk(c, .82) + (255,))
            d.rectangle([0, 880, 3840, H], fill=(206, 160, 100, 255))
        elif kind == 'hills':
            for col, base, amp, f2 in (((150, 196, 180), 760, 170, 3), ((110, 168, 150), 850, 130, 5)):
                pts = [(0, H)] + [(x, base - amp * (0.5 + 0.5 * math.sin(x * 2 * math.pi / 3840 * f2 + f2))) for x in range(0, 3841, 40)] + [(3840, H)]; d.polygon(pts, fill=col + (255,))
                if f2 == 3:   # great wall along the ridge
                    for x in range(0, 3840, 30):
                        y = base - amp * (0.5 + 0.5 * math.sin(x * 2 * math.pi / 3840 * f2 + f2)); d.rectangle([x, y - 26, x + 30, y - 4], fill=(150, 160, 170, 255)); d.rectangle([x, y - 36, x + 12, y - 26], fill=(150, 160, 170, 255))
                        if x % 480 == 0: d.rectangle([x - 16, y - 76, x + 40, y - 20], fill=(130, 140, 152, 255))
        else:
            cols = {'city': ((60, 62, 104), (44, 46, 84)), 'snow': ((150, 170, 200), (120, 142, 178)), 'warm': ((226, 150, 140), (204, 120, 116))}[kind]
            for col, base in zip(cols, (790, 850)):
                x = 0
                while x < 3840:
                    bw, bh = rnd.randrange(80, 200), rnd.randrange(60, 260 if kind == 'city' else 150); d.rectangle([x, base - bh, x + bw, H], fill=col + (255,))
                    if kind != 'city' and rnd.random() < .35: d.pieslice([x + bw * .15, base - bh - bw * .35, x + bw * .85, base - bh + bw * .35], 180, 360, fill=col + (255,))
                    if kind == 'city': wins(d, x + 8, base - bh + 10, x + bw - 6, base, (250, 214, 130), 18, 24, 6, 10, rnd, .3)
                    x += bw
    return f

CITIES = {
 3: dict(g=(214, 176, 118), gtop=(240, 214, 160), gacc=(176, 96, 60), gstyle='stone', br=(196, 140, 80), box=(132, 78, 36), blk=(206, 170, 116), blk2=(150, 96, 60), pipe=(196, 150, 96), n=8,
         e_kind='cat', e_body=(130, 126, 120), e_face=(236, 226, 210), fish=(230, 140, 60), goal=(214, 178, 124), gk='dome', dome=(232, 210, 160),
         sky=[(0, (30, 28, 78)), (.45, (84, 62, 122)), (.8, (196, 110, 120)), (1, (240, 170, 120))], sun=(700, 250, 70, (255, 246, 214)), sil='pyramids', stars=260, mid=mid_cairo, haze=((120, 90, 130), .22),
         hero=dict(hat='tarboosh', hatc=(180, 34, 30), top=(140, 168, 184), hem=2, legs=(140, 168, 184), shoes=(96, 60, 30), collar=(244, 240, 230), stripes=(112, 140, 158))),
 4: dict(g=(124, 133, 144), gtop=(250, 252, 255), gacc=(166, 44, 34), gstyle='snow', br=(166, 44, 34), box=(40, 110, 70), blk=(150, 160, 172), blk2=(60, 100, 170), pipe=(170, 50, 40), n=6,
         e_kind='bear', e_body=(120, 80, 50), e_face=(220, 190, 150), fish=(110, 150, 190), goal=(240, 236, 228), gk='onion',
         sky=[(0, (110, 140, 190)), (.6, (170, 196, 226)), (1, (226, 236, 246))], sun=(3000, 260, 60, (255, 255, 240)), sil='snow', stars=0, mid=mid_moscow, haze=((200, 214, 232), .26), band=(900, (236, 242, 250), (255, 255, 255)),
         hero=dict(hat='ushanka', hatc=(110, 76, 46), top=(60, 76, 106), hem=1, legs=(34, 40, 58), shoes=(24, 24, 28), collar=(190, 160, 120), buttons=GOLD, cuff=(190, 160, 120))),
 5: dict(g=(176, 66, 46), gtop=(244, 238, 226), gacc=(42, 143, 122), gstyle='brick', br=(224, 123, 26), box=(150, 40, 60), blk=(244, 238, 226), blk2=(176, 66, 46), pipe=(244, 238, 226), n=8,
         e_kind='monkey', e_body=(140, 96, 60), e_face=(226, 190, 150), fish=(250, 170, 60), goal=(176, 66, 46), gk='dome', dome=(244, 238, 226),
         sky=[(0, (240, 120, 150)), (.5, (248, 170, 180)), (1, (254, 220, 196))], sun=(1900, 420, 90, (255, 244, 220)), sil='warm', stars=0, mid=mid_delhi, haze=((250, 196, 190), .26),
         hero=dict(hat='pagri', hatc=(224, 123, 26), top=(243, 230, 200), hem=1, legs=(246, 242, 232), shoes=(138, 90, 29), sash=(42, 143, 122), buttons=GOLD)),
 6: dict(g=(127, 143, 160), gtop=(176, 188, 200), gacc=(200, 16, 46), gstyle='stone', br=(200, 16, 46), box=(160, 20, 36), blk=(127, 143, 160), blk2=(47, 111, 94), pipe=(60, 150, 90), n=4,
         e_kind='panda', e_body=(246, 246, 246), e_face=(252, 252, 252), fish=(240, 110, 60), goal=(190, 30, 40), gk='pagoda', roof=(40, 110, 92),
         sky=[(0, (130, 196, 190)), (.6, (190, 226, 214)), (1, (232, 244, 232))], sun=(2600, 300, 70, (255, 250, 230)), sil='hills', stars=0, mid=mid_beijing, haze=((200, 228, 216), .26),
         hero=dict(hat='douli', hatc=(214, 180, 104), top=(200, 16, 46), hem=0, legs=(24, 24, 24), shoes=(20, 20, 20), buttons=GOLD, frog=True, cuff=GOLD)),
 7: dict(g=(64, 68, 78), gtop=(160, 166, 176), gacc=(242, 182, 50), gstyle='asphalt', br=(224, 78, 57), box=(40, 70, 140), blk=(110, 116, 130), blk2=(58, 68, 102), pipe=(224, 78, 57), n=5,
         e_kind='rat', e_body=(110, 108, 116), e_face=(196, 190, 196), fish=(120, 170, 150), goal=(90, 96, 124), gk='flat',
         sky=[(0, (22, 28, 60)), (.5, (62, 54, 104)), (.85, (176, 88, 122)), (1, (240, 150, 110))], sun=(3200, 220, 54, (255, 250, 230)), sil='city', stars=220, mid=mid_nyc, haze=((70, 60, 110), .30),
         hero=dict(hat='capback', hatc=(224, 78, 57), top=(31, 58, 110), hem=0, legs=(48, 52, 63), shoes=(244, 244, 244), open=(244, 240, 232), cuff=(255, 255, 255), belt=(242, 182, 50))),
}
if __name__ == '__main__':
    only = [int(a) for a in sys.argv[1:]] or list(CITIES)
    for n in only:
        c = CITIES[n]; S = os.path.join(g.OUT, f'stage{n}'); os.makedirs(S, exist_ok=True); g.S1 = S
        tiles(S, c); critter(S, c); hero(n, c['hero']); items(S, n); goal(S, c); g.coin(); g.flag()
        sky(S, c['sky'], c['sun'], far_sil(c['sil']), c.get('band'), c['stars'], n)
        im = Image.new('RGBA', (W, H)); c['mid'](ImageDraw.Draw(im), random.Random(n * 7)); haze(im, *c['haze']).save(os.path.join(S, 'bg_mid.png')); print('stage', n, 'done')
    # the water enemy for stages 1 and 2 as well
    for n, fc in ((1, (240, 150, 60)), (2, (120, 170, 150))):
        S = os.path.join(g.OUT, f'stage{n}'); im, d = canvas(384, 128)
        for i in range(3):
            ox = i * 128; t = (0, 10, 0)[i]
            P(d, [(28, 64), (4, 34 + t), (4, 94 - t)], dk(fc, .75), ox); E(d, 20, 34, 96, 60, fc, ox); E(d, 36, 60, 70, 30, lt(fc, .4), ox); P(d, [(50, 38), (70, 14), (86, 38)], dk(fc, .75), ox)
            if i < 2: E(d, 86, 46, 18, 18, (255, 255, 255), ox); E(d, 93, 50, 9, 10, (20, 20, 20), ox)
            else: R(d, 86, 52, 16, 4, (20, 20, 20), 0, ox)
        save(im, os.path.join(S, 'enemy_water.png'), 384, 128)
