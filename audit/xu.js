const { chromium } = require('playwright');
const path='file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1440,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text());});
 await p.goto(path); await p.waitForTimeout(600);
 // 左导航是否含选修
 console.log('左导航', await p.evaluate(()=>[...document.querySelectorAll('.toc a')].filter(a=>/选修/.test(a.textContent)).map(a=>a.textContent.trim())));
 // 选修页目录栏
 console.log('选修rail', await p.evaluate(()=>{
   const r=document.querySelector('#xuanxiu .prail');
   if(!r) return '无';
   const as=[...r.querySelectorAll('a')];
   return {n:as.length, L1:as.filter(a=>a.className.includes('l1')).length,
     author:as.filter(a=>a.getAttribute('data-kind')==='author').length,
     poem:as.filter(a=>a.getAttribute('data-kind')==='poem').length,
     first:as.slice(0,6).map(a=>a.textContent)};
 }));
 // 直达
 async function go(hash){
   await p.evaluate(h=>{location.hash=h;},hash); await p.waitForTimeout(800);
   return await p.evaluate(()=>{
     const pg=document.querySelector('.page.active');
     const el=(location.hash.split('::')[1]||'').replace(/%20/g,'');
     const t=document.getElementById(el);
     return {page:pg.id, top:t?Math.round(t.getBoundingClientRect().top):null,
       on:(document.querySelector('.page.active .prail a.on')||{}).textContent};
   });
 }
 for(const h of ['#xuanxiu::p-xu-laozi','#xuanxiu::p-xu-liuyi','#xuanxiu::p-xu-shijingbiji','#xuanxiu::a-xu-huangzongxi','#mao::p-mao-youshui','#tangchu::p-tengwangge-wangbo']){
   console.log(h, JSON.stringify(await go(h)));
 }
 // 搜索
 for(const q of ['嵇康','柳毅传','高祖还乡','水调歌头','麻叶洞天','诗品序']){
   await p.fill('#q',''); await p.click('#q'); await p.type('#q',q); await p.waitForTimeout(250);
   const r=await p.evaluate(()=>[...document.querySelectorAll('.sr-item')].slice(0,2).map(e=>e.textContent.replace(/\s+/g,' ').trim()));
   console.log('搜',q,'→',JSON.stringify(r));
 }
 await p.keyboard.press('Escape');
 await p.evaluate(()=>{location.hash='#xuanxiu';}); await p.waitForTimeout(600);
 await p.screenshot({path:'audit/s20-xuanxiu.png'});
 await p.evaluate(()=>window.scrollTo(0,1500)); await p.waitForTimeout(500);
 await p.screenshot({path:'audit/s21-xuanxiu2.png'});
 console.log('错误', errs.length?errs:'无');
 await b.close();
})();
