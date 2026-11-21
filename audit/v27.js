const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  for (const w of [1440, 900, 768, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(400);
    const r = await p.evaluate(() => {
      const n = document.querySelector('#indexall table.t-novel');
      const tw = n.closest('.tw');
      return { tableW: Math.round(n.getBoundingClientRect().width), boxC: tw.clientWidth, boxS: tw.scrollWidth,
        bodyOv: document.body.scrollWidth - innerWidth,
        cellOv: [...document.querySelectorAll('#indexall .t-novel td')].filter(t => t.scrollWidth - t.clientWidth > 1).length };
    });
    console.log(w, JSON.stringify(r));
    if (w === 390) { await p.evaluate(() => document.getElementById('idx-novel').scrollIntoView({block:'start'})); await p.waitForTimeout(300); await p.screenshot({ path: 'audit/s27-novel-390.png' }); }
    await p.close();
  }
  await b.close();
})();
