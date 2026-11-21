const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto(file + '#indexall', { waitUntil: 'load' }); await p.waitForTimeout(600);

  // 1. 全量校验 data-goto 目标是否存在
  const bad = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('#indexall [data-goto]').forEach(a => {
      const v = a.getAttribute('data-goto');
      if (!v.includes('::')) { if (!document.getElementById(v)) out.push(v); return; }
      const [pg, id] = v.split('::');
      const sec = document.getElementById(pg);
      if (!sec || !sec.querySelector('#' + CSS.escape(id))) out.push(v);
    });
    return out;
  });
  console.log('坏链:', bad.length, bad.slice(0, 10));
  const total = await p.evaluate(() => document.querySelectorAll('#indexall [data-goto]').length);
  console.log('data-goto 总数:', total);

  // 2. 逐类点击测试
  const tests = [
    ['专页·守株待兔', '.t-new a[data-goto="xiaowen::p-shouzhu"]'],
    ['专页·致云雀', '.t-new a[data-goto="xiandai::p-zhiyunque"]'],
    ['重点·李白名', '.t-ming a[data-goto="libai"]'],
    ['重点·江城子乙卯', '.t-ming a[data-goto="sushi::p-sushi-jiangchengzi-yimao"]'],
    ['合篇·王实甫', '.t-groups a[data-goto="yuanqu::a-wangshifu"]'],
    ['延伸·登快阁', '.t-extend a[data-goto="songshi::p-dengkuaige-huang"]'],
    ['小说·三顾茅庐', '.t-novel a[data-goto="novel::p-sanguo-sangumaolu"]'],
  ];
  for (const [name, sel] of tests) {
    await p.evaluate(() => { location.hash = '#indexall'; });
    await p.waitForTimeout(400);
    const ok = await p.evaluate(s => {
      const a = document.querySelector(s); if (!a) return 'no-el';
      a.click(); return 'clicked';
    }, sel);
    await p.waitForTimeout(1100);
    const r = await p.evaluate(() => {
      const sec = document.querySelector('section.page.active');
      const tgt = document.querySelector('.target-flash,.flash') || null;
      const pg = sec ? sec.id : null;
      // 取可见页面顶部元素的位置
      const ids = (location.hash || '').replace('#','').split('::');
      let top = null, id = ids[1] || null;
      if (id) { const el = document.getElementById(id); if (el) top = Math.round(el.getBoundingClientRect().top); }
      return { pg, id, top, hash: location.hash, title: document.querySelector('section.page.active .ptitle')?.textContent.trim().slice(0,20) };
    });
    console.log(name, ok, JSON.stringify(r));
  }

  // 3. 手机端横向滚动能力
  const p2 = await b.newPage({ viewport: { width: 390, height: 800 } });
  await p2.goto(file + '#indexall', { waitUntil: 'load' }); await p2.waitForTimeout(500);
  console.log('390 滚动容器:', await p2.evaluate(() => [...document.querySelectorAll('#indexall .tw')].map(w => ({ c: w.clientWidth, s: w.scrollWidth }))));
  console.log('JS错误:', errs.length, errs.slice(0, 3));
  await b.close();
})();
