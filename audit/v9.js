const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/教材作者集成/index.html').replace(/\\/g, '/');
  const browser = await chromium.launch();

  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto(file, { waitUntil: 'load' });
  await page.waitForTimeout(400);

  for (const q of ['廉颇', '滕王阁序', '黄宗羲', '井干', '浑沌', '东海有勇妇']) {
    await page.keyboard.press('/');
    await page.waitForTimeout(130);
    await page.keyboard.type(q, { delay: 12 });
    await page.waitForTimeout(260);
    const r = await page.evaluate(() => {
      const sels = '.sr-item';
      const items = [...document.querySelectorAll(sels)].slice(0, 3);
      return {
        n: document.querySelectorAll(sels).length,
        first: items.map(x => x.textContent.replace(/\s+/g, ' ').trim().slice(0, 22))
      };
    });
    console.log('搜索[' + q + ']', JSON.stringify(r));
    await page.keyboard.press('Escape');
    await page.waitForTimeout(130);
  }

  await page.keyboard.press('/');
  await page.waitForTimeout(130);
  await page.keyboard.type('黄宗羲', { delay: 12 });
  await page.waitForTimeout(260);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(850);
  const hit = await page.evaluate(() => {
    const pg = document.querySelector('section.page.active');
    const el = document.getElementById('a-xu-huangzongxi');
    return { page: pg && pg.id, top: el ? Math.round(el.getBoundingClientRect().top) : null };
  });
  console.log('搜索回车直达:', JSON.stringify(hit), 'JS错误', errs.length ? errs : '无');

  const m = await browser.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const merr = [];
  m.on('pageerror', e => merr.push(e.message));
  await m.goto(file + '#xuanxiu', { waitUntil: 'load' });
  await m.waitForTimeout(550);
  const mob = await m.evaluate(() => {
    const rail = document.querySelector('#xuanxiu nav.prail');
    const rb = rail ? rail.getBoundingClientRect() : null;
    return {
      railW: rb ? Math.round(rb.width) : null,
      overflowX: document.body.scrollWidth - window.innerWidth,
      railHead: rail ? rail.textContent.replace(/\s+/g, ' ').trim().slice(0, 18) : null
    };
  });
  console.log('窄屏:', JSON.stringify(mob), 'JS错误', merr.length ? merr : '无');
  await m.screenshot({ path: 'audit/s26-xuanxiu-mobile.png' });

  await browser.close();
})();
