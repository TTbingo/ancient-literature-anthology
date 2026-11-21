const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  for (const w of [1440, 1180, 900, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(file + '#jiaocai', { waitUntil: 'load' }); await p.waitForTimeout(500);
    const r = await p.evaluate(() => {
      const ov=[]; document.querySelectorAll('#jiaocai td').forEach(td=>{ if(td.scrollWidth-td.clientWidth>1) ov.push([td.textContent.trim().slice(0,16), td.scrollWidth, td.clientWidth]); });
      return { bodyOv: document.body.scrollWidth - window.innerWidth, cellOv: ov.length, sample: ov.slice(0,3) };
    });
    console.log(w, JSON.stringify(r));
    if (w === 390) { await p.evaluate(() => document.querySelectorAll('#jiaocai h3')[0].scrollIntoView()); await p.waitForTimeout(250); await p.screenshot({ path: 'audit/s43-jc-mobile.png' }); }
    await p.close();
  }
  await b.close();
})();
