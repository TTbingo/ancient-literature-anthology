const { chromium } = require('playwright');
const path = 'file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
  await p.goto(path); await p.waitForTimeout(500);
  await p.evaluate(()=>{location.hash='#dufu';}); await p.waitForTimeout(400);
  await p.evaluate(()=>window.scrollTo(0,1200)); await p.waitForTimeout(400);
  await p.screenshot({path:'audit/s1-dufu.png'});
  await p.evaluate(()=>{location.hash='#tangwan';}); await p.waitForTimeout(300);
  await p.evaluate(()=>window.scrollTo(0,900)); await p.waitForTimeout(400);
  await p.screenshot({path:'audit/s2-tangwan.png'});
  await p.evaluate(()=>{location.hash='#libai';}); await p.waitForTimeout(300);
  await p.evaluate(()=>window.scrollTo(0,1400)); await p.waitForTimeout(400);
  await p.screenshot({path:'audit/s3-libai.png'});
  await p.evaluate(()=>{location.hash='#home';}); await p.waitForTimeout(400);
  await p.screenshot({path:'audit/s4-home.png'});
  // 窄屏
  await p.setViewportSize({width:430,height:880});
  await p.evaluate(()=>{location.hash='#dufu';}); await p.waitForTimeout(400);
  await p.screenshot({path:'audit/s5-mobile.png'});
  await b.close();
})();
