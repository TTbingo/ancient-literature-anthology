const { chromium } = require('playwright');
const path=require('path');
(async()=>{
 const file='file:///'+path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g,'/');
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1440,height:950}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto(file,{waitUntil:'load'}); await p.waitForTimeout(700);

 // 首次正文检索耗时（含建索引）
 console.log('首次含建索引', await p.evaluate(()=>{
   const i=document.getElementById('q'); const t0=performance.now();
   i.value='报任安书'; i.dispatchEvent(new Event('input',{bubbles:true}));
   const t1=performance.now();
   return Math.round(t1-t0)+'ms';
 }));
 console.log('二次查询', await p.evaluate(()=>{
   const i=document.getElementById('q'); const t0=performance.now();
   i.value='落霞与孤鹜齐飞'; i.dispatchEvent(new Event('input',{bubbles:true}));
   return Math.round(performance.now()-t0)+'ms';
 }));
 console.log('名句结果', await p.evaluate(()=>[...document.querySelectorAll('#srPanel .sr-item')].slice(0,3).map(e=>e.textContent.trim())));
 console.log('别名·青莲居士', await p.evaluate(()=>{const i=document.getElementById('q');i.value='青莲居士';i.dispatchEvent(new Event('input',{bubbles:true}));
   return [...document.querySelectorAll('#srPanel .sr-item')].slice(0,2).map(e=>e.textContent.trim());}));
 console.log('别名·稼轩', await p.evaluate(()=>{const i=document.getElementById('q');i.value='稼轩';i.dispatchEvent(new Event('input',{bubbles:true}));
   return [...document.querySelectorAll('#srPanel .sr-item')].slice(0,3).map(e=>e.textContent.trim());}));
 console.log('别名·东坡', await p.evaluate(()=>{const i=document.getElementById('q');i.value='东坡';i.dispatchEvent(new Event('input',{bubbles:true}));
   return [...document.querySelectorAll('#srPanel .sr-item')].slice(0,3).map(e=>e.textContent.trim());}));
 console.log('别号·放翁', await p.evaluate(()=>{const i=document.getElementById('q');i.value='放翁';i.dispatchEvent(new Event('input',{bubbles:true}));
   return [...document.querySelectorAll('#srPanel .sr-item')].slice(0,2).map(e=>e.textContent.trim());}));
 // 点击正文命中项
 const click=await p.evaluate(()=>{
   const i=document.getElementById('q'); i.value='报任安书'; i.dispatchEvent(new Event('input',{bubbles:true}));
   const it=[...document.querySelectorAll('#srPanel .sr-item')][0]; it.dispatchEvent(new MouseEvent('mousedown',{bubbles:true}));
   return it.textContent.trim();
 });
 await p.waitForTimeout(1100);
 console.log('点击', click.slice(0,30), await p.evaluate(()=>{
   const h=(location.hash||'').replace('#',''); const [pg,id]=h.split('::');
   const el=id?document.getElementById(id):null;
   return {pg,id,top:el?Math.round(el.getBoundingClientRect().top):null,active:document.querySelector('section.page.active')?.id};
 }));
 // 面板截图（桌面）
 await p.evaluate(()=>{const i=document.getElementById('q');i.value='登高';i.dispatchEvent(new Event('input',{bubbles:true}));});
 await p.waitForTimeout(250);
 await p.screenshot({path:'audit/s36-search-1440.png'});
 console.log('JS错误',errs.length,errs.slice(0,3));
 await b.close();
})();
