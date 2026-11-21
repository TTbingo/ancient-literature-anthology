const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(file, { waitUntil: 'load' }); await p.waitForTimeout(400);
  console.log('页数/目录栏:', await p.evaluate(() => ({
    pages: document.querySelectorAll('section.page').length,
    rails: document.querySelectorAll('nav.prail').length,
    active: document.querySelectorAll('section.page.active').length })));

  // 1) 六个新卡直达
  for (const [pid, id] of [['yuanqu','p-wangshifu-changting'],['songwen','p-shenkuo-huoban'],
      ['hanprose','p-simaqian-chenshe'],['zhuzi','p-mengzi-dedaoduozhu'],
      ['novel','p-xiyou-houwang'],['novel','p-sanguo-caochuan']]) {
    await p.goto(file + '#' + pid + '::' + id, { waitUntil: 'load' }); await p.waitForTimeout(650);
    const st = await p.evaluate((i) => {
      const el = document.getElementById(i); if (!el) return null;
      const v = el.querySelector('.verse');
      const rail = document.querySelector('section.page.active nav.prail a.on');
      return { top: Math.round(el.getBoundingClientRect().top),
               chars: v ? v.textContent.replace(/\s/g,'').length : 0,
               dims: el.querySelectorAll('.dim').length,
               rail: rail ? rail.textContent.trim().slice(0,10) : null };
    }, id);
    console.log('直达', id, JSON.stringify(st));
  }

  // 2) 教材页点击九行
  await p.goto(file + '#jiaocai', { waitUntil: 'load' }); await p.waitForTimeout(400);
  const rows = await p.evaluate(() => [...document.querySelectorAll('#jiaocai a[data-goto^="novel::"], #jiaocai a[data-goto="songwen::p-shenkuo-huoban"], #jiaocai a[data-goto="zhuzi::p-mengzi-dedaoduozhu"], #jiaocai a[data-goto="hanprose::p-simaqian-chenshe"], #jiaocai a[data-goto="yuanqu::p-wangshifu-changting"]')]
    .map(a => [a.textContent.trim(), a.getAttribute('data-goto')]));
  console.log('教材表新增行:', rows.length, JSON.stringify(rows));
  for (const [txt, go] of rows) {
    await p.goto(file + '#jiaocai', { waitUntil: 'load' }); await p.waitForTimeout(300);
    await p.evaluate((g) => { const a = document.querySelector('#jiaocai a[data-goto="' + g + '"]'); a && a.click(); }, go);
    await p.waitForTimeout(780);
    const st = await p.evaluate((g) => {
      const id = g.split('::')[1];
      const el = document.getElementById(id);
      const pg = document.querySelector('section.page.active');
      return { page: pg && pg.id, top: el ? Math.round(el.getBoundingClientRect().top) : null };
    }, go);
    console.log('  点击', txt, go, JSON.stringify(st));
  }

  // 3) 搜索
  await p.goto(file + '#novel', { waitUntil: 'load' }); await p.waitForTimeout(500);
  console.log('novel 目录条数:', await p.evaluate(() => document.querySelectorAll('#novel nav.prail a').length));
  for (const q of ['长亭送别', '草船借箭', '陈涉世家', '得道多助']) {
    await p.goto(file, { waitUntil: 'load' }); await p.waitForTimeout(300);
    await p.keyboard.press('/'); await p.waitForTimeout(130);
    await p.keyboard.type(q, { delay: 12 }); await p.waitForTimeout(260);
    const r = await p.evaluate(() => [...document.querySelectorAll('.sr-item')].slice(0,2).map(x => x.textContent.replace(/\s+/g,' ').trim().slice(0,26)));
    console.log('搜索[' + q + ']:', JSON.stringify(r));
    await p.keyboard.press('Escape'); await p.waitForTimeout(120);
  }

  // 4) 移动端
  const m = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await m.goto(file + '#novel', { waitUntil: 'load' }); await m.waitForTimeout(500);
  console.log('移动端溢出:', await m.evaluate(() => document.body.scrollWidth - window.innerWidth));
  await m.screenshot({ path: 'audit/s32-novel-mobile.png' });
  await p.goto(file + '#yuanqu::p-wangshifu-changting', { waitUntil: 'load' }); await p.waitForTimeout(600);
  await p.screenshot({ path: 'audit/s33-changting.png' });
  console.log('JS 报错:', errs.length ? errs : '无');
  await b.close();
})();
