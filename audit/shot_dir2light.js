const {chromium}=require('playwright');
const fs=require('fs');
const file='file:///D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/design-demos/preview-dir2-light.html';
const shotDir='D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/design-demos/dir2-light-shots/';
if(!fs.existsSync(shotDir)) fs.mkdirSync(shotDir,{recursive:true});
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
  await p.goto(file); await p.waitForTimeout(700);
  await p.screenshot({path:shotDir+'桌面-首页.png'});
  await p.evaluate(()=>{var e=document.getElementById('home');var b=e.querySelector('.d2-band-shell');if(b)b.scrollIntoView({block:'center'});});
  await p.waitForTimeout(300);
  await p.screenshot({path:shotDir+'桌面-首页-色带.png'});
  await p.click('[data-goto="quyuan"]'); await p.waitForTimeout(500);
  await p.screenshot({path:shotDir+'桌面-屈原页.png'});
  await p.evaluate(()=>{var e=document.getElementById('p-lisao-qu');if(e)e.scrollIntoView({block:'start'});});
  await p.waitForTimeout(350);
  await p.screenshot({path:shotDir+'桌面-屈原-离骚.png'});
  await p.evaluate(()=>{
    var q=document.querySelector('#p-xiangfuren-qu .d2-quote');
    if(q) q.scrollIntoView({block:'center'});
  });
  await p.waitForTimeout(300);
  await p.screenshot({path:shotDir+'桌面-名句加粗.png'});
  const check=await p.evaluate(()=>{
    var cs=getComputedStyle(document.body);
    var dim=document.querySelector('#p-lisao-qu .poem .dim');
    return {
      bodyBg:cs.backgroundColor,
      sidebar:!!document.querySelector('.sidebar'),
      prail:!!document.querySelector('.prail'),
      prailItems:document.querySelectorAll('.prail a').length,
      topbarPos:getComputedStyle(document.querySelector('.topbar')).position,
      bars:document.querySelectorAll('.d2-band-shell .d2-bar').length,
      idmarks:[].slice.call(document.querySelectorAll('#quyuan .idmark')).map(x=>x.textContent.trim()),
      dimWrapped:!!document.querySelector('#p-lisao-qu .d2-dims'),
      dimKDisplay:dim?getComputedStyle(dim.querySelector('.k')).display:'',
      dimKFont:dim?getComputedStyle(dim.querySelector('.k')).fontSize:'',
      dimVFont:dim?getComputedStyle(dim.querySelector('.v')).fontSize:'',
      chip:document.querySelector('#p-lisao-qu').getAttribute('data-chip')
    };
  });
  console.log('桌面实测:',JSON.stringify(check,null,2));
  await p.evaluate(()=>window.scrollTo(0,2200)); await p.waitForTimeout(300);
  const sticky=await p.evaluate(()=>{var r=document.querySelector('.topbar').getBoundingClientRect();return {top:r.top,visible:r.top>=-1&&r.top<3};});
  console.log('顶栏吸顶:',JSON.stringify(sticky));
  await p.close();

  const m=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});
  await m.goto(file); await m.waitForTimeout(700);
  await m.screenshot({path:shotDir+'手机-首页.png'});
  await m.evaluate(()=>{var e=document.querySelector('[data-goto="quyuan"]');if(e)e.dispatchEvent(new MouseEvent('click',{bubbles:true}));});
  await m.waitForTimeout(500);
  await m.screenshot({path:shotDir+'手机-屈原页.png'});
  await m.evaluate(()=>{var e=document.getElementById('p-lisao-qu');if(e)e.scrollIntoView({block:'start'});});
  await m.waitForTimeout(350);
  await m.screenshot({path:shotDir+'手机-屈原-离骚.png'});
  const mob=await m.evaluate(()=>({
    activePage:(document.querySelector('.page.active')||{}).id,
    bodyBg:getComputedStyle(document.body).backgroundColor,
    bars:document.querySelectorAll('.d2-band-shell .d2-bar').length,
    sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth
  }));
  console.log('手机实测:',JSON.stringify(mob,null,2),'横向溢出:',mob.sw>mob.cw);
  await m.close(); await b.close();
  console.log('截图完成');
})();
