const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
  const errs=[]; p.on('pageerror', e=>errs.push(String(e)));
  await p.goto(file + '#xuanxiu', { waitUntil: 'load' }); await p.waitForTimeout(700);
  console.log('选修新表', await p.evaluate(() => {
    const t = document.querySelector('table.xu-table');
    return t ? { rows: t.rows.length, links: t.querySelectorAll('a.tlink').length, w: Math.round(t.getBoundingClientRect().width) } : null;
  }));
  console.log('页内目录', await p.evaluate(() => [...document.querySelectorAll('#xuanxiu .prail-list .l1>a')].map(a=>a.textContent.trim())));
  // 点最后一课马伶传
  await p.evaluate(() => { document.querySelector('a.tlink[data-goto="xuanxiu::p-xu-maling"]').click(); });
  await p.waitForTimeout(900);
  console.log('马伶传落点', await p.evaluate(() => { const e=document.getElementById('p-xu-maling'); return {top: Math.round(e.getBoundingClientRect().top), hash: location.hash}; }));
  // 李白表
  await p.evaluate(() => { location.hash = '#libai'; }); await p.waitForTimeout(500);
  const lib = await p.evaluate(() => {
    const t = [...document.querySelectorAll('#libai table')][0];
    return { links: t.querySelectorAll('a[data-goto]').length, sample: t.querySelector('a[data-goto]')?.getAttribute('data-goto') };
  });
  console.log('李白索引表', JSON.stringify(lib));
  await p.evaluate(() => { document.querySelector('a[data-goto="libai::p-mengyou"]').click(); });
  await p.waitForTimeout(900);
  console.log('梦游天姥落点', await p.evaluate(() => ({top: Math.round(document.getElementById('p-mengyou').getBoundingClientRect().top), hash: location.hash})));
  // 全站 tlink 校验
  console.log('全站 tlink 校验', await p.evaluate(() => {
    let n=0, bad=[];
    document.querySelectorAll('a.tlink').forEach(a=>{ n++; const v=a.getAttribute('data-goto'); if(!v) return;
      const [pg,id]=v.split('::'); const sec=document.getElementById(pg);
      if(!sec || !sec.querySelector('#'+CSS.escape(id))) bad.push(v); });
    return { n, bad: bad.slice(0,5), badN: bad.length };
  }));
  console.log('JS错误', errs.length, errs.slice(0,3));
  await p.evaluate(() => document.getElementById('xu-list').scrollIntoView({block:'start'}));
  await p.waitForTimeout(300);
  await p.screenshot({ path: 'audit/s31-xulist.png' });
  await b.close();
})();
