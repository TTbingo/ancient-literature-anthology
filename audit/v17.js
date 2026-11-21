const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  await p.goto(file + '#indexall', { waitUntil: 'load' });
  await p.waitForTimeout(600);
  const r = await p.evaluate(() => {
    const t = document.querySelector('#indexall table.t-xuanxiu');
    const rows = [...t.querySelectorAll('tr')].slice(1, 4);
    return rows.map(tr => [...tr.children].map(td => {
      const cs = getComputedStyle(td);
      return { txt: td.textContent.trim().slice(0, 14), w: Math.round(td.getBoundingClientRect().width), align: cs.textAlign };
    }));
  });
  console.log(JSON.stringify(r, null, 1));
  const cls = await p.evaluate(() => [...document.querySelectorAll('#indexall table')].map(t => t.className));
  console.log('classes', JSON.stringify(cls));
  await b.close();
})();
