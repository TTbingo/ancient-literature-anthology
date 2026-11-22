// 全书视觉推广自检：抽样多页实测样式、色标、解析区原版排版、导航、链接、搜索
const { chromium } = require('playwright');
const path = require('path');
const FILE = 'file:///' + path.resolve(__dirname, '../统编教材古代作家文学集成.html').replace(/\\/g, '/');

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  p.on('pageerror', e => errors.push(e.message));
  await p.goto(FILE);
  await p.waitForTimeout(900);

  const r = await p.evaluate(() => {
    const pages = [].slice.call(document.querySelectorAll('section.page'));
    const poems = [].slice.call(document.querySelectorAll('.poem'));
    // 抽样：每类页面取一个代表作品的色标与标题字号
    const ids = ['p-chunxiao-meng','p-wangyue-df','p-lunyu-xuan','p-chusai-wangchangling',
      'p-yujiaao-fanzhongyan','p-shizuo-lunyu','p-lisao-qu','p-congjunxing-yangjiong',
      'p-liangzhouci-wanghan','p-lanlingling','p-tengwangge-wangbo','p-jishierlang-hanyu'];
    const samples = ids.map(id => {
      const el = document.getElementById(id);
      if (!el) return { id, missing: true };
      const im = el.querySelector('.idmark');
      const pt = el.querySelector('.ptitle');
      const ve = el.querySelector('.verse');
      const dm = el.querySelector('.dim');
      const k = dm && dm.querySelector('.k'), v = dm && dm.querySelector('.v');
      return {
        id, chip: el.getAttribute('data-chip'), mark: im ? im.textContent.trim() : null,
        ptitleFont: pt ? getComputedStyle(pt).fontSize : null,
        verseBg: ve ? getComputedStyle(ve).backgroundColor : null,
        kDisplay: k ? getComputedStyle(k).display : null,
        kFont: k ? getComputedStyle(k).fontSize : null,
        vFont: v ? getComputedStyle(v).fontSize : null
      };
    });
    // 页面封面字号抽样
    const covers = [].slice.call(document.querySelectorAll('.page .author-cover h1')).slice(0, 6)
      .map(x => ({ text: x.textContent.trim().slice(0, 12), font: getComputedStyle(x).fontSize, align: getComputedStyle(x.parentElement).textAlign }));
    // 坏链检查
    const anchors = [].slice.call(document.querySelectorAll('[data-goto]'));
    const targets = new Set([].slice.call(document.querySelectorAll('[id]')).map(x => x.id));
    const bad = anchors.filter(a => {
      const g = a.getAttribute('data-goto') || '';
      const id = g.indexOf('::') >= 0 ? g.split('::')[1] : g;
      return id && !targets.has(id);
    }).map(a => a.getAttribute('data-goto'));
    // 色标分布
    const dist = {};
    poems.forEach(el => { const c = el.getAttribute('data-chip') || '(无)'; dist[c] = (dist[c] || 0) + 1; });
    return {
      pages: pages.length, poems: poems.length,
      labeled: poems.filter(x => x.querySelector('.idmark')).length,
      sidebar: document.querySelectorAll('.sidebar a[data-target]').length,
      anchors: anchors.length, badLinks: [...new Set(bad)],
      topbar: getComputedStyle(document.querySelector('.topbar')).position,
      homeCoord: !!document.querySelector('#home .d2-coord'),
      quyuanCoord: !!document.querySelector('#quyuan .d2-coord'),
      d2bars: document.querySelectorAll('#home .d2-bar').length,
      quotes: window.__d2Quotes, dist, samples, covers
    };
  });

  // 搜索测试
  await p.click('.search input').catch(() => {});
  await p.fill('.search input', '离骚').catch(() => {});
  await p.waitForTimeout(300);
  const searchHits = await p.evaluate(() => document.querySelectorAll('.search-results a, .sr-item, .results a').length);

  console.log(JSON.stringify({ ...r, searchHits, pageErrors: errors }, null, 2));
  await b.close();
})();
