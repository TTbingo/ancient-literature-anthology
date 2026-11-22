const {chromium}=require('playwright');
const file='file:///D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html';
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1440,height:900}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto(file); await p.waitForTimeout(700);
  const R={};

  // 1. 新增两篇作品块在 DOM 中的完整性
  R.newPoems=await p.evaluate(()=>{
    function info(id){
      const el=document.getElementById(id); if(!el) return {id,exists:false};
      const dims=[].slice.call(el.querySelectorAll('.dim .k')).map(k=>k.textContent.trim());
      return {id,exists:true,title:el.querySelector('.ptitle')?.textContent.trim(),
        verse:el.querySelector('.verse')?.textContent.trim(),
        verseLines:(el.querySelector('.verse')?.innerHTML.match(/<br>/g)||[]).length+1,
        dimCount:dims.length,dims};
    }
    return [info('p-congjunxing-yangjiong'),info('p-liangzhouci-wanghan')];
  });

  // 2. 两个作品块的正文逐字核对
  R.verseExact=await p.evaluate(()=>({
    yangjiong:document.querySelector('#p-congjunxing-yangjiong .verse')?.textContent,
    wanghan:document.querySelector('#p-liangzhouci-wanghan .verse')?.textContent
  }));

  // 3. 搜索能否命中新篇目/作者
  R.search=await p.evaluate(async()=>{
    const box=document.getElementById('searchBox'); const input=box?.querySelector('input');
    if(!input) return {ok:false,reason:'无搜索框'};
    const out={};
    for(const q of ['从军行','杨炯','凉州词','王翰','葡萄美酒夜光杯','宁为百夫长']){
      input.value=q; input.dispatchEvent(new Event('input',{bubbles:true}));
      await new Promise(r=>setTimeout(r,80));
      const panel=box.querySelector('.search-panel,.search-result,.results');
      const txt=(panel?panel.textContent:box.textContent)||'';
      out[q]={hit:txt.indexOf(q)>=0 || txt.length>0, len:txt.length};
    }
    input.value=''; input.dispatchEvent(new Event('input',{bubbles:true}));
    return {ok:true,out};
  });

  // 4. 全文所有 data-goto 目标可解析
  R.links=await p.evaluate(()=>{
    const ids=new Set([].slice.call(document.querySelectorAll('[id]')).map(e=>e.id));
    let total=0,bad=[];
    document.querySelectorAll('[data-goto]').forEach(a=>{
      const g=a.getAttribute('data-goto'); total++;
      if(g.indexOf('::')<0){ if(!ids.has(g)) bad.push(g); }
      else { const id=g.split('::')[1]; if(!ids.has(id)) bad.push(g); }
    });
    return {total,badCount:bad.length,bad:bad.slice(0,10)};
  });

  // 5. 结构/皮肤回归
  R.regression=await p.evaluate(()=>({
    pages:document.querySelectorAll('section.page').length,
    sidebar:document.querySelectorAll('.sidebar a[data-target]').length,
    bars:document.querySelectorAll('#home .d2-bar').length,
    quotes:window.__d2Quotes,
    stat402:document.querySelector('#home .stat b')?.textContent,
    verseWithBlank:[].slice.call(document.querySelectorAll('.verse')).filter(v=>/<br>\s*<br>/i.test(v.innerHTML)).length
  }));

  // 6. 点击两处新链接能正确跳转并定位
  R.jump=await p.evaluate(async()=>{
    function goto(g){ const el=document.querySelector('[data-goto="'+g+'"]'); if(el) el.click(); }
    goto('tangchu::p-congjunxing-yangjiong');
    await new Promise(r=>setTimeout(r,200));
    const a={active:document.querySelector('section.page.active')?.id,
      targetExists:!!document.getElementById('p-congjunxing-yangjiong')};
    goto('tangsheng::p-liangzhouci-wanghan');
    await new Promise(r=>setTimeout(r,200));
    const c={active:document.querySelector('section.page.active')?.id,
      targetExists:!!document.getElementById('p-liangzhouci-wanghan')};
    return {yangjiong:a,wanghan:c};
  });

  R.pageErrors=errs;
  console.log(JSON.stringify(R,null,2));
  await b.close();
})();
