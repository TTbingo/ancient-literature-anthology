const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  const url = 'file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
  await p.goto(url, { waitUntil: 'load' });
  await p.waitForTimeout(400);

  const active0 = await p.evaluate(() => document.querySelector('.page.active').id);
  console.log('初始页:', active0);

  // 1) 进入教材顺序索引页
  await p.evaluate(() => document.querySelector('[data-target="jiaocai"]').click());
  await p.waitForTimeout(300);
  const jcRows = await p.evaluate(() => document.querySelectorAll('#jiaocai a[data-goto]').length);
  console.log('索引页可点条目:', jcRows);

  // 2) 点击索引页里"咏鹅"直达
  const r1 = await p.evaluate(() => {
    const a = [...document.querySelectorAll('#jiaocai a[data-goto]')].find(x => x.textContent.includes('咏鹅'));
    if (!a) return { ok: false };
    const go = a.getAttribute('data-goto');
    a.click();
    return { ok: true, go };
  });
  await p.waitForTimeout(700);
  const s1 = await p.evaluate(() => ({
    page: document.querySelector('.page.active').id,
    scrollY: Math.round(window.scrollY),
    hash: location.hash,
    visible: (() => { const el = document.getElementById('p-yongue'); if (!el) return null; const r = el.getBoundingClientRect(); return { top: Math.round(r.top), inView: r.top > -50 && r.top < window.innerHeight }; })()
  }));
  console.log('点击咏鹅:', r1, '→', JSON.stringify(s1));

  // 3) 杜甫页内阶段目录跳转
  await p.evaluate(() => document.querySelector('[data-target="dufu"]').click());
  await p.waitForTimeout(300);
  const tocLinks = await p.evaluate(() => document.querySelectorAll('#dufu .sub-toc a').length);
  await p.evaluate(() => { const a = [...document.querySelectorAll('#dufu .sub-toc a')].find(x => x.textContent.includes('漂泊西南')); if (a) a.click(); });
  await p.waitForTimeout(700);
  const s2 = await p.evaluate(() => ({
    scrollY: Math.round(window.scrollY),
    targetTop: (() => { const el = document.getElementById('dufu-s4'); return el ? Math.round(el.getBoundingClientRect().top) : null; })()
  }));
  console.log('杜甫页内目录链接数:', tocLinks, '跳到 s4:', JSON.stringify(s2));

  // 4) 合篇页：作者卡后面是否紧跟作品（可视化检查两个节点距离）
  await p.evaluate(() => document.querySelector('[data-target="xinqiji"]').click());
  await p.waitForTimeout(300);
  const xq = await p.evaluate(() => {
    const card = document.getElementById('a-xinqiji') || document.querySelector('#xinqiji .author-card');
    const poem = card ? card.nextElementSibling : null;
    return { cardId: card && card.id, nextTag: poem && poem.className, nextId: poem && poem.id };
  });
  console.log('辛弃疾卡后紧邻:', JSON.stringify(xq));

  // 5) 键盘翻页
  const before = await p.evaluate(() => document.querySelector('.page.active').id);
  await p.keyboard.press('ArrowRight');
  await p.waitForTimeout(300);
  const after = await p.evaluate(() => document.querySelector('.page.active').id);
  console.log('键盘右翻页:', before, '→', after);

  // 6) 深链（页面::锚点）
  await p.goto(url + '#sushi::p-sushi-chibifu', { waitUntil: 'load' });
  await p.waitForTimeout(800);
  const s3 = await p.evaluate(() => {
    const el = document.getElementById('p-sushi-chibifu');
    return { page: document.querySelector('.page.active').id, found: !!el, top: el ? Math.round(el.getBoundingClientRect().top) : null };
  });
  console.log('深链直达赤壁赋:', JSON.stringify(s3));

  console.log('JS 错误:', errs.length ? errs : '无');
  await b.close();
})();
