"""Default art for stage 2: Baghdad in the Ottoman governors' era. Replaceable by hand-made designs of the same size."""
import os, math, random, sys
sys.path.insert(0, os.path.dirname(__file__))
import gen_stage1 as g
from PIL import Image, ImageDraw, ImageFilter
S2 = os.path.join(g.OUT, 'stage2'); os.makedirs(S2, exist_ok=True); g.S1 = S2
R, E, P, canvas, save, noise, SS = g.R, g.E, g.P, g.canvas, g.save, g.noise, g.SS
SAND=(217,164,65); SAND_L=(244,201,122); SAND_D=(169,119,42); MUD=(190,140,80); WOOD=(122,74,34); WOOD_D=(84,48,20); TURQ=(31,163,163); TURQ_L=(120,214,206); TURQ_D=(18,110,116); CREAM=(233,220,192)

def star8(d, cx, cy, r, col, ox=0, oy=0):
    for rot in (0, math.pi/4):
        P(d, [(cx + r*math.cos(rot + i*math.pi/2), cy + r*math.sin(rot + i*math.pi/2)) for i in range(4)], col, ox, oy)

def ground(top):
    im, d = canvas(128, 128, SAND_D + (255,))
    # herringbone-like farshi brick paving
    for row in range(4):
        off = 0 if row % 2 == 0 else -32
        for col in range(3):
            x, y = off + col*64, row*32
            shade = [(217,164,65),(226,176,80),(206,152,56)][(row+col) % 3]
            R(d, x+2, y+2, 60, 28, shade, 2); R(d, x+4, y+3, 56, 5, (240,196,108), 2)
    if top:
        R(d, 0, 0, 128, 20, SAND_L); R(d, 0, 0, 128, 6, (255,226,160)); R(d, 0, 20, 128, 4, SAND_D)
        for x in range(8, 128, 32): star8(d, x+8, 10, 6, TURQ)
    noise(im, 9, 4 if top else 5)
    save(im, os.path.join(S2, 'ground_top.png' if top else 'ground_fill.png'), 128, 128)

def brick():
    im, d = canvas(128, 128, (120,78,36,255))
    for row in range(4):
        off = 0 if row % 2 == 0 else -32
        for col in range(3):
            x, y = off + col*64, row*32
            R(d, x+2, y+2, 60, 28, MUD, 3); R(d, x+4, y+3, 56, 6, (222,176,112), 2); R(d, x+4, y+23, 56, 5, (150,104,54), 2)
    noise(im, 9, 6); save(im, os.path.join(S2, 'brick.png'), 128, 128)

def box(used):
    base, lt, dk = ((112,84,58),(140,110,82),(74,54,36)) if used else (WOOD,(170,112,58),WOOD_D)
    im, d = canvas(128, 128, dk + (255,))
    R(d, 4, 4, 120, 120, base, 8)
    for y in (36, 66, 96): R(d, 6, y, 116, 3, dk)
    metal, metal_l = ((120,110,96),(150,140,124)) if used else (g.GOLD, g.GOLD_L)
    R(d, 4, 4, 120, 14, metal, 6); R(d, 4, 110, 120, 14, metal, 6); R(d, 4, 4, 14, 120, metal, 6); R(d, 110, 4, 14, 120, metal, 6); R(d, 8, 6, 112, 4, metal_l, 2)
    for x, y in [(11,11),(117,11),(11,117),(117,117)]: E(d, x-5, y-5, 10, 10, dk)
    if not used:
        star8(d, 64, 64, 34, g.GOLD_D); star8(d, 64, 64, 30, g.GOLD); star8(d, 64, 64, 16, TURQ); E(d, 57, 57, 14, 14, g.GOLD_L)
    noise(im, 6, 7); save(im, os.path.join(S2, 'box_used.png' if used else 'box.png'), 128, 128)

def block():
    im, d = canvas(128, 128, (150,112,60,255))
    R(d, 4, 4, 120, 120, (214,178,120), 6); R(d, 4, 4, 120, 10, (240,212,160), 4); R(d, 4, 114, 120, 10, (170,130,76), 4)
    R(d, 20, 20, 88, 88, TURQ_D, 4); R(d, 24, 24, 80, 80, TURQ, 3); star8(d, 64, 64, 34, CREAM); star8(d, 64, 64, 20, TURQ_D); E(d, 56, 56, 16, 16, g.GOLD)
    noise(im, 7, 8); save(im, os.path.join(S2, 'block.png'), 128, 128)

def pipe():
    # a glazed minaret-style column instead of a pipe
    for name, top in (('pipe_top.png', True), ('pipe_body.png', False)):
        im, d = canvas(256, 128)
        x0, w = (0, 256) if top else (20, 216)
        R(d, x0, 0, w, 128, (150,112,60), 10 if top else 0)
        R(d, x0+8, 0 if not top else 6, w-16, 128 if not top else 116, (214,178,120), 6 if top else 0)
        R(d, x0+26, 0 if not top else 6, 30, 128 if not top else 116, (240,212,160)); R(d, x0+w-62, 0 if not top else 6, 44, 128 if not top else 116, (180,140,84))
        if top:
            R(d, 8, 30, 240, 68, TURQ_D); R(d, 8, 34, 240, 60, TURQ)
            for x in range(32, 256, 48): star8(d, x, 64, 20, CREAM); star8(d, x, 64, 9, g.GOLD)
            R(d, 8, 104, 240, 16, (150,112,60))
        else:
            for y in (30, 94): R(d, x0+8, y, w-16, 4, (170,130,76))
        save(im, os.path.join(S2, name), 256, 128)

def enemy():
    # scorpion: walk1, walk2, squashed
    im, d = canvas(384, 128)
    B=(92,44,20); BL=(150,78,34); BD=(56,26,12)
    for i in range(3):
        ox = i*128
        if i == 2:
            E(d, 8, 96, 112, 28, B, ox); E(d, 80, 100, 34, 18, BL, ox); continue
        f = 0 if i == 0 else 8
        for k in range(4):  # legs
            lx = 30 + k*16
            P(d, [(lx, 92), (lx+8, 92), (lx+2 + (f if k % 2 else -f), 122), (lx-6 + (f if k % 2 else -f), 122)], BD, ox)
        # tail segments curling up and forward
        pts = [(26,84),(14,66),(14,46),(26,30),(44,24)]
        for j,(x,y) in enumerate(pts): E(d, x-11+j, y-11+j, 22-2*j, 22-2*j, B if j % 2 == 0 else BL, ox)
        P(d, [(48,18),(70,26-f/2),(50,32)], BD, ox)
        E(d, 20, 70, 84, 40, B, ox); E(d, 30, 74, 60, 14, BL, ox)
        E(d, 82, 66, 36, 34, B, ox); E(d, 100, 74, 9, 10, (255,255,255), ox); E(d, 104, 77, 5, 6, (20,20,20), ox)
        # claws
        R(d, 104, 92, 16, 8, BD, 3, ox); E(d, 108, 84+f/2, 20, 16, BL, ox); P(d, [(122,84+f/2),(128,90),(120,94)], BD, ox)
    save(im, os.path.join(S2, 'enemy1.png'), 384, 128)

def goal():
    # Baghdadi gate: pointed arch, turquoise dome, two small towers
    im, d = canvas(640, 640)
    R(d, 40, 250, 560, 390, (214,178,120)); R(d, 40, 250, 560, 20, (240,212,160)); R(d, 40, 270, 560, 26, TURQ)
    for x in range(64, 600, 44): star8(d, x, 283, 10, CREAM)
    for x in (40, 520):
        R(d, x, 150, 80, 110, (200,162,104)); d.pieslice([x*SS, 100*SS, (x+80)*SS, 200*SS], 180, 360, fill=TURQ); R(d, x+37, 76, 6, 30, g.GOLD)
    d.pieslice([200*SS, 60*SS, 440*SS, 440*SS], 180, 360, fill=TURQ); d.pieslice([230*SS, 90*SS, 330*SS, 300*SS], 180, 270, fill=TURQ_L)
    R(d, 316, 20, 8, 50, g.GOLD); E(d, 308, 12, 24, 24, g.GOLD)
    R(d, 190, 240, 260, 16, (240,212,160))
    R(d, 230, 400, 180, 240, (36,22,12)); P(d, [(230,400),(320,300),(410,400)], (36,22,12)); d.pieslice([230*SS, 330*SS, 410*SS, 470*SS], 180, 360, fill=(36,22,12))
    P(d, [(214,404),(320,282),(426,404),(410,404),(320,300),(230,404)], TURQ_D)
    for x in (90, 480): R(d, x, 360, 70, 120, WOOD_D, 6); [R(d, x+6, 368+j*14, 58, 5, WOOD) for j in range(8)]
    save(im, os.path.join(S2, 'goal.png'), 640, 640)

def bg_far():
    w, h = 3840, 1080
    im = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(im)
    stops = [(0,(232,120,70)),(0.35,(246,170,90)),(0.7,(250,208,140)),(1,(252,228,176))]
    for y in range(h):
        t = y/h
        for (t0,c0),(t1,c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                k=(t-t0)/(t1-t0); d.line([(0,y),(w,y)], fill=tuple(int(c0[i]+(c1[i]-c0[i])*k) for i in range(3))+(255,)); break
    glow = Image.new('RGBA', (w, h)); gd = ImageDraw.Draw(glow)
    gd.ellipse([2500, 180, 3100, 780], fill=(255,236,170,90)); glow = glow.filter(ImageFilter.GaussianBlur(70)); im.alpha_composite(glow)
    d.ellipse([2690, 370, 2910, 590], fill=(255,244,200,255))
    rnd = random.Random(11)
    # distant skyline silhouette (tiles horizontally: built on a 3840 period)
    for col, base, n, seed in (((214,150,96), 800, 26, 1), ((190,124,78), 850, 22, 2)):
        rnd = random.Random(seed); x = 0
        while x < w:
            bw = rnd.randrange(90, 220); bh = rnd.randrange(60, 170); kind = rnd.random()
            d.rectangle([x, base-bh, x+bw, h], fill=col+(255,))
            if kind < 0.3: d.pieslice([x+bw*0.15, base-bh-bw*0.35, x+bw*0.85, base-bh+bw*0.35], 180, 360, fill=col+(255,))
            elif kind < 0.5: d.rectangle([x+bw*0.4, base-bh-rnd.randrange(120,220), x+bw*0.4+18, base-bh], fill=col+(255,)); 
            x += bw
        d.rectangle([0, base, w, h], fill=col+(255,))
    # Tigris
    for y in range(880, 1080):
        k=(y-880)/200; d.line([(0,y),(w,y)], fill=(int(96+40*k), int(150+20*k), int(170-10*k), 255))
    for i in range(160):
        x=rnd.randrange(w); y=rnd.randrange(890,1070); d.line([(x,y),(x+rnd.randrange(30,110),y)], fill=(255,230,170,255), width=2)
    im.convert('RGB').save(os.path.join(S2, 'bg_far.jpg'), quality=92); print('wrote stage2/bg_far.jpg')

def bg_mid():
    w, h, GL = 4720, 1080, 940
    im = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(im); rnd = random.Random(21)
    def palm(x, s):
        for i in range(12): d.rectangle([x-7+math.sin(i*.5)*4, GL-s+i*s/12, x+7+math.sin(i*.5)*4, GL-s+(i+1)*s/12], fill=(110,70,36,255) if i%2 else (132,86,44,255))
        for a in range(-80, 261, 34):
            ar=math.radians(a); pts=[(x, GL-s)]
            for t in range(1,7): pts.append((x+math.cos(ar)*t*18, GL-s-math.sin(ar)*t*18+t*t*2.2))
            d.line(pts, fill=(40,104,56,255), width=12); d.line(pts, fill=(58,132,70,255), width=5)
        for dx in (-10, 8): d.ellipse([x+dx-9, GL-s+4, x+dx+9, GL-s+26], fill=(150,82,30,255))
    def lattice(x0, y0, x1, y1):
        d.rectangle([x0, y0, x1, y1], fill=(60,34,14,255))
        for x in range(int(x0), int(x1), 9): d.line([(x, y0), (x, y1)], fill=(150,96,46,255), width=2)
        for y in range(int(y0), int(y1), 9): d.line([(x0, y), (x1, y)], fill=(150,96,46,255), width=2)
        d.rectangle([x0, y0, x1, y1], outline=(84,48,20,255), width=4)
    def house(x, bw, bh, col):
        d.rectangle([x, GL-bh, x+bw, GL], fill=col+(255,)); d.rectangle([x, GL-bh, x+bw, GL-bh+10], fill=(244,214,160,255))
        for cx in range(x+8, x+bw-8, 18): d.rectangle([cx, GL-bh-12, cx+9, GL-bh], fill=col+(255,))
        # shanasheel: overhanging wooden bay on the upper floor
        sy0, sy1 = GL-bh+50, GL-bh+50+min(170, bh*0.42)
        d.rectangle([x-14, sy0, x+bw+14, sy1], fill=(122,74,34,255)); d.rectangle([x-14, sy0, x+bw+14, sy0+10], fill=(150,96,46,255))
        d.polygon([(x-14, sy1), (x+bw+14, sy1), (x+bw, sy1+22), (x, sy1+22)], fill=(84,48,20,255))
        n = max(2, bw//80); ww = (bw+8)/n
        for i in range(n):
            lattice(x-6+i*ww+8, sy0+22, x-6+(i+1)*ww-8, sy1-14)
            d.pieslice([x-6+i*ww+8, sy0+4, x-6+(i+1)*ww-8, sy0+44], 180, 360, fill=(31,163,163,255))
        dx = x + bw*0.5 - 34
        d.rectangle([dx, GL-120, dx+68, GL], fill=(60,34,14,255)); d.pieslice([dx, GL-158, dx+68, GL-82], 180, 360, fill=(60,34,14,255))
        d.arc([dx-4, GL-162, dx+72, GL-78], 180, 360, fill=(31,163,163,255), width=6)
    def mosque(x):
        d.rectangle([x, GL-230, x+360, GL], fill=(206,166,104,255)); d.rectangle([x, GL-230, x+360, GL-206], fill=(31,163,163,255))
        d.pieslice([x+60, GL-420, x+300, GL-60], 180, 360, fill=(31,163,163,255)); d.pieslice([x+90, GL-396, x+190, GL-200], 180, 270, fill=(120,214,206,255))
        d.rectangle([x+176, GL-470, x+184, GL-416], fill=(212,175,55,255))
        for k in range(3): d.pieslice([x+50+k*100, GL-170, x+110+k*100, GL-70], 180, 360, fill=(60,34,14,255)); d.rectangle([x+50+k*100, GL-120, x+110+k*100, GL], fill=(60,34,14,255))
        mx = x+390
        d.rectangle([mx, GL-560, mx+46, GL], fill=(214,178,120,255)); d.rectangle([mx-10, GL-430, mx+56, GL-408], fill=(122,74,34,255)); d.rectangle([mx-8, GL-300, mx+54, GL-284], fill=(31,163,163,255))
        d.pieslice([mx-4, GL-610, mx+50, GL-520], 180, 360, fill=(31,163,163,255)); d.rectangle([mx+20, GL-650, mx+26, GL-606], fill=(212,175,55,255))
    def qishla(x):
        # clock tower
        d.rectangle([x, GL-520, x+120, GL], fill=(196,150,90,255)); d.rectangle([x-12, GL-540, x+132, GL-516], fill=(122,74,34,255))
        d.rectangle([x+20, GL-640, x+100, GL-540], fill=(206,162,100,255)); d.polygon([(x+10, GL-640), (x+60, GL-720), (x+110, GL-640)], fill=(122,74,34,255)); d.rectangle([x+57, GL-760, x+63, GL-716], fill=(212,175,55,255))
        d.ellipse([x+18, GL-500, x+102, GL-416], fill=(255,246,214,255), outline=(84,48,20,255), width=6)
        d.line([(x+60, GL-458), (x+60, GL-490)], fill=(30,20,10,255), width=5); d.line([(x+60, GL-458), (x+82, GL-446)], fill=(30,20,10,255), width=5)
        for yy in (GL-380, GL-250): d.rectangle([x+40, yy, x+80, yy+80], fill=(60,34,14,255)); d.pieslice([x+40, yy-24, x+80, yy+24], 180, 360, fill=(60,34,14,255))
        # long arcaded barracks wing
        d.rectangle([x+120, GL-200, x+620, GL], fill=(210,168,108,255)); d.rectangle([x+120, GL-200, x+620, GL-186], fill=(244,214,160,255))
        for k in range(7): d.rectangle([x+140+k*68, GL-110, x+186+k*68, GL], fill=(60,34,14,255)); d.pieslice([x+140+k*68, GL-140, x+186+k*68, GL-80], 180, 360, fill=(60,34,14,255))
    x = 40; cols=[(214,170,108),(200,152,92),(224,184,124),(190,140,84)]
    plan = ['h','h','p','m','h','p','h','q','p','h','h','m','p','h','h','p']
    for k in plan:
        if k == 'h':
            bw = rnd.randrange(170, 280); house(x, bw, rnd.randrange(330, 520), rnd.choice(cols)); x += bw + rnd.randrange(30, 70)
        elif k == 'p': palm(x+30, rnd.randrange(330, 470)); palm(x+110, rnd.randrange(260, 380)); x += 170
        elif k == 'm': mosque(x); x += 490
        elif k == 'q': qishla(x); x += 680
    print('bg_mid used width', x)
    # warm haze so the playable blocks stand out against the city
    haze = Image.new('RGBA', im.size, (250, 206, 140, 255)); alpha = im.getchannel('A')
    im = Image.blend(im, haze, 0.30); im.putalpha(alpha)
    im.save(os.path.join(S2, 'bg_mid.png')); print('wrote stage2/bg_mid.png')

# ---------- hero in Baghdadi dress: charawiya headwrap, striped zboon robe, wide belt ----------
ROBE=(233,220,192); ROBE_D=(204,188,154); STRIPE=(139,90,43); BELT=(138,31,31); SHOE=(122,59,29); WRAP=(246,242,232)
def hero_frame(d, ox, pose):
    bl, blift, fl, flift, arm = {'idle': (76,0,100,0,0), 'run1': (60,0,114,12,16), 'run2': (84,8,94,0,0), 'run3': (114,12,60,0,-16), 'jump': (62,20,116,4,-28)}[pose]
    oy = (4 if pose == 'run2' else 0) + (-6 if pose == 'jump' else 0)
    spread = {'idle': 0, 'run1': 14, 'run2': 4, 'run3': 14, 'jump': 18}[pose]
    R(d, 66-arm, 124+oy, 24, 60, ROBE_D, 12, ox); E(d, 66-arm, 170+oy, 24, 24, g.SKIN_D, ox)
    for lx, lift in ((bl, blift), (fl, flift)):
        R(d, lx-10, 206+oy, 22, 26-lift, g.SKIN_D, 6, ox); R(d, lx-16, 228-lift, 46, 20, SHOE, 9, ox); R(d, lx+14, 224-lift, 18, 12, SHOE, 6, ox)
    # robe
    P(d, [(58,120+oy),(134,120+oy),(142+spread,214+oy),(50-spread,214+oy)], ROBE, ox); R(d, 58, 110+oy, 76, 40, ROBE, 18, ox)
    for sx in (72, 88, 104, 120):
        k=(sx-96)/38; P(d, [(sx-2,116+oy),(sx+2,116+oy),(sx+2+k*spread,214+oy),(sx-3+k*spread,214+oy)], STRIPE, ox)
    R(d, 54, 156+oy, 84, 20, BELT, 6, ox); R(d, 88, 154+oy, 20, 24, g.GOLD, 4, ox)
    # head
    E(d, 56, 34+oy, 84, 84, g.SKIN, ox); E(d, 128, 74+oy, 20, 18, g.SKIN, ox)
    P(d, [(60,82+oy),(140,86+oy),(134,116+oy),(104,126+oy),(72,116+oy)], g.BEARD, ox); E(d, 56, 62+oy, 22, 46, g.BEARD, ox)
    R(d, 112, 90+oy, 22, 5, g.SKIN_D, 2, ox)
    E(d, 108, 62+oy, 16, 20, (255,255,255), ox); E(d, 115, 66+oy, 9, 13, (20,20,20), ox); R(d, 102, 54+oy, 28, 6, g.BEARD, 3, ox)
    # charawiya (wrapped headcloth)
    E(d, 46, 10+oy, 104, 56, WRAP, ox); R(d, 50, 36+oy, 96, 22, WRAP, 8, ox)
    for k in range(4): P(d, [(52+k*24, 22+oy), (60+k*24, 16+oy), (84+k*24, 54+oy), (76+k*24, 58+oy)], (40,40,44), ox)
    R(d, 50, 52+oy, 96, 6, (210,204,190), 3, ox); P(d, [(50,48+oy),(38,96+oy),(54,100+oy),(62,56+oy)], WRAP, ox)
    R(d, 96+arm, 124+oy, 24, 58, ROBE, 12, ox); R(d, 106+arm, 126+oy, 4, 50, STRIPE, 0, ox); E(d, 96+arm, 170+oy, 26, 26, g.SKIN, ox)

def hero():
    im, d = canvas(960, 256)
    for i, p in enumerate(['idle','run1','run2','run3','jump']): hero_frame(d, i*192, p)
    save(im, os.path.join(g.HERO, 'stage2.png'), 960, 256)

for f in (lambda: ground(True), lambda: ground(False), brick, lambda: box(False), lambda: box(True), block, pipe, g.coin, enemy, g.flag, goal, bg_far, bg_mid, hero): f()
