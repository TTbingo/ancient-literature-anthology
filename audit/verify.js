const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  const url = 'file:///D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html';
  await p.goto(url, { waitUntil: 'load' });

  const activeId = async () => p.evaluate(() => document.querySelector('.page.active').id);
  console.log('初始页:', await activeId());

  // 1 目录点击进入新增页
  await p.click('.toc-group a[data-target="xiaowen"]');
  console.log('点击目录→小学文言启蒙:', await activeId());
  console.log('  卡片数:', await p.evaluate(() => document.querySelectorAll('#xiaowen .poem').length));

  await p.click('.toc-group a[data-target="xiandai"]');
  console.log('点击目录→近现代诗词:', await activeId());
  console.log('  卡片数:', await p.evaluate(() => document.querySelectorAll('#xiandai .poem').length));

  // 2 首页卡片 data-goto
  await p.click('.toc-group a[data-target="home"]');
  await p.click('.quick[data-goto="xiaowen"]');
  console.log('首页卡片→小学文言启蒙:', await activeId());

  // 3 上下篇
  await p.click('#prevBtn');
  console.log('上一篇:', await activeId());
  await p.click('#nextBtn');
  console.log('下一篇:', await activeId());

  // 4 键盘翻页
  await p.keyboard.press('ArrowRight');
  console.log('键盘右翻:', await activeId());

  // 5 深链
  await p.goto(url + '#xiandai', { waitUntil: 'load' });
  console.log('URL深链#xiandai:', await activeId());

  // 6 李白页内锚点兼容
  await p.goto(url + '#libai', { waitUntil: 'load' });
  await p.evaluate(() => { location.hash = '#index'; });
  await p.waitForTimeout(400);
  console.log('李白页内锚点#index 后仍在:', await activeId());

  console.log('JS错误:', errs.length ? errs : '无');
  await b.close();
})();
