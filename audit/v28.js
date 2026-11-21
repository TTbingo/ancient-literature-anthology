const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(500);
  for (const [id, name] of [['idx-new','new'],['idx-groups','groups'],['idx-extend','extend']]) {
    const r = await p.evaluate(i => {
      const h = document.getElementById(i);
      const tw = h.nextElementSibling?.nextElementSibling?.classList?.contains('tw') ? h.nextElementSibling.nextElementSibling : [...h.parentNode.querySelectorAll('.tw')].find(w => w.compareDocumentPosition(h) & 4);
      const t = h.parentNode.querySelector('.tw table');
      return { w: Math.round(t.getBoundingClientRect().width), cols: [...t.querySelectorAll('tr:first-child th')].map(x=>Math.round(x.getBoundingClientRect().width)), ov: [...t.querySelectorAll('td')].filter(x=>x.scrollWidth-x.clientWidth>1).length };
    }, id);
    console.log(id, JSON.stringify(r));
    await p.evaluate(i => document.getElementById(i).scrollIntoView({block:'start'}), id);
    await p.waitForTimeout(250);
    await p.screenshot({ path: `audit/s28-${name}.png` });
  }
  await b.close();
})();
