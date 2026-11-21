const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const file = 'file:///' + path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/教材作者集成/index.html').replace(/\\/g, '/');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 950 } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));

  const cases = [
    ['《〈老子〉四章》', 'zhuzi', 'p-laozi-sizhang'],
    ['《老子》十章', 'xuanxiu', 'p-xu-laozi'],
    ['《庖丁解牛》', 'zhuzi', 'p-zhuangzi-paodingjieniu'],
    ['《琵琶行并序》', 'baijuyi', 'p-pipa-bjy'],
    ['《屈原列传》', 'hanprose', 'p-simaqian-qunyuanliezhuan'],
    ['《滕王阁序》', 'tangchu', 'p-tengwangge-wangbo'],
    ['《庄子》五石之瓠', 'zhuzi', 'p-zhuangzi-wushizhihu'],
    ['《马伶传》', 'xuanxiu', 'p-xu-maling']
  ];

  for (const [label, wantPage, wantId] of cases) {
    await p.goto(file + '#xuanxiu', { waitUntil: 'load' });
    await p.waitForTimeout(450);
    const clicked = await p.evaluate((lb) => {
      const as = [...document.querySelectorAll('a.xlink')];
      const a = as.find(x => x.textContent.trim() === lb);
      if (!a) return null;
      a.click();
      return a.getAttribute('data-goto');
    }, label);
    await p.waitForTimeout(900);
    const st = await p.evaluate((id) => {
      const pg = document.querySelector('section.page.active');
      const el = document.getElementById(id);
      const rail = document.querySelector('section.page.active nav.prail a.on');
      return {
        page: pg && pg.id,
        top: el ? Math.round(el.getBoundingClientRect().top) : null,
        rail: rail ? rail.textContent.trim().slice(0, 12) : null
      };
    }, wantId);
    const ok = st.page === wantPage && st.top !== null && st.top > 40 && st.top < 120;
    console.log((ok ? 'PASS' : 'FAIL'), label, '→', clicked, JSON.stringify(st));
  }

  // 未收录标记不可点
  const miss = await p.evaluate(() => {
    const el = [...document.querySelectorAll('.xmiss')];
    return el.map(x => ({ t: x.textContent.trim(), tag: x.tagName, goto: x.getAttribute('data-goto') }));
  });
  console.log('未收录标记:', JSON.stringify(miss));

  // 视觉截图：老子卡
  await p.goto(file + '#xuanxiu::a-xu-laozi', { waitUntil: 'load' });
  await p.waitForTimeout(700);
  await p.screenshot({ path: 'audit/s28-xlink-laozi.png' });
  await p.goto(file + '#xuanxiu::a-xu-baijuyi', { waitUntil: 'load' }).catch(() => {});
  console.log('JS 报错:', errs.length ? errs : '无');
  await b.close();
})();
