// العوالم والجولات: كل مدينة 8 مراحل. الخرائط تتولد من بذرة ثابتة (نفس الخريطة كل مرة) عدا المرحلتين المرسومتين باليد.
(function () {
  const GROUND = 13, ROWS = 15;
  const HAND = window.STAGES;   // [شارع البداية, بغداد 1]
  function rng(seed) { let s = seed >>> 0; const f = () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; f.int = (a, b) => a + Math.floor(f() * (b - a + 1)); f.pick = arr => arr[Math.floor(f() * arr.length)]; return f; }

  // ---------- مرحلة أرضية ----------
  function land(seed, diff, o) {
    const R = rng(seed), len = Math.floor(Math.min(232, 150 + diff * 7)), width = len + 90;
    return build();
    function build() {
      let L; L = makeLevel(width, (a) => {
        let x = 10, n = 0, powers = 0, star = false, secret = false, cp = false, sew = null, exitDone = false;
        const foes = []; const foe = (c, row) => foes.push({ c, row });
        const special = (c, row) => {   // شنو ينحط بالصندوق
          if (powers < 1 || (n > powers * 3 && powers < 4)) { powers++; a.power(c, row); }
          else if (!star && x > len * 0.5) { star = true; a.star(c, row); }
          else a.box(c, row);
        };
        const nf = () => 1 + Math.min(2, Math.floor(diff / 4));
        const chunks = {
          coins() { const k = R.int(3, 5); a.coin(x + 1, 10, k); if (!secret && x > len * 0.3) { secret = true; a.secret(x + k + 2, 9); a.coin(x + k + 2, 11); } x += k + 5; },
          boxes() { const k = R.int(1, 3); for (let i = 0; i < k; i++) (i === 0 ? special : a.box)(x + 1 + i * 2, 9); if (k === 3 && R() < 0.6) a.box(x + 3, 5); for (let i = 0; i < nf(); i++) foe(x + k * 2 + 2 + i * 1.6); x += k * 2 + 6; },
          bricks() {
            const k = R.int(4, 8); a.brick(x + 1, 9, k); special(x + 1 + R.int(1, k - 2), 9); if (k > 5) a.box(x + 1 + R.int(0, k - 1), 9);
            if (R() < 0.5) { a.brick(x + 2, 5, 3); a.coin(x + 2, 4, 3); }
            if (R() < 0.5) foe(x + 2, 8); for (let i = 0; i < nf(); i++) foe(x + 3 + i * 1.7); x += k + 5;
          },
          pipe() { const h = R.int(2, Math.min(4, 2 + Math.floor(diff / 3))); a.pipe(x + 1, h); foe(x + 5); if (R() < 0.5) { a.pipe(x + 8, R.int(2, 3)); a.coin(x + 4, 11, 3); x += 6; } x += 7; },
          gap() { const w = Math.min(4, 2 + (diff > 5 && R() < 0.5 ? 1 : 0) + (diff > 9 && R() < 0.4 ? 1 : 0)); a.gap(x + 2, x + 1 + w); a.coinArc(x + 0.5 + w / 2, 9); x += w + 6; },
          stairs() { const k = R.int(3, 4), w = R.int(2, 3); a.stairUp(x + 1, k); a.gap(x + 1 + k, x + k + w); a.stairDown(x + 1 + k + w, k); a.coinArc(x + k + w / 2 - 0.5, 12 - k - 2); foe(x + 2 * k + w + 3); x += 2 * k + w + 6; },
          columns() { [2, 3, 4].forEach((h, i) => a.column(x + 1 + i * 3, h)); a.coin(x + 7, 7); foe(x + 9.5); x += 13; },
          pillars() { a.column(x + 1, 2); a.gap(x + 2, x + 3); a.column(x + 4, 4); a.gap(x + 5, x + 6); a.column(x + 7, 5); a.coin(x + 4, 7); a.coin(x + 7, 6); foe(x + 11); x += 13; }
        };
        const pool = ['coins', 'boxes', 'bricks', 'pipe', 'gap', 'bricks', 'boxes', 'stairs', 'columns'].concat(diff >= 4 ? ['gap', 'pillars'] : []).concat(diff >= 8 ? ['pillars', 'stairs', 'gap'] : []);
        let last = '';
        chunks.coins(); chunks.boxes();
        while (x < len) {
          if ((o.sewer || o.secret) && !sew && x > len * (o.secret ? 0.42 : 0.28)) { sew = { c: x + 1 }; a.pipe(x + 1, o.secret ? 3 : 2); x += 7; continue; }   // مدخل المجاري أو المرحلة السرية
          if (sew && !exitDone && x > sew.c + 44) { sew.exit = x + 1; a.pipe(x + 1, 2); exitDone = true; x += 6; continue; }  // مخرج المجاري
          if (!cp && x > len * 0.5) { cp = true; a.checkpoint(x); a.coin(x, 10, 2); x += 4; }
          let c; do { c = R.pick(pool); } while (c === last); last = c; chunks[c](); n++;
        }
        if (sew && !exitDone) { sew.exit = x + 1; a.pipe(x + 1, 2); x += 6; }
        if (o.boss) { a._note = x - 3; a._boss = { from: x + 2, to: x + 26 }; a.coin(x + 8, 9, 3); a.power(x + 4, 9); x += 30; a.flag(x + 4); a.goal(x + 9); }
        else { a.stairUp(x + 2, 8); a.column(x + 10, 8); a.flag(x + 19); a.goal(x + 24); }
        a._foes = foes; a._sew = sew;
        // أنواع الأعداء تتغير حسب الجولة
        foes.forEach(f => { a.enemy(f.c, f.row); });
        a._types = foes.map(() => { const r = R(); return o.round >= 2 && r < 0.12 + o.round * 0.03 ? 'hop' : (diff >= 5 && r > 0.82 - diff * 0.01 ? 'fast' : 'walk'); });
        L0 = a;
      });
      L.enemies.forEach((e, i) => { e.type = L0._types[i]; });
      L.kind = 'land'; L.boss = L0._boss || null; L.width = L.goalCol + 12;
      if (L0._sew) L.sewer = { c: L0._sew.c, exit: L0._sew.exit, secret: !!o.secret, sub: o.secret ? bonus(seed + 7) : sewer(seed + 99, diff, o.warps) };
      if (L0._note) L.note = { c: L0._note, got: false };
      if (o.birds) L.birds = { c: 16, on: false, t: 0 };
      return L;
    }
  }
  let L0 = null;

  // ---------- المجاري (منطقة فرعية تحت الأرض) ----------
  // بيها سر: فتحة بالسقف توصلك فوك السقف، تمشي فوكه وتعبر الحايط لغرفة بيها 4 أنابيب انتقال لمدن ثانية
  function sewer(seed, diff, warps) {
    const R = rng(seed), end = 60, width = warps ? 92 : 64;
    const L = makeLevel(width, (a) => {
      for (let c = 0; c < end + 2; c++) { a.block(c, 2); a.block(c, 3); }
      for (let r = 0; r < GROUND; r++) a.block(0, r);
      for (let r = 4; r < GROUND; r++) { a.block(end, r); a.block(end + 1, r); }
      let x = 6;
      while (x < (warps ? 34 : 48)) {
        const k = R.int(0, 3);
        if (k === 0) { a.coin(x, 10, 5); a.coin(x, 9, 5); a.coin(x + 1, 8, 3); x += 8; }
        else if (k === 1) { const n = R.int(4, 6); a.brick(x, 9, n); a.coin(x, 8, n); a.enemy(x + 2); x += n + 3; }
        else if (k === 2) { a.column(x, 2); a.column(x + 4, 3); a.coin(x + 1, 9, 3); a.enemy(x + 7); x += 9; }
        else { a.box(x, 9); a.power(x + 2, 9); a.box(x + 4, 9); a.enemy(x + 6); x += 9; }
      }
      a.coin(50, 10, 4); a.pipe(57, 3);
      if (warps) {
        a.brick(38, 10, 2); a.brick(41, 7, 2); a.block(44, 5); a.coin(44, 4);
        for (let r = 0; r < GROUND; r++) { a.block(width - 1, r); a.block(width - 2, r); a.block(width - 3, r); }
        warps.forEach((w, i) => a.pipe(67 + i * 5, 2));
      } else for (let r = 0; r < GROUND; r++) { a.block(62, r); a.block(63, r); }
    });
    if (warps) { [41, 42, 43, 44, 45, 46].forEach(c => { L.grid[2][c] = '.'; L.grid[3][c] = '.'; }); L.warps = warps.map((w, i) => ({ c: 67 + i * 5, idx: w.idx, label: w.label })); }
    L.kind = 'sewer'; L.exitCol = 57; L.flagCol = 9999; L.goalCol = 9999; L.checkpoint = 0;
    L.enemies.forEach(e => { e.type = 'walk'; });
    return L;
  }
  // ---------- المرحلة السرية (فوك الغيوم): عملات وأرواح، بدون أعداء ----------
  function bonus(seed) {
    const R = rng(seed), width = 78;
    const L = makeLevel(width, (a) => {
      for (let r = 0; r < GROUND; r++) { a.block(0, r); a.block(width - 1, r); a.block(width - 2, r); }
      let x = 5;
      while (x < 58) {
        const k = R.int(0, 3);
        if (k === 0) { for (let r = 6; r <= 11; r++) a.coin(x, r, 6); x += 9; }
        else if (k === 1) { a.block(x, 9); a.block(x + 1, 9); a.block(x + 3, 6); a.block(x + 4, 6); a.coin(x, 8, 2); a.coin(x + 3, 5, 2); a.coin(x + 2, 3, 4); x += 8; }
        else if (k === 2) { a.box(x, 9); a.box(x + 1, 9); a.box(x + 2, 9); a.box(x + 3, 9); a.secret(x + 5, 9); x += 9; }
        else { for (let i = 0; i < 7; i++) a.coin(x + i, 10 - Math.round(Math.sin(i / 6 * Math.PI) * 4)); x += 9; }
      }
      a.power(60, 9); a.star(62, 9); a.secret(64, 9); a.coin(66, 10, 3); a.pipe(72, 3);
    });
    L.kind = 'bonus'; L.exitCol = 72; L.flagCol = 9999; L.goalCol = 9999; L.checkpoint = 0;
    return L;
  }

  // ---------- مرحلة الغوص ----------
  function water(seed, diff) {
    const R = rng(seed), width = 176;
    const L = makeLevel(width, (a) => {
      for (let c = 0; c < width; c++) a.block(c, 0);
      let x = 12, p = 0;
      while (x < width - 30) {
        const k = R.int(0, 4), h = R.int(2, 6);
        if (k === 0) { a.column(x, h); for (let r = 1; r < 12 - h - 4; r++) a.block(x, r); a.coin(x, 12 - h - 2); a.coin(x, 12 - h - 3); x += 7; }
        else if (k === 1) { const row = R.int(4, 9); a.coin(x, row, 6); a.enemy(x + 8, row + 1); x += 10; }
        else if (k === 2) { a.column(x, h + 1); a.column(x + 1, h); a.enemy(x + 4, R.int(3, 7)); a.coinArc(x - 1, 12 - h - 3); x += 8; }
        else if (k === 3) { const row = R.int(5, 9); a.brick(x, row, 3); (p++ % 2 === 0 ? a.power : a.box)(x + 1, row); a.enemy(x + 5, row - 2); x += 9; }
        else { for (let r = 1; r < R.int(4, 7); r++) a.block(x, r); a.enemy(x + 3, 10); a.coin(x + 2, 11, 4); x += 8; }
        if (diff > 5 && R() < 0.5) a.enemy(x - 2, R.int(3, 10));
      }
      a.checkpoint(Math.floor(width / 2)); a.flag(width - 16); a.goal(width - 11);
    });
    L.kind = 'water'; L.enemies.forEach(e => { e.type = 'fish'; });
    return L;
  }

  const WEAPONS = {
    stage1: { name: 'الكرة', speed: 760, vy: 200, gravity: 2600, bounce: 4, max: 2, cool: 0.25 },
    stage2: { name: 'المصيادة', speed: 1250, vy: -40, gravity: 420, breaks: true, max: 1, cool: 0.45 },
    stage3: { name: 'النبّوت', speed: 640, vy: 0, gravity: 0, life: 0.3, pierce: true, breaks: true, max: 1, cool: 0.32 },      // ضربة قريبة قوية
    stage4: { name: 'كرة الثلج', speed: 700, vy: -520, gravity: 1700, max: 2, cool: 0.3 },                                   // ترمي بقوس
    stage5: { name: 'الچاكرام', speed: 920, vy: 0, gravity: 0, life: 1.0, pierce: true, max: 1, cool: 0.5 },                 // قرص يخترق كل الأعداء
    stage6: { name: 'الألعاب النارية', speed: 560, vy: -640, gravity: 1900, blast: 190, max: 1, cool: 0.6 },                 // تنفجر وتضرب اللي حولها
    stage7: { name: 'كرة البيسبول', speed: 1350, vy: -60, gravity: 260, wallBounce: 2, max: 2, cool: 0.3 }                   // سريعة وترتد من الحيطان
  };
  const CITIES = [
    { id: 'stage2', short: 'بغداد', title: 'بغداد زمن الوالي', sky: '#f8c97d', water: 'نهر دجلة', boss: 'ملك العقارب', era: 'بغداد العثمانية، زمن الولاة', style: 'مقام عراقي: عود، جوزة، سنطور، إيقاع جورجينة' },
    { id: 'stage3', short: 'القاهرة', title: 'ليالي خان الخليلي', sky: '#3a3a72', water: 'نهر النيل', boss: 'قط الخان الأسود', era: 'القاهرة القديمة، ليالي الخان', style: 'عود وقانون وطبلة، إيقاع مقسوم' },
    { id: 'stage4', short: 'موسكو', title: 'ثلوج الكرملين', sky: '#9fb8d6', water: 'نهر موسكفا المتجمد', boss: 'الدب الأكبر', era: 'موسكو القيصرية بالشتاء', style: 'بالالايكا وأكورديون، يتسارع' },
    { id: 'stage5', short: 'دلهي', title: 'قلاع دلهي الحمراء', sky: '#f7a8b8', water: 'نهر يامونا', boss: 'زعيم القرود', era: 'دلهي المغولية', style: 'سيتار وطبلة هندية وبانسوري' },
    { id: 'stage6', short: 'بكين', title: 'سور الصين العظيم', sky: '#bfe3d6', water: 'بحيرة القصر', boss: 'الباندا العملاق', era: 'بكين الإمبراطورية', style: 'سلم خماسي: إرهو وغوجنغ وطبول' },
    { id: 'stage7', short: 'نيويورك', title: 'ناطحات نيويورك', sky: '#1c2340', water: 'نهر هدسون', boss: 'ملك جرذان المترو', era: 'نيويورك العشرينات، عصر الجاز', style: 'جاز وسوينغ: ساكسفون وكونترباص' }
  ];
  const ROUNDS = [
    { key: 'day', label: 'النهار', tod: 'النهار' },
    { key: 'alt', label: 'العصر', tod: 'العصر، ألوان مختلفة' },
    { key: 'night', label: 'الليل', tod: 'الليل' },
    { key: 'noon', label: 'الظهر', tod: 'الظهر، شمس قوية' },
    { key: 'sewer', label: 'المجاري', tod: 'النهار + تحت الأرض' },
    { key: 'water', label: 'الغوص', tod: 'تحت الماء' },
    { key: 'dawn', label: 'الفجر', tod: 'الفجر، ضباب' },
    { key: 'boss', label: 'الوحش', tod: 'الغروب، معركة الوحش' }
  ];

  const list = [Object.assign(HAND[0], { world: 0, round: 1, variant: 'day', label: 'شارع البداية', weapon: WEAPONS.stage1, cityName: 'البداية' })];
  CITIES.forEach((c, ci) => ROUNDS.forEach((r, ri) => {
    const round = ri + 1, diff = ci * 1.3 + round, seed = (ci + 1) * 1000 + round * 37;
    const base = `${c.short} ${ci + 1}-${round}`;
    let level;
    if (ci === 0 && round === 1) level = () => { const L = HAND[1].level(); L.kind = 'land'; L.enemies.forEach(e => { e.type = 'walk'; }); return L; };
    else if (r.key === 'water') level = () => water(seed, diff);
    else {
      // أنابيب الانتقال السرية بجولة المجاري: 4 وجهات لمدن أبعد (نيويورك ما بيها)
      let warps = null;
      if (r.key === 'sewer' && ci < CITIES.length - 1) {
        const t = []; for (let k = ci + 1; k < CITIES.length && t.length < 4; k++) t.push([k, 1]);
        for (const rr of [5, 3, 7, 4]) { if (t.length >= 4) break; for (let k = ci + 1; k < CITIES.length && t.length < 4; k++) t.push([k, rr]); }
        warps = t.map(([k, rr]) => ({ idx: 1 + k * 8 + (rr - 1), label: `${CITIES[k].short} ${k + 1}-${rr}` }));
      }
      level = () => land(seed, diff, { round, sewer: r.key === 'sewer', boss: r.key === 'boss', secret: r.key === 'dawn', birds: round === 2, warps });
    }
    list.push({
      id: c.id, world: ci + 1, round, variant: r.key, cityName: c.short, label: r.label,
      name: round === 1 ? c.title : (r.key === 'water' ? `${base}  غوص ب${c.water}` : r.key === 'boss' ? `${base}  ${c.boss}` : `${base}  ${r.label}`),
      sky: c.sky, time: r.key === 'boss' ? 400 : 320, weapon: WEAPONS[c.id], bossName: c.boss, bossHp: 3 + Math.floor(ci / 2),
      fly: ['bird', 'bird', 'bird', 'kite', 'lantern', 'plane'][ci], noteKind: ci === CITIES.length - 1 ? 'phone' : 'letter',
      final: ci === CITIES.length - 1 && r.key === 'boss', nextCity: CITIES[ci + 1] ? CITIES[ci + 1].short : null, era: c.era, style: c.style, tod: r.tod, level
    });
  }));
  HAND[0].level = (lv => () => { const L = lv(); L.kind = 'land'; L.enemies.forEach(e => { e.type = 'walk'; }); return L; })(HAND[0].level);
  list[0].era = 'مرحلة تعليمية'; list[0].style = 'لحن مرح سريع'; list[0].tod = 'النهار';
  window.STAGES = list; window.CITY_NAMES = ['البداية'].concat(CITIES.map(c => c.short)); window.ROUND_LABELS = ROUNDS.map(r => r.label);
})();
