/* IBRA World Tour — محرك اللعبة. دقة داخلية 1920×1080، البلاطة 72px والصور الأصلية 128px حتى تبقى واضحة لحد 4K. */
(() => {
  const VW = 1920, VH = 1080, T = 72, ROWS = 15, GROUND = 13;
  const cv = document.getElementById('c'), ctx = cv.getContext('2d');
  const GOLD = '#d4af37';
  const FONT = '"Segoe UI",Tahoma,"Noto Sans Arabic",Arial,sans-serif';

  function fit() {
    const dpr = window.devicePixelRatio || 1, s = Math.min(innerWidth / VW, innerHeight / VH);
    cv.style.width = Math.floor(VW * s) + 'px'; cv.style.height = Math.floor(VH * s) + 'px';
    const pw = Math.min(3840, Math.round(VW * s * dpr)), ph = Math.round(pw * VH / VW);
    if (cv.width !== pw) { cv.width = pw; cv.height = ph; }
    ctx.setTransform(cv.width / VW, 0, 0, cv.height / VH, 0, 0); ctx.imageSmoothingQuality = 'high';
  }
  addEventListener('resize', fit); fit();

  // ---------- شكل كل جولة: فلتر ألوان ينطبق على الصور الأساسية. إذا حطيت صورة خاصة بمجلد الجولة (rN) تنستخدم مثل ما هي ----------
  const VARIANT = {
    day: { tile: '', bg: '' },
    alt: { tile: 'hue-rotate(-28deg) saturate(1.15)', bg: 'sepia(0.4) saturate(1.5) hue-rotate(-14deg) brightness(0.96)' },
    night: { tile: 'brightness(0.62) saturate(0.85) hue-rotate(12deg)', bg: 'brightness(0.34) saturate(0.7) hue-rotate(28deg) contrast(1.1)', night: true, mul: 'rgb(150,160,230)' },
    noon: { tile: 'brightness(1.1) saturate(1.1) hue-rotate(18deg)', bg: 'brightness(1.2) saturate(0.8) contrast(1.05)', glare: true },
    sewer: { tile: 'hue-rotate(62deg) saturate(0.9)', bg: 'hue-rotate(20deg) saturate(1.1)' },
    water: { tile: 'hue-rotate(150deg) saturate(0.8) brightness(0.9)', bg: 'hue-rotate(170deg) saturate(0.7) brightness(0.7)' },
    dawn: { tile: 'hue-rotate(-50deg) saturate(0.9) brightness(1.04)', bg: 'hue-rotate(-34deg) saturate(0.75) brightness(1.08)', fog: true },
    boss: { tile: 'brightness(0.72) saturate(1.1) hue-rotate(-14deg)', bg: 'sepia(0.6) saturate(2.1) hue-rotate(-32deg) brightness(0.62)', mul: 'rgb(255,190,170)' }
  };
  const IMG = {};
  const TILES = { ground_top: 'ground_top.png', ground_fill: 'ground_fill.png', brick: 'brick.png', box: 'box.png', box_used: 'box_used.png', block: 'block.png', pipe_top: 'pipe_top.png', pipe_body: 'pipe_body.png', goal: 'goal.png' };
  const BGS = { bg_far: 'bg_far.jpg', bg_mid: 'bg_mid.png' };
  const FOES = { enemy1: 'enemy1.png', enemy_water: 'enemy_water.png', boss: 'boss.png' };
  const PLAIN = { coin: 'coin.png', flag: 'flag.png', item_grow: 'item_grow.png', item_weapon: 'item_weapon.png', shot: 'shot.png', item_life: 'item_life.png', item_star: 'item_star.png' };
  function tryLoad(paths) {   // يجرب المسارات بالترتيب، ويرجع الصورة ورقم المسار اللي نجح
    return new Promise(res => { let i = 0; const next = () => { if (i >= paths.length) return res(null); const im = new Image(), k = i++; im.onload = () => res({ im, k }); im.onerror = next; im.src = paths[k] + '?v=' + Date.now(); }; next(); });
  }
  function bake(im, filter) { if (!filter) return im; const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const x = c.getContext('2d'); x.filter = filter; x.drawImage(im, 0, 0); return c; }
  function loadStage(st) {
    const V = VARIANT[st.variant] || VARIANT.day, dir = `assets/${st.id}/`, rdir = `${dir}r${st.round}/`, jobs = [];
    const grp = (files, filter) => Object.entries(files).forEach(([k, f]) => jobs.push(tryLoad(st.world ? [rdir + f, dir + f] : [dir + f]).then(r => { IMG[k] = r ? (r.k === 0 && st.world ? r.im : bake(r.im, filter)) : null; })));
    grp(TILES, V.tile); grp(BGS, V.bg); grp(PLAIN, ''); grp(FOES, st.round > 1 ? `hue-rotate(${(st.round - 1) * 47}deg)` : '');
    jobs.push(tryLoad([`assets/hero/${st.id}_r${st.round}.png`, `assets/hero/${st.id}.png`]).then(r => { IMG.hero = r ? r.im : null; }));
    jobs.push(tryLoad(['assets/hero/friend.png']).then(r => { IMG.friend = r ? r.im : null; }));
    return Promise.all(jobs);
  }

  // ---------- الصوت ----------
  let AC = null, muted = false; const music = new Audio(); music.loop = true; music.volume = 0.55;
  const musicP = new Audio(); musicP.loop = true; musicP.volume = 0.6; let powerOk = false;
  function ac() { if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { } } return AC; }
  function beep(f0, f1, dur, type = 'square', vol = 0.12) {
    const a = ac(); if (!a || muted) return;
    const o = a.createOscillator(), g = a.createGain(), t = a.currentTime;
    o.type = type; o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(Math.max(30, f1), t + dur);
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.001, t + dur); o.connect(g).connect(a.destination); o.start(t); o.stop(t + dur);
  }
  const seq = (fs, gap, d, type, vol) => fs.forEach((f, i) => setTimeout(() => beep(f, f, d, type, vol), i * gap));
  const SFX = {
    jump: () => beep(330, 760, 0.18), swim: () => beep(260, 420, 0.14, 'sine', 0.2), coin: () => { beep(988, 988, 0.07); setTimeout(() => beep(1319, 1319, 0.22), 70); },
    stomp: () => beep(420, 90, 0.16, 'triangle', 0.25), bump: () => beep(160, 110, 0.09, 'triangle', 0.25), brk: () => beep(220, 50, 0.22, 'sawtooth', 0.14), die: () => beep(520, 70, 0.8, 'triangle', 0.22),
    win: () => seq([523, 659, 784, 1047], 140, 0.22), life: () => seq([659, 784, 1319], 90, 0.14), grow: () => seq([392, 523, 659, 784, 1047], 60, 0.09), shrink: () => seq([784, 587, 440, 330], 70, 0.1, 'triangle', 0.2),
    shoot: () => beep(900, 300, 0.1, 'square', 0.1), item: () => beep(200, 600, 0.35, 'triangle', 0.2), boom: () => beep(180, 40, 0.4, 'sawtooth', 0.25), pipe: () => seq([400, 300, 220], 110, 0.12, 'square', 0.14), bossHit: () => beep(160, 60, 0.3, 'square', 0.25)
  };
  // يجرب قائمة ملفات موسيقى بالترتيب (ملف الجولة أولاً، بعدين ملف المدينة)
  function chain(audio, list, onOk) { let i = 0; const next = () => { if (i >= list.length) return; audio.onerror = next; audio.oncanplaythrough = () => { audio.oncanplaythrough = null; onOk && onOk(); }; audio.src = list[i++]; audio.load(); }; next(); }
  function musicList(st, kind) {
    const d = `assets/${st.id}/`, r = `${d}r${st.round}/`, l = [];
    if (kind === 'power') return [r + 'music_power.mp3', d + 'music_power.mp3'];
    if (kind === 'boss') return [r + 'music_boss.mp3', d + 'music_boss.mp3', d + 'music.mp3'];
    if (kind === 'sewer') return [r + 'music_sewer.mp3', d + 'music_sewer.mp3', d + 'music_water.mp3', d + 'music.mp3'];
    if (st.variant === 'water') l.push(r + 'music.mp3', d + 'music_water.mp3'); else l.push(r + 'music.mp3');
    l.push(d + 'music.mp3'); return l;
  }
  function playMusic(kind) {
    music.muted = muted; music.playbackRate = 1; chain(music, musicList(G.stage, kind), () => { if (G.mode === 'play' && !(G.hero && G.hero.star > 0 && powerOk)) music.play().catch(() => { }); });
    if (!kind) { powerOk = false; musicP.muted = muted; chain(musicP, musicList(G.stage, 'power'), () => { powerOk = true; }); }
  }
  function starMusic(on) {
    if (on) { if (powerOk) { music.pause(); musicP.currentTime = 0; musicP.play().catch(() => { }); } else music.playbackRate = 1.4; }
    else { musicP.pause(); music.playbackRate = 1; if (G.hero && !G.hero.dead && G.hero.state === 'play') music.play().catch(() => { }); }
  }
  function pauseAll() { music.pause(); musicP.pause(); }
  function resumeMusic() { if (G.hero && G.hero.star > 0 && powerOk) musicP.play().catch(() => { }); else music.play().catch(() => { }); }

  // ---------- الإدخال ----------
  const keys = {}; let pressed = {};
  addEventListener('keydown', e => {
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space', 'Tab'].includes(e.code)) e.preventDefault();
    if (!keys[e.code]) pressed[e.code] = true; keys[e.code] = true; ac();
    if (e.code === 'KeyM') { muted = !muted; music.muted = muted; musicP.muted = muted; }
    if (e.code === 'F5') { e.preventDefault(); if (G.stage) loadStage(G.stage); }
    if (e.code === 'F2' && window.ibra) window.ibra.openAssets();
    if (e.code === 'F11' && window.ibra) { e.preventDefault(); window.ibra.toggleFullscreen(); }
  });
  addEventListener('keyup', e => { keys[e.code] = false; });
  let padPrev = {};
  function input() {
    const p = (navigator.getGamepads ? [...navigator.getGamepads()].find(x => x) : null);
    const pb = i => !!(p && p.buttons[i] && p.buttons[i].pressed), ax = p ? p.axes[0] : 0, ay = p ? p.axes[1] : 0;
    const now = { jump: pb(0) || pb(1), start: pb(9), fire: pb(2), l: ax < -0.5 || pb(14), r: ax > 0.5 || pb(15), u: ay < -0.5 || pb(12), d: ay > 0.5 || pb(13) };
    const edge = k => now[k] && !padPrev[k];
    const st = {
      left: keys.ArrowLeft || keys.KeyA || now.l, right: keys.ArrowRight || keys.KeyD || now.r, down: keys.ArrowDown || keys.KeyS || now.d,
      jump: keys.Space || keys.ArrowUp || keys.KeyW || now.jump, run: keys.ShiftLeft || keys.ShiftRight || keys.KeyX || pb(3) || pb(5) || pb(7),
      jumpP: pressed.Space || pressed.ArrowUp || pressed.KeyW || edge('jump'),
      start: pressed.Enter || pressed.NumpadEnter || pressed.Space || edge('start') || edge('jump'),
      pause: pressed.KeyP || pressed.Escape || edge('start'), back: pressed.Escape || pressed.Backspace, quit: pressed.KeyQ,
      fire: pressed.KeyZ || pressed.KeyF || pressed.ControlLeft || pressed.ControlRight || edge('fire'),
      mL: pressed.ArrowLeft || pressed.KeyA || edge('l'), mR: pressed.ArrowRight || pressed.KeyD || edge('r'), mU: pressed.ArrowUp || pressed.KeyW || edge('u'), mD: pressed.ArrowDown || pressed.KeyS || edge('d')
    };
    padPrev = now; pressed = {}; return st;
  }

  // ---------- الحالة ----------
  const G = { mode: 'title', stageIndex: 0, stage: null, L: null, hero: null, enemies: [], coins: [], fx: [], cam: 0, score: 0, coinsN: 0, lives: 3, time: 0, t: 0, msgT: 0, respawnCol: 2, power: 0, items: [], shots: [], main: null, boss: null, sel: 0, done: {} };
  window.__game = G;
  const store = { get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } } };
  G.best = store.get('iwt_best', 0); G.sel = Math.min(STAGES.length - 1, store.get('iwt_last', 0)); G.done = store.get('iwt_done', {});

  const HH = [76, 124, 124];   // ارتفاع البطل: صغير، كبير، مسلح
  const solid = ch => ch === '#' || ch === 'B' || ch === '?' || ch === 'M' || ch === 'T' || ch === 'U' || ch === 'S' || ch === 'P';
  function cell(c, r) { if (r < 0) return '.'; if (r >= ROWS || c < 0 || c >= G.L.width) return c < 0 || c >= G.L.width ? 'S' : '.'; return G.L.grid[r][c]; }
  const water = () => G.L.kind === 'water';

  async function startStage(i, keep) {
    G.mode = 'loading'; G.stageIndex = i; G.stage = STAGES[i]; G.sel = i; store.set('iwt_last', i);
    await loadStage(G.stage);
    if (!keep) { G.score = 0; G.coinsN = 0; G.lives = 3; G.power = 0; }
    G.respawnCol = 2; resetLevel(); G.mode = 'play'; playMusic();
  }
  function mkEnemy(e) {
    const sp = (1 + (G.stage.round - 1) * 0.07 + G.stage.world * 0.03) * 110, type = e.type || 'walk';
    const o = { x: e.c * T + 6, y: (e.row + 1) * T - 60, w: 60, h: 60, vx: -sp * (type === 'fast' ? 1.8 : type === 'fish' ? 0.9 : 1), vy: 0, dead: 0, on: false, type, t: (e.c * 7) % 5 };
    if (type === 'fish') { o.y0 = o.y; o.x0 = o.x; } return o;
  }
  function setLevel(L) {
    G.L = L; G.enemies = L.enemies.map(mkEnemy); G.coins = L.coins.map(c => ({ x: c.c * T + T / 2, y: c.row * T + T / 2, got: false }));
    G.items = []; G.shots = []; G.fx = [];
  }
  function resetLevel() {
    setLevel(G.stage.level()); G.main = null; G.time = G.stage.time; G.t = 0; G.boss = null; G.bossDead = false; G.bossOn = false;
    if (G.L.boss) G.boss = { x: (G.L.boss.to - 5) * T, y: GROUND * T - 170, w: 150, h: 170, vx: 0, vy: 0, hp: G.stage.bossHp, max: G.stage.bossHp, inv: 0, t: 0, dir: -1, dead: 0, ground: false };
    const wy = water() ? 6 * T : GROUND * T - HH[G.power];
    G.hero = { x: G.respawnCol * T, y: wy, w: 44, h: HH[G.power], cool: 0, star: 0, vx: 0, vy: 0, ground: false, face: 1, anim: 0, dead: 0, inv: 0, coyote: 0, buf: 0, state: 'play', slideT: 0 };
    G.cam = Math.max(0, G.hero.x - VW * 0.4);
  }
  // ---------- المجاري: منطقة فرعية ندخلها من الأنبوب ونطلع من أنبوب أبعد ----------
  function enterSewer() {
    const h = G.hero; SFX.pipe();
    G.main = { L: G.L, enemies: G.enemies, coins: G.coins, items: G.items };
    setLevel(G.main.L.sewer.sub); h.x = 3 * T; h.y = 4 * T; h.vx = 0; h.vy = 0; G.cam = 0; playMusic('sewer');
  }
  function exitSewer() {
    const h = G.hero, m = G.main, s = m.L.sewer; SFX.pipe(); G.main = null;
    G.L = m.L; G.enemies = m.enemies; G.coins = m.coins; G.items = m.items; G.shots = []; G.fx = [];
    h.x = s.exit * T + T - h.w / 2; h.y = (GROUND - 2) * T - h.h - 4; h.vx = 0; h.vy = -700; G.cam = Math.max(0, h.x - VW * 0.4);
    G.respawnCol = Math.max(G.respawnCol, s.exit + 3);
    playMusic();
  }

  // ---------- الفيزياء ----------
  function moveBody(b, dt, onBump) {
    b.x += b.vx * dt;
    let c0 = Math.floor(b.x / T), c1 = Math.floor((b.x + b.w - 0.01) / T), r0 = Math.floor(b.y / T), r1 = Math.floor((b.y + b.h - 0.01) / T);
    b.hitWall = false;
    for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) if (solid(cell(c, r))) {
      if (b.vx > 0) b.x = c * T - b.w; else if (b.vx < 0) b.x = (c + 1) * T; b.hitWall = true;
      c0 = Math.floor(b.x / T); c1 = Math.floor((b.x + b.w - 0.01) / T);
    }
    b.y += b.vy * dt; b.ground = false;
    c0 = Math.floor(b.x / T); c1 = Math.floor((b.x + b.w - 0.01) / T); r0 = Math.floor(b.y / T); r1 = Math.floor((b.y + b.h - 0.01) / T);
    for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) if (solid(cell(c, r))) {
      if (b.vy > 0) { b.y = r * T - b.h; b.vy = 0; b.ground = true; }
      else if (b.vy < 0) { b.y = (r + 1) * T; b.vy = 0; if (onBump) { const mid = Math.floor((b.x + b.w / 2) / T); onBump(solid(cell(mid, r)) ? mid : c, r); onBump = null; } }
    }
  }
  function spark(x, y) { G.fx.push({ type: 'spark', x, y, t: 0 }); }
  function bump(c, r) {
    const ch = cell(c, r), g = G.L.grid;
    G.enemies.forEach(e => { if (!e.dead && e.ground && Math.abs(e.y + e.h - r * T) < 4 && e.x + e.w > c * T && e.x < (c + 1) * T) killEnemy(e); });
    G.coins.forEach(k => { if (!k.got && Math.floor(k.x / T) === c && Math.floor(k.y / T) === r - 1) getCoin(k); });
    if (ch === 'M') { g[r][c] = 'U'; G.fx.push({ type: 'bounce', c, r, t: 0 }); SFX.item(); spawnItem(G.power === 0 ? 'grow' : 'weapon', c, r); }
    else if (ch === 'T' || ch === 'H') { g[r][c] = 'U'; G.fx.push({ type: 'bounce', c, r, t: 0 }); SFX.item(); spawnItem(ch === 'T' ? 'star' : 'life', c, r); }
    else if (ch === '?') { g[r][c] = 'U'; G.fx.push({ type: 'pop', x: c * T + T / 2, y: r * T, t: 0 }); G.fx.push({ type: 'bounce', c, r, t: 0 }); addCoin(); G.score += 200; }
    else if (ch === 'B' && G.power === 0) { SFX.bump(); G.fx.push({ type: 'bounce', c, r, t: 0 }); }
    else if (ch === 'B') breakBrick(c, r);
    else SFX.bump();
  }
  function spawnItem(type, c, r) { G.items.push({ type, x: c * T + 6, y: r * T, w: 60, h: 60, vx: 0, vy: 0, rise: 0, r, dir: G.hero.face || 1 }); }
  function breakBrick(c, r) {
    G.L.grid[r][c] = '.'; SFX.brk(); G.score += 50;
    for (let i = 0; i < 4; i++) G.fx.push({ type: 'shard', x: c * T + T / 2, y: r * T + T / 2, vx: (i % 2 ? 1 : -1) * (160 + i * 40), vy: -700 - (i > 1 ? 250 : 0), t: 0 });
  }
  function setPower(p) { const h = G.hero, old = h.h; G.power = p; h.h = HH[p]; h.y -= h.h - old; }
  // لمسة العدو تنزل البطل درجة: مسلح ← كبير ← صغير ← يخسر محاولة
  function hurt() { if (G.power > 0) { setPower(G.power - 1); G.hero.inv = 2; SFX.shrink(); return false; } killHero(); return true; }
  function killEnemy(e) { if (e.dead) return; e.dead = 0.01; e.vy = -500; e.flip = true; G.score += 100; SFX.stomp(); spark(e.x + 30, e.y + 20); }
  function hitBoss(dmg, withInv) {
    const b = G.boss; if (!b || b.dead || (withInv && b.inv > 0)) return;
    b.hp -= dmg; if (withInv) b.inv = 1.1; b.flash = 0.25; SFX.bossHit(); spark(b.x + b.w / 2, b.y + 30);
    if (b.hp <= 0) { b.dead = 0.01; b.vy = -700; G.bossDead = true; G.score += 5000; SFX.boom(); for (let i = 0; i < 8; i++) spark(b.x + Math.random() * b.w, b.y + Math.random() * b.h); G.enemies.forEach(killEnemy); playMusic(); SFX.win(); }
  }
  function fire() {
    const h = G.hero, W = G.stage.weapon; if (G.power < 2 || h.cool > 0 || G.shots.length >= W.max) return;
    h.cool = W.cool; SFX.shoot();
    G.shots.push({ x: h.x + h.w / 2 + h.face * 30 - 14, y: h.y + h.h * 0.55, w: 28, h: 28, vx: h.face * W.speed, vy: water() ? (W.vy || 0) * 0.3 : (W.vy || 0), t: 0, n: 0, wb: 0, hitSet: [] });
  }
  function endShot(s, W) {
    s.gone = true; spark(s.x + 14, s.y + 14);
    if (W.blast) {   // انفجار يضرب كل اللي حوله
      SFX.boom(); G.fx.push({ type: 'blast', x: s.x + 14, y: s.y + 14, r: W.blast, t: 0 });
      for (const e of G.enemies) if (!e.dead && e.on && Math.hypot(e.x + 30 - s.x - 14, e.y + 30 - s.y - 14) < W.blast) killEnemy(e);
      const b = G.boss; if (b && !b.dead && G.bossOn && Math.hypot(b.x + b.w / 2 - s.x, b.y + b.h / 2 - s.y) < W.blast + 60) hitBoss(1, false);
    }
  }
  function stepItems(dt) {
    const h = G.hero;
    for (const it of G.items) {
      if (it.rise < 1) { it.rise = Math.min(1, it.rise + dt * 2.2); it.y = it.r * T - it.h * it.rise - (it.rise >= 1 ? 0.5 : 0); if (it.rise >= 1 && it.type !== 'weapon') { it.sp = it.type === 'star' ? 230 : 150; it.vx = it.sp * it.dir; } }
      else { it.vy += (water() ? 500 : 2600) * dt; if (water() && it.vy > 160) it.vy = 160; moveBody(it, dt); if (it.hitWall) { it.dir = -it.dir; it.vx = (it.sp || 0) * it.dir; } if (it.type === 'star' && it.ground) it.vy = water() ? -300 : -780; if (it.y > VH + 200) it.gone = true; }
      if (!it.gone && it.rise > 0.5 && hit(h, it)) {
        it.gone = true; G.score += 1000; SFX.grow(); spark(it.x + 30, it.y + 30);
        if (it.type === 'grow') { if (G.power < 1) setPower(1); }
        else if (it.type === 'weapon') setPower(2);
        else if (it.type === 'life') { G.lives++; SFX.life(); }
        else if (it.type === 'star') { h.star = 10; starMusic(true); }
      }
    }
    G.items = G.items.filter(i => !i.gone);
    const W = G.stage.weapon;
    for (const s of G.shots) {
      s.t += dt; s.vy += (W.gravity || 0) * (water() ? 0.3 : 1) * dt;
      const nx = s.x + s.vx * dt + (s.vx > 0 ? s.w : 0), c = Math.floor(nx / T), r = Math.floor((s.y + s.h / 2) / T);
      if (solid(cell(c, r))) {
        if (W.breaks && cell(c, r) === 'B') breakBrick(c, r);
        if (W.wallBounce && s.wb < W.wallBounce) { s.wb++; s.vx = -s.vx; } else { endShot(s, W); continue; }
      }
      moveBody(s, dt);
      if (s.ground) { if (W.bounce && s.n < W.bounce) { s.vy = -620; s.n++; } else if (W.gravity) { endShot(s, W); continue; } }
      for (const e of G.enemies) if (!e.dead && e.on && hit(s, e) && !s.hitSet.includes(e)) { killEnemy(e); if (W.pierce) s.hitSet.push(e); else { endShot(s, W); break; } }
      const b = G.boss;
      if (!s.gone && b && !b.dead && G.bossOn && hit(s, b) && !s.hitSet.includes(b)) { if (W.blast) endShot(s, W); else { hitBoss(0.5, false); if (W.pierce) s.hitSet.push(b); else s.gone = true; } }
      if (s.t > (W.life || 2.5) || s.x < G.cam - 100 || s.x > G.cam + VW + 100 || s.y > VH) s.gone = true;
    }
    G.shots = G.shots.filter(x => !x.gone);
  }
  function addCoin() { G.coinsN++; SFX.coin(); if (G.coinsN % 100 === 0) { G.lives++; SFX.life(); } }
  function getCoin(k) { k.got = true; addCoin(); G.score += 100; spark(k.x, k.y); }
  const hit = (a, b) => a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
  function killHero() {
    const h = G.hero; if (h.dead || h.state !== 'play') return;
    h.dead = 0.001; h.vy = -900; h.vx = 0; h.star = 0; pauseAll(); music.playbackRate = 1; SFX.die(); G.lives--;
  }
  function stepEnemies(dt, I) {
    const h = G.hero;
    for (const e of G.enemies) {
      if (e.dead) { e.dead += dt; if (e.flip) { e.vy += 2600 * dt; e.y += e.vy * dt; } continue; }
      if (!e.on) { if (e.x < G.cam + VW + 150) e.on = true; else continue; }
      e.t += dt;
      if (e.type === 'fish') { e.x += e.vx * dt; e.y = e.y0 + Math.sin(e.t * 2) * 46; const c = Math.floor((e.x + (e.vx > 0 ? e.w + 4 : -4)) / T), r = Math.floor((e.y + 30) / T); if (solid(cell(c, r)) || Math.abs(e.x - e.x0) > 330) { e.vx = -e.vx; e.x += e.vx * dt * 2; } }
      else {
        e.vy += 3000 * dt; if (e.type === 'hop' && e.ground && e.t > 1.5) { e.vy = -820; e.t = 0; }
        moveBody(e, dt); if (e.hitWall) e.vx = -e.vx;
        for (const o of G.enemies) if (o !== e && !o.dead && o.on && o.type !== 'fish' && hit(e, o) && Math.sign(o.x - e.x) === Math.sign(e.vx)) e.vx = -e.vx;
        if (e.y > VH + 200) e.dead = 9;
      }
      if (hit(h, e)) {
        if (h.star > 0) killEnemy(e);
        else if (e.type !== 'fish' && h.vy > 120 && h.y + h.h - e.y < 46) { e.dead = 0.01; h.vy = I.jump ? -900 : -560; G.score += 100; SFX.stomp(); spark(e.x + 30, e.y); }
        else if (h.inv <= 0) { if (hurt()) return true; }
      }
    }
    return false;
  }
  function stepBoss(dt) {
    const b = G.boss, h = G.hero, A = G.L.boss; if (!b) return false;
    if (b.dead) { b.dead += dt; b.vy += 2200 * dt; b.y += b.vy * dt; return false; }
    if (!G.bossOn) { if (h.x > (A.from + 3) * T) { G.bossOn = true; playMusic('boss'); } else return false; }
    b.t += dt; if (b.inv > 0) b.inv -= dt; if (b.flash > 0) b.flash -= dt;
    const rage = 1 + (b.max - b.hp) * 0.22;
    b.dir = h.x + h.w / 2 < b.x + b.w / 2 ? -1 : 1; b.vx = b.dir * 120 * rage * (b.ground ? 1 : 2.2); b.vy += 2600 * dt;
    if (b.ground && b.t > 2.2 / rage) { b.vy = -1050; b.t = 0; }
    moveBody(b, dt); b.x = Math.max(A.from * T, Math.min(b.x, A.to * T - b.w));
    if (hit(h, b)) {
      if (h.star > 0) hitBoss(1, true);
      else if (h.vy > 120 && h.y + h.h - b.y < 60) { h.vy = -900; if (b.inv <= 0) hitBoss(1, true); }
      else if (h.inv <= 0 && b.inv <= 0.6) { if (hurt()) return true; h.vx = -b.dir * -500; }
    }
    return false;
  }

  function step(dt, I) {
    const h = G.hero, L = G.L, W = water(); G.t += dt;
    for (const f of G.fx) f.t += dt; G.fx = G.fx.filter(f => f.t < 0.9);
    if (h.dead) {
      h.dead += dt; if (h.dead > 0.4) { h.vy += 2600 * dt; h.y += h.vy * dt; }
      if (h.dead > 2.6) { if (G.lives <= 0) { G.mode = 'over'; G.msgT = 0; saveBest(); } else { G.power = 0; resetLevel(); playMusic(); } }
      return;
    }
    if (h.state === 'slide') {
      h.vx = 0; h.y = Math.min(h.y + 420 * dt, GROUND * T - h.h); h.slideT += dt;
      if (h.y >= GROUND * T - h.h && h.slideT > 0.6) { h.state = 'walk'; h.face = 1; }
      return;
    }
    if (h.state === 'walk') {
      h.vx = 260; h.vy += 3200 * dt; moveBody(h, dt); h.anim += dt * 9;
      const stop = G.stage.final ? (L.goalCol - 1.4) * T : (L.goalCol + 2.2) * T;
      if (h.x > stop) { h.state = 'done'; h.vx = 0; G.mode = 'clear'; G.msgT = 0; G.score += Math.floor(G.time) * 20; saveBest(); G.done[G.stageIndex] = 1; store.set('iwt_done', G.done); }
      return;
    }
    G.time -= dt; if (G.time <= 0) { G.time = 0; killHero(); return; }
    const dir = (I.right ? 1 : 0) - (I.left ? 1 : 0);
    if (W) {   // سباحة: كل ضغطة قفز دفعة لفوك
      const max = I.run ? 380 : 290;
      if (dir) { h.vx += dir * 900 * dt; h.face = dir; if (Math.abs(h.vx) > max) h.vx = Math.sign(h.vx) * max; } else { const f = 500 * dt; h.vx = Math.abs(h.vx) <= f ? 0 : h.vx - Math.sign(h.vx) * f; }
      if (I.jumpP) { h.vy = -430; SFX.swim(); G.fx.push({ type: 'bubble', x: h.x + h.w / 2, y: h.y + h.h, t: 0 }); }
      h.vy += 760 * dt; if (h.vy > 250) h.vy = 250;
    } else {
      const max = I.run ? 640 : 430, acc = h.ground ? 1700 : 1150;
      if (dir) { h.vx += dir * acc * (Math.sign(h.vx) === -dir ? 2.2 : 1) * dt; h.face = dir; if (Math.abs(h.vx) > max) h.vx -= Math.sign(h.vx) * Math.min(Math.abs(h.vx) - max, 1500 * dt); }
      else if (h.ground) { const f = 1800 * dt; h.vx = Math.abs(h.vx) <= f ? 0 : h.vx - Math.sign(h.vx) * f; }
      h.coyote = h.ground ? 0.09 : h.coyote - dt; h.buf = I.jumpP ? 0.12 : h.buf - dt;
      if (h.buf > 0 && h.coyote > 0) { h.vy = -960 - Math.abs(h.vx) * 0.12; h.ground = false; h.coyote = 0; h.buf = 0; SFX.jump(); }
      h.vy += (h.vy < 0 && I.jump ? 1450 : 3300) * dt; if (h.vy > 1350) h.vy = 1350;
    }
    if (h.x < G.cam && h.vx < 0) { h.x = G.cam; h.vx = 0; }
    if (L.boss && !G.bossDead && h.x + h.w > L.boss.to * T) { h.x = L.boss.to * T - h.w; h.vx = Math.min(0, h.vx); }   // حاجز الوحش
    if (h.star > 0) { h.star -= dt; if (h.star <= 0) { h.star = 0; starMusic(false); } }
    if (h.vy < 0) {   // حجر مخفي
      const hc = Math.floor((h.x + h.w / 2) / T), hr = Math.floor((h.y + h.vy * dt) / T);
      if (cell(hc, hr) === 'H' && h.y >= (hr + 1) * T - 2) { h.y = (hr + 1) * T; h.vy = 0; bump(hc, hr); }
    }
    moveBody(h, dt, bump);
    h.anim += (W ? 120 + Math.abs(h.vx) : Math.abs(h.vx)) * dt / 34; if (h.inv > 0) h.inv -= dt; if (h.cool > 0) h.cool -= dt;
    if (I.fire) fire();
    stepItems(dt);
    if (h.y > VH + 200) { killHero(); return; }
    if (L.checkpoint && h.x > L.checkpoint * T) G.respawnCol = Math.max(G.respawnCol, L.checkpoint);
    for (const k of G.coins) if (!k.got && Math.abs(k.x - (h.x + h.w / 2)) < 50 && Math.abs(k.y - (h.y + h.h / 2)) < h.h / 2 + 26) getCoin(k);
    if (stepEnemies(dt, I)) return;
    if (stepBoss(dt)) return;
    // دخول وخروج المجاري
    if (L.sewer && !G.main && h.ground && I.down && h.x + h.w / 2 > L.sewer.c * T + 10 && h.x + h.w / 2 < (L.sewer.c + 2) * T - 10 && h.y + h.h < (GROUND - 1) * T) { enterSewer(); return; }
    if (L.kind === 'sewer' && h.x + h.w >= L.exitCol * T - 3 && h.y + h.h > (GROUND - 3) * T) { exitSewer(); return; }
    // العلم
    if (h.x + h.w > L.flagCol * T + T / 2 - 8 && h.state === 'play') {
      h.state = 'slide'; h.x = L.flagCol * T + T / 2 - h.w - 2; h.vx = 0; h.vy = 0; h.slideT = 0;
      const height = Math.max(0, GROUND * T - (h.y + h.h)); G.score += 100 + Math.round(height / T) * 400; h.star = 0; pauseAll(); music.playbackRate = 1; SFX.win();
    }
    let target = h.x - VW * 0.4;
    if (L.kind === 'sewer' || G.bossOn && !G.bossDead) { target = h.x - VW * 0.5; G.cam += (target - G.cam) * Math.min(1, dt * 6); }
    else if (target > G.cam) G.cam += Math.min(target - G.cam, 900 * dt + (target - G.cam) * 0.12);
    G.cam = Math.max(0, Math.min(G.cam, L.width * T - VW));
  }
  function saveBest() { if (G.score > G.best) { G.best = G.score; store.set('iwt_best', G.best); } }

  // ---------- الرسم ----------
  function img(key, x, y, w, h, color, sx, sy, sw, sh) {
    const i = IMG[key];
    if (i) { if (sw) ctx.drawImage(i, sx, sy, sw, sh, x, y, w, h); else ctx.drawImage(i, x, y, w, h); }
    else { ctx.fillStyle = color || '#f0f'; ctx.fillRect(x, y, w, h); }
  }
  function parallax(key, f) {
    const i = IMG[key]; if (!i) return; const w = i.width * VH / i.height; let x = -((G.cam * f) % w);
    for (; x < VW; x += w) ctx.drawImage(i, Math.floor(x), 0, Math.ceil(w) + 1, VH);
  }
  function text(s, x, y, size, color = '#fff', align = 'center', weight = 800) {
    ctx.font = `${weight} ${size}px ${FONT}`; ctx.textAlign = align; ctx.textBaseline = 'middle'; ctx.direction = 'rtl';
    ctx.lineJoin = 'round'; ctx.lineWidth = Math.max(4, size / 7); ctx.strokeStyle = 'rgba(0,0,0,.75)'; ctx.strokeText(s, x, y); ctx.fillStyle = color; ctx.fillText(s, x, y);
  }
  const rnd = i => { const x = Math.sin(i * 127.1) * 43758.5453; return x - Math.floor(x); };
  function drawWorld() {
    const L = G.L, cam = Math.round(G.cam), V = VARIANT[G.stage.variant] || VARIANT.day, sew = L.kind === 'sewer', W = water(), h = G.hero;
    if (sew) {
      const g = ctx.createLinearGradient(0, 0, 0, VH); g.addColorStop(0, '#10140f'); g.addColorStop(1, '#232b1c'); ctx.fillStyle = g; ctx.fillRect(0, 0, VW, VH);
      ctx.globalAlpha = 0.16; for (let x = -((cam * 0.5) % 144); x < VW; x += 144) for (let y = 144; y < 936; y += 144) img('brick', x, y, 144, 144, '#333'); ctx.globalAlpha = 1;
    } else {
      ctx.fillStyle = G.stage.sky; ctx.fillRect(0, 0, VW, VH); parallax('bg_far', 0.15);
      if (V.night) { ctx.fillStyle = '#fff'; for (let i = 0; i < 90; i++) { const tw = 0.5 + 0.5 * Math.sin(G.t * 2 + i); ctx.globalAlpha = 0.4 + 0.6 * tw; ctx.fillRect(rnd(i) * VW, rnd(i + 200) * 560, 4, 4); } ctx.globalAlpha = 1; ctx.fillStyle = '#f4f1d8'; ctx.beginPath(); ctx.arc(1500, 190, 76, 0, 7); ctx.fill(); ctx.fillStyle = 'rgba(244,241,216,.14)'; ctx.beginPath(); ctx.arc(1500, 190, 150, 0, 7); ctx.fill(); }
      parallax('bg_mid', 0.4);
      if (V.fog) { const g = ctx.createLinearGradient(0, 300, 0, 940); g.addColorStop(0, 'rgba(255,240,236,0)'); g.addColorStop(1, 'rgba(255,240,236,.6)'); ctx.fillStyle = g; ctx.fillRect(0, 300, VW, 640); }
      if (V.glare) { const g = ctx.createRadialGradient(960, -100, 50, 960, -100, 1100); g.addColorStop(0, 'rgba(255,252,220,.75)'); g.addColorStop(1, 'rgba(255,252,220,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, VW, VH); }
      if (W) { ctx.fillStyle = 'rgba(8,60,120,.45)'; ctx.fillRect(0, 0, VW, VH); }
    }
    ctx.save(); ctx.translate(-cam, 0);
    if (L.goalCol < 9000) {
      img('goal', L.goalCol * T, GROUND * T - 5 * T, 5 * T, 5 * T, '#b25a3c');
      if (G.stage.final) img('friend', (L.goalCol - 0.4) * T, GROUND * T - 150 + Math.sin(G.t * 3) * 3, 112, 150, '#1f8f8f');
      img('flag', L.flagCol * T + T / 2 - T, GROUND * T - 9 * T, 2 * T, 9 * T, '#eee');
    }
    const c0 = Math.max(0, Math.floor(cam / T) - 2), c1 = Math.min(L.width - 1, c0 + Math.ceil(VW / T) + 3);
    const bounce = {}; G.fx.forEach(f => { if (f.type === 'bounce' && f.t < 0.18) bounce[f.c + ',' + f.r] = -Math.sin(f.t / 0.18 * Math.PI) * 18; });
    for (let r = 0; r < ROWS; r++) for (let c = c0; c <= c1; c++) {
      const ch = L.grid[r][c]; if (ch === '.' || ch === 'P' || ch === 'H') continue;
      const x = c * T, y = r * T + (bounce[c + ',' + r] || 0);
      if (ch === '#') img(r > 0 && L.grid[r - 1][c] === '#' ? 'ground_fill' : 'ground_top', x, y, T + 1, T + 1, '#8b5a2b');
      else if (ch === 'B') img('brick', x, y, T, T, '#c0392b');
      else if (ch === '?' || ch === 'M' || ch === 'T') img('box', x, y, T, T, GOLD);
      else if (ch === 'U') img('box_used', x, y, T, T, '#786046');
      else if (ch === 'S') img('block', x, y, T, T, '#968a7c');
    }
    for (const p of L.pipes) {
      if ((p.c + 2) * T < cam || p.c * T > cam + VW) continue;
      const top = (GROUND - p.h) * T;
      for (let i = 1; i < p.h; i++) img('pipe_body', p.c * T, top + i * T, 2 * T, T + 1, '#2ea060');
      img('pipe_top', p.c * T, top, 2 * T, T, '#2ea060');
    }
    if (L.sewer && !G.main) { const px = (L.sewer.c + 1) * T, py = (GROUND - 2) * T - 70 + Math.sin(G.t * 5) * 10; ctx.fillStyle = GOLD; ctx.strokeStyle = '#000'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(px - 26, py); ctx.lineTo(px + 26, py); ctx.lineTo(px, py + 38); ctx.closePath(); ctx.stroke(); ctx.fill(); }
    if (L.kind === 'sewer') { const px = L.exitCol * T - 60 + Math.sin(G.t * 5) * 10, py = (GROUND - 1) * T - 20; ctx.fillStyle = GOLD; ctx.beginPath(); ctx.moveTo(px, py - 26); ctx.lineTo(px, py + 26); ctx.lineTo(px + 38, py); ctx.closePath(); ctx.fill(); }
    const cf = Math.floor(G.t * 9) % 4;
    for (const k of G.coins) if (!k.got && k.x > cam - T && k.x < cam + VW + T) img('coin', k.x - 30, k.y - 30, 60, 60, GOLD, cf * 128, 0, 128, 128);
    for (const e of G.enemies) {
      if (e.x < cam - 200 || e.x > cam + VW + 200 || e.dead > 0.5 && !e.flip || e.dead > 3) continue;
      const fr = e.dead && !e.flip ? 2 : Math.floor(G.t * (e.type === 'fast' ? 11 : 6)) % 2, s = e.type === 'fast' ? 0.86 : 1;
      ctx.save(); ctx.translate(e.x + e.w / 2, e.y + e.h / 2); ctx.scale((e.vx > 0 ? 1 : -1) * s, (e.flip ? -1 : 1) * s);
      img(e.type === 'fish' ? 'enemy_water' : 'enemy1', -42, -54, 84, 84, '#6a4428', fr * 128, 0, 128, 128); ctx.restore();
    }
    const b = G.boss;
    if (b && b.dead < 3 && !(b.inv > 0 && Math.floor(G.t * 16) % 2)) {
      ctx.save(); ctx.translate(b.x + b.w / 2, b.y + b.h); ctx.scale(b.dir > 0 ? 1 : -1, 1); if (b.dead) { ctx.translate(0, -b.h / 2); ctx.rotate(b.dead * 4); ctx.translate(0, b.h / 2); }
      if (b.flash > 0) ctx.filter = 'brightness(2.2)';
      img('boss', -120, -226, 240, 240, '#933', (b.dead ? 2 : Math.floor(G.t * 5) % 2) * 256, 0, 256, 256); ctx.restore();
    }
    if (!(h.inv > 0 && Math.floor(G.t * 20) % 2)) {
      let fr = 0; if (h.dead || !h.ground && h.state !== 'slide' && !W) fr = 4; else if (W || Math.abs(h.vx) > 20 || h.state === 'walk') fr = 1 + Math.floor(h.anim) % 3;
      const k = G.power ? 1.2 : 0.78, dw = 108 * k, dh = 144 * k;
      ctx.save(); ctx.translate(h.x + h.w / 2, h.y + h.h); ctx.scale(h.face, 1);
      if (W && !h.dead) { ctx.translate(0, -h.h / 2); ctx.rotate(0.5 + Math.max(-0.3, Math.min(0.4, h.vy / 700))); ctx.translate(0, h.h / 2); }
      if (h.star > 0 && (h.star > 2.5 || Math.floor(G.t * 10) % 2)) { ctx.shadowColor = Math.floor(G.t * 12) % 2 ? '#fff3a0' : GOLD; ctx.shadowBlur = 46; ctx.filter = 'brightness(1.35) saturate(1.3)'; }
      img('hero', -dw / 2 - 6 * k, -dh + 10 * k, dw, dh, '#111', fr * 192, 0, 192, 256);
      if (G.power === 2 && !h.dead) img('item_weapon', 6, -h.h * 0.52, 46, 46, GOLD);
      ctx.restore();
    }
    for (const it of G.items) {
      ctx.save(); ctx.beginPath(); ctx.rect(it.x - 20, it.r * T - 200, 110, it.rise < 1 ? 200 : 2000); ctx.clip();
      img('item_' + it.type, it.x - 6, it.y - 12, 72, 72, it.type === 'grow' || it.type === 'life' ? '#e33' : GOLD); ctx.restore();
    }
    for (const sh of G.shots) { ctx.save(); ctx.translate(sh.x + 14, sh.y + 14); ctx.rotate(sh.t * 14 * Math.sign(sh.vx)); img('shot', -24, -24, 48, 48, '#fff'); ctx.restore(); }
    if (h.star > 0) { ctx.fillStyle = '#fff3a0'; for (let i = 0; i < 5; i++) { const a = G.t * 5 + i * 1.256, rr = 62 + Math.sin(G.t * 9 + i) * 10; ctx.fillRect(h.x + h.w / 2 + Math.cos(a) * rr - 5, h.y + h.h / 2 + Math.sin(a) * rr * 1.2 - 5, 10, 10); } }
    for (const f of G.fx) {
      if (f.type === 'pop') { const y = f.y - 40 - Math.sin(Math.min(1, f.t / 0.45) * Math.PI) * 150; if (f.t < 0.45) img('coin', f.x - 30, y - 30, 60, 60, GOLD, (Math.floor(f.t * 30) % 4) * 128, 0, 128, 128); }
      else if (f.type === 'shard') { const x = f.x + f.vx * f.t, y = f.y + f.vy * f.t + 1600 * f.t * f.t; ctx.save(); ctx.translate(x, y); ctx.rotate(f.t * 12); img('brick', -18, -18, 36, 36, '#c0392b', 0, 0, 64, 64); ctx.restore(); }
      else if (f.type === 'spark') { ctx.globalAlpha = Math.max(0, 1 - f.t * 2.5); ctx.fillStyle = '#fff3c4'; for (let i = 0; i < 6; i++) { const a = i * Math.PI / 3, d = 20 + f.t * 220; ctx.fillRect(f.x + Math.cos(a) * d - 5, f.y + Math.sin(a) * d - 5, 10, 10); } ctx.globalAlpha = 1; }
      else if (f.type === 'blast') { ctx.globalAlpha = Math.max(0, 1 - f.t * 2.2); ctx.fillStyle = '#ffd24a'; ctx.beginPath(); ctx.arc(f.x, f.y, f.r * Math.min(1, f.t * 5), 0, 7); ctx.fill(); ctx.fillStyle = '#ff6a2a'; ctx.beginPath(); ctx.arc(f.x, f.y, f.r * 0.6 * Math.min(1, f.t * 5), 0, 7); ctx.fill(); ctx.globalAlpha = 1; }
      else if (f.type === 'bubble') { ctx.globalAlpha = Math.max(0, 1 - f.t * 1.2); ctx.strokeStyle = '#dff'; ctx.lineWidth = 3; for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.arc(f.x + (i - 1) * 16, f.y - f.t * 160 - i * 12, 7 + i * 2, 0, 7); ctx.stroke(); } ctx.globalAlpha = 1; }
    }
    ctx.restore();
    if (W) {   // مي: لون أزرق، أشعة ضوء وفقاعات
      ctx.fillStyle = 'rgba(20,110,190,.26)'; ctx.fillRect(0, 0, VW, VH);
      ctx.fillStyle = 'rgba(200,240,255,.07)'; for (let i = 0; i < 6; i++) { const x = ((i * 380 - cam * 0.3 + Math.sin(G.t + i) * 40) % 2280 + 2280) % 2280 - 180; ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x + 120, 0); ctx.lineTo(x - 80, VH); ctx.lineTo(x - 280, VH); ctx.fill(); }
      ctx.strokeStyle = 'rgba(220,245,255,.5)'; ctx.lineWidth = 3; for (let i = 0; i < 24; i++) { const x = (rnd(i) * 2400 - cam * 0.6) % 2000, y = VH - ((G.t * (60 + rnd(i + 9) * 80) + rnd(i + 5) * VH) % VH); ctx.beginPath(); ctx.arc((x + 2000) % 2000, y, 5 + rnd(i + 3) * 8, 0, 7); ctx.stroke(); }
    }
    if (sew) { const g = ctx.createRadialGradient(h.x + h.w / 2 - cam, h.y + h.h / 2, 200, h.x + h.w / 2 - cam, h.y + h.h / 2, 1000); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,.72)'); ctx.fillStyle = g; ctx.fillRect(0, 0, VW, VH); }
    else if (V.mul) { ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = V.mul; ctx.fillRect(0, 0, VW, VH); ctx.globalCompositeOperation = 'source-over'; }
  }
  function hud() {
    const g = ctx.createLinearGradient(0, 0, 0, 120); g.addColorStop(0, 'rgba(0,0,0,.55)'); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, VW, 120);
    text(G.L.kind === 'sewer' ? G.stage.cityName + '  تحت الأرض' : G.stage.name, VW - 40, 46, 36, GOLD, 'right');
    text(String(G.score).padStart(6, '0'), 1250, 46, 36, '#fff', 'right');
    img('coin', 880, 18, 56, 56, GOLD, 0, 0, 128, 128); text('× ' + G.coinsN, 950, 46, 36, '#fff', 'left');
    text('♥ ' + G.lives, 470, 46, 38, '#ff6b6b', 'left');
    if (G.power >= 1) img('item_grow', 600, 18, 56, 56, '#e33');
    if (G.power >= 2) { img('item_weapon', 664, 18, 56, 56, GOLD); text('Z', 740, 48, 30, GOLD, 'left'); }
    if (G.hero.star > 0) { img('item_star', 780, 20, 52, 52, GOLD); ctx.fillStyle = 'rgba(0,0,0,.5)'; ctx.fillRect(776, 80, 60, 10); ctx.fillStyle = GOLD; ctx.fillRect(776, 80, 60 * G.hero.star / 10, 10); }
    text('الوقت  ' + Math.ceil(G.time), 50, 46, 36, G.time < 60 ? '#ff6b6b' : '#fff', 'left');
    const b = G.boss;
    if (b && G.bossOn && !b.dead) { text(G.stage.bossName, VW / 2, 130, 40, '#ff8a70'); ctx.fillStyle = 'rgba(0,0,0,.6)'; ctx.fillRect(VW / 2 - 304, 160, 608, 30); ctx.fillStyle = '#e0452f'; ctx.fillRect(VW / 2 - 300, 164, 600 * Math.max(0, b.hp) / b.max, 22); }
    if (G.L.sewer && !G.main && Math.abs(G.hero.x - (G.L.sewer.c + 1) * T) < 500) text('اوكف فوك الأنبوب واضغط السهم لجوه للنزول للمجاري', VW / 2, 220, 34, '#fff');
  }
  function panel(title, lines, hint) {
    ctx.fillStyle = 'rgba(8,6,3,.72)'; ctx.fillRect(0, 0, VW, VH);
    ctx.fillStyle = 'rgba(28,25,19,.95)'; ctx.strokeStyle = GOLD; ctx.lineWidth = 4; ctx.beginPath(); ctx.roundRect(VW / 2 - 620, 250, 1240, 560, 28); ctx.fill(); ctx.stroke();
    text(title, VW / 2, 350, 76, GOLD); lines.forEach((l, i) => text(l, VW / 2, 470 + i * 70, 42, '#f1e9d6', 'center', 600));
    if (Math.floor(G.msgT * 2) % 2 === 0) text(hint, VW / 2, 740, 40, '#fff');
  }
  function backdrop() {
    const g = ctx.createLinearGradient(0, 0, 0, VH); g.addColorStop(0, '#1a1509'); g.addColorStop(1, '#0a0806'); ctx.fillStyle = g; ctx.fillRect(0, 0, VW, VH);
    ctx.strokeStyle = 'rgba(212,175,55,.14)'; ctx.lineWidth = 2; for (let i = 0; i < 9; i++) { ctx.beginPath(); ctx.ellipse(VW / 2, 1500, 500 + i * 190, 420 + i * 150, 0, Math.PI, 2 * Math.PI); ctx.stroke(); }
  }
  function title() {
    backdrop(); ctx.direction = 'ltr'; ctx.font = `900 190px ${FONT}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const tg = ctx.createLinearGradient(0, 250, 0, 430); tg.addColorStop(0, '#fff1b0'); tg.addColorStop(0.5, GOLD); tg.addColorStop(1, '#8f7524');
    ctx.fillStyle = 'rgba(0,0,0,.6)'; ctx.fillText('IBRA', VW / 2 + 8, 298); ctx.fillStyle = tg; ctx.fillText('IBRA', VW / 2, 290);
    ctx.font = `800 96px ${FONT}`; ctx.fillStyle = '#f1e9d6'; ctx.fillText('W O R L D   T O U R', VW / 2, 440);
    text('جولة حول مدن العالم', VW / 2, 540, 48, GOLD, 'center', 600);
    if (Math.floor(G.msgT * 2) % 2 === 0) text('اضغط Enter للبدء', VW / 2, 700, 56);
    text('الأسهم أو A / D للحركة   •   Space للقفز   •   Shift للركض   •   Z للضرب   •   P توقف   •   M كتم الصوت', VW / 2, 850, 32, '#a89d85', 'center', 500);
    if (G.best) text('أعلى نتيجة  ' + G.best, VW / 2, 930, 30, '#f1e9d6', 'center', 600);
    text('تصميم وتطوير إبراهيم الخزرجي   •   t.me/ibraprogram', VW / 2, 1020, 28, '#8f7524', 'center', 500);
  }
  // شاشة اختيار المرحلة: صف لكل مدينة و8 جولات
  function select(I) {
    const cur = STAGES[G.sel]; let w = cur.world, r = cur.round;
    if (I.mU) w = (w + 6) % 7; if (I.mD) w = (w + 1) % 7;
    if (w === 0) r = 1; else { if (I.mL) r = Math.min(8, r + 1); if (I.mR) r = Math.max(1, r - 1); }
    G.sel = w === 0 ? 0 : 1 + (w - 1) * 8 + (r - 1);
    backdrop(); text('اختار المرحلة', VW / 2, 80, 64, GOLD);
    const cw = 176, xr = VW - 330, y0 = 190, rh = 112;   // العمود الأول يمين (الواجهة عربية)
    for (let i = 0; i < 8; i++) text(ROUND_LABELS[i], xr - i * cw - cw / 2, y0 - 44, 28, '#a89d85', 'center', 600);
    for (let wi = 0; wi < 7; wi++) {
      const y = y0 + wi * rh; text(CITY_NAMES[wi], VW - 60, y + 42, 42, wi === w ? GOLD : '#f1e9d6', 'right');
      for (let ri = 0; ri < (wi === 0 ? 1 : 8); ri++) {
        const idx = wi === 0 ? 0 : 1 + (wi - 1) * 8 + ri, x = xr - (ri + 1) * cw + 8, on = idx === G.sel;
        ctx.fillStyle = on ? GOLD : G.done[idx] ? 'rgba(60,110,70,.9)' : 'rgba(40,36,28,.95)'; ctx.strokeStyle = on ? '#fff' : '#5a5040'; ctx.lineWidth = on ? 5 : 2;
        ctx.beginPath(); ctx.roundRect(x, y, cw - 16, 84, 14); ctx.fill(); ctx.stroke();
        text(wi === 0 ? 'تدريب' : wi + '-' + (ri + 1), x + (cw - 16) / 2, y + 42, 36, on ? '#1a1509' : '#f1e9d6');
        if (G.done[idx]) text('✓', x + 26, y + 22, 24, '#bff5c8');
      }
    }
    text(STAGES[G.sel].name + '   •   ' + (STAGES[G.sel].tod || ''), VW / 2, 1000, 38, '#fff');
    text('الأسهم للتنقل   •   Enter للدخول   •   Esc رجوع', VW / 2, 1050, 26, '#a89d85', 'center', 500);
    if (I.back) G.mode = 'title'; else if (I.enter) startStage(G.sel);
  }

  // ---------- الحلقة ----------
  let last = performance.now(), accT = 0; const DT = 1 / 120;
  function frame(now) {
    const d = Math.min(0.1, (now - last) / 1000); last = now; G.msgT += d;
    const enter = pressed.Enter || pressed.NumpadEnter, I = input(); I.enter = enter || (I.start && !I.jumpP);
    if (G.mode === 'title') { title(); if (I.start) G.mode = 'select'; }
    else if (G.mode === 'select') select(I);
    else if (G.mode === 'loading') { ctx.fillStyle = '#0a0806'; ctx.fillRect(0, 0, VW, VH); text(G.stage.name, VW / 2, VH / 2 - 40, 64, GOLD); text(G.stage.tod || '', VW / 2, VH / 2 + 50, 36, '#f1e9d6', 'center', 500); }
    else if (G.mode === 'play') {
      if (I.pause && !G.hero.dead) { G.mode = 'pause'; pauseAll(); }
      accT += d; let first = true;
      while (accT >= DT) { step(DT, first ? I : Object.assign({}, I, { jumpP: false, fire: false })); first = false; accT -= DT; if (G.mode !== 'play') break; }
      drawWorld(); hud();
    }
    else if (G.mode === 'pause') { drawWorld(); hud(); panel('توقف مؤقت', ['P للرجوع للعب   •   Q لاختيار مرحلة ثانية', 'F5 يعيد تحميل التصاميم   •   F2 يفتح مجلد التصاميم'], 'اضغط P للمتابعة'); if (I.quit) G.mode = 'select'; else if (I.pause) { G.mode = 'play'; resumeMusic(); } }
    else if (G.mode === 'clear') {
      const st = G.stage, nx = STAGES[G.stageIndex + 1]; drawWorld(); hud();
      if (st.final) panel('أخيراً التقيتوا!', ['لفّيت العالم كله ووصلت لصديقتك بنيويورك', 'النقاط: ' + G.score + '     العملات: ' + G.coinsN], 'اضغط Enter للرجوع للقائمة');
      else if (st.variant === 'boss') panel('هزمت ' + st.bossName + '!', ['لكن صديقتك مو هنا... سافرت إلى ' + st.nextCity, 'النقاط: ' + G.score + '     العملات: ' + G.coinsN], 'اضغط Enter للسفر إلى ' + st.nextCity);
      else panel('أحسنت! خلصت المرحلة', ['النقاط: ' + G.score + '     العملات: ' + G.coinsN, 'المحطة الجاية: ' + (nx ? nx.name : '')], 'اضغط Enter للمحطة الجاية');
      if (I.start && G.msgT > 1) { if (nx && !st.final) startStage(G.stageIndex + 1, true); else G.mode = 'title'; }
    }
    else if (G.mode === 'over') { drawWorld(); panel('انتهت المحاولات', ['النقاط: ' + G.score], 'اضغط Enter للمحاولة من جديد'); if (I.start && G.msgT > 1) G.mode = 'select'; }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
