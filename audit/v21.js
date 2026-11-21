const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  for (const w of [1600, 1440, 1180, 900, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(500);
    const r = await p.evaluate(() => {
      const t = document.querySelector('#indexall table.t-ming');
      const ths = [...t.querySelectorAll('tr:first-child th')].map(x => Math.round(x.getBoundingClientRect().width));
      const ov = [];
      document.querySelectorAll('#indexall td').forEach(td => { if (td.scrollWidth - td.clientWidth > 1) ov.push(td.textContent.trim().slice(0,10)); });
      return { cols: ths, tableW: Math.round(t.getBoundingClientRect().width), bodyOv: document.body.scrollWidth - window.innerWidth, cellOv: ov.length };
    });
    console.log(w, JSON.stringify(r));
    if (w === 1180) { await p.evaluate(() => document.getElementById('idx-ming').scrollIntoView()); await p.waitForTimeout(250); await p.screenshot({ path: 'audit/s42-1180.png' }); }
    await p.close();
  }
  await b.close();
})();
