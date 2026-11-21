const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto(file + '#dufu', { waitUntil: 'load' }); await p.waitForTimeout(600);

  // 1) 全站 tlink 目标校验
  const bad = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('a.tlink').forEach(a => {
      const v = a.getAttribute('data-goto'); if (!v) return;
      const [pg, id] = v.split('::');
      const sec = document.getElementById(pg);
      if (!sec || !sec.querySelector('#' + CSS.escape(id))) out.push(v);
    });
    return out;
  });
  const n = await p.evaluate(() => document.querySelectorAll('a.tlink').length);
  console.log('tlink 数', n, '坏链', bad.length, bad.slice(0,5));

  // 2) 点几个表内链接
  const tests = [
    ['杜甫·登高', '#dufu a.tlink[data-goto="dufu::p-denggao-df"]'],
    ['中晚唐·江雪→唐古文', '#tangwan a.tlink[data-goto="tangguwen::p-jiangxue-liuzongyuan"]'],
    ['毛·井冈山', '#mao a.tlink[data-goto="mao::p-mao-jinggangshan"]'],
    ['小学文言·学弈', '#xiaowen a.tlink[data-goto="xiaowen::p-xueyi"]'],
  ];
  for (const [name, sel] of tests) {
    await p.evaluate(() => { location.hash = '#indexall'; }); await p.waitForTimeout(350);
    const ok = await p.evaluate(s => { const a = document.querySelector(s); if (!a) return 'no-el'; a.click(); return 'ok'; }, sel);
    await p.waitForTimeout(1000);
    const r = await p.evaluate(() => {
      const h = (location.hash||'').replace('#',''); const [pg,id] = h.split('::');
      const el = id ? document.getElementById(id) : null;
      return { pg, id, top: el ? Math.round(el.getBoundingClientRect().top) : null, active: document.querySelector('section.page.active')?.id };
    });
    console.log(name, ok, JSON.stringify(r));
  }

  // 3) 李白页原有的 #p- 链接是否可用
  await p.evaluate(() => { location.hash = '#libai'; }); await p.waitForTimeout(500);
  const before = await p.evaluate(() => Math.round(document.getElementById('p-jingyesi').getBoundingClientRect().top));
  await p.evaluate(() => { document.querySelector('a[href="#p-jingyesi"]').click(); });
  await p.waitForTimeout(900);
  const after = await p.evaluate(() => ({ top: Math.round(document.getElementById('p-jingyesi').getBoundingClientRect().top), hash: location.hash, active: document.querySelector('section.page.active')?.id }));
  console.log('李白原链接 点击前top', before, '点击后', JSON.stringify(after));
  console.log('JS错误', errs.length, errs.slice(0,3));
  await b.close();
})();
