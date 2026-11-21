const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/教材作者集成/index.html').replace(/\\/g, '/');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  page.on('pageerror', e => errs.push('PAGEERROR ' + e.message));

  await page.goto(file, { waitUntil: 'load' });
  await page.waitForTimeout(400);

  // 1. 分页数与目录栏
  const stat = await page.evaluate(() => ({
    pages: document.querySelectorAll('section.page').length,
    rails: document.querySelectorAll('nav.prail').length,
    active: document.querySelectorAll('section.page.active').length
  }));
  console.log('分页/目录栏/激活:', JSON.stringify(stat));

  // 2. 深链跳转落点
  const jumps = [
    'xuanxiu::p-xu-laozi',
    'xuanxiu::a-xu-huangzongxi',
    'xuanxiu::p-xu-tengwang',
    'xuanxiu::a-xu-mengyuanlao',
    'tangchu::p-tengwangge-wangbo',
    'mao::p-mao-youshui',
    'hanprose::p-su-wu'
  ];
  for (const j of jumps) {
    await page.evaluate(j => { location.hash = j; }, j);
    await page.waitForTimeout(650);
    const r = await page.evaluate(() => {
      const pg = document.querySelector('section.page.active');
      const id = location.hash.split('::')[1];
      const el = id ? document.getElementById(id) : null;
      const rb = el ? el.getBoundingClientRect() : null;
      const rail = pg ? pg.querySelector('nav.prail a.on') : null;
      return {
        page: pg ? pg.id : null,
        top: rb ? Math.round(rb.top) : null,
        railOn: rail ? rail.textContent.trim().slice(0, 14) : null
      };
    });
    console.log('跳转', j, '→', JSON.stringify(r));
  }

  // 3. 繁体残留扫描（正文可见文本）
  const residue = await page.evaluate(() => {
    const bad = '於後餘鬥撃倶禦儘歎爲眾內驩彊髮發沖裏臺甯幹痾缻鲊動';
    const out = {};
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walker.nextNode())) {
      const t = n.nodeValue;
      for (const c of bad) {
        if (t.indexOf(c) >= 0) {
          const k = (n.parentElement.closest('[id]') || {}).id || 'no-id';
          out[c] = out[c] || [];
          if (out[c].length < 3) out[c].push(k + ': ' + t.trim().slice(0, 26));
        }
      }
    }
    return out;
  });
  console.log('繁体残留:', JSON.stringify(residue, null, 1));
  console.log('JS 报错:', errs.length ? errs : '无');
  await browser.close();
})();
