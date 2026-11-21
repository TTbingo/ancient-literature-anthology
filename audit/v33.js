const { chromium } = require('playwright');
const path=require('path');
(async()=>{
 const file='file:///'+path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g,'/');
 const b=await chromium.launch();
 for (const w of [1440,1180,768,390]) {
  const p=await b.newPage({viewport:{width:w,height:950}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(file+'#xuanxiu',{waitUntil:'load'}); await p.waitForTimeout(650);
  const r=await p.evaluate(()=>{
    const t=document.querySelector('table.xu-table'); if(!t) return null;
    const box=t.closest('.tscroll');
    const rows=[...t.rows].slice(1);
    const unitWrap=[...t.querySelectorAll('td.xu-unit')].map(c=>{
      const h=c.getBoundingClientRect().height, lh=parseFloat(getComputedStyle(c).lineHeight)||20;
      return {txt:c.textContent.trim(), h:Math.round(h), lines:Math.round(h/lh), sw:c.scrollWidth, cw:c.clientWidth};
    });
    return {
      cols:[...t.rows[0].cells].map(c=>c.textContent.trim()),
      colW:[...t.rows[0].cells].map(c=>Math.round(c.getBoundingClientRect().width)),
      tableW:Math.round(t.getBoundingClientRect().width),
      boxC:box.clientWidth, boxS:box.scrollWidth,
      rows:rows.length,
      ov:[...t.querySelectorAll('td,th')].filter(c=>c.scrollWidth-c.clientWidth>1).map(c=>c.textContent.trim().slice(0,10)),
      bodyOv: document.body.scrollWidth-innerWidth,
      unitWrap,
      links:t.querySelectorAll('a.tlink').length,
      titleAlign: getComputedStyle(t.querySelector('td.xu-title')).textAlign,
      unitNowrap: getComputedStyle(t.querySelector('td.xu-unit')).whiteSpace,
    };
  });
  console.log(w, JSON.stringify(r));
  if ([1440,390].includes(w)) { await p.evaluate(()=>document.getElementById('xu-list').scrollIntoView({block:'start'})); await p.waitForTimeout(300); await p.screenshot({path:'audit/s35-xulist-'+w+'.png'}); }
  console.log('  JS错误', errs.length);
  await p.close();
 }
 await b.close();
})();
