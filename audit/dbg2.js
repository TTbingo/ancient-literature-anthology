const { chromium } = require('playwright');
const path='file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
(async()=>{
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1440,height:900}});
 await p.goto(path); await p.waitForTimeout(400);
 await p.evaluate(()=>{location.hash='#tangwan';}); await p.waitForTimeout(400);
 console.log(await p.evaluate(()=>{
   const r=document.querySelector('#tangwan .prail');
   return {scrollH:r.scrollHeight, clientH:r.clientHeight, canScroll:r.scrollHeight>r.clientHeight};
 }));
 // 滚到底部，看高亮与自动跟随
 await p.evaluate(()=>window.scrollTo(0,document.querySelector('#tangwan').scrollHeight));
 await p.waitForTimeout(500);
 console.log(await p.evaluate(()=>{
   const r=document.querySelector('#tangwan .prail'), on=r.querySelector('a.on');
   return {railScrollTop:Math.round(r.scrollTop), on:on?on.textContent:'(无)', onVisible: on? (on.getBoundingClientRect().top>r.getBoundingClientRect().top&&on.getBoundingClientRect().bottom<r.getBoundingClientRect().bottom):null};
 }));
 // 点击卡片层级
 await p.evaluate(()=>{const a=document.querySelector('#tangwan .prail .l2 a'); a.click();});
 await p.waitForTimeout(800);
 console.log(await p.evaluate(()=>{
   const t=document.querySelector('#tangwan .l2 a').getAttribute('data-jump');
   const el=document.getElementById(t);
   return {id:t, top:Math.round(el.getBoundingClientRect().top), authorEl:el.className};
 }));
 await p.screenshot({path:'audit/s6-tangwan-mid.png'});
 await b.close();
})();
