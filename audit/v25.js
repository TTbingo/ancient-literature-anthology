const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  for (const w of [1600, 1440, 1280, 1180, 900, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 950 } });
    await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(500);
    const r = await p.evaluate(() => {
      const o = {};
      const t = document.querySelector('#indexall table.t-ming');
      o.mingCols = [...t.querySelectorAll('tr:first-child th')].map(x => Math.round(x.getBoundingClientRect().width));
      o.mingW = Math.round(t.getBoundingClientRect().width);
      const n = document.querySelector('#indexall table.t-novel');
      o.novelW = Math.round(n.getBoundingClientRect().width);
      o.novelCols = [...n.querySelectorAll('tr:first-child th')].map(x => Math.round(x.getBoundingClientRect().width));
      const ov = [];
      document.querySelectorAll('#indexall td, #indexall th').forEach(td => { if (td.scrollWidth - td.clientWidth > 1) ov.push(td.textContent.trim().slice(0,12)+':'+(td.scrollWidth-td.clientWidth)); });
      o.cellOv = ov;
      o.bodyOv = document.body.scrollWidth - window.innerWidth;
      o.tablesW = [...document.querySelectorAll('#indexall table')].map(x=>Math.round(x.getBoundingClientRect().width));
      return o;
    });
    console.log(w, JSON.stringify(r));
    if ([1440,1180,390].includes(w)) {
      await p.evaluate(() => document.getElementById('idx-ming').scrollIntoView({block:'start'}));
      await p.waitForTimeout(300);
      await p.screenshot({ path: `audit/s25-ming-${w}.png` });
      await p.evaluate(() => document.getElementById('idx-novel').scrollIntoView({block:'start'}));
      await p.waitForTimeout(300);
      await p.screenshot({ path: `audit/s25-novel-${w}.png` });
    }
    await p.close();
  }
  await b.close();
})();
