"""Original default music loops for stages 3-7, plus boss/water variants for all stages. Melodies are generated from each city's scale with a fixed seed."""
import numpy as np, wave, os, subprocess, random, sys
SR = 44100
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'assets')
def hz(semi): return 440 * 2 ** ((semi - 69) / 12)
def osc(kind, f, t):
    if kind == 'pluck': return sum(np.sin(2*np.pi*f*k*t)/k**1.3 for k in range(1, 8)) + .4*sum(np.sin(2*np.pi*f*1.006*k*t)/k**1.5 for k in range(1, 5))
    if kind == 'bow': v = 1 + .006*np.sin(2*np.pi*5.5*t); return sum(np.sin(2*np.pi*f*k*t*v)/k for k in range(1, 7))
    if kind == 'reed': return sum(np.sin(2*np.pi*f*k*t)/k**.9 for k in (1, 2, 3, 4, 5, 6)) * (1 + .15*np.sin(2*np.pi*6*t))
    if kind == 'pulse': return np.where((t*f) % 1 < .25, 1.0, -1.0)
    return 2*np.abs(2*((t*f) % 1) - 1) - 1
def note(kind, f, dur, vol):
    t = np.arange(int(SR*dur))/SR
    dec = {'pluck': 4.5, 'bow': .5, 'reed': .8, 'pulse': 2.2, 'tri': .8}[kind]; att = .05 if kind in ('bow', 'reed') else .004
    return osc(kind, f, t) * np.minimum(1, t/att) * np.exp(-t*dec) * np.minimum(1, (dur - t)/.03) * vol
def compose(n, scale, root, beat, meter, lead, drums, bass_kind='tri', swing=0, bars=16, tremolo=False):
    rnd = random.Random(n*101); step = beat/2; L = meter*2   # steps (eighths) per bar
    total = int(SR*step*L*bars); mix = np.zeros(total + SR)
    def put(sig, at):
        i = int(at*SR); k = min(len(sig), len(mix) - i)
        if k > 0: mix[i:i+k] += sig[:k]
    def phrase():   # one bar: list of (degree, steps)
        out, left, deg = [], L, rnd.choice([0, 2, 4])
        while left > 0:
            d = min(left, rnd.choice([1, 1, 2, 2, 2, 3, 4])); out.append((deg, d)); left -= d
            deg = max(-2, min(9, deg + rnd.choice([-2, -1, -1, 1, 1, 2, 0])))
        return out
    A, B, C = [phrase() for _ in range(2)], [phrase() for _ in range(2)], [phrase() for _ in range(2)]
    cad = [(4, L//4), (2, L//4), (1, L//4), (0, L - 3*(L//4))]
    form = A + B + A + [B[0], cad] + C + B + A + [C[0], cad]
    prog = [0, 0, 3, 4, 0, 5, 3, 4, 3, 4, 0, 5, 0, 3, 4, 0]
    rng = np.random.default_rng(n)
    for b in range(bars):
        t0 = b*L*step; pos = 0
        for deg, d in form[b % len(form)]:
            off = swing*step if pos % 2 else 0
            f = hz(root + 12*(deg // len(scale)) + scale[deg % len(scale)] + 12)
            if tremolo and d >= 3:
                for k in range(int(d*step/.07)): put(note(lead, f, .11, .17), t0 + pos*step + k*.07)
            else: put(note(lead, f, d*step*(1.4 if lead == 'pluck' else .96), .2), t0 + pos*step + off)
            pos += d
        r = root - 24 + scale[prog[b] % len(scale)]
        for e in range(L):
            at = t0 + e*step + (swing*step if e % 2 else 0); tt = np.arange(int(SR*.14))/SR
            if bass_kind == 'walk': put(note('tri', hz(r + 12 + [0, 4, 7, 9, 10, 9, 7, 4][e % 8]), step*.95, .3), at) if e % 2 == 0 else None
            elif e % 2 == 0: put(note('tri', hz(r + 12 + (7 if e % 4 == 2 else 0)), step*1.6, .3), at)
            ch = drums[e % len(drums)]
            if ch == 'D': put(np.sin(2*np.pi*(100*np.exp(-tt*18) + 58)*tt)*np.exp(-tt*16)*.55, at)
            elif ch == 'T': put((rng.uniform(-1, 1, len(tt))*.5 + np.sin(2*np.pi*420*tt))*np.exp(-tt*55)*.2, at)
            elif ch == 'h': put(rng.uniform(-1, 1, len(tt))*np.exp(-tt*110)*.07, at)
            elif ch == 'g': put(np.sin(2*np.pi*620*tt)*np.exp(-tt*9)*.12, at)   # gong/bell
    mix = np.tanh(mix[:total]*1.25)*.8
    d = os.path.join(OUT, f'stage{n}')
    with wave.open('/tmp/mc.wav', 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/tmp/mc.wav', '-b:a', '160k', d + '/music.mp3'], check=True)
    print('stage', n, 'music', round(total/SR, 1), 's')
HIJAZ = [0, 1, 4, 5, 7, 8, 10]; HMIN = [0, 2, 3, 5, 7, 8, 11]; BHAIRAV = [0, 1, 4, 5, 7, 8, 11]; PENTA = [0, 2, 4, 7, 9]; BLUES = [0, 3, 5, 6, 7, 10]
compose(3, HIJAZ, 55, .40, 4, 'pluck', 'D.T.D.T.', tremolo=True)        # Cairo: oud-like, maqsum pulse
compose(4, HMIN, 57, .30, 2, 'pluck', 'D.T.', tremolo=True, bars=48)             # Moscow: balalaika-like, fast 2/4
compose(5, BHAIRAV, 48, .42, 4, 'bow', 'D.hTD.Th')                      # Delhi: drone-like bowed lead, tabla-ish
compose(6, PENTA, 60, .44, 4, 'bow', 'g...D.h.')                        # Beijing: pentatonic, erhu-like
compose(7, BLUES, 53, .36, 4, 'reed', 'D.hTD.hT', bass_kind='walk', swing=.33)   # New York: swing with walking bass
# variants for every stage: protection (faster/higher), boss (lower/driving), water (slow/muffled)
for n in range(1, 8):
    d = os.path.join(OUT, f'stage{n}')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', d + '/music.mp3', '-af', 'asetrate=44100*1.189,aresample=44100,atempo=1.12', '-b:a', '160k', d + '/music_power.mp3'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', d + '/music.mp3', '-af', 'asetrate=44100*0.84,aresample=44100,atempo=1.42,acompressor', '-b:a', '160k', d + '/music_boss.mp3'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', d + '/music.mp3', '-af', 'atempo=0.82,lowpass=f=1400,aecho=0.8:0.7:120:0.35', '-b:a', '160k', d + '/music_water.mp3'], check=True)
print('variants ok')
