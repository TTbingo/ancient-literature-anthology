const { chromium } = require('playwright');
const path=require('path');
(async()=>{
 const file='file:///'+path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g,'/');
 const b=await chromium.launch();
 for (const w of [1440, 390]) {
  const p=await b.newPage({viewport:{width:w,height:900}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(file,{waitUntil:'load'}); await p.waitForTimeout(650);
  await p.evaluate(()=>{const i=document.getElementById('q');i.focus();i.value='先天下之忧而忧';i.dispatchEvent(new Event('input',{bubbles:true}));});
  await p.waitForTimeout(300);
  console.log(w, await p.evaluate(()=>{
    const pn=document.getElementById('srPanel');
    return {show:getComputedStyle(pn).display, w:Math.round(pn.getBoundingClientRect().width),
      items:[...pn.querySelectorAll('.sr-item')].length,
      first:pn.querySelector('.sr-item')?.textContent.trim().slice(0,50),
      overflowX: pn.scrollWidth-pn.clientWidth,
      bodyOv: document.body.scrollWidth-innerWidth};
  }));
  await p.screenshot({path:'audit/s37-search-'+w+'.png'});
  // 键盘 Enter
  await p.keyboard.press('ArrowDown'); await p.keyboard.press('Enter');
  await p.waitForTimeout(1000);
  console.log('  回车落点', await p.evaluate(()=>{const h=(location.hash||'').replace('#','');const [pg,id]=h.split('::');
    const el=id?document.getElementById(id):null; return {pg,id,top:el?Math.round(el.getBoundingClientRect().top):null};}));
  console.log('  JS错误', errs.length);
  await p.close();
 }
 await b.close();
})();
