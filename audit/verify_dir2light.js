const {chromium}=require('playwright');
const src='file:///D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html';
const dst='file:///D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/design-demos/preview-dir2-light.html';
function clean(sel){return document.querySelector(sel).cloneNode(true);}
(async()=>{
  const b=await chromium.launch();
  const a=await b.newPage(); await a.goto(src);
  const c=await b.newPage(); await c.goto(dst); await c.waitForTimeout(500);
  for(const id of ['home','quyuan']){
    const ta=await a.evaluate(id=>document.getElementById(id).textContent,id);
    const tb=await c.evaluate(id=>{
      var n=document.getElementById(id).cloneNode(true);
      n.querySelectorAll('.d2-band-shell,.idmark,.d2-topic-detail').forEach(x=>x.remove());
      return n.textContent;
    },id);
    const na=ta.replace(/\s+/g,''), nb=tb.replace(/\s+/g,'');
    var i=0; while(i<na.length&&na[i]===nb[i]) i++;
    console.log(id,'原文字数',na.length,'预览字数',nb.length,'逐字一致',na===nb,
      '首个差异位置',i, i<Math.min(na.length,nb.length)?JSON.stringify({a:na.slice(i,i+40),b:nb.slice(i,i+40)}):'');
  }
  const extras=await c.evaluate(()=>{
    var bars=[].slice.call(document.querySelectorAll('#home .d2-bar'));
    var colors=bars.map(b=>b.dataset.color);
    var q=document.querySelector('#p-xiangfuren-qu .dim .d2-quote');
    return {
      bars:bars.length,
      uniqueColors:new Set(colors).size,
      detail:!!document.querySelector('#home .d2-topic-detail'),
      detailName:(document.querySelector('#home .d2-td-name')||{}).textContent,
      detailHasText:((document.querySelector('#home .d2-td-line')||{}).textContent||'').length>20,
      quotes:window.__d2Quotes,
      sampleQuote:q?q.textContent:'',
      quoteBold:q?getComputedStyle(q).fontWeight:''
    };
  });
  console.log('新增结构:',JSON.stringify(extras));
  const pages=await c.evaluate(()=>({pages:document.querySelectorAll('section.page').length,
    sidebarLinks:document.querySelectorAll('.sidebar a[data-target]').length}));
  console.log('预览结构:',JSON.stringify(pages));
  await b.close();
})();
