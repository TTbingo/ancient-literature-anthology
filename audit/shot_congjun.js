const {chromium}=require('playwright');
const file='file:///D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html';
const dir='D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/design-demos/fix-shots/';
const fs=require('fs'); fs.mkdirSync(dir,{recursive:true});
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
  await p.goto(file); await p.waitForTimeout(600);

  // 杨炯从军行：激活 tangchu 页并滚动到作品块
  await p.evaluate(()=>{const a=document.querySelector('[data-goto="tangchu::p-congjunxing-yangjiong"]');if(a)a.click();});
  await p.waitForTimeout(300);
  await p.evaluate(()=>{const e=document.getElementById('p-congjunxing-yangjiong');if(e)e.scrollIntoView({block:'start'});});
  await p.waitForTimeout(250);
  await p.screenshot({path:dir+'杨炯-从军行.png'});

  // 王翰凉州词
  await p.evaluate(()=>{const a=document.querySelector('[data-goto="tangsheng::p-liangzhouci-wanghan"]');if(a)a.click();});
  await p.waitForTimeout(300);
  await p.evaluate(()=>{const e=document.getElementById('p-liangzhouci-wanghan');if(e)e.scrollIntoView({block:'start'});});
  await p.waitForTimeout(250);
  await p.screenshot({path:dir+'王翰-凉州词.png'});

  // 手机端杨炯
  await p.setViewportSize({width:390,height:844});
  await p.evaluate(()=>{const a=document.querySelector('[data-goto="tangchu::p-congjunxing-yangjiong"]');if(a)a.click();});
  await p.waitForTimeout(300);
  await p.evaluate(()=>{const e=document.getElementById('p-congjunxing-yangjiong');if(e)e.scrollIntoView({block:'start'});});
  await p.waitForTimeout(250);
  await p.screenshot({path:dir+'手机-杨炯-从军行.png'});

  console.log('截图完成');
  await b.close();
})();
