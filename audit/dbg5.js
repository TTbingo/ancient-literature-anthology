const { chromium } = require('playwright');
const path='file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1440,height:900}});
 await p.goto(path); await p.waitForTimeout(400);
 await p.click('#q'); await p.type('#q','月'); await p.waitForTimeout(300);
 console.log(await p.evaluate(()=>{
   const it=document.querySelector('.sr-item'); const out={};
   out.before=it.getBoundingClientRect().height;
   it.style.alignItems='center'; out.center=it.getBoundingClientRect().height;
   it.style.alignItems=''; it.style.display='block'; out.block=it.getBoundingClientRect().height;
   it.style.display=''; 
   // 逐个子元素隐藏看影响
   const i=it.querySelector('i'); i.style.display='none'; out.noTag=it.getBoundingClientRect().height; i.style.display='';
   const em=it.querySelector('em'); em.style.display='none'; out.noEm=it.getBoundingClientRect().height; em.style.display='';
   const bb=it.querySelector('b'); bb.style.display='none'; out.noB=it.getBoundingClientRect().height; bb.style.display='';
   out.iStyle={h:i.getBoundingClientRect().height, lh:getComputedStyle(i).lineHeight, pad:getComputedStyle(i).padding};
   out.panelStyle={pad:getComputedStyle(document.getElementById('srPanel')).padding};
   return out;
 }));
 await b.close();
})();
