const { chromium } = require('playwright');
const path='file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
(async()=>{
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:430,height:880}});
 await p.goto(path); await p.waitForTimeout(400);
 await p.evaluate(()=>{location.hash='#dufu';}); await p.waitForTimeout(400);
 console.log(await p.evaluate(()=>{
   const rail=document.querySelector('#dufu .prail'), pw=rail.parentNode, cs=getComputedStyle(rail), cw=getComputedStyle(pw);
   return {railW:rail.getBoundingClientRect().width, pwrapW:pw.getBoundingClientRect().width,
     disp:cs.display, flex:cs.flex, width:cs.width, maxW:cs.maxWidth,
     pwDisp:cw.display, pwDir:cw.flexDirection, pwAlign:cw.alignItems, mainW:document.querySelector('.main').getBoundingClientRect().width,
     scrollH:rail.scrollHeight, clientH:rail.clientHeight};
 }));
 await b.close();
})();
