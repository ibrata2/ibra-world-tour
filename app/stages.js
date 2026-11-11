// تعريف المراحل. كل مرحلة لها مجلد داخل assets وخريطة تنبني هنا.
// الخريطة: 15 صف، الأرض بالصفين 13 و14. row = رقم الصف من فوق.
(function () {
  const ROWS = 15, GROUND = 13;

  function makeLevel(width, build) {
    const g = Array.from({ length: ROWS }, () => Array(width).fill('.'));
    const L = { width, grid: g, pipes: [], enemies: [], coins: [], flagCol: 0, goalCol: 0, checkpoint: 0 };
    const api = {
      ground(from, to) { for (let c = from; c <= to; c++) { g[GROUND][c] = '#'; g[GROUND + 1][c] = '#'; } },
      gap(from, to) { for (let c = from; c <= to; c++) { g[GROUND][c] = '.'; g[GROUND + 1][c] = '.'; } },
      brick(c, row, n = 1) { for (let i = 0; i < n; i++) g[row][c + i] = 'B'; },
      box(c, row) { g[row][c] = '?'; },
      block(c, row) { g[row][c] = 'S'; },
      stairUp(c, n) { for (let i = 0; i < n; i++) for (let h = 0; h <= i; h++) g[GROUND - 1 - h][c + i] = 'S'; },
      stairDown(c, n) { for (let i = 0; i < n; i++) for (let h = 0; h < n - i; h++) g[GROUND - 1 - h][c + i] = 'S'; },
      column(c, h) { for (let i = 0; i < h; i++) g[GROUND - 1 - i][c] = 'S'; },
      pipe(c, h) { L.pipes.push({ c, h }); for (let i = 0; i < h; i++) { g[GROUND - 1 - i][c] = 'P'; g[GROUND - 1 - i][c + 1] = 'P'; } },
      enemy(c, row = GROUND - 1) { L.enemies.push({ c, row }); },
      coin(c, row, n = 1) { for (let i = 0; i < n; i++) L.coins.push({ c: c + i, row }); },
      coinArc(c, row) { [[0, 0], [1, -1], [2, -1], [3, 0]].forEach(([dx, dy]) => L.coins.push({ c: c + dx, row: row + dy })); },
      flag(c) { L.flagCol = c; },
      goal(c) { L.goalCol = c; },
      checkpoint(c) { L.checkpoint = c; }
    };
    api.ground(0, width - 1);
    build(api);
    return L;
  }

  window.STAGES = [
    {
      id: 'stage1', name: 'شارع البداية', city: 'المرحلة الكلاسيكية', time: 300, sky: '#6ec3ff',
      next: 'بغداد زمن الوالي',
      level: () => makeLevel(206, (a) => {
        a.coin(8, 10, 3);
        a.box(13, 9);
        a.brick(17, 9); a.box(18, 9); a.brick(19, 9); a.coin(17, 5, 3);
        a.enemy(24);
        a.pipe(30, 2);
        a.brick(35, 9, 6); a.box(37, 9); a.box(37, 5); a.box(38, 5);
        a.enemy(42); a.enemy(44.5);
        a.gap(48, 49); a.coinArc(47, 9);
        a.pipe(54, 3); a.enemy(58); a.pipe(62, 2);
        a.stairUp(68, 4); a.gap(72, 74); a.stairDown(75, 4); a.coinArc(71.5, 7);
        a.brick(82, 9, 8); a.box(84, 9); a.box(87, 9); a.enemy(85); a.enemy(91);
        a.brick(94, 5, 6); a.coin(94, 4, 6);
        a.checkpoint(100);
        a.pipe(104, 4); a.enemy(109); a.enemy(111);
        a.gap(114, 115); a.coinArc(113, 9);
        a.box(120, 9); a.box(123, 9); a.box(126, 9); a.box(123, 5);
        a.enemy(128); a.enemy(130); a.enemy(132);
        a.pipe(138, 2); a.pipe(144, 3); a.coin(140, 11, 3);
        a.brick(150, 9, 4); a.box(154, 9); a.enemy(152, 8);
        a.gap(158, 159);
        a.enemy(163);
        a.stairUp(168, 8); a.column(176, 8);
        a.flag(185); a.goal(190);
      })
    }
  ];
})();
