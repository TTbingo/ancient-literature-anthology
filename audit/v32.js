const { chromium } = require('playwright');
const path=require('path');
(async()=>{
 const file='file:///'+path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g,'/');
 const b=await chromium.launch();
 const pages=['baijuyi','caocao','dufu','dumu','fanzhongyan','hanprose','lihe','liqingzhao','luyou','mao','mingqingshi','mingqingwen','ouyangxiu','quyuan','shangyin','shijing','songci','songshi','songwen','sushi','tangchu','tangguwen','tangsheng','tangwan','taoyuanming','wanganshi','wangwei','weijinprose','xiandai','xiaowen','xinqiji','yuanqu','zhuzi','xuanxiu','libai'];
 for (const w of [1440,390]) {
  const p=await b.newPage({viewport:{width:w,height:900}});
  await p.goto(file,{waitUntil:'load'});
  const out=[];
  for (const id of pages) {
    await p.evaluate(i=>{ location.hash='#'+i; }, id);
    await p.waitForTimeout(120);
    const r=await p.evaluate(()=>{
      let ov=0, tw=0, cells=0;
      document.querySelectorAll('section.page.active table.mlist').forEach(t=>{
        tw=Math.max(tw, Math.round(t.getBoundingClientRect().width));
        t.querySelectorAll('td,th').forEach(c=>{ cells++; if(c.scrollWidth-c.clientWidth>1) ov++; });
      });
      return {ov, tw, bodyOv: document.body.scrollWidth - innerWidth, cells};
    });
    if (r.ov || r.bodyOv) out.push([id, r]);
  }
  console.log(w, '问题页', JSON.stringify(out));
  await p.close();
 }
 await b.close();
})();
