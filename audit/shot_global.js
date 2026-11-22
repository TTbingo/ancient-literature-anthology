// 全书视觉推广截图：首页、盛唐页、诸子页、屈原页、手机端
const { chromium } = require('playwright');
const path = require('path');
const FILE = 'file:///' + path.resolve(__dirname, '../统编教材古代作家文学集成.html').replace(/\\/g, '/');
const DIR = path.resolve(__dirname, '../design-demos/global-shots');
const fs = require('fs');
if (!fs.existsSync(DIR)) fs.mkdirSync(DIR, { recursive: true });

async function shot(p, pageId, anchor, name) {
  await p.evaluate(pg => {
    var link = document.querySelector('.sidebar a[data-target="' + pg + '"]');
    if (link) link.click();
  }, pageId);
  await p.waitForTimeout(400);
  if (anchor) {
    await p.evaluate(a => { var e = document.getElementById(a); if (e) e.scrollIntoView({ block: 'start' }); }, anchor);
  } else {
    await p.evaluate(() => window.scrollTo(0, 0));
  }
  await p.waitForTimeout(350);
  await p.screenshot({ path: path.join(DIR, name) });
  console.log('截图:', name);
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  await p.goto(FILE);
  await p.waitForTimeout(800);

  await shot(p, 'home', null, '全书-首页.png');
  await shot(p, 'tangsheng', 'p-chunxiao-meng', '全书-盛唐-春晓.png');
  await shot(p, 'zhuzi', 'p-lunyu-xuan', '全书-诸子-论语.png');
  await shot(p, 'quyuan', 'p-lisao-qu', '全书-屈原-离骚.png');
  await shot(p, 'tangchu', 'p-congjunxing-yangjiong', '全书-初唐-杨炯从军行.png');
  await shot(p, 'xiaowen', 'p-shouzhu', '全书-小学文言-守株.png');

  const m = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await m.goto(FILE);
  await m.waitForTimeout(800);
  await m.evaluate(() => window.scrollTo(0, 0));
  await m.waitForTimeout(300);
  await m.screenshot({ path: path.join(DIR, '全书-手机-首页.png') });
  await m.evaluate(() => {
    var link = document.querySelector('.sidebar a[data-target="tangsheng"]');
    if (link) link.click();
  });
  await m.waitForTimeout(400);
  await m.evaluate(() => { var e = document.getElementById('p-chunxiao-meng'); if (e) e.scrollIntoView({ block: 'start' }); });
  await m.waitForTimeout(300);
  await m.screenshot({ path: path.join(DIR, '全书-手机-春晓.png') });
  console.log('截图: 手机端');
  await b.close();
})();
