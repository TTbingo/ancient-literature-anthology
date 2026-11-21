const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const url = 'file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
  await p.goto(url + '#jiaocai', { waitUntil: 'load' }); await p.waitForTimeout(300);
  await p.evaluate(() => { const a=[...document.querySelectorAll('#jiaocai a[data-goto]')].find(x=>x.textContent.includes('咏鹅')); a.click(); });
  await p.waitForTimeout(900);
  console.log(await p.evaluate(() => { const el=document.getElementById('p-yonge-luobinwang'); const r=el.getBoundingClientRect(); return {page:document.querySelector('.page.active').id, top:Math.round(r.top), inView:r.top>-80&&r.top<300}; }));
  // 抽查几条不同学段的直达
  for (const t of ['两小儿辩日','渔家傲','浣溪沙','过零丁洋','致云雀','氓']) {
    await p.goto(url + '#jiaocai', { waitUntil: 'load' }); await p.waitForTimeout(250);
    const res = await p.evaluate((name) => {
      const rows=[...document.querySelectorAll('#jiaocai tr')];
      for (const r of rows) { const a=r.querySelector('a[data-goto]'); if(a&&a.textContent.includes(name)){ const go=a.getAttribute('data-goto'); a.click(); return go; } }
      return null;
    }, t);
    await p.waitForTimeout(700);
    const st = await p.evaluate((go) => { if(!go) return null; const id=go.split('::')[1]; const el=document.getElementById(id); return {page:document.querySelector('.page.active').id, top: el?Math.round(el.getBoundingClientRect().top):null}; }, res);
    console.log(t, '→', res, JSON.stringify(st));
  }
  await b.close();
})();
