const { chromium } = require('playwright');
const path='file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1440,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text());});
 await p.goto(path); await p.waitForTimeout(500);

 // 目录栏里王勃两项
 console.log('目录', await p.evaluate(()=>{
   document.querySelector('#tangchu').classList.add('active');
   const as=[...document.querySelectorAll('#tangchu .prail a[data-jump]')];
   const wb=as.filter(a=>/王勃|送杜|滕王/.test(a.textContent));
   return {total:as.length, items:wb.map(a=>a.textContent+' ['+a.getAttribute('data-kind')+'/'+a.className+']')};
 }));

 // 直达
 await p.evaluate(()=>{location.hash='#tangchu::p-tengwangge-wangbo';});
 await p.waitForTimeout(900);
 console.log('直达', await p.evaluate(()=>{
   const el=document.getElementById('p-tengwangge-wangbo');
   const on=document.querySelector('#tangchu .prail a.on');
   return {page:document.querySelector('.page.active').id, top:Math.round(el.getBoundingClientRect().top),
     railOn:on?on.textContent:'(无)', verseLen:el.querySelector('.verse').textContent.length,
     dims:el.querySelectorAll('.dim').length,
     verseH:Math.round(el.querySelector('.verse').getBoundingClientRect().height)};
 }));

 // 搜索
 await p.fill('#q',''); await p.click('#q'); await p.type('#q','滕王阁'); await p.waitForTimeout(300);
 console.log('搜索', await p.evaluate(()=>[...document.querySelectorAll('.sr-item')].slice(0,4).map(e=>e.textContent.replace(/\s+/g,' ').trim())));
 await p.keyboard.press('Enter'); await p.waitForTimeout(900);
 console.log('搜索落点', await p.evaluate(()=>({page:document.querySelector('.page.active').id, hash:location.hash,
   top:Math.round(document.getElementById('p-tengwangge-wangbo').getBoundingClientRect().top)})));

 // 截图
 await p.evaluate(()=>{location.hash='#tangchu::p-tengwangge-wangbo';}); await p.waitForTimeout(900);
 await p.screenshot({path:'audit/s15-tengwang.png'});
 await p.evaluate(()=>window.scrollBy(0,700)); await p.waitForTimeout(400);
 await p.screenshot({path:'audit/s16-tengwang2.png'});
 console.log('错误', errs.length?errs:'无');
 await b.close();
})();
