const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  for (const wait of [650, 1200, 2000]) {
    const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
    await p.goto(file + '#novel::p-xiyou-houwang', { waitUntil: 'load' });
    await p.waitForTimeout(wait);
    const st = await p.evaluate(() => {
      const el = document.getElementById('p-xiyou-houwang');
      const rail = document.querySelector('#novel nav.prail a.on');
      return { top: Math.round(el.getBoundingClientRect().top), y: Math.round(window.scrollY),
               rail: rail && rail.textContent.trim().slice(0,10),
               docH: document.body.scrollHeight, winH: window.innerHeight };
    });
    console.log('wait', wait, JSON.stringify(st));
    await p.close();
  }
  await b.close();
})();
