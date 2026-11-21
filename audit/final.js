const { chromium } = require('playwright');
const path='file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1440,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text());});
 await p.goto(path); await p.waitForTimeout(500);
 // 索引规模
 console.log('索引', await p.evaluate(()=>{
   const l=[...document.querySelectorAll('.prail a[data-jump]')];
   return {页面:document.querySelectorAll('.page').length, 锚点:l.length,
     诗人:l.filter(a=>a.getAttribute('data-kind')==='author').length,
     诗篇:l.filter(a=>a.getAttribute('data-kind')==='poem').length};
 }));
 // 章节类搜索落点
 async function go(q){
   await p.fill('#q',''); await p.click('#q'); await p.type('#q',q); await p.waitForTimeout(250);
   await p.click('.sr-item'); await p.waitForTimeout(700);
   return await p.evaluate(()=>{
     const t=document.querySelector('.page.active');
     const h=location.hash.split('::');
     const el=h[1]?document.getElementById(h[1]):null;
     return {page:t.id, anchor:h[1]||'', top: el?Math.round(el.getBoundingClientRect().top):null};
   });
 }
 for(const q of ['少年出蜀','李清照','声声慢','岳阳楼记','曹刿论战','毛泽东']){
   console.log(q.padEnd(6), JSON.stringify(await go(q)));
 }
 // 目录栏仍正常
 console.log('rail', await p.evaluate(()=>{
   const pg=document.querySelector('.page.active'), r=pg.querySelector('.prail');
   return {items:r.querySelectorAll('a[data-jump]').length, on:!!r.querySelector('a.on')};
 }));
 // 移动端
 await p.setViewportSize({width:390,height:844});
 await p.fill('#q',''); await p.click('#q'); await p.type('#q','杜甫'); await p.waitForTimeout(300);
 console.log('移动端', await p.evaluate(()=>{
   const pn=document.getElementById('srPanel').getBoundingClientRect();
   const inp=document.getElementById('q').getBoundingClientRect();
   return {panelW:Math.round(pn.width), panelRight:Math.round(pn.right), vw:innerWidth,
     inputFullRow: Math.round(inp.width)>300, overflow: pn.right>innerWidth+1};
 }));
 await p.screenshot({path:'audit/s12-final-mobile.png'});
 console.log('错误', errs.length?errs:'无');
 await b.close();
})();
