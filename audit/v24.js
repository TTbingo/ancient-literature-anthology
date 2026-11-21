const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  for (const wait of [600, 900, 1600]) {
    const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
    await p.goto(file + '#xuanxiu::p-xu-laozi', { waitUntil: 'load' });
    await p.waitForTimeout(wait);
    const st = await p.evaluate(() => {
      const e = document.getElementById('p-xu-laozi');
      const pg = document.querySelector('section.page.active');
      const rail = document.querySelector('section.page.active nav.prail a.on');
      return { page: pg && pg.id, top: Math.round(e.getBoundingClientRect().top), y: Math.round(window.scrollY), rail: rail && rail.textContent.trim().slice(0,10) };
    });
    console.log('wait', wait, JSON.stringify(st));
    await p.close();
  }
  await b.close();
})();
