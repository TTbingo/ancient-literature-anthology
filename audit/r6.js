const { chromium } = require('playwright');
const path = 'file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });
  await p.goto(path);
  await p.waitForTimeout(600);

  // 1. rail 数量与条目
  const railInfo = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.page').forEach(pg => {
      const r = pg.querySelector('.prail');
      out.push({
        id: pg.id,
        items: r ? r.querySelectorAll('a[data-jump]').length : -1,
        l1: r ? r.querySelectorAll('.l1').length : 0,
        hd: r ? r.querySelector('.prail-hd').textContent.trim() : '',
        subTocShown: !!pg.querySelector('.sub-toc') && pg.querySelector('.sub-toc').offsetParent !== null
      });
    });
    return out;
  });
  console.log('页面数', railInfo.length);
  railInfo.forEach(r => console.log(`${r.id.padEnd(14)} 条目=${String(r.items).padStart(3)} L1=${String(r.l1).padStart(2)} ${r.subTocShown ? '✗旧目录仍显示' : ''} ${r.hd}`));
  console.log('无条目页:', railInfo.filter(r => r.items <= 0).map(r => r.id).join(',') || '无');

  // 2. 桌面布局：rail 是否 sticky 且不与正文重叠
  await p.evaluate(() => { location.hash = '#dufu'; });
  await p.waitForTimeout(400);
  const lay = await p.evaluate(() => {
    const r = document.querySelector('#dufu .prail').getBoundingClientRect();
    const b = document.querySelector('#dufu .pbody').getBoundingClientRect();
    return { railTop: Math.round(r.top), railW: Math.round(r.width), railRight: Math.round(r.right), bodyRight: Math.round(b.right), overlap: b.right > r.left };
  });
  console.log('杜甫页布局', JSON.stringify(lay));

  // 3. 滚动后 sticky 与高亮
  await p.evaluate(() => window.scrollTo(0, 3000));
  await p.waitForTimeout(500);
  const after = await p.evaluate(() => {
    const r = document.querySelector('#dufu .prail').getBoundingClientRect();
    const on = document.querySelector('#dufu .prail a.on');
    return { railTop: Math.round(r.top), onText: on ? on.textContent : '(无)', scrollY: Math.round(window.scrollY) };
  });
  console.log('滚动3000后', JSON.stringify(after));

  // 4. 点条目跳转定位精度
  const jumpTest = await p.evaluate(() => {
    const a = document.querySelector('#dufu .prail a[data-jump="p-chunwang-df"]') || document.querySelector('#dufu .prail a[data-jump]');
    const id = a.getAttribute('data-jump');
    a.click();
    return id;
  });
  await p.waitForTimeout(900);
  const pos = await p.evaluate(id => {
    const t = document.getElementById(id).getBoundingClientRect();
    return { id, top: Math.round(t.top) };
  }, jumpTest);
  console.log('点击条目跳转', JSON.stringify(pos));

  // 5. 李白页 rail（含 section.stage）
  await p.evaluate(() => { location.hash = '#libai'; });
  await p.waitForTimeout(500);
  const libai = await p.evaluate(() => {
    const r = document.querySelector('#libai .prail');
    const items = [...r.querySelectorAll('a[data-jump]')].map(a => a.textContent);
    return { n: items.length, first: items.slice(0, 6), navTocHidden: getComputedStyle(document.querySelector('#libai nav.toc')).display };
  });
  console.log('李白页', JSON.stringify(libai));

  // 6. 窄屏收起
  await p.setViewportSize({ width: 480, height: 860 });
  await p.waitForTimeout(400);
  const mob = await p.evaluate(() => {
    const rail = document.querySelector('#libai .prail');
    const list = rail.querySelector('.prail-list');
    const before = getComputedStyle(list).display;
    rail.querySelector('.prail-hd').click();
    const after = getComputedStyle(list).display;
    const r = rail.getBoundingClientRect();
    const mb = document.querySelector('.mobile-bar').getBoundingClientRect();
    const tb = document.querySelector('.topbar').getBoundingClientRect();
    return { before, after, railW: Math.round(r.width), mobileBarTop: Math.round(mb.top), mobileBarBottom: Math.round(mb.bottom), topbarTop: Math.round(tb.top) };
  });
  console.log('窄屏', JSON.stringify(mob));

  console.log('错误', errs.length ? errs : '无');
  await b.close();
})();
