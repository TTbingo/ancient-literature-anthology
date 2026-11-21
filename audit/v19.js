const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(500);
  // 1) 点击表内链接
  for (const [txt, page] of [['李白专篇','libai'],['中华传统文化专题研讨','xuanxiu'],['《草船借箭》','novel']]) {
    await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(300);
    const ok = await p.evaluate((t) => {
      const a = [...document.querySelectorAll('#indexall a[data-goto], #indexall a')].find(x => x.textContent.trim() === t);
      if (!a) return 'noanchor'; a.click(); return a.getAttribute('data-goto') || a.getAttribute('href');
    }, txt);
    await p.waitForTimeout(800);
    const st = await p.evaluate((pg) => {
      const s = document.querySelector('section.page.active');
      const rail = document.querySelector('section.page.active nav.prail a.on');
      return { page: s && s.id, rail: rail ? rail.textContent.trim().slice(0,10) : null, y: Math.round(window.scrollY) };
    }, page);
    console.log('点击', txt, ok, '→', JSON.stringify(st), st.page === page ? 'PASS' : 'CHECK');
  }
  // 2) 页内目录高亮
  await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(400);
  await p.evaluate(() => document.getElementById('idx-novel').scrollIntoView()); await p.waitForTimeout(600);
  console.log('页内目录高亮:', await p.evaluate(() => document.querySelector('#indexall nav.prail a.on')?.textContent.trim().slice(0,12)));
  console.log('目录条数:', await p.evaluate(() => document.querySelectorAll('#indexall nav.prail a').length));
  await p.evaluate(() => document.getElementById('idx-novel').scrollIntoView()); await p.waitForTimeout(300);
  await p.screenshot({ path: 'audit/s39-novel2.png' });
  console.log('JS:', errs.length ? errs : '无');
  await b.close();
})();
