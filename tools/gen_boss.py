"""Boss art (per stage, from the stage enemy, bigger with a crown) and the friend the hero is looking for."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import gen_stage1 as g
from PIL import Image, ImageDraw, ImageEnhance
for n in range(1, 8):
    S = os.path.join(g.OUT, f'stage{n}'); src = Image.open(os.path.join(S, 'enemy1.png')).convert('RGBA')
    out = Image.new('RGBA', (768, 256))
    for i in range(3):
        fr = src.crop((i*128, 0, i*128 + 128, 128)).resize((256, 256), Image.LANCZOS)
        r, gg, b, a = fr.split(); fr = Image.merge('RGBA', (r.point(lambda v: min(255, int(v*1.15 + 30))), gg.point(lambda v: int(v*.7)), b.point(lambda v: int(v*.75)), a))
        out.alpha_composite(fr, (i*256, 0))
        if i < 2:
            d = ImageDraw.Draw(out); x = i*256
            d.polygon([(x+120, 70), (x+128, 18), (x+152, 52), (x+176, 8), (x+200, 52), (x+224, 18), (x+232, 70)], fill=(212, 175, 55, 255)); d.rectangle([x+120, 62, x+232, 78], fill=(143, 117, 36, 255))
            for cx in (x+148, x+176, x+204): d.ellipse([cx-7, 62, cx+7, 76], fill=(200, 30, 40, 255))
    out.save(os.path.join(S, 'boss.png')); print('boss', n)
# friend: one standing frame 192x256, facing left
im, d = g.canvas(192, 256); R, E, P = g.R, g.E, g.P
HAIR=(40, 24, 18); DRESS=(31, 143, 143); DR_D=(20, 104, 108)
E(d, 44, 22, 100, 150, HAIR); P(d, [(50, 120), (146, 120), (160, 236), (34, 236)], DRESS); P(d, [(96, 120), (146, 120), (160, 236), (110, 236)], DR_D)
R(d, 60, 108, 72, 60, DRESS, 18); R(d, 58, 150, 76, 12, g.GOLD, 4); R(d, 34, 228, 126, 10, g.GOLD, 4)
E(d, 54, 34, 80, 82, g.SKIN); E(d, 44, 70, 20, 18, g.SKIN); d.pieslice([50*g.SS, 22*g.SS, 138*g.SS, 100*g.SS], 180, 360, fill=HAIR); E(d, 112, 40, 30, 90, HAIR)
E(d, 68, 64, 15, 19, (255, 255, 255)); E(d, 69, 68, 9, 12, (20, 20, 20)); R(d, 62, 56, 26, 5, HAIR, 2); P(d, [(66, 96), (88, 96), (78, 104)], (190, 60, 70)); E(d, 112, 28, 22, 22, g.GOLD)
R(d, 46, 126, 20, 60, DRESS, 10); E(d, 44, 176, 22, 22, g.SKIN); R(d, 66, 236, 26, 14, g.GOLD_D, 6); R(d, 100, 236, 26, 14, g.GOLD_D, 6)
g.save(im, os.path.join(g.HERO, 'friend.png'), 192, 256)
