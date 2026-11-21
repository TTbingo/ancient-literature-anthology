const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  await p.goto(file + '#jiaocai', { waitUntil: 'load' }); await p.waitForTimeout(600);
  await p.evaluate(() => document.querySelectorAll('#jiaocai h3')[0].scrollIntoView()); await p.waitForTimeout(250);
  await p.screenshot({ path: 'audit/s40-jiaocai.png' });
  const ov = await p.evaluate(() => {
    const bad=[]; document.querySelectorAll('section.page.active td').forEach(td=>{ if(td.scrollWidth-td.clientWidth>1) bad.push(td.textContent.trim().slice(0,12)); });
    return bad;
  });
  console.log('jiaocai 溢出', ov.length, JSON.stringify(ov.slice(0,5)));
  await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(400);
  await p.evaluate(() => document.getElementById('idx-novel').scrollIntoView()); await p.waitForTimeout(300);
  await p.screenshot({ path: 'audit/s41-novel3.png' });
  await b.close();
})();
