const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(file + '#indexall', { waitUntil: 'load' });
  await p.waitForTimeout(700);
  const info = await p.evaluate(() => {
    const t = document.querySelector('#indexall table.t-ming');
    const ths = [...t.querySelectorAll('tr:first-child th')].map(x => ({ w: Math.round(x.getBoundingClientRect().width), t: x.textContent.trim() }));
    const c = t.querySelector('tbody tr td');
    const r = document.querySelector('#indexall .pbody') || document.querySelector('#indexall');
    return { tableW: Math.round(t.getBoundingClientRect().width), containerW: Math.round(r.getBoundingClientRect().width),
             ths, firstCell: { w: Math.round(c.getBoundingClientRect().width), h: Math.round(c.getBoundingClientRect().height), txt: c.textContent.trim() },
             bodyOverflow: document.body.scrollWidth - window.innerWidth };
  });
  console.log(JSON.stringify(info, null, 1));
  await p.evaluate(() => document.getElementById('idx-ming').scrollIntoView());
  await p.waitForTimeout(300);
  await p.screenshot({ path: 'audit/s34-index-ming.png' });
  await p.evaluate(() => document.getElementById('idx-xuanxiu').scrollIntoView());
  await p.waitForTimeout(300);
  await p.screenshot({ path: 'audit/s35-index-xu.png' });
  await p.evaluate(() => document.getElementById('idx-novel').scrollIntoView());
  await p.waitForTimeout(300);
  await p.screenshot({ path: 'audit/s36-index-novel.png' });
  console.log('JS:', errs.length ? errs : '无');
  await b.close();
})();
