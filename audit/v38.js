const { chromium } = require('playwright');
const path=require('path');
(async()=>{
 const file='file:///'+path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g,'/');
 const b=await chromium.launch();
 for (const w of [1440,1180,768,390]) {
  const p=await b.newPage({viewport:{width:w,height:950}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(file,{waitUntil:'load'}); await p.waitForTimeout(550);
  const r=await p.evaluate(()=>{
    const t=document.querySelector('table.clue');
    return {
      page:document.querySelector('section.page.active')?.id,
      stats:[...document.querySelectorAll('.stat b')].map(x=>x.textContent),
      quickCards:document.querySelectorAll('#home-map ~ .quick-grid .quick').length,
      clueRows:t?t.rows.length:0,
      clueCols:t?[...t.rows[0].cells].map(c=>c.textContent.trim()):[],
      colW:t?[...t.rows[0].cells].map(c=>Math.round(c.getBoundingClientRect().width)):[],
      tableW:t?Math.round(t.getBoundingClientRect().width):0,
      cellOv:t?[...t.querySelectorAll('td,th')].filter(c=>c.scrollWidth-c.clientWidth>1).map(c=>c.textContent.trim().slice(0,10)):[],
      bodyOv:document.body.scrollWidth-innerWidth,
      clueLinks:t?t.querySelectorAll('a[data-goto]').length:0,
      h2s:[...document.querySelectorAll('#home h2')].map(h=>h.textContent.trim()),
    };
  });
  console.log(w, JSON.stringify(r));
  if([1440,390].includes(w)){ await p.evaluate(()=>document.getElementById('home-feature').scrollIntoView({block:'start'})); await p.waitForTimeout(300); await p.screenshot({path:'audit/s41-home-'+w+'.png'}); }
  console.log('  JS错误',errs.length, errs.slice(0,2));
  await p.close();
 }
 // 点线索里的链接
 const p=await b.newPage({viewport:{width:1440,height:950}});
 await p.goto(file,{waitUntil:'load'}); await p.waitForTimeout(500);
 for (const [name,sel] of [['线索·苏轼','table.clue a[data-goto="sushi"]'],['地图·总索引','#home-map ~ .quick-grid .quick[data-goto="indexall"]'],['地图·编例','.quick[data-goto="method"]']]) {
   await p.evaluate(()=>{location.hash='#home';}); await p.waitForTimeout(400);
   const ok=await p.evaluate(s=>{const a=document.querySelector(s); if(!a) return 'no-el'; a.click(); return 'ok';},sel);
   await p.waitForTimeout(800);
   console.log(name, ok, await p.evaluate(()=>({active:document.querySelector('section.page.active')?.id, hash:location.hash, top:Math.round((document.querySelector('section.page.active')?.getBoundingClientRect().top)||0)})));
 }
 await b.close();
})();
