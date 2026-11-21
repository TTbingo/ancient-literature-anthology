const { chromium } = require('playwright');
const path='file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
(async()=>{
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1440,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text());});
 await p.goto(path); await p.waitForTimeout(500);

 async function search(q){
   await p.click('#q'); await p.fill('#q',''); await p.type('#q',q);
   await p.waitForTimeout(250);
   return await p.evaluate(()=>{
     const items=[...document.querySelectorAll('.sr-item')];
     return {n:items.length, shown:getComputedStyle(document.getElementById('srPanel')).display,
             top:items.slice(0,5).map(e=>e.textContent.replace(/\s+/g,' ').trim())};
   });
 }
 for(const q of ['杜甫','静夜思','苏轼','山居秋暝','琵琶行','小学文言','陈子昂','渔家傲']){
   const r=await search(q);
   console.log(q.padEnd(6), r.shown, '结果'+r.n, JSON.stringify(r.top.slice(0,3)));
 }

 // 点击第一条
 await p.click('#q'); await p.fill('#q',''); await p.type('#q','静夜思'); await p.waitForTimeout(250);
 await p.click('.sr-item');
 await p.waitForTimeout(800);
 console.log('点击后', await p.evaluate(()=>{
   const p=document.querySelector('.page.active');
   const el=document.querySelector('.page.active .poem[data-hit], .page.active');
   return {page:p.id, hash:location.hash, crumb:document.getElementById('crumb').textContent,
     srOpen:getComputedStyle(document.getElementById('srPanel')).display};
 }));

 // 键盘：/ 聚焦，↓ 选择，Enter
 await p.keyboard.press('Escape');
 await p.evaluate(()=>window.scrollTo(0,0));
 await p.keyboard.press('/');
 await p.waitForTimeout(150);
 const focused=await p.evaluate(()=>document.activeElement.id);
 await p.type('#q','李清照'); await p.waitForTimeout(250);
 await p.keyboard.press('ArrowDown'); await p.keyboard.press('ArrowDown');
 await p.keyboard.press('Enter'); await p.waitForTimeout(700);
 console.log('键盘', focused, await p.evaluate(()=>({page:(document.querySelector('.page.active')||{}).id, hash:location.hash})));

 // 无结果
 await p.fill('#q',''); await p.type('#q','zzzz不存在'); await p.waitForTimeout(200);
 console.log('无结果', await p.evaluate(()=>document.getElementById('srPanel').textContent.trim().slice(0,40)));

 // 截图
 await p.fill('#q',''); await p.type('#q','月'); await p.waitForTimeout(300);
 await p.screenshot({path:'audit/s10-search.png'});
 // 窄屏
 await p.setViewportSize({width:430,height:880}); await p.waitForTimeout(300);
 await p.fill('#q',''); await p.type('#q','月'); await p.waitForTimeout(300);
 await p.screenshot({path:'audit/s11-search-mobile.png'});
 console.log('错误', errs.length?errs:'无');
 await b.close();
})();
