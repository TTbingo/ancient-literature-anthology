const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(file, { waitUntil: 'load' }); await p.waitForTimeout(400);
  console.log('页数/目录栏/激活:', await p.evaluate(() => [document.querySelectorAll('section.page').length, document.querySelectorAll('nav.prail').length, document.querySelectorAll('section.page.active').length]));
  // 深链与搜索
  for (const [u, id] of [['#indexall','indexall'],['#jiaocai','jiaocai'],['#xuanxiu::p-xu-laozi','p-xu-laozi'],['#novel::p-honglou-chunqu','p-honglou-chunqu']]) {
    await p.goto(file + u, { waitUntil: 'load' }); await p.waitForTimeout(600);
    const st = await p.evaluate((i) => { const e=document.getElementById(i); return e? Math.round(e.getBoundingClientRect().top):null; }, id);
    console.log(u, 'top', st);
  }
  await p.goto(file, { waitUntil: 'load' }); await p.waitForTimeout(300);
  await p.keyboard.press('/'); await p.waitForTimeout(130);
  await p.keyboard.type('赤壁赋', { delay: 14 }); await p.waitForTimeout(300);
  console.log('搜索[赤壁赋]:', await p.evaluate(() => [...document.querySelectorAll('.sr-item')].slice(0,2).map(x=>x.textContent.replace(/\s+/g,' ').trim().slice(0,26))));
  await p.keyboard.press('Escape');
  console.log('JS:', errs.length ? errs : '无');
  await b.close();
})();
