const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/教材作者集成/index.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(file, { waitUntil: 'load' }); await p.waitForTimeout(400);

  console.log('页数/目录栏:', await p.evaluate(() => ({
    pages: document.querySelectorAll('section.page').length,
    rails: document.querySelectorAll('nav.prail').length
  })));

  // 1. 从教材顺序页点四篇
  for (const [name, wantId] of [['智取生辰纲','p-shuihu-shengchengang'],['范进中举','p-rulin-fanjin'],['三顾茅庐','p-sanguo-sangumaolu'],['刘姥姥进大观园','p-honglou-liulaolao']]) {
    await p.goto(file + '#jiaocai', { waitUntil: 'load' }); await p.waitForTimeout(400);
    const go = await p.evaluate((n) => {
      const a = [...document.querySelectorAll('#jiaocai a[data-goto]')].find(x => x.textContent.includes(n));
      if (!a) return null; const g = a.getAttribute('data-goto'); a.click(); return g;
    }, name);
    await p.waitForTimeout(850);
    const st = await p.evaluate((id) => {
      const pg = document.querySelector('section.page.active');
      const el = document.getElementById(id);
      const rail = document.querySelector('section.page.active nav.prail a.on');
      return { page: pg && pg.id, top: el ? Math.round(el.getBoundingClientRect().top) : null, rail: rail ? rail.textContent.trim().slice(0,14) : null };
    }, wantId);
    console.log('教材页→', name, go, JSON.stringify(st));
  }

  // 2. 选修页原"未收"两处现在应可点
  await p.goto(file + '#xuanxiu::a-luoguanzhong', { waitUntil: 'load' }); await p.waitForTimeout(600);
  const xu = await p.evaluate(() => {
    const links = [...document.querySelectorAll('#xuanxiu a.xlink')].filter(a => /三顾茅庐|范进中举/.test(a.textContent));
    return links.map(a => ({ t: a.textContent.trim(), g: a.getAttribute('data-goto') }));
  });
  console.log('选修页互链:', JSON.stringify(xu));
  console.log('未收标记:', await p.evaluate(() => document.querySelectorAll('.xmiss').length));

  // 3. 本页目录栏条数 + 搜索
  await p.goto(file + '#novel', { waitUntil: 'load' }); await p.waitForTimeout(600);
  console.log('novel 目录条数:', await p.evaluate(() => document.querySelectorAll('#novel nav.prail a').length));
  await p.keyboard.press('/'); await p.waitForTimeout(140);
  await p.keyboard.type('刘姥姥', { delay: 14 }); await p.waitForTimeout(280);
  console.log('搜索[刘姥姥]:', await p.evaluate(() => [...document.querySelectorAll('.sr-item')].slice(0,2).map(x => x.textContent.replace(/\s+/g,' ').trim().slice(0,24))));
  await p.keyboard.press('Escape');

  await p.goto(file + '#novel::p-sanguo-sangumaolu', { waitUntil: 'load' }); await p.waitForTimeout(700);
  await p.screenshot({ path: 'audit/s29-novel.png' });
  console.log('JS 报错:', errs.length ? errs : '无');
  await b.close();
})();
