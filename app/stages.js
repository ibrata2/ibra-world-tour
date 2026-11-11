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
      power(c, row) { g[row][c] = 'M'; },
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
      // السلاح: كرة تنط على الأرض
      weapon: { name: 'الكرة', speed: 760, vy: 200, gravity: 2600, bounce: 4, breaks: false, max: 2, cool: 0.25 },
      next: 'بغداد زمن الوالي',
      level: () => makeLevel(206, (a) => {
        a.coin(8, 10, 3);
        a.power(13, 9);
        a.brick(17, 9); a.box(18, 9); a.brick(19, 9); a.coin(17, 5, 3);
        a.enemy(24);
        a.pipe(30, 2);
        a.brick(35, 9, 6); a.box(37, 9); a.power(37, 5); a.box(38, 5);
        a.enemy(42); a.enemy(44.5);
        a.gap(48, 49); a.coinArc(47, 9);
        a.pipe(54, 3); a.enemy(58); a.pipe(62, 2);
        a.stairUp(68, 4); a.gap(72, 74); a.stairDown(75, 4); a.coinArc(71.5, 7);
        a.brick(82, 9, 8); a.box(84, 9); a.power(87, 9); a.enemy(85); a.enemy(91);
        a.brick(94, 5, 6); a.coin(94, 4, 6);
        a.checkpoint(100);
        a.pipe(104, 4); a.enemy(109); a.enemy(111);
        a.gap(114, 115); a.coinArc(113, 9);
        a.box(120, 9); a.box(123, 9); a.box(126, 9); a.power(123, 5);
        a.enemy(128); a.enemy(130); a.enemy(132);
        a.pipe(138, 2); a.pipe(144, 3); a.coin(140, 11, 3);
        a.brick(150, 9, 4); a.box(154, 9); a.enemy(152, 8);
        a.gap(158, 159);
        a.enemy(163);
        a.stairUp(168, 8); a.column(176, 8);
        a.flag(185); a.goal(190);
      })
    },
    {
      id: 'stage2', name: 'بغداد زمن الوالي', city: 'بغداد، العراق', time: 320, sky: '#f8c97d',
      // السلاح: مصيادة ترمي حصوة سريعة بخط شبه مستقيم وتكسر الطابوق
      weapon: { name: 'المصيادة', speed: 1250, vy: -40, gravity: 420, bounce: 0, breaks: true, max: 1, cool: 0.45 },
      next: 'ليالي خان الخليلي',
      level: () => makeLevel(222, (a) => {
        a.coin(7, 10, 4);
        a.brick(12, 9, 3); a.power(13, 9); a.enemy(17);
        a.pipe(21, 2); a.coin(21, 9, 2);
        a.box(26, 9); a.box(28, 9); a.power(27, 5); a.enemy(29); a.enemy(31);
        a.gap(34, 35); a.coinArc(33, 9);
        a.column(38, 2); a.column(41, 3); a.column(44, 4); a.coin(44, 7); a.enemy(46);
        a.brick(49, 9, 7); a.box(51, 9); a.power(54, 9); a.brick(51, 5, 3); a.coin(51, 4, 3); a.enemy(52, 8);
        a.pipe(59, 3); a.enemy(63); a.enemy(65);
        a.gap(68, 71); a.coinArc(68, 9);
        a.stairUp(74, 3); a.column(77, 3); a.gap(78, 80); a.stairDown(81, 3); a.coinArc(77.5, 7);
        a.box(87, 9); a.brick(88, 9, 2); a.box(90, 9); a.enemy(89); a.enemy(92); a.enemy(94);
        a.pipe(97, 4); a.pipe(102, 2);
        a.checkpoint(106);
        a.brick(108, 9, 3); a.brick(113, 6, 3); a.brick(118, 9, 3); a.coin(113, 5, 3); a.power(114, 2);
        a.enemy(112); a.enemy(116); a.enemy(120);
        a.gap(123, 124); a.gap(128, 129); a.coinArc(122, 9); a.coinArc(127, 9); a.enemy(126);
        a.pipe(133, 3); a.enemy(137); a.pipe(140, 3); a.coin(135, 11, 4);
        a.brick(145, 9, 10); a.box(147, 9); a.power(150, 9); a.box(153, 9); a.enemy(148, 8); a.enemy(152, 8); a.enemy(149); a.enemy(156);
        a.gap(159, 161); a.coinArc(158.5, 9);
        a.column(165, 2); a.gap(166, 167); a.column(168, 4); a.gap(169, 170); a.column(171, 6); a.coin(168, 7); a.coin(171, 5);
        a.enemy(176); a.enemy(178);
        a.stairUp(182, 8); a.column(190, 8);
        a.flag(199); a.goal(204);
      })
    }
  ];
})();
