# -*- coding: utf-8 -*-
"""从正式成品复制预览：dir-2 排版骨架 + 原版浅纸底 + 12 题材唯一色 + 首页色卡解读 + 名句加粗。
只插入 CSS 与 JS，不改动 41 页任何原文文字；名句加粗以 <b> 包裹原文文字节点。"""
import io, os

BASE = r"D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析"
SRC  = os.path.join(BASE, "统编教材古代作家文学集成.html")
OUT  = os.path.join(BASE, "design-demos", "preview-dir2-light.html")

s = io.open(SRC, encoding="utf-8").read()

SKIN_CSS = r"""
  /* ===== dir-2 骨架 + 原版浅纸底：只作用于首页与屈原页 ===== */
  /* 底色不覆盖：body 仍是原版 --bg:#f7f4ec；侧栏/章节栏/顶栏/语义 tag 配色零改动 */

  /* --- 色带导航脊：12 类各一色，色名不重复 --- */
  .d2-band-shell{margin:26px 0 34px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);}
  .d2-band-scroll{overflow:hidden;}
  .d2-band{display:flex;align-items:flex-end;height:104px;padding-top:20px;width:100%;min-width:0;}
  .d2-bar{position:relative;flex:1 1 0;min-width:0;height:72px;border:0;background:var(--c);
    cursor:pointer;padding:0 0 8px;display:flex;align-items:flex-end;justify-content:center;
    transition:flex-grow .25s cubic-bezier(.2,.7,.2,1),height .25s;
    font-family:-apple-system,"PingFang SC",sans-serif;}
  .d2-bar .vname{writing-mode:vertical-rl;text-orientation:upright;font-size:12px;font-weight:600;
    letter-spacing:.08em;color:var(--t);line-height:1.15;white-space:nowrap;}
  .d2-bar:hover{flex-grow:1.5;height:84px;}
  .d2-bar.on{box-shadow:0 0 0 2px var(--ink) inset;}
  .d2-bar.on .vname{font-weight:700;font-size:12.5px;}
  .d2-band-meta{display:flex;flex-direction:column;gap:7px;border-top:1px solid var(--line);
    padding:8px 0 10px;font-family:-apple-system,"PingFang SC",sans-serif;}
  .d2-ruler{display:flex;width:100%;justify-content:space-between;gap:2px;min-width:0;}
  .d2-ruler span{flex:1 1 0;text-align:center;font-size:11px;color:#8a8378;white-space:nowrap;}
  .d2-coord{font-size:11px;color:var(--ink-soft);text-align:right;align-self:flex-end;}
  .d2-coord b{color:var(--accent);font-weight:700;}

  /* --- 首页色卡解读：题材名／色名／原文释义／代表篇目 --- */
  #home .d2-topic-detail{display:flex;align-items:center;gap:24px;padding:22px 0 6px;
    border-bottom:1px solid var(--line);font-family:-apple-system,"PingFang SC",sans-serif;}
  #home .d2-swatch{width:64px;height:64px;flex:0 0 auto;background:var(--c);}
  #home .d2-td-body{flex:1;min-width:0;}
  #home .d2-td-name{font-family:"Songti SC","STSong",serif;font-size:26px;font-weight:700;
    letter-spacing:.04em;color:var(--ink);}
  #home .d2-td-line{font-size:13px;color:var(--ink-soft);line-height:1.9;margin-top:6px;}
  #home .d2-td-line b{color:var(--accent);font-weight:700;}
  #home .d2-td-work{flex:0 0 300px;max-width:300px;border-left:1px solid var(--line);
    padding-left:22px;font-size:13.5px;line-height:1.9;}
  #home .d2-td-work .wk{font-size:11px;color:#8a8378;letter-spacing:.14em;margin-bottom:4px;}
  #home .d2-td-work a{color:var(--accent2);border-bottom:1px dotted #c9c0ad;cursor:pointer;}
  #home .d2-td-work a:hover{color:var(--accent);text-decoration:none;}

  /* --- 名句类解读：引号中的名句加粗放大 --- */
  .d2-quote{font-weight:700;color:var(--ink);font-size:1.12em;line-height:inherit;}

  /* --- 首页：h1 分层、导语、四栏统计 --- */
  #home .home-hero{text-align:left;padding:52px 0 30px;border-bottom:1px solid var(--line);}
  #home .home-hero .eyebrow{font-size:12.5px;letter-spacing:.22em;color:var(--accent);margin-bottom:20px;}
  #home .home-hero h1{font-size:clamp(42px,5.6vw,72px);line-height:1.1;letter-spacing:.02em;
    margin:0;max-width:10em;color:#1c1a17;font-weight:700;}
  #home .home-hero .sub{font-size:17px;line-height:2;color:var(--ink-soft);max-width:760px;margin-top:20px;}
  #home .lead{background:transparent;border:0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);
    border-radius:0;box-shadow:none;padding:22px 0;margin:28px 0 34px;font-size:16px;line-height:2;max-width:860px;}
  #home .stat-row{display:grid;grid-template-columns:repeat(4,1fr);margin:44px 0 8px;
    border-top:1px solid var(--line);}
  #home .stat{background:transparent;border:0;border-right:1px solid var(--line);border-radius:0;
    box-shadow:none;text-align:left;padding:20px 18px 4px 0;}
  #home .stat:last-child{border-right:0;}
  #home .stat:not(:first-child){padding-left:22px;}
  #home .stat b{display:block;font-family:"Songti SC","STSong",serif;font-size:clamp(32px,4vw,50px);
    line-height:1;font-weight:700;color:var(--ink);}
  #home .stat span{display:block;margin-top:10px;font-family:-apple-system,"PingFang SC",sans-serif;
    font-size:12px;letter-spacing:.08em;color:#8a8378;}

  /* --- 章节题：dir-2 式细线 + 小额 + 大标题 --- */
  #home h2,#quyuan h2{display:flex;align-items:baseline;gap:16px;border-top:1px solid var(--line);
    border-bottom:0;padding:14px 0 0;margin:48px 0 24px;font-size:29px;font-weight:700;letter-spacing:.04em;}
  #home h2 .num,#quyuan h2 .num{display:inline;font-family:-apple-system,"PingFang SC",sans-serif;
    font-size:12px;letter-spacing:.2em;color:var(--accent);margin:0;}
  #home .info-grid,#quyuan .info-grid{gap:0;border-top:1px solid var(--line);}
  #home .info-box,#quyuan .info-box{background:transparent;border:0;border-right:1px solid var(--line);
    border-radius:0;padding:22px 24px 6px 0;}
  #home .info-box:last-child,#quyuan .info-box:last-child{border-right:0;padding-left:24px;}
  #home .info-box h4,#quyuan .info-box h4{font-family:-apple-system,"PingFang SC",sans-serif;
    font-size:12px;letter-spacing:.16em;color:var(--accent);margin:0 0 10px;}
  #home .info-box p,#quyuan .info-box p{font-size:15px;line-height:2;}

  /* --- 入口卡：三列顶色条，去卡片化 --- */
  #home .quick-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin:18px 0 26px;
    border-top:1px solid var(--line);}
  #home .quick{position:relative;background:transparent;border:0;border-right:1px solid var(--line);
    border-bottom:1px solid var(--line);border-radius:0;box-shadow:none;padding:22px 20px 24px 0;
    font-size:13.5px;line-height:1.8;color:var(--ink-soft);cursor:pointer;}
  #home .quick::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:var(--accent);}
  #home .quick:not(:nth-child(3n+1)){padding-left:20px;}
  #home .quick:nth-child(3n){border-right:0;}
  #home .quick b{display:block;font-family:"Songti SC","STSong",serif;font-size:20px;
    font-weight:700;color:var(--ink);margin-bottom:6px;letter-spacing:.02em;}
  #home .quick:hover{background:rgba(155,47,47,.04);}

  /* --- 屈原页：封面转 hero，保留原 tag 配色 --- */
  #quyuan .author-cover{text-align:left;padding:52px 0 30px;border-bottom:1px solid var(--line);}
  #quyuan .author-cover .eyebrow{font-size:12.5px;letter-spacing:.22em;color:var(--accent);margin-bottom:20px;}
  #quyuan .author-cover h1{font-size:clamp(42px,5.6vw,72px);line-height:1.1;letter-spacing:.02em;
    margin:0;font-weight:700;color:#1c1a17;}
  #quyuan .author-cover .sub{font-size:16px;line-height:2;color:var(--ink-soft);max-width:760px;margin-top:18px;}
  #quyuan .author-cover .badges{margin-top:20px;display:flex;gap:10px;flex-wrap:wrap;}
  #quyuan .lead{background:transparent;border:0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);
    border-radius:0;box-shadow:none;padding:22px 0;margin:28px 0 34px;font-size:16.5px;line-height:2;max-width:880px;}
  #quyuan .timeline li{font-size:15px;line-height:1.9;}

  /* --- 作品：dir-2 竖色条 + 大标题 + 浅色全文块；解析 dim 留原位用原版紧凑横排样式 --- */
  #quyuan .poem{position:relative;background:transparent;border:0;border-radius:0;box-shadow:none;
    padding:0 0 0 64px;margin:34px 0 68px;scroll-margin-top:82px;}
  #quyuan .poem::before{content:attr(data-chip);position:absolute;left:0;top:0;width:40px;height:86px;
    background:var(--chip-c);color:var(--chip-t);writing-mode:vertical-rl;text-orientation:upright;
    display:flex;align-items:center;justify-content:center;font-family:-apple-system,"PingFang SC",sans-serif;
    font-size:14px;font-weight:600;letter-spacing:.18em;}
  #quyuan .poem .idmark{font-family:-apple-system,"PingFang SC",sans-serif;font-size:12.5px;
    color:#6b6455;margin:0 0 8px;display:flex;align-items:center;gap:7px;letter-spacing:.02em;}
  #quyuan .poem .idmark i{width:3px;height:15px;border-radius:1px;display:inline-block;flex:0 0 3px;}
  #quyuan .poem .idmark b{font-weight:700;color:var(--ink);}
  #quyuan .poem .ptitle{font-size:42px;line-height:1.2;font-weight:700;letter-spacing:.04em;
    border-bottom:1px solid var(--line);padding-bottom:12px;margin:0 0 8px;color:#1c1a17;}
  #quyuan .poem .ptitle .tag{font-size:11.5px;vertical-align:middle;}
  #quyuan .poem .pmeta{font-family:-apple-system,"PingFang SC",sans-serif;font-size:12.5px;
    color:#8a8378;letter-spacing:.04em;margin:10px 0 18px;}
  #quyuan .poem .pmeta .tag{font-size:11.5px;}
  #quyuan .poem .verse{background:var(--tint);border:0;border-top:1px solid var(--line);
    border-bottom:1px solid var(--line);border-radius:0;padding:24px 28px 28px;margin:0 0 28px;
    font-size:18px;line-height:2.15;letter-spacing:.02em;color:#2c2823;}
  /* 解析区不套网格：dim 留在 poem 内原位，沿用原版 .dim 紧凑横排（标签 inline-block + 正文同行，14.5/15px） */
  #quyuan .poem .dim{margin:12px 0;}
  #quyuan .poem .dim .k{display:inline-block;min-width:96px;}
  #quyuan .poem .dim .v{display:inline;}

  /* --- 手机 --- */
  @media(max-width:820px){
    .d2-band{height:92px;padding-top:14px;}
    .d2-bar{height:62px;}
    .d2-bar .vname{font-size:11px;letter-spacing:0;}
    .d2-ruler{display:none;}
    .d2-coord{border-left:0;padding-left:0;}
    #home .d2-topic-detail{flex-wrap:wrap;gap:14px;padding:18px 0 8px;}
    #home .d2-swatch{width:52px;height:52px;}
    #home .d2-td-name{font-size:22px;}
    #home .d2-td-work{flex:1 1 100%;max-width:none;border-left:0;border-top:1px dashed var(--line);
      padding:10px 0 0;}
    .d2-quote{font-size:1.06em;}
    #home .home-hero,#quyuan .author-cover{padding:38px 0 24px;}
    #home .home-hero h1,#quyuan .author-cover h1{max-width:none;font-size:clamp(34px,9vw,52px);}
    #home .stat-row{grid-template-columns:repeat(2,1fr);}
    #home .stat{padding:16px 12px 16px 0;border-bottom:1px solid var(--line);}
    #home .stat:not(:first-child){padding-left:0;}
    #home .stat:nth-child(even){padding-left:14px;border-right:0;}
    #home .stat b{font-size:32px;}
    #home .quick-grid{grid-template-columns:1fr;}
    #home .quick,#home .quick:not(:nth-child(3n+1)){padding:16px 0 18px;border-right:0;padding-left:0;}
    #home .info-box,#home .info-box:last-child,#quyuan .info-box,#quyuan .info-box:last-child{
      border-right:0;border-bottom:1px solid var(--line);padding:18px 0 12px;}
    #quyuan .poem{padding-left:48px;margin:28px 0 52px;scroll-margin-top:150px;}
    #quyuan .poem::before{width:34px;height:76px;font-size:12.5px;}
    #quyuan .poem .ptitle{font-size:30px;}
    #quyuan .poem .verse{font-size:16px;line-height:2;padding:18px 16px 20px;}
    #quyuan .poem .dim .k{display:block;min-width:0;}
    #home h2,#quyuan h2{font-size:23px;gap:10px;}
  }
"""

assert s.count("</style>") == 1, "style 块数量异常"
s = s.replace("</style>", SKIN_CSS + "\n</style>", 1)

INJECT_JS = r"""
<script>
(function(){
  // 12 题材来自第三篇索引；一题材一传统色（取 dir-2 原色谱，无重复）
  var topics=[
    ['送别赠友','月白','#D7E8EC','#1C1B18'],
    ['边塞征战','绛',  '#9B2F2F','#F4F1E6'],
    ['羁旅思乡','鸦青','#424B4E','#F4F1E6'],
    ['山水田园','缥碧','#8FBFA8','#1C1B18'],
    ['咏史怀古','檀色','#A9614A','#F4F1E6'],
    ['咏物寄意','缃叶','#D9C97C','#1C1B18'],
    ['爱情闺情','桃夭','#E8A7A0','#1C1B18'],
    ['忧国伤时','墨',  '#1E2326','#F4F1E6'],
    ['抒怀言志','朱',  '#C8382A','#F4F1E6'],
    ['说理劝学','竹青','#7FA88C','#1C1B18'],
    ['叙事写人','秋香','#B9A44C','#1C1B18'],
    ['节令童趣','藤黄','#E3B23C','#1C1B18']
  ];
  function bandHTML(mode){
    var bars=topics.map(function(t,i){
      return '<button class="d2-bar'+(i===0?' on':'')+'" data-i="'+i+'" data-color="'+t[1]+'" style="--c:'+t[2]+';--t:'+t[3]+'" title="'+t[0]+' · '+t[1]+'">'+
             '<span class="vname">'+t[0]+'</span></button>';
    }).join('');
    var ruler=topics.map(function(t){return '<span>'+t[1]+'</span>';}).join('');
    // 坐标说明只在首页出现（首页就地切换解读）；正文页点色块直达题材页，不需要也不该显示
    var coord=(mode==='home')?'<div class="d2-coord">当前坐标 · <b>'+topics[0][0]+' / '+topics[0][1]+'</b></div>':'';
    return '<div class="d2-band-shell"><div class="d2-band-scroll"><nav class="d2-band">'+bars+'</nav></div>'+
      '<div class="d2-band-meta"><div class="d2-ruler">'+ruler+'</div>'+coord+'</div></div>';
  }
  function detailHTML(){
    return '<div class="d2-topic-detail"><div class="d2-swatch" style="--c:'+topics[0][2]+'"></div>'+
      '<div class="d2-td-body"><div class="d2-td-name"></div><div class="d2-td-line"></div></div>'+
      '<div class="d2-td-work"><div class="wk">代表篇目</div><div class="wks"></div></div></div>';
  }
  // 解读文字直接取题材分类索引原文，不新造说明
  var cats=[].slice.call(document.querySelectorAll('#ticai .cat'));
  function detailData(i){
    var t=topics[i], cat=cats[i], desc='', works=[];
    if(cat){
      var main=cat.querySelector('tr td');
      if(main) desc=(main.textContent||'').replace(/\s+/g,'').slice(0,58)+'…';
      works=[].slice.call(cat.querySelectorAll('.works a.tlink')).slice(0,3).map(function(a){
        return {text:a.textContent.trim(),goto:a.getAttribute('data-goto')};
      });
    }
    return {t:t,desc:desc,works:works};
  }
  function fillDetail(box,i){
    var d=detailData(i);
    box.querySelector('.d2-swatch').style.setProperty('--c',d.t[2]);
    box.querySelector('.d2-td-name').textContent=d.t[0];
    box.querySelector('.d2-td-line').innerHTML='题材色：<b>'+d.t[1]+'</b> · '+d.desc;
    var ws=box.querySelector('.wks');
    ws.innerHTML=d.works.map(function(w){
      return '<a href="#" data-goto="'+w.goto+'">《'+w.text+'》</a> ';
    }).join('')+'<a href="#" data-goto="ticai::tc-'+String(i+1).padStart(2,'0')+'">查看全部 →</a>';
  }
  function addBand(host,afterSel,mode){
    if(!host||host.querySelector('.d2-band-shell')) return;
    var wrap=document.createElement('div'); wrap.innerHTML=bandHTML(mode);
    var node=wrap.firstChild;
    var ref=host.querySelector(afterSel);
    if(ref) ref.insertAdjacentElement('afterend',node); else host.appendChild(node);
    var detail=null;
    if(mode==='home'){
      var dw=document.createElement('div'); dw.innerHTML=detailHTML(); detail=dw.firstChild;
      node.insertAdjacentElement('afterend',detail);
      fillDetail(detail,0);
      detail.addEventListener('click',function(e){
        var a=e.target.closest('a[data-goto]'); if(!a) return;
        e.preventDefault();
        var key=a.getAttribute('data-goto');
        var exist=[].slice.call(document.querySelectorAll('[data-goto]')).filter(function(x){
          return x!==a && !x.closest('.d2-topic-detail') && x.getAttribute('data-goto')===key;
        })[0];
        if(exist) exist.click();
      });
    }
    node.addEventListener('click',function(e){
      var b=e.target.closest('.d2-bar'); if(!b) return;
      var i=+b.dataset.i, t=topics[i];
      node.querySelectorAll('.d2-bar').forEach(function(x){x.classList.remove('on');});
      b.classList.add('on');
      var coordB=node.querySelector('.d2-coord b');
      if(coordB) coordB.textContent=t[0]+' / '+t[1];
      if(detail){ fillDetail(detail,i); return; }  // 首页：就地解读，不跳走
      var link=[].slice.call(document.querySelectorAll('[data-goto]')).filter(function(x){
        return x.getAttribute('data-goto')==='ticai::tc-'+String(i+1).padStart(2,'0');
      })[0];
      if(link) link.click();                       // 正文页：保持简洁，点色块直达题材页
    });
  }
  var home=document.getElementById('home');
  if(home) addBand(home,'.home-hero','home');
  var qy=document.getElementById('quyuan');
  if(qy) addBand(qy,'.author-cover','page');

  // 屈原三篇：题材色标 + 竖色 chip；解析 dim 保持原版 DOM 与紧凑样式，不摘出重排
  var mark={
    'p-lisao-qu':     ['#1E2326','#F4F1E6','墨','忧国伤时','rgba(30,35,38,.06)'],
    'p-guoshang-qu':  ['#9B2F2F','#F4F1E6','绛','边塞征战','rgba(155,47,47,.06)'],
    'p-xiangfuren-qu':['#E8A7A0','#1C1B18','桃夭','爱情闺情','rgba(232,167,160,.14)']
  };
  Object.keys(mark).forEach(function(id){
    var el=document.getElementById(id); if(!el) return;
    var m=mark[id], title=el.querySelector('.ptitle');
    if(title && !el.querySelector('.idmark')){
      var d=document.createElement('div'); d.className='idmark';
      d.innerHTML='<i style="background:'+m[0]+'"></i><b>'+m[2]+'</b>｜'+m[3];
      title.insertAdjacentElement('beforebegin',d);
    }
    el.setAttribute('data-chip',m[2]);
    el.style.setProperty('--chip-c',m[0]);
    el.style.setProperty('--chip-t',m[1]);
    el.style.setProperty('--tint',m[4]);
  });

  // 名句类解读：先登记「名句释义」中的名句，再只加粗这些名句在全书各处的复现
  // 只包 <b>，文字一字不动；术语解释（如「其词鄙陋」）不会被误加粗
  function norm(t){return (t||'').replace(/\s+/g,'');}
  var quoteSet={};
  [].slice.call(document.querySelectorAll('.dim')).forEach(function(dim){
    var k=dim.querySelector('.k'), v=dim.querySelector('.v');
    if(!k||!v||k.textContent.trim()!=='名句释义') return;
    var txt=v.textContent||'', re=/[\u201c"]([^\u201d"]{4,120})[\u201d"]/g, m;
    while((m=re.exec(txt))) quoteSet[norm(m[1])]=1;
  });
  var quoted=0;
  [].slice.call(document.querySelectorAll('.dim')).forEach(function(dim){
    var k=dim.querySelector('.k'), v=dim.querySelector('.v');
    if(!k||!v) return;
    var isMingju=(k.textContent.trim()==='名句释义');
    var walker=document.createTreeWalker(v,NodeFilter.SHOW_TEXT,null,false), nodes=[];
    while(walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function(n){
      var txt=n.nodeValue||'', re=/[\u201c"]([^\u201d"]{2,120})[\u201d"]/g, m, last=0, frag=null;
      while((m=re.exec(txt))){
        if(!isMingju && !quoteSet[norm(m[1])]) continue;
        if(!frag) frag=document.createDocumentFragment();
        if(m.index>last) frag.appendChild(document.createTextNode(txt.slice(last,m.index)));
        var b=document.createElement('b'); b.className='d2-quote'; b.textContent=m[0];
        frag.appendChild(b); last=m.index+m[0].length; quoted++;
      }
      if(frag){
        if(last<txt.length) frag.appendChild(document.createTextNode(txt.slice(last)));
        n.parentNode.replaceChild(frag,n);
      }
    });
  });
  window.__d2Quotes=quoted;
})();
</script>
"""
assert s.count("</body>") == 1, "body 数量异常"
s = s.replace("</body>", INJECT_JS + "\n</body>", 1)

io.open(OUT, "w", encoding="utf-8").write(s)
print("生成:", OUT)
print("字节:", len(s.encode("utf-8")), "| 原成品:", len(io.open(SRC, encoding="utf-8").read().encode("utf-8")))
print("插入: CSS 1处, JS 1处；底色/原文/导航/tag 配色零改动；名句仅加粗不改字")
