const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1280,height:900}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  const url='file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
  await p.goto(url,{waitUntil:'load'}); await p.waitForTimeout(400);
  const n=await p.evaluate(()=>document.querySelectorAll('.page').length);
  const tocN=await p.evaluate(()=>document.querySelectorAll('.toc-group a').length);
  console.log('分页',n,'侧栏目录',tocN);
  // 索引页逐条随机抽验 8 条
  const tests=['石壕吏','春夜喜雨','静女','氓','窦娥冤','致云雀','长相思','卜算子·咏梅','赤壁赋','朝天子·咏喇叭'];
  for(const t of tests){
    await p.goto(url+'#jiaocai',{waitUntil:'load'}); await p.waitForTimeout(220);
    const go=await p.evaluate((name)=>{const rows=[...document.querySelectorAll('#jiaocai tr')];for(const r of rows){const a=r.querySelector('a[data-goto]');if(a&&a.textContent.includes(name)){const g=a.getAttribute('data-goto');a.click();return g;}}return null;},t);
    await p.waitForTimeout(650);
    const st=await p.evaluate((g)=>{if(!g)return null;const id=g.split('::')[1];const el=document.getElementById(id);return{page:document.querySelector('.page.active').id,top:el?Math.round(el.getBoundingClientRect().top):null,ok:!!el};},go);
    console.log(' ',t,'→',go,JSON.stringify(st));
  }
  // 毛诗阶段目录
  await p.goto(url+'#mao',{waitUntil:'load'}); await p.waitForTimeout(300);
  const maoSt=await p.evaluate(()=>({toc:document.querySelectorAll('#mao .sub-toc a').length, stages:document.querySelectorAll('#mao .stage-h').length}));
  console.log('毛诗页:',JSON.stringify(maoSt));
  await p.evaluate(()=>{const a=[...document.querySelectorAll('#mao .sub-toc a')].find(x=>x.textContent.includes('卜算子'));if(a)a.click();});
  await p.waitForTimeout(500);
  console.log('毛诗跳卜算子 top:',await p.evaluate(()=>Math.round(document.getElementById('p-mao-busuanzi-mei').getBoundingClientRect().top)));
  console.log('JS错误:',errs.length?errs:'无');
  await b.close();
})();
