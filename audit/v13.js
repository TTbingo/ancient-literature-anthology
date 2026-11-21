const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/教材作者集成/index.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  for (const id of ['p-shuihu-shengchengang','p-rulin-fanjin','p-sanguo-sangumaolu','p-honglou-liulaolao']) {
    await p.goto(file + '#novel::' + id, { waitUntil: 'load' }); await p.waitForTimeout(700);
    const st = await p.evaluate((i) => {
      const el = document.getElementById(i);
      const v = el.querySelector('.verse');
      const d = el.querySelectorAll('.dim').length;
      return { top: Math.round(el.getBoundingClientRect().top), chars: v.textContent.replace(/\s/g,'').length, dims: d };
    }, id);
    console.log(id, JSON.stringify(st));
  }
  await p.goto(file + '#novel::p-honglou-liulaolao', { waitUntil: 'load' }); await p.waitForTimeout(700);
  await p.screenshot({ path: 'audit/s30-liulaolao.png' });
  // 移动端
  const m = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await m.goto(file + '#novel', { waitUntil: 'load' }); await m.waitForTimeout(600);
  console.log('移动端溢出:', await m.evaluate(() => document.body.scrollWidth - window.innerWidth));
  await m.screenshot({ path: 'audit/s31-novel-mobile.png' });
  console.log('JS:', errs.length ? errs : '无');
  await b.close();
})();
