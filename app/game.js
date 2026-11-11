/* IBRA World Tour — محرك اللعبة. دقة داخلية 1920×1080، البلاطة 72px والصور الأصلية 128px حتى تبقى واضحة لحد 4K. */
(() => {
  const VW = 1920, VH = 1080, T = 72, ROWS = 15, GROUND = 13;
  const cv = document.getElementById('c'), ctx = cv.getContext('2d');
  const GOLD = '#d4af37';
  const FONT = '"Segoe UI",Tahoma,"Noto Sans Arabic",Arial,sans-serif';

  // ---------- تكبير الشاشة ----------
  function fit() {
    const dpr = window.devicePixelRatio || 1;
    const s = Math.min(innerWidth / VW, innerHeight / VH);
    cv.style.width = Math.floor(VW * s) + 'px'; cv.style.height = Math.floor(VH * s) + 'px';
    const pw = Math.min(3840, Math.round(VW * s * dpr)), ph = Math.round(pw * VH / VW);
    if (cv.width !== pw) { cv.width = pw; cv.height = ph; }
    ctx.setTransform(cv.width / VW, 0, 0, cv.height / VH, 0, 0);
    ctx.imageSmoothingQuality = 'high';
  }
  addEventListener('resize', fit); fit();

  // ---------- تحميل الصور (الناقص ينرسم مستطيل بديل) ----------
  const IMG = {};
  const FILES = { ground_top: 'ground_top.png', ground_fill: 'ground_fill.png', brick: 'brick.png', box: 'box.png', box_used: 'box_used.png', block: 'block.png', pipe_top: 'pipe_top.png', pipe_body: 'pipe_body.png', coin: 'coin.png', enemy1: 'enemy1.png', flag: 'flag.png', goal: 'goal.png', bg_far: 'bg_far.jpg', bg_mid: 'bg_mid.png', item_grow: 'item_grow.png', item_weapon: 'item_weapon.png', shot: 'shot.png' };
  function loadImg(key, src) {
    return new Promise(res => { const i = new Image(); i.onload = () => { IMG[key] = i; res(); }; i.onerror = () => { IMG[key] = null; res(); }; i.src = src + '?v=' + Date.now(); });
  }
  function loadStage(st) {
    const jobs = Object.entries(FILES).map(([k, f]) => loadImg(k, `assets/${st.id}/${f}`));
    jobs.push(loadImg('hero', `assets/hero/${st.id}.png`));
    return Promise.all(jobs);
  }

  // ---------- الصوت ----------
  let AC = null, muted = false; const music = new Audio(); music.loop = true; music.volume = 0.55;
  function ac() { if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { } } return AC; }
  function beep(f0, f1, dur, type = 'square', vol = 0.12) {
    const a = ac(); if (!a || muted) return;
    const o = a.createOscillator(), g = a.createGain(), t = a.currentTime;
    o.type = type; o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(Math.max(30, f1), t + dur);
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.001, t + dur);
    o.connect(g).connect(a.destination); o.start(t); o.stop(t + dur);
  }
  const SFX = {
    jump: () => beep(330, 760, 0.18), coin: () => { beep(988, 988, 0.07); setTimeout(() => beep(1319, 1319, 0.22), 70); },
    stomp: () => beep(420, 90, 0.16, 'triangle', 0.25), bump: () => beep(160, 110, 0.09, 'triangle', 0.25),
    brk: () => beep(220, 50, 0.22, 'sawtooth', 0.14), die: () => beep(520, 70, 0.8, 'triangle', 0.22),
    win: () => [523, 659, 784, 1047].forEach((f, i) => setTimeout(() => beep(f, f, 0.22), i * 140)), life: () => [659, 784, 1319].forEach((f, i) => setTimeout(() => beep(f, f, 0.14), i * 90)),
    grow: () => [392, 523, 659, 784, 1047].forEach((f, i) => setTimeout(() => beep(f, f, 0.09), i * 60)), shrink: () => [784, 587, 440, 330].forEach((f, i) => setTimeout(() => beep(f, f, 0.1, 'triangle', 0.2), i * 70)),
    shoot: () => beep(900, 300, 0.1, 'square', 0.1), item: () => beep(200, 600, 0.35, 'triangle', 0.2)
  };
  function playMusic(st) { music.src = `assets/${st.id}/music.mp3`; music.muted = muted; music.play().catch(() => { }); }

  // ---------- الإدخال ----------
  const keys = {}; let pressed = {};
  addEventListener('keydown', e => {
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'].includes(e.code)) e.preventDefault();
    if (!keys[e.code]) pressed[e.code] = true; keys[e.code] = true; ac();
    if (e.code === 'KeyM') { muted = !muted; music.muted = muted; }
    if (e.code === 'F5') { e.preventDefault(); if (G.stage) loadStage(G.stage); }
    if (e.code === 'F2' && window.ibra) window.ibra.openAssets();
    if (e.code === 'F11' && window.ibra) { e.preventDefault(); window.ibra.toggleFullscreen(); }
  });
  addEventListener('keyup', e => { keys[e.code] = false; });
  let padPrev = {};
  function input() {
    const p = (navigator.getGamepads ? [...navigator.getGamepads()].find(x => x) : null);
    const pb = i => !!(p && p.buttons[i] && p.buttons[i].pressed), ax = p ? p.axes[0] : 0;
    const now = { jump: pb(0) || pb(1), start: pb(9), fire: pb(2) };
    const st = {
      left: keys.ArrowLeft || keys.KeyA || ax < -0.4 || pb(14), right: keys.ArrowRight || keys.KeyD || ax > 0.4 || pb(15),
      jump: keys.Space || keys.ArrowUp || keys.KeyW || now.jump, run: keys.ShiftLeft || keys.ShiftRight || keys.KeyX || pb(3) || pb(5) || pb(7),
      jumpP: pressed.Space || pressed.ArrowUp || pressed.KeyW || (now.jump && !padPrev.jump),
      start: pressed.Enter || pressed.NumpadEnter || pressed.Space || (now.start && !padPrev.start) || (now.jump && !padPrev.jump),
      pause: pressed.KeyP || pressed.Escape || (now.start && !padPrev.start),
      fire: pressed.KeyZ || pressed.KeyF || pressed.ControlLeft || pressed.ControlRight || (now.fire && !padPrev.fire)
    };
    padPrev = now; pressed = {}; return st;
  }

  // ---------- الحالة ----------
  const G = { mode: 'title', stageIndex: 0, stage: null, L: null, hero: null, enemies: [], coins: [], fx: [], cam: 0, score: 0, coinsN: 0, lives: 3, time: 0, t: 0, msgT: 0, respawnCol: 2, power: 0, items: [], shots: [] };
  window.__game = G;
  try { G.best = +localStorage.getItem('iwt_best') || 0; } catch (e) { G.best = 0; }

  const HH = [76, 124, 124];   // ارتفاع البطل: صغير، كبير، مسلح
  const solid = ch => ch === '#' || ch === 'B' || ch === '?' || ch === 'M' || ch === 'U' || ch === 'S' || ch === 'P';
  function cell(c, r) { if (r < 0) return '.'; if (r >= ROWS || c < 0 || c >= G.L.width) return c < 0 || c >= G.L.width ? 'S' : '.'; return G.L.grid[r][c]; }

  async function startStage(i, keep) {
    G.mode = 'loading'; G.stageIndex = i; G.stage = STAGES[i];
    await loadStage(G.stage);
    if (!keep) { G.score = 0; G.coinsN = 0; G.lives = 3; G.respawnCol = 2; G.power = 0; }
    resetLevel(); playMusic(G.stage); G.mode = 'play';
  }
  function resetLevel() {
    const L = G.L = G.stage.level();
    G.enemies = L.enemies.map(e => ({ x: e.c * T + 6, y: (e.row + 1) * T - 60, w: 60, h: 60, vx: -110, vy: 0, dead: 0, on: false }));
    G.coins = L.coins.map(c => ({ x: c.c * T + T / 2, y: c.row * T + T / 2, got: false }));
    G.fx = []; G.items = []; G.shots = []; G.time = G.stage.time; G.t = 0;
    G.hero = { x: G.respawnCol * T, y: GROUND * T - HH[G.power], w: 44, h: HH[G.power], cool: 0, vx: 0, vy: 0, ground: false, face: 1, anim: 0, dead: 0, inv: 0, coyote: 0, buf: 0, state: 'play', slideT: 0 };
    G.cam = Math.max(0, G.hero.x - VW * 0.4);
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
      else if (b.vy < 0) {
        b.y = (r + 1) * T; b.vy = 0;
        if (onBump) { const mid = Math.floor((b.x + b.w / 2) / T); onBump(solid(cell(mid, r)) ? mid : c, r); onBump = null; }
      }
    }
  }
  function bump(c, r) {
    const ch = cell(c, r), g = G.L.grid;
    G.enemies.forEach(e => { if (!e.dead && e.ground && Math.abs(e.y + e.h - r * T) < 4 && e.x + e.w > c * T && e.x < (c + 1) * T) { e.dead = 0.01; e.vy = -500; e.flip = true; G.score += 100; } });
    G.coins.forEach(k => { if (!k.got && Math.floor(k.x / T) === c && Math.floor(k.y / T) === r - 1) getCoin(k); });
    if (ch === 'M') {
      g[r][c] = 'U'; G.fx.push({ type: 'bounce', c, r, t: 0 }); SFX.item();
      const type = G.power === 0 ? 'grow' : 'weapon';
      G.items.push({ type, x: c * T + 6, y: r * T, w: 60, h: 60, vx: 0, vy: 0, rise: 0, r, dir: G.hero.face });
    }
    else if (ch === '?') { g[r][c] = 'U'; G.fx.push({ type: 'pop', x: c * T + T / 2, y: r * T, t: 0 }); G.fx.push({ type: 'bounce', c, r, t: 0 }); addCoin(); G.score += 200; }
    else if (ch === 'B' && G.power === 0) { SFX.bump(); G.fx.push({ type: 'bounce', c, r, t: 0 }); }
    else if (ch === 'B') { breakBrick(c, r); }
    else SFX.bump();
  }
  function breakBrick(c, r) {
    G.L.grid[r][c] = '.'; SFX.brk(); G.score += 50;
    for (let i = 0; i < 4; i++) G.fx.push({ type: 'shard', x: c * T + T / 2, y: r * T + T / 2, vx: (i % 2 ? 1 : -1) * (160 + i * 40), vy: -700 - (i > 1 ? 250 : 0), t: 0 });
  }
  function setPower(p) { const h = G.hero, old = h.h; G.power = p; h.h = HH[p]; h.y -= h.h - old; }
  // لمسة العدو تنزل البطل درجة: مسلح ← كبير ← صغير ← يخسر محاولة
  function hurt() {
    if (G.power > 0) { setPower(G.power - 1); G.hero.inv = 2; SFX.shrink(); return false; }
    killHero(); return true;
  }
  function killEnemy(e) { e.dead = 0.01; e.vy = -500; e.flip = true; G.score += 100; SFX.stomp(); G.fx.push({ type: 'spark', x: e.x + 30, y: e.y + 20, t: 0 }); }
  function fire() {
    const h = G.hero, W = G.stage.weapon; if (G.power < 2 || h.cool > 0 || G.shots.length >= W.max) return;
    h.cool = W.cool; SFX.shoot();
    G.shots.push({ x: h.x + h.w / 2 + h.face * 30 - 14, y: h.y + h.h * 0.55, w: 28, h: 28, vx: h.face * W.speed, vy: W.vy, t: 0, n: 0 });
  }
  function stepItems(dt) {
    const h = G.hero;
    for (const it of G.items) {
      if (it.rise < 1) { it.rise = Math.min(1, it.rise + dt * 2.2); it.y = it.r * T - it.h * it.rise - (it.rise >= 1 ? 0.5 : 0); if (it.rise >= 1 && it.type === 'grow') it.vx = 150 * it.dir; }
      else { it.vy += 2600 * dt; moveBody(it, dt); if (it.hitWall) { it.dir = -it.dir; it.vx = 150 * it.dir; } if (it.y > VH + 200) it.gone = true; }
      if (!it.gone && it.rise > 0.5 && hit(h, it)) {
        it.gone = true; G.score += 1000; SFX.grow(); G.fx.push({ type: 'spark', x: it.x + 30, y: it.y + 30, t: 0 });
        if (it.type === 'grow') { if (G.power < 1) setPower(1); } else setPower(2);
      }
    }
    G.items = G.items.filter(i => !i.gone);
    const W = G.stage.weapon;
    for (const s of G.shots) {
      s.t += dt; s.vy += W.gravity * dt;
      const nx = s.x + s.vx * dt + (s.vx > 0 ? s.w : 0), c = Math.floor(nx / T), r = Math.floor((s.y + s.h / 2) / T);
      if (solid(cell(c, r))) {   // صدمة بحايط
        if (W.breaks && cell(c, r) === 'B') breakBrick(c, r);
        s.gone = true; G.fx.push({ type: 'spark', x: s.x + 14, y: s.y + 14, t: 0 }); continue;
      }
      moveBody(s, dt);
      if (s.ground) { if (W.bounce && s.n < W.bounce) { s.vy = -620; s.n++; } else { s.gone = true; G.fx.push({ type: 'spark', x: s.x + 14, y: s.y + 14, t: 0 }); } }
      for (const e of G.enemies) if (!e.dead && e.on && hit(s, e)) { killEnemy(e); s.gone = true; break; }
      if (s.t > 2.5 || s.x < G.cam - 100 || s.x > G.cam + VW + 100 || s.y > VH) s.gone = true;
    }
    G.shots = G.shots.filter(x => !x.gone);
  }
  function addCoin() { G.coinsN++; SFX.coin(); if (G.coinsN % 100 === 0) { G.lives++; SFX.life(); } }
  function getCoin(k) { k.got = true; addCoin(); G.score += 100; G.fx.push({ type: 'spark', x: k.x, y: k.y, t: 0 }); }
  const hit = (a, b) => a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;

  function killHero() {
    const h = G.hero; if (h.dead || h.state !== 'play') return;
    h.dead = 0.001; h.vy = -900; h.vx = 0; music.pause(); SFX.die(); G.lives--;
  }

  function step(dt, I) {
    const h = G.hero; G.t += dt;
    if (h.dead) {
      h.dead += dt; if (h.dead > 0.4) { h.vy += 2600 * dt; h.y += h.vy * dt; }
      if (h.dead > 2.6) { if (G.lives <= 0) { G.mode = 'over'; G.msgT = 0; saveBest(); } else { G.power = 0; resetLevel(); music.currentTime = 0; music.play().catch(() => { }); } }
      return;
    }
    if (h.state === 'slide') {
      h.vx = 0; h.y = Math.min(h.y + 420 * dt, GROUND * T - h.h); h.slideT += dt;
      if (h.y >= GROUND * T - h.h && h.slideT > 0.6) { h.state = 'walk'; h.face = 1; }
      return;
    }
    if (h.state === 'walk') {
      h.vx = 260; h.vy += 3200 * dt; moveBody(h, dt); h.anim += dt * 9;
      if (h.x > (G.L.goalCol + 2.2) * T) { h.state = 'done'; G.mode = 'clear'; G.msgT = 0; G.score += Math.floor(G.time) * 20; saveBest(); }
      return;
    }
    G.time -= dt; if (G.time <= 0) { G.time = 0; killHero(); return; }
    // حركة أفقية
    const max = I.run ? 640 : 430, acc = h.ground ? 1700 : 1150;
    const dir = (I.right ? 1 : 0) - (I.left ? 1 : 0);
    if (dir) { h.vx += dir * acc * (Math.sign(h.vx) === -dir ? 2.2 : 1) * dt; h.face = dir; if (Math.abs(h.vx) > max) h.vx -= Math.sign(h.vx) * Math.min(Math.abs(h.vx) - max, 1500 * dt); }
    else if (h.ground) { const f = 1800 * dt; h.vx = Math.abs(h.vx) <= f ? 0 : h.vx - Math.sign(h.vx) * f; }
    // قفز (مع مهلة صغيرة حتى تكون الاستجابة مريحة)
    h.coyote = h.ground ? 0.09 : h.coyote - dt; h.buf = I.jumpP ? 0.12 : h.buf - dt;
    if (h.buf > 0 && h.coyote > 0) { h.vy = -960 - Math.abs(h.vx) * 0.12; h.ground = false; h.coyote = 0; h.buf = 0; SFX.jump(); }
    h.vy += (h.vy < 0 && I.jump ? 1450 : 3300) * dt; if (h.vy > 1350) h.vy = 1350;
    if (h.x < G.cam && h.vx < 0) { h.x = G.cam; h.vx = 0; }
    moveBody(h, dt, bump);
    h.anim += Math.abs(h.vx) * dt / 34; if (h.inv > 0) h.inv -= dt; if (h.cool > 0) h.cool -= dt;
    if (I.fire) fire();
    stepItems(dt);
    if (h.y > VH + 200) { killHero(); return; }
    if (G.L.checkpoint && h.x > G.L.checkpoint * T) G.respawnCol = G.L.checkpoint;
    // عملات
    for (const k of G.coins) if (!k.got && Math.abs(k.x - (h.x + h.w / 2)) < 50 && Math.abs(k.y - (h.y + h.h / 2)) < h.h / 2 + 26) getCoin(k);
    // أعداء
    for (const e of G.enemies) {
      if (e.dead) { e.dead += dt; if (e.flip) { e.vy += 2600 * dt; e.y += e.vy * dt; } continue; }
      if (!e.on) { if (e.x < G.cam + VW + 150) e.on = true; else continue; }
      e.vy += 3000 * dt; moveBody(e, dt); if (e.hitWall) e.vx = -e.vx;
      for (const o of G.enemies) if (o !== e && !o.dead && o.on && hit(e, o) && Math.sign(o.x - e.x) === Math.sign(e.vx)) e.vx = -e.vx;
      if (e.y > VH + 200) e.dead = 9;
      if (hit(h, e)) {
        if (h.vy > 120 && h.y + h.h - e.y < 46) { e.dead = 0.01; h.vy = I.jump ? -900 : -560; G.score += 100; SFX.stomp(); G.fx.push({ type: 'spark', x: e.x + 30, y: e.y, t: 0 }); }
        else if (h.inv <= 0) { if (hurt()) return; }
      }
    }
    // العلم
    if (h.x + h.w > G.L.flagCol * T + T / 2 - 8 && h.state === 'play') {
      h.state = 'slide'; h.x = G.L.flagCol * T + T / 2 - h.w - 2; h.vx = 0; h.vy = 0; h.slideT = 0;
      const height = Math.max(0, GROUND * T - (h.y + h.h)); G.score += 100 + Math.round(height / T) * 400; music.pause(); SFX.win();
    }
    for (const f of G.fx) f.t += dt; G.fx = G.fx.filter(f => f.t < 0.9);
    const target = h.x - VW * 0.4; if (target > G.cam) G.cam += Math.min(target - G.cam, 900 * dt + (target - G.cam) * 0.12);
    G.cam = Math.max(0, Math.min(G.cam, G.L.width * T - VW));
  }
  function saveBest() { if (G.score > G.best) { G.best = G.score; try { localStorage.setItem('iwt_best', G.best); } catch (e) { } } }

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
  function drawWorld() {
    const L = G.L, cam = Math.round(G.cam);
    ctx.fillStyle = G.stage.sky; ctx.fillRect(0, 0, VW, VH);
    parallax('bg_far', 0.15); parallax('bg_mid', 0.4);
    ctx.save(); ctx.translate(-cam, 0);
    // بيت النهاية والعلم
    img('goal', L.goalCol * T, GROUND * T - 5 * T, 5 * T, 5 * T, '#b25a3c');
    img('flag', L.flagCol * T + T / 2 - T, GROUND * T - 9 * T, 2 * T, 9 * T, '#eee');
    const c0 = Math.max(0, Math.floor(cam / T) - 2), c1 = Math.min(L.width - 1, c0 + Math.ceil(VW / T) + 3);
    const bounce = {}; G.fx.forEach(f => { if (f.type === 'bounce' && f.t < 0.18) bounce[f.c + ',' + f.r] = -Math.sin(f.t / 0.18 * Math.PI) * 18; });
    for (let r = 0; r < ROWS; r++) for (let c = c0; c <= c1; c++) {
      const ch = L.grid[r][c]; if (ch === '.' || ch === 'P') continue;
      const x = c * T, y = r * T + (bounce[c + ',' + r] || 0);
      if (ch === '#') img(r > 0 && L.grid[r - 1][c] === '#' ? 'ground_fill' : 'ground_top', x, y, T + 1, T + 1, '#8b5a2b');
      else if (ch === 'B') img('brick', x, y, T, T, '#c0392b');
      else if (ch === '?' || ch === 'M') img('box', x, y, T, T, GOLD);
      else if (ch === 'U') img('box_used', x, y, T, T, '#786046');
      else if (ch === 'S') img('block', x, y, T, T, '#968a7c');
    }
    for (const p of L.pipes) {
      if ((p.c + 2) * T < cam || p.c * T > cam + VW) continue;
      const top = (GROUND - p.h) * T;
      for (let i = 1; i < p.h; i++) img('pipe_body', p.c * T, top + i * T, 2 * T, T + 1, '#2ea060');
      img('pipe_top', p.c * T, top, 2 * T, T, '#2ea060');
    }
    // عملات
    const cf = Math.floor(G.t * 9) % 4;
    for (const k of G.coins) if (!k.got && k.x > cam - T && k.x < cam + VW + T) img('coin', k.x - 30, k.y - 30, 60, 60, GOLD, cf * 128, 0, 128, 128);
    // أعداء
    for (const e of G.enemies) {
      if (e.x < cam - 200 || e.x > cam + VW + 200 || e.dead > 0.5 && !e.flip || e.dead > 3) continue;
      const fr = e.dead && !e.flip ? 2 : Math.floor(G.t * 6) % 2;
      ctx.save(); ctx.translate(e.x + e.w / 2, e.y + e.h / 2); ctx.scale(e.vx > 0 ? 1 : -1, e.flip ? -1 : 1);
      img('enemy1', -42, -54, 84, 84, '#6a4428', fr * 128, 0, 128, 128); ctx.restore();
    }
    // البطل
    const h = G.hero;
    if (!(h.inv > 0 && Math.floor(G.t * 20) % 2)) {
      let fr = 0; if (h.dead || !h.ground && h.state !== 'slide') fr = 4; else if (Math.abs(h.vx) > 20 || h.state === 'walk') fr = 1 + Math.floor(h.anim) % 3;
      const k = G.power ? 1.2 : 0.78, dw = 108 * k, dh = 144 * k;
      ctx.save(); ctx.translate(h.x + h.w / 2, h.y + h.h); ctx.scale(h.face, 1);
      img('hero', -dw / 2 - 6 * k, -dh + 10 * k, dw, dh, '#111', fr * 192, 0, 192, 256);
      if (G.power === 2 && !h.dead) img('item_weapon', 6, -h.h * 0.52, 46, 46, GOLD);
      ctx.restore();
    }
    // الجوائز والمقذوفات
    for (const it of G.items) {
      ctx.save(); ctx.beginPath(); ctx.rect(it.x - 20, it.r * T - 200, 110, it.rise < 1 ? 200 : 2000); ctx.clip();
      img(it.type === 'grow' ? 'item_grow' : 'item_weapon', it.x - 6, it.y - 12, 72, 72, it.type === 'grow' ? '#e33' : GOLD); ctx.restore();
    }
    for (const sh of G.shots) { ctx.save(); ctx.translate(sh.x + 14, sh.y + 14); ctx.rotate(sh.t * 14 * Math.sign(sh.vx)); img('shot', -20, -20, 40, 40, '#fff'); ctx.restore(); }
    // مؤثرات
    for (const f of G.fx) {
      if (f.type === 'pop') { const y = f.y - 40 - Math.sin(Math.min(1, f.t / 0.45) * Math.PI) * 150; if (f.t < 0.45) img('coin', f.x - 30, y - 30, 60, 60, GOLD, (Math.floor(f.t * 30) % 4) * 128, 0, 128, 128); }
      else if (f.type === 'shard') { const x = f.x + f.vx * f.t, y = f.y + f.vy * f.t + 1600 * f.t * f.t; ctx.save(); ctx.translate(x, y); ctx.rotate(f.t * 12); img('brick', -18, -18, 36, 36, '#c0392b', 0, 0, 64, 64); ctx.restore(); }
      else if (f.type === 'spark') { ctx.globalAlpha = Math.max(0, 1 - f.t * 2.5); ctx.fillStyle = '#fff3c4'; for (let i = 0; i < 6; i++) { const a = i * Math.PI / 3, d = 20 + f.t * 220; ctx.fillRect(f.x + Math.cos(a) * d - 5, f.y + Math.sin(a) * d - 5, 10, 10); } ctx.globalAlpha = 1; }
    }
    ctx.restore();
  }
  function hud() {
    const g = ctx.createLinearGradient(0, 0, 0, 120); g.addColorStop(0, 'rgba(0,0,0,.55)'); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, VW, 120);
    text(G.stage.name, VW - 50, 46, 40, GOLD, 'right');
    text('النقاط  ' + String(G.score).padStart(6, '0'), VW - 520, 46, 36, '#fff', 'right');
    img('coin', 880, 18, 56, 56, GOLD, 0, 0, 128, 128); text('× ' + G.coinsN, 950, 46, 36, '#fff', 'left');
    text('♥ ' + G.lives, 470, 46, 38, '#ff6b6b', 'left');
    if (G.power >= 1) img('item_grow', 600, 18, 56, 56, '#e33');
    if (G.power >= 2) { img('item_weapon', 664, 18, 56, 56, GOLD); text('Z', 740, 48, 30, GOLD, 'left'); }
    text('الوقت  ' + Math.ceil(G.time), 50, 46, 36, G.time < 60 ? '#ff6b6b' : '#fff', 'left');
  }
  function panel(title, lines, hint) {
    ctx.fillStyle = 'rgba(8,6,3,.72)'; ctx.fillRect(0, 0, VW, VH);
    ctx.fillStyle = 'rgba(28,25,19,.95)'; ctx.strokeStyle = GOLD; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.roundRect(VW / 2 - 520, 250, 1040, 560, 28); ctx.fill(); ctx.stroke();
    text(title, VW / 2, 350, 84, GOLD);
    lines.forEach((l, i) => text(l, VW / 2, 470 + i * 70, 44, '#f1e9d6', 'center', 600));
    if (Math.floor(G.msgT * 2) % 2 === 0) text(hint, VW / 2, 740, 40, '#fff');
  }
  function title() {
    const g = ctx.createLinearGradient(0, 0, 0, VH); g.addColorStop(0, '#1a1509'); g.addColorStop(1, '#0a0806'); ctx.fillStyle = g; ctx.fillRect(0, 0, VW, VH);
    ctx.strokeStyle = 'rgba(212,175,55,.14)'; ctx.lineWidth = 2;
    for (let i = 0; i < 9; i++) { ctx.beginPath(); ctx.ellipse(VW / 2, 1500, 500 + i * 190, 420 + i * 150, 0, Math.PI, 2 * Math.PI); ctx.stroke(); }
    ctx.direction = 'ltr'; ctx.font = `900 190px ${FONT}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const tg = ctx.createLinearGradient(0, 250, 0, 430); tg.addColorStop(0, '#fff1b0'); tg.addColorStop(0.5, GOLD); tg.addColorStop(1, '#8f7524');
    ctx.fillStyle = 'rgba(0,0,0,.6)'; ctx.fillText('IBRA', VW / 2 + 8, 298); ctx.fillStyle = tg; ctx.fillText('IBRA', VW / 2, 290);
    ctx.font = `800 96px ${FONT}`; ctx.fillStyle = '#f1e9d6'; ctx.fillText('W O R L D   T O U R', VW / 2, 440);
    text('جولة حول مدن العالم', VW / 2, 540, 48, GOLD, 'center', 600);
    if (Math.floor(G.msgT * 2) % 2 === 0) text('اضغط Enter للبدء', VW / 2, 700, 56);
    text('الأسهم أو A / D للحركة   •   Space للقفز   •   Shift للركض   •   Z للضرب   •   P توقف   •   M كتم الصوت', VW / 2, 850, 32, '#a89d85', 'center', 500);
    text('اختيار مرحلة مباشرة:  ' + STAGES.map((s, i) => (i + 1) + ' ' + s.name).join('   •   '), VW / 2, 920, 30, '#f1e9d6', 'center', 600);
    if (G.best) text('أعلى نتيجة  ' + G.best, VW / 2, 970, 30, '#f1e9d6', 'center', 600);
    text('تصميم وتطوير إبراهيم الخزرجي   •   t.me/ibraprogram', VW / 2, 1020, 28, '#8f7524', 'center', 500);
  }

  // ---------- الحلقة ----------
  let last = performance.now(), accT = 0; const DT = 1 / 120;
  function frame(now) {
    let d = Math.min(0.1, (now - last) / 1000); last = now; G.msgT += d;
    const I = input();
    if (G.mode === 'title') { title(); const pick = STAGES.findIndex((s, i) => keys['Digit' + (i + 1)] || keys['Numpad' + (i + 1)]); if (pick >= 0) startStage(pick); else if (I.start) startStage(0); }
    else if (G.mode === 'loading') { ctx.fillStyle = '#0a0806'; ctx.fillRect(0, 0, VW, VH); text('جاري التحميل...', VW / 2, VH / 2, 56, GOLD); }
    else if (G.mode === 'play') {
      if (I.pause && !G.hero.dead) { G.mode = 'pause'; music.pause(); }
      accT += d; let first = true;
      while (accT >= DT) { step(DT, first ? I : Object.assign({}, I, { jumpP: false })); first = false; accT -= DT; if (G.mode !== 'play') break; }
      drawWorld(); hud();
    }
    else if (G.mode === 'pause') { drawWorld(); hud(); panel('توقف مؤقت', ['P أو Esc للرجوع للعب', 'F5 يعيد تحميل التصاميم   •   F2 يفتح مجلد التصاميم'], 'اضغط P للمتابعة'); if (I.pause) { G.mode = 'play'; music.play().catch(() => { }); } }
    else if (G.mode === 'clear') {
      const nx = STAGES[G.stageIndex + 1];
      drawWorld(); hud(); panel('أحسنت! خلصت المرحلة', ['النقاط: ' + G.score + '     العملات: ' + G.coinsN, 'المحطة الجاية: ' + (nx ? nx.name : G.stage.next + ' (قيد التصميم)')], nx ? 'اضغط Enter للسفر للمحطة الجاية' : 'اضغط Enter للرجوع للقائمة');
      if (I.start && G.msgT > 1) { G.respawnCol = 2; if (nx) startStage(G.stageIndex + 1, true); else G.mode = 'title'; }
    }
    else if (G.mode === 'over') { drawWorld(); panel('انتهت المحاولات', ['النقاط: ' + G.score], 'اضغط Enter للمحاولة من جديد'); if (I.start && G.msgT > 1) { G.mode = 'title'; G.respawnCol = 2; } }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
