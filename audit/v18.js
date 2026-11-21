const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(600);
  for (const [id, name] of [['idx-new','a'],['idx-groups','b'],['idx-extend','c'],['idx-xuanxiu','d']]) {
    await p.evaluate((x) => document.getElementById(x).scrollIntoView(), id);
    await p.waitForTimeout(250);
    await p.screenshot({ path: 'audit/s37-' + name + '.png' });
  }
  // 溢出检测：所有单元格内容是否超出单元格
  const ov = await p.evaluate(() => {
    const bad = [];
    document.querySelectorAll('#indexall td, #indexall th').forEach(td => {
      if (td.scrollWidth - td.clientWidth > 1) bad.push([td.textContent.trim().slice(0,14), td.scrollWidth, td.clientWidth]);
    });
    return bad;
  });
  console.log('单元格横向溢出:', ov.length, JSON.stringify(ov.slice(0,6)));
  const m = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await m.goto(file + '#indexall', { waitUntil: 'load' }); await m.waitForTimeout(600);
  console.log('移动端 body 溢出:', await m.evaluate(() => document.body.scrollWidth - window.innerWidth));
  console.log('移动端 内部滚动容器:', await m.evaluate(() => {
    const t = document.querySelector('#indexall .tw');
    return { clientW: t.clientWidth, scrollW: t.scrollWidth };
  }));
  await m.evaluate(() => document.getElementById('idx-ming').scrollIntoView());
  await m.waitForTimeout(250);
  await m.screenshot({ path: 'audit/s38-mobile.png' });
  await b.close();
})();
