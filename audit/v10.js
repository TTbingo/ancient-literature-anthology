const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/教材作者集成/index.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
  await p.goto(file + '#xuanxiu::p-xu-lianpo', { waitUntil: 'load' });
  await p.waitForTimeout(900);
  const info = await p.evaluate(() => {
    const el = document.getElementById('p-xu-lianpo');
    const t = el.textContent.replace(/\s+/g, '');
    return { chars: t.length, head: t.slice(0, 40), tail: t.slice(-30), top: Math.round(el.getBoundingClientRect().top) };
  });
  console.log(JSON.stringify(info, null, 1));
  await p.screenshot({ path: 'audit/s27-lianpo.png' });
  await b.close();
})();
