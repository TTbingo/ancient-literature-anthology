const {chromium}=require('playwright');
const file='file:///D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html';
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1440,height:900}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto(file); await p.waitForTimeout(700);
  const R={};

  // 1. 结构与皮肤
  R.structure=await p.evaluate(()=>({
    pages:document.querySelectorAll('section.page').length,
    sidebar:document.querySelectorAll('.sidebar a[data-target]').length,
    prail:document.querySelectorAll('.prail a').length,
    topbar:getComputedStyle(document.querySelector('.topbar')).position,
    bodyBg:getComputedStyle(document.body).backgroundColor,
    bars:document.querySelectorAll('#home .d2-bar').length,
    uniqueBarColors:new Set([].slice.call(document.querySelectorAll('#home .d2-bar')).map(x=>x.dataset.color)).size,
    homeCoord:!!document.querySelector('#home .d2-coord'),
    quyuanCoord:!!document.querySelector('#quyuan .d2-coord'),
    quotes:window.__d2Quotes,
    idmarks:[].slice.call(document.querySelectorAll('#quyuan .idmark')).map(x=>x.textContent.trim())
  }));

  // 2. 名句加粗样例
  R.quote=await p.evaluate(()=>{
    const all=[].slice.call(document.querySelectorAll('.d2-quote'));
    const hit=all.find(x=>x.textContent.indexOf('袅袅兮秋风')>=0);
    return {count:all.length,hit:!!hit,bold:hit?getComputedStyle(hit).fontWeight:null};
  });

  // 3. 空行：全文 verse 无 <br><br>
  R.blankLines=await p.evaluate(()=>{
    let bad=0,total=0;
    document.querySelectorAll('.verse').forEach(v=>{total++;if(/<br>\s*<br>/i.test(v.innerHTML))bad++;});
    return {verseTotal:total,withBlankLine:bad,
      shizuoBr:(document.querySelector('#p-shizuo-lunyu .verse').innerHTML.match(/<br>/g)||[]).length};
  });

  // 4. 所有 data-goto 目标可解析（不真的逐个跳，检查目标存在）
  R.gotoTargets=await p.evaluate(()=>{
    const bad=[]; let n=0;
    const resolve=(key)=>{
      if(key.indexOf('::')>0){const [pg,anchor]=key.split('::');
        const page=document.getElementById(pg); if(!page) return false;
        if(!anchor) return true;
        return !!(document.getElementById(anchor)||page.querySelector('#'+anchor));}
      return !!document.getElementById(key)||!!document.querySelector('[data-target="'+key+'"]');
    };
    document.querySelectorAll('[data-goto]').forEach(a=>{
      n++;const k=a.getAttribute('data-goto');if(!resolve(k))bad.push(k);
    });
    return {total:n,bad:bad.slice(0,20),badCount:bad.length};
  });

  // 5. 搜索：输入"离骚"应命中
  R.search=await p.evaluate(()=>{
    const q=document.getElementById('q'); if(!q) return {ok:false,reason:'无搜索框'};
    q.value='离骚'; q.dispatchEvent(new Event('input',{bubbles:true}));
    return {ok:true,hasPanel:!!document.getElementById('srPanel')};
  });
  await p.waitForTimeout(400);
  R.searchResults=await p.evaluate(()=>({
    panelItems:document.querySelectorAll('#srPanel a, #srPanel .sr-item, #srPanel [data-goto]').length,
    panelText:(document.getElementById('srPanel').textContent||'').slice(0,120)
  }));

  // 6. 深链：带 hash 打开定位到屈原页
  const p2=await b.newPage({viewport:{width:1440,height:900}});
  await p2.goto(file+'#quyuan'); await p2.waitForTimeout(700);
  R.deeplink=await p2.evaluate(()=>{
    const act=document.querySelector('.page.active');
    return {activePage:act?act.id:null,crumb:(document.getElementById('crumb').textContent||'').trim()};
  });
  await p2.close();

  // 7. 色卡交互：首页点第8色应更新解读与坐标
  R.colorCard=await p.evaluate(()=>{
    const bars=document.querySelectorAll('#home .d2-bar');
    if(bars.length<8) return {ok:false};
    bars[7].click();
    const name=(document.querySelector('#home .d2-td-name')||{}).textContent||'';
    const coord=(document.querySelector('#home .d2-coord b')||{}).textContent||'';
    return {clicked8th:true,detailName:name,coord:coord};
  });

  // 8. 导航跳转：点第30个侧栏链接
  R.navClick=await p.evaluate(()=>{
    const links=document.querySelectorAll('.sidebar a[data-target]');
    const l=links[29]; if(!l) return {ok:false};
    const t=l.getAttribute('data-target'); l.click();
    return {target:t,clicked:true};
  });
  await p.waitForTimeout(400);
  R.navResult=await p.evaluate(()=>{const a=document.querySelector('.page.active');return {activePage:a?a.id:null};});

  // 9. 顶栏吸顶
  await p.evaluate(()=>window.scrollTo(0,2000)); await p.waitForTimeout(300);
  R.sticky=await p.evaluate(()=>{const r=document.querySelector('.topbar').getBoundingClientRect();return {top:Math.round(r.top),visible:r.top>=-1&&r.top<3};});

  R.pageErrors=errs;
  console.log(JSON.stringify(R,null,2));
  await b.close();
})();
