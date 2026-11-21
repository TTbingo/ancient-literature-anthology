const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  for (const w of [1600, 1440, 1280, 1180, 900, 768, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(450);
    const r = await p.evaluate(() => {
      const out = [];
      document.querySelectorAll('#indexall table').forEach(t => {
        const box = t.closest('.tw');
        const cells = [...t.querySelectorAll('td,th')];
        const ov = cells.filter(c => c.scrollWidth - c.clientWidth > 1).length;
        out.push({ cls: t.className, w: Math.round(t.getBoundingClientRect().width), box: box.clientWidth, ov, rows: t.rows.length });
      });
      return { tables: out, bodyOv: document.body.scrollWidth - innerWidth };
    });
    console.log(w, JSON.stringify(r));
    await p.close();
  }
  await b.close();
})();
