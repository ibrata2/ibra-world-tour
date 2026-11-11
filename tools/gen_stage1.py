"""Generates the default (placeholder) art for stage 1. Every file can be replaced by a hand-made design of the same size."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), '..', 'app', 'assets')
S1 = os.path.join(OUT, 'stage1'); HERO = os.path.join(OUT, 'hero')
os.makedirs(S1, exist_ok=True); os.makedirs(HERO, exist_ok=True)
SS = 2  # supersampling
GOLD = (212, 175, 55); GOLD_D = (143, 117, 36); GOLD_L = (255, 232, 140)

def canvas(w, h, bg=(0, 0, 0, 0)):
    im = Image.new('RGBA', (w * SS, h * SS), bg)
    return im, ImageDraw.Draw(im)

def save(im, path, w, h):
    im.resize((w, h), Image.LANCZOS).save(path)
    print('wrote', os.path.relpath(path, OUT), w, h)

def R(d, x, y, w, h, c, r=0, ox=0, oy=0):
    b = [(ox + x) * SS, (oy + y) * SS, (ox + x + w) * SS - 1, (oy + y + h) * SS - 1]
    if r: d.rounded_rectangle(b, r * SS, fill=c)
    else: d.rectangle(b, fill=c)

def E(d, x, y, w, h, c, ox=0, oy=0):
    d.ellipse([(ox + x) * SS, (oy + y) * SS, (ox + x + w) * SS - 1, (oy + y + h) * SS - 1], fill=c)

def P(d, pts, c, ox=0, oy=0):
    d.polygon([((ox + x) * SS, (oy + y) * SS) for x, y in pts], fill=c)

def noise(im, amt=10, seed=1):
    rnd = random.Random(seed); px = im.load(); w, h = im.size
    for _ in range(w * h // 6):
        x, y = rnd.randrange(w), rnd.randrange(h); r, g, b, a = px[x, y]
        if a:
            k = rnd.randint(-amt, amt); px[x, y] = (max(0, min(255, r + k)), max(0, min(255, g + k)), max(0, min(255, b + k)), a)

# ---------- tiles (128x128) ----------
def ground(top):
    im, d = canvas(128, 128, (139, 90, 43, 255))
    rnd = random.Random(7 if top else 9)
    for _ in range(26):
        x, y, s = rnd.randrange(128), rnd.randrange(30 if top else 0, 128), rnd.randrange(6, 16)
        E(d, x, y, s, s * 0.7, rnd.choice([(120, 76, 34), (156, 104, 54), (104, 66, 30)]))
    if top:
        R(d, 0, 0, 128, 30, (62, 158, 74))
        R(d, 0, 0, 128, 10, (104, 200, 96))
        for x in range(0, 128, 16):
            P(d, [(x, 30), (x + 8, 44), (x + 16, 30)], (62, 158, 74))
        R(d, 0, 28, 128, 3, (40, 116, 54))
    noise(im, 8)
    save(im, os.path.join(S1, 'ground_top.png' if top else 'ground_fill.png'), 128, 128)

def brick():
    im, d = canvas(128, 128, (92, 34, 22, 255))
    for row in range(4):
        off = 0 if row % 2 == 0 else -32
        for col in range(3):
            x = off + col * 64; y = row * 32
            R(d, x + 2, y + 2, 60, 28, (192, 70, 48), 3)
            R(d, x + 4, y + 3, 56, 6, (226, 104, 76), 2)
            R(d, x + 4, y + 23, 56, 5, (150, 50, 34), 2)
    noise(im, 8)
    save(im, os.path.join(S1, 'brick.png'), 128, 128)

def box(used):
    base, lt, dk = ((120, 96, 70), (150, 124, 94), (84, 66, 48)) if used else (GOLD, GOLD_L, GOLD_D)
    im, d = canvas(128, 128, dk + (255,))
    R(d, 4, 4, 120, 120, base, 10)
    R(d, 8, 8, 112, 14, lt, 6)
    R(d, 8, 108, 112, 12, dk, 6)
    for x, y in [(14, 14), (106, 14), (14, 106), (106, 106)]:
        E(d, x, y, 9, 9, dk)
    if not used:
        # star emblem instead of a question mark
        cx, cy, pts = 64, 66, []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5; r = 34 if i % 2 == 0 else 14
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        P(d, [(x + 3, y + 3) for x, y in pts], dk); P(d, pts, (255, 250, 220))
    noise(im, 6)
    save(im, os.path.join(S1, 'box_used.png' if used else 'box.png'), 128, 128)

def block():
    im, d = canvas(128, 128, (88, 78, 70, 255))
    R(d, 4, 4, 120, 120, (150, 138, 124), 8)
    P(d, [(4, 4), (124, 4), (104, 24), (24, 24)], (190, 178, 162))
    P(d, [(4, 124), (124, 124), (104, 104), (24, 104)], (108, 98, 88))
    R(d, 24, 24, 80, 80, (160, 148, 134))
    noise(im, 10)
    save(im, os.path.join(S1, 'block.png'), 128, 128)

def pipe():
    for name, top in (('pipe_top.png', True), ('pipe_body.png', False)):
        im, d = canvas(256, 128)
        x0, w = (0, 256) if top else (16, 224)
        R(d, x0, 0, w, 128, (24, 92, 60), 10 if top else 0)
        R(d, x0 + 8, 6 if top else 0, w - 16, 116 if top else 128, (46, 160, 96), 6 if top else 0)
        R(d, x0 + 28, 6 if top else 0, 26, 116 if top else 128, (130, 222, 160))
        R(d, x0 + 62, 6 if top else 0, 10, 116 if top else 128, (92, 196, 130))
        R(d, x0 + w - 60, 6 if top else 0, 40, 116 if top else 128, (30, 122, 74))
        if top: R(d, 8, 104, 240, 16, (24, 92, 60))
        save(im, os.path.join(S1, name), 256, 128)

def coin():
    im, d = canvas(512, 128)
    for i, wf in enumerate([1, 0.7, 0.25, 0.7]):
        cx = i * 128 + 64; w = 84 * wf
        E(d, cx - w / 2, 18, w, 92, GOLD_D); E(d, cx - w / 2 + 3 * wf, 18, w - 6 * wf, 86, GOLD)
        if wf > 0.5:
            E(d, cx - w / 2 + 14 * wf, 30, w - 28 * wf, 62, GOLD_L); E(d, cx - w / 2 + 20 * wf, 36, w - 40 * wf, 50, GOLD)
    save(im, os.path.join(S1, 'coin.png'), 512, 128)

def enemy():
    # hedgehog: walk1, walk2, squashed
    im, d = canvas(384, 128)
    for i in range(3):
        ox = i * 128
        if i == 2:
            E(d, 10, 92, 108, 34, (92, 62, 40), ox); E(d, 76, 100, 38, 24, (232, 196, 150), ox); continue
        for k in range(7):
            a = math.pi * (0.95 - k * 0.13); bx, by = 58 + 40 * math.cos(a), 78 - 34 * math.sin(a)
            P(d, [(bx - 12, by + 10), (bx + 12, by + 10), (bx + 26 * math.cos(a), by - 30 * math.sin(a) - 4)], (64, 42, 28), ox)
        E(d, 12, 40, 96, 78, (104, 70, 44), ox)
        E(d, 66, 62, 52, 52, (232, 196, 150), ox)
        E(d, 108, 82, 14, 12, (40, 26, 20), ox)
        E(d, 86, 72, 14, 16, (255, 255, 255), ox); E(d, 92, 76, 8, 10, (20, 20, 20), ox)
        P(d, [(80, 68), (102, 74), (102, 70), (82, 62)], (40, 26, 20), ox)
        f = 0 if i == 0 else 14
        E(d, 26 + f, 108, 30, 18, (60, 40, 28), ox); E(d, 78 - f, 108, 30, 18, (60, 40, 28), ox)
    save(im, os.path.join(S1, 'enemy1.png'), 384, 128)

def flag():
    im, d = canvas(256, 1152)
    R(d, 118, 40, 20, 1112, (230, 230, 235), 8); R(d, 122, 40, 6, 1112, (255, 255, 255), 3)
    E(d, 104, 0, 48, 48, GOLD); E(d, 114, 8, 16, 16, GOLD_L)
    P(d, [(118, 70), (118, 190), (0, 130)], (26, 26, 26)); P(d, [(108, 96), (108, 164), (40, 130)], GOLD)
    R(d, 64, 1100, 128, 52, (88, 78, 70), 6)
    save(im, os.path.join(S1, 'flag.png'), 256, 1152)

def goal():
    im, d = canvas(640, 640)
    R(d, 60, 240, 520, 400, (178, 90, 60)); R(d, 60, 240, 520, 24, (120, 56, 36))
    for x in range(60, 580, 104): R(d, x, 180, 60, 60, (178, 90, 60))
    R(d, 200, 60, 240, 180, (196, 104, 70))
    for x in range(200, 440, 96): R(d, x, 10, 48, 50, (196, 104, 70))
    R(d, 260, 430, 120, 210, (30, 22, 20)); E(d, 260, 370, 120, 120, (30, 22, 20))
    for x in (120, 440): R(d, x, 330, 70, 90, (30, 22, 20), 30)
    R(d, 290, 110, 60, 80, (30, 22, 20), 26)
    save(im, os.path.join(S1, 'goal.png'), 640, 640)

# ---------- backgrounds ----------
def bg_far():
    w, h = 3840, 1080
    im = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(im)
    top, bot = (64, 150, 240), (190, 232, 255)
    for y in range(h):
        t = y / h; d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,))
    rnd = random.Random(3)
    cl = Image.new('RGBA', (w, h)); cd = ImageDraw.Draw(cl)
    def cloud(cx, cy, s):
        for dx, dy, r in [(-1.3, .1, .7), (-.5, -.35, .95), (.4, -.2, .85), (1.2, .12, .65), (0, .25, 1.0)]:
            cd.ellipse([cx + dx * s - r * s, cy + dy * s - r * s * .7, cx + dx * s + r * s, cy + dy * s + r * s * .7], fill=(255, 255, 255, 235))
        cd.rectangle([cx - 1.9 * s, cy + .25 * s, cx + 1.8 * s, cy + .9 * s], fill=(255, 255, 255, 235))
    for i in range(9):
        cx = i * 430 + rnd.randrange(60, 300)
        cloud(cx, rnd.randrange(110, 480), rnd.randrange(60, 120))
        if cx < 400: cloud(cx + w, 0, 0)
    # far mountains, wrapped so the image tiles
    for layer, (col, base, amp) in enumerate([((140, 190, 232), 800, 150), ((112, 170, 216), 880, 110)]):
        pts = [(0, h)]
        for x in range(0, w + 1, 40):
            y = base - amp * (0.5 + 0.5 * math.sin(x * 2 * math.pi / w * (3 + layer * 2) + layer)) - 30 * math.sin(x * 2 * math.pi / w * 11)
            pts.append((x, y))
        pts.append((w, h)); d.polygon(pts, fill=col + (255,))
    im.alpha_composite(cl.filter(ImageFilter.GaussianBlur(2)))
    im.convert('RGB').save(os.path.join(S1, 'bg_far.jpg'), quality=92); print('wrote stage1/bg_far.jpg', w, h)

def bg_mid():
    w, h = 3840, 1080
    im = Image.new('RGBA', (w * 1, h)); d = ImageDraw.Draw(im)
    rnd = random.Random(5)
    for cx, r, col in [(300, 520, (58, 150, 78)), (1250, 380, (72, 170, 88)), (2100, 600, (58, 150, 78)), (2950, 420, (72, 170, 88)), (3600, 340, (64, 160, 82))]:
        for ox in (-w, 0, w):
            d.ellipse([cx + ox - r, h - r * 0.8, cx + ox + r, h + r * 0.8], fill=col + (255,))
            d.ellipse([cx + ox - r * .55, h - r * .72, cx + ox - r * .05, h - r * .45], fill=(120, 205, 120, 120))
    for i in range(14):
        x = i * 280 + rnd.randrange(0, 160); base = h - rnd.randrange(20, 90); s = rnd.randrange(70, 120)
        d.rectangle([x - s * .09, base - s * .9, x + s * .09, base], fill=(96, 62, 36, 255))
        for k, rr in enumerate([1.0, .8, .6]):
            d.ellipse([x - s * rr * .6, base - s * (1.2 + k * .45) - s * rr * .5, x + s * rr * .6, base - s * (1.2 + k * .45) + s * rr * .5], fill=[(34, 120, 62, 255), (44, 140, 72, 255), (60, 160, 84, 255)][k])
    im.save(os.path.join(S1, 'bg_mid.png')); print('wrote stage1/bg_mid.png', w, h)

# ---------- hero (5 frames 192x256: idle, run1, run2, run3, jump) ----------
SKIN = (217, 160, 102); SKIN_D = (180, 124, 74); BEARD = (43, 29, 20); BLK = (28, 28, 30); BLK_L = (58, 58, 64); JEAN = (47, 74, 122); JEAN_D = (32, 52, 90); SHOE = (240, 240, 240)

def hero_frame(d, ox, pose):
    # leg/arm offsets per pose: (back leg x, back leg lift, front leg x, front leg lift, arm swing)
    bl, blift, fl, flift, arm = {'idle': (72, 0, 100, 0, 0), 'run1': (56, 0, 116, 14, 18), 'run2': (84, 10, 92, 0, 0), 'run3': (116, 14, 56, 0, -18), 'jump': (60, 22, 118, 4, -30)}[pose]
    bob = 4 if pose in ('run2',) else 0
    oy = bob + (-6 if pose == 'jump' else 0)
    # back arm
    R(d, 66 - arm, 124 + oy, 24, 62, BLK_L, 12, ox); E(d, 66 - arm, 172 + oy, 24, 24, SKIN_D, ox)
    # legs
    for lx, lift, col in ((bl, blift, JEAN_D), (fl, flift, JEAN)):
        R(d, lx - 14, 176 + oy, 30, 56 - lift, col, 10, ox)
        R(d, lx - 16, 226 - lift + oy * 0, 46, 24, (60, 60, 66), 10, ox); R(d, lx - 16, 226 - lift, 46, 16, SHOE, 8, ox)
    # torso
    R(d, 58, 112 + oy, 76, 78, BLK, 20, ox); R(d, 58, 150 + oy, 76, 9, GOLD, 0, ox); R(d, 62, 116 + oy, 16, 34, BLK_L, 8, ox)
    # head
    E(d, 56, 34 + oy, 84, 84, SKIN, ox); E(d, 128, 74 + oy, 20, 18, SKIN, ox)
    P(d, [(60, 82 + oy), (140, 86 + oy), (134, 116 + oy), (104, 126 + oy), (72, 116 + oy)], BEARD, ox); E(d, 56, 62 + oy, 22, 46, BEARD, ox)
    R(d, 112, 90 + oy, 22, 5, SKIN_D, 2, ox)
    E(d, 108, 62 + oy, 16, 20, (255, 255, 255), ox); E(d, 115, 66 + oy, 9, 13, (20, 20, 20), ox)
    R(d, 102, 54 + oy, 28, 6, BEARD, 3, ox)
    # cap
    d.pieslice([(ox + 52) * SS, (20 + oy) * SS, (ox + 142) * SS, (104 + oy) * SS], 180, 360, fill=BLK)
    R(d, 110, 54 + oy, 62, 12, BLK, 6, ox); R(d, 52, 56 + oy, 90, 8, BLK_L, 0, ox); E(d, 88, 30 + oy, 22, 22, GOLD, ox)
    # front arm
    R(d, 96 + arm, 124 + oy, 24, 60, BLK, 12, ox); E(d, 96 + arm, 170 + oy, 26, 26, SKIN, ox)

def hero():
    im, d = canvas(960, 256)
    for i, p in enumerate(['idle', 'run1', 'run2', 'run3', 'jump']): hero_frame(d, i * 192, p)
    save(im, os.path.join(HERO, 'stage1.png'), 960, 256)

for f in (lambda: ground(True), lambda: ground(False), brick, lambda: box(False), lambda: box(True), block, pipe, coin, enemy, flag, goal, bg_far, bg_mid, hero): f()
