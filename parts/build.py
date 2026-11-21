# -*- coding: utf-8 -*-
import io, os, re

BASE = r"D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析"
SRC  = os.path.join(BASE, "李白诗词与人生历程系统解析.html")
OUT  = os.path.join(BASE, "统编教材古代作家文学集成.html")
PARTS = os.path.join(BASE, "parts")

s = io.open(SRC, encoding="utf-8").read()
lines = s.splitlines(True)
css = re.search(r"<style>(.*?)</style>", s, re.S).group(1)
# 原文件第83行(<div class="wrap">)至第635行(</div>)，即 82:635
libai_inner = "".join(lines[82:635])
# 避免与附录页 id="method" 冲突
libai_inner = libai_inner.replace('<footer id="method">', '<footer id="libai-method">')
# 李白页原有「#p-xxx」锚点改走分页路由，深链与右侧目录才能正确联动
libai_inner = re.sub(r'<a href="#(p-[a-z0-9\-]+)">',
                     r'<a data-goto="libai::\1" class="tlink">', libai_inner)

EXTRA_CSS = r"""
  /* ===== 分页框架 ===== */
  .app{display:flex;min-height:100vh;}
  .sidebar{width:272px;flex:0 0 272px;background:#efe9dc;border-right:1px solid var(--line);
    height:100vh;overflow-y:auto;position:sticky;top:0;padding:18px 0 50px;}
  .sidebar .brand{padding:0 18px 14px;border-bottom:1px solid var(--line);}
  .sidebar .brand b{font-size:16px;color:var(--accent);}
  .sidebar .brand span{display:block;font-size:11px;color:#8a8378;letter-spacing:.12em;margin-top:4px;
    font-family:-apple-system,"PingFang SC",sans-serif;}
  .toc-group{margin:16px 0 4px;}
  .toc-group>.gt{font-size:11px;color:var(--accent);font-weight:bold;letter-spacing:.18em;
    padding:6px 18px;font-family:-apple-system,"PingFang SC",sans-serif;}
  .toc-group a{display:block;padding:5px 18px 5px 26px;font-size:13.5px;color:var(--ink-soft);
    border-left:3px solid transparent;cursor:pointer;}
  .toc-group a:hover{background:#e5ddcb;color:var(--accent);text-decoration:none;}
  .toc-group a.active{background:var(--paper);border-left-color:var(--accent);color:var(--accent);font-weight:bold;}
  .main{flex:1;min-width:0;padding:0 30px 90px;}
  .topbar{position:sticky;top:0;z-index:20;background:rgba(247,244,236,.96);backdrop-filter:blur(6px);
    border-bottom:1px solid var(--line);padding:11px 0;display:flex;align-items:center;
    justify-content:space-between;gap:12px;flex-wrap:wrap;}
  .topbar .crumb{font-size:13px;color:#8a8378;}
  .nav-btns{display:flex;gap:8px;}
  .nav-btns button{font-family:inherit;font-size:12.5px;padding:6px 13px;border:1px solid var(--line);
    background:var(--paper);border-radius:6px;cursor:pointer;color:var(--ink-soft);}
  .nav-btns button:hover:not(:disabled){border-color:var(--accent);color:var(--accent);}
  .nav-btns button:disabled{opacity:.38;cursor:default;}
  .page{display:none;animation:fade .22s ease;}
  .page.active{display:block;}
  @keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
  .mobile-bar{display:none;}
  .author-cover{text-align:center;padding:40px 16px 26px;border-bottom:2px solid var(--line);}
  .author-cover .eyebrow{color:var(--accent);letter-spacing:.32em;font-size:12px;margin-bottom:12px;
    font-family:-apple-system,"PingFang SC",sans-serif;}
  .author-cover h1{font-size:34px;margin:0 0 10px;color:#1c1a17;letter-spacing:.06em;}
  .author-cover .sub{color:var(--ink-soft);font-size:15px;}
  .author-cover .badges{margin-top:16px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap;}
  .author-card{border:1px solid var(--line);border-radius:10px;padding:20px 24px;margin:22px 0;background:#fffefb;}
  .author-card h3{font-size:19px;color:var(--accent2);margin:0 0 10px;padding-bottom:8px;border-bottom:1px dashed var(--line);}
  .mini-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:10px;margin:14px 0;}
  .mini-grid .m{background:#faf6ec;border:1px solid var(--line);border-radius:6px;padding:10px 12px;
    font-size:14px;color:var(--ink-soft);}
  .mini-grid .m b{display:block;color:var(--accent2);font-size:13px;margin-bottom:3px;
    font-family:-apple-system,"PingFang SC",sans-serif;}
  .home-hero{text-align:center;padding:64px 16px 42px;border-bottom:2px solid var(--line);}
  .home-hero .eyebrow{color:var(--accent);letter-spacing:.4em;font-size:13px;margin-bottom:18px;}
  .home-hero h1{font-size:38px;margin:0 0 16px;color:#1c1a17;letter-spacing:.04em;}
  .home-hero .sub{color:var(--ink-soft);font-size:17px;}
  .stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:32px 0;}
  .stat{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:18px;text-align:center;box-shadow:var(--shadow);}
  .stat b{display:block;font-size:28px;color:var(--accent);font-family:Georgia,serif;}
  .stat span{font-size:13px;color:#8a8378;}
  .quick-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:18px 0;}
  .quick{display:block;background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:14px 16px;
    cursor:pointer;color:var(--ink-soft);font-size:14px;box-shadow:var(--shadow);}
  .quick:hover{border-color:var(--accent);color:var(--accent);text-decoration:none;}
  .quick b{display:block;color:var(--accent2);font-size:15px;margin-bottom:4px;}
  /* 首页「阅读线索」表：四列，说明占主宽，末两列窄 */
  table.clue{table-layout:fixed;}
  table.clue th{text-align:left;white-space:nowrap;}
  table.clue th:nth-child(1),table.clue td:nth-child(1){width:19%;}
  table.clue th:nth-child(3),table.clue td:nth-child(3){width:25%;}
  table.clue th:nth-child(4),table.clue td:nth-child(4){width:21%;}
  table.clue td{vertical-align:top;line-height:1.85;font-size:13.5px;}
  table.clue td:first-child{color:var(--accent);font-weight:bold;line-height:1.7;}
  table.clue td:nth-child(3) a,table.clue td:nth-child(4){font-size:13px;}
  table.clue td:nth-child(3) a{display:inline-block;margin:0 6px 2px 0;white-space:nowrap;}
  @media(max-width:820px){
    table.clue{table-layout:auto;border:none;background:none;}
    table.clue,table.clue tbody,table.clue tr,table.clue td{display:block;width:auto;}
    table.clue tr:first-child{display:none;}
    table.clue tr{background:var(--paper);border:1px solid var(--line);border-radius:8px;
      padding:13px 15px;margin:0 0 10px;}
    table.clue td,table.clue td:nth-child(1),table.clue td:nth-child(3),table.clue td:nth-child(4){border:none;padding:0;width:auto;font-size:13px;line-height:1.8;}
    table.clue td:first-child{font-size:15px;margin-bottom:6px;}
    table.clue td:nth-child(3),table.clue td:nth-child(4){font-size:12.5px;color:var(--ink-soft);margin-top:7px;}
    table.clue td:nth-child(3)::before{content:"对应分页：";color:#8a8378;}
    table.clue td:nth-child(4)::before{content:"代表作者：";color:#8a8378;}
    table.clue td:nth-child(3) a{margin-right:9px;}
  }
  /* ===== 页内目录与生平阶段 ===== */
  .sub-toc{background:#faf6ec;border:1px solid var(--line);border-radius:8px;padding:14px 18px;margin:22px 0;}
  .sub-toc>b{display:block;font-size:11.5px;letter-spacing:.2em;color:var(--accent);margin-bottom:9px;
    font-family:-apple-system,"PingFang SC",sans-serif;}
  .sub-toc a{display:inline-block;margin:3px 14px 3px 0;font-size:13.5px;color:var(--ink-soft);cursor:pointer;
    border-bottom:1px dotted #c9c0ad;}
  .sub-toc a:hover{color:var(--accent);border-bottom-color:var(--accent);text-decoration:none;}
  .sub-toc .g{display:block;margin:10px 0 2px;font-size:12px;color:#a09786;}
  .stage-h{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;border-left:4px solid var(--accent);
    padding-left:13px;margin:38px 0 4px;}
  .stage-h b{font-size:21px;color:var(--accent2);letter-spacing:.03em;}
  .stage-h span{font-size:13px;color:#8a8378;}
  .stage-note{margin:8px 0 18px;font-size:14.5px;color:var(--ink-soft);line-height:1.85;}
  .cardtoc{margin:16px 0 0;font-size:13.5px;color:var(--ink-soft);}
  .cardtoc a{color:var(--accent2);cursor:pointer;border-bottom:1px dotted #c9c0ad;margin-right:10px;}
  .cardtoc a:hover{color:var(--accent);}
  /* 教材篇目交叉链接：可点即五册/本页已有全文，点不动者标虚线下划线 */
  a.xlink{color:var(--accent2);text-decoration:none;cursor:pointer;
    border-bottom:1px dotted #c9c0ad;transition:color .15s,border-color .15s;}
  a.xlink:hover{color:var(--accent);border-bottom-style:solid;border-bottom-color:var(--accent);}
  .xmiss{color:#9a9384;border-bottom:1px dotted #d8d2c6;cursor:help;}
  .xlink::after{content:"↗";font-size:9px;vertical-align:super;margin-left:1px;color:#b9b0a0;}
  .xmiss::after{content:"·未收";font-size:9.5px;vertical-align:super;margin-left:1px;color:#b9b0a0;}
  /* 各页「教材篇目一览」表内的篇目直达链接 */
  td a.tlink,caption a.tlink{color:var(--accent2);cursor:pointer;
    border-bottom:1px dotted #c9c0ad;transition:color .15s,border-color .15s;}
  td a.tlink:hover{color:var(--accent);border-bottom-style:solid;border-bottom-color:var(--accent);
    text-decoration:none;}
  /* 通用可横向滑动的表格容器（选修篇目一览等） */
  .tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch;}
  table.xu-table th,table.mlist th{text-align:center;white-space:nowrap;}
  table.mlist td:first-child{white-space:nowrap;text-align:center;vertical-align:middle;}
  table.xu-table td.xu-unit{text-align:center;vertical-align:middle;white-space:nowrap;}
  table.xu-table td.xu-title{text-align:left;vertical-align:middle;line-height:1.75;}
  table.xu-table td.xu-author{text-align:center;vertical-align:middle;white-space:nowrap;}
  table.xu-table td.xu-point{text-align:left;vertical-align:middle;line-height:1.75;}
  @media(max-width:640px){.tscroll>table{min-width:520px;}}
  .jc-table{font-size:13.5px;table-layout:fixed;}
  .jc-table th,.jc-table td{text-align:center;vertical-align:middle;padding:8px 10px;line-height:1.7;}
  .jc-table th:nth-child(1),.jc-table td:nth-child(1){width:46%;}
  .jc-table th:nth-child(2),.jc-table td:nth-child(2){width:16%;}
  .jc-table th:nth-child(3),.jc-table td:nth-child(3){width:38%;}
  .jc-table td:first-child{white-space:nowrap;color:#8a8378;font-size:12.5px;}
  .jc-table a{cursor:pointer;color:var(--accent2);border-bottom:1px dotted #c9c0ad;}
  .jc-table a:hover{color:var(--accent);text-decoration:none;}
  /* ===== 附录速查表：列宽按内容分配，单元格居中 ===== */
  #indexall table{table-layout:fixed;font-size:13.5px;}
  #indexall th,#indexall td{text-align:center;vertical-align:middle;padding:9px 12px;line-height:1.72;}
  #indexall th{white-space:nowrap;font-size:13px;letter-spacing:.06em;}
  #indexall td:first-child{white-space:nowrap;color:var(--ink-soft);font-size:13px;}
  #indexall td:first-child b{color:var(--ink);}
  #indexall tbody tr:hover td{background:#fbf7ee;}
  /* 长句说明列靠左，避免居中后每行首字参差 */
  #indexall .t-new td:nth-child(2),
  #indexall .t-xuanxiu td:last-child{text-align:left;line-height:1.8;}
  /* 课次/课文一类短列不折行 */
  #indexall .t-xuanxiu td:nth-child(2):not(:last-child){white-space:nowrap;}
  #indexall td[colspan]{white-space:normal;text-align:left;}
  #indexall .tt{white-space:nowrap;}
  #indexall .tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:18px 0;}
  #indexall .tw>table{margin:0;}
  /* 重点作家表：四列，按内容自适应；篇名整体不拆，列宽随最长篇名伸缩 */
  #indexall .t-ming{table-layout:auto;}
  #indexall .t-ming td{padding:8px 9px;line-height:1.9;}
  #indexall .t-ming .tt{white-space:nowrap;}
  #indexall .t-ming td:first-child,#indexall .t-ming th:first-child{min-width:78px;}
  /* 白话小说表：按内容定宽居中，不横向拉满留白 */
  #indexall .tw>table.t-novel{width:auto;table-layout:auto;margin:18px auto;}
  #indexall .t-novel th,#indexall .t-novel td{white-space:nowrap;padding:8px 14px;}
  #indexall .t-novel td:first-child{color:#8a8378;font-size:12.5px;}
  @media (max-width:900px){
    #indexall .tw>table{min-width:860px;}
    #indexall .tw>table.t-novel{min-width:0;}
    #indexall th,#indexall td{padding:8px 9px;}
    /* 窄屏下教材表回到自适应，长篇名允许折行 */
    .jc-table{table-layout:auto;}
    .jc-table td:first-child{white-space:normal;}
    .jc-table th:nth-child(2),.jc-table td:nth-child(2){white-space:nowrap;}
  }
  .poem{scroll-margin-top:70px;}
  /* ===== 每篇独立侧边目录栏 ===== */
  .pwrap{display:flex;align-items:flex-start;gap:26px;}
  .pbody{flex:1;min-width:0;}
  .pbody .sub-toc,.pbody nav.toc{display:none;}
  .page h2,.page section.stage,.page .author-card,.page h3.jc-grade{scroll-margin-top:66px;}
  .page table tr[id]{scroll-margin-top:78px;}
  .prail{flex:0 0 206px;width:206px;position:sticky;top:56px;max-height:calc(100vh - 72px);
    overflow-y:auto;overflow-x:hidden;background:#faf6ec;border:1px solid var(--line);
    border-radius:8px;padding:0 10px 14px;box-shadow:var(--shadow);
    font-family:-apple-system,"PingFang SC",sans-serif;}
  .prail-hd{display:flex;align-items:center;gap:6px;font-size:11px;letter-spacing:.16em;
    color:var(--accent);padding:12px 4px 9px;border-bottom:1px dashed var(--line);margin-bottom:7px;
    position:sticky;top:0;z-index:2;background:#faf6ec;}
  .prail-hd em{font-style:normal;font-size:10.5px;letter-spacing:0;color:#a09786;margin-left:auto;}
  .prail-tg{display:none;font-style:normal;font-size:11px;letter-spacing:0;color:var(--accent2);}
  .prail-list{font-size:12.5px;line-height:1.5;}
  .prail-list .l1{margin-top:9px;}
  .prail-list .l1:first-child{margin-top:0;}
  .prail-list a{display:block;padding:3px 6px;border-radius:4px;color:var(--ink-soft);
    text-decoration:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
  .prail-list a:hover{background:#f1e9d7;color:var(--accent);text-decoration:none;}
  .prail-list a.on{background:#efe5cf;color:var(--accent);font-weight:bold;}
  .prail-list .l1>a{color:var(--accent2);font-weight:bold;border-left:2px solid var(--line);
    border-radius:0 4px 4px 0;padding-left:8px;}
  .prail-list .l1>a.on{border-left-color:var(--accent);}
  .prail-list .l2>a{padding-left:15px;}
  .prail-list .l3>a{padding-left:27px;font-size:12px;color:#847b6e;}
  /* ===== 顶栏搜索 ===== */
  .search{position:relative;flex:0 1 268px;margin-left:auto;min-width:180px;}
  .search input{width:100%;font-family:inherit;font-size:13px;padding:7px 40px 7px 30px;
    border:1px solid var(--line);border-radius:6px;background:var(--paper);color:var(--ink);
    outline:none;transition:border-color .15s,box-shadow .15s;}
  .search input::-webkit-search-cancel-button{display:none;}
  .search input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(155,47,47,.08);}
  .search input::placeholder{color:#a89f8f;}
  .search:before{content:"";position:absolute;left:11px;top:50%;width:9px;height:9px;margin-top:-6px;
    border:1.6px solid #a89f8f;border-radius:50%;pointer-events:none;}
  .search:after{content:"";position:absolute;left:19px;top:50%;width:5px;height:1.6px;margin-top:1px;
    background:#a89f8f;transform:rotate(45deg);pointer-events:none;}
  .search kbd{position:absolute;right:9px;top:50%;transform:translateY(-50%);font-family:inherit;
    font-size:11px;color:#a89f8f;border:1px solid var(--line);border-radius:4px;padding:0 5px;line-height:16px;}
  .sr-panel{display:none;position:absolute;right:0;top:calc(100% + 7px);width:392px;max-width:82vw;
    max-height:62vh;overflow-y:auto;background:var(--paper);border:1px solid var(--line);
    border-radius:8px;box-shadow:0 8px 30px rgba(60,50,35,.16);z-index:60;padding:5px;}
  .sr-item{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 8px;padding:7px 9px;border-radius:5px;
    cursor:pointer;font-size:13.5px;color:var(--ink-soft);}
  .sr-item:hover,.sr-item.on{background:#f1e9d7;}
  .sr-item b{font-weight:normal;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
  .sr-item mark{background:#f6e2b3;color:inherit;padding:0 1px;border-radius:2px;}
  .sr-item em{margin-left:auto;font-style:normal;font-size:11.5px;color:#a09786;white-space:nowrap;flex:none;}
  .sr-tag{flex:none;font-style:normal;font-size:10.5px;padding:1px 6px;border-radius:3px;margin:0;
    line-height:1.5;background:#efe7d4;color:#8a7a58;letter-spacing:.04em;}
  .sr-tag.k-poem{background:#e4ebe6;color:#3d6a52;}
  .sr-tag.k-author{background:#e6ebef;color:#3a5a6b;}
  .sr-tag.k-page{background:#f0e0e0;color:var(--accent);}
  .sr-tag.k-table{background:#f3ece0;color:#8a6f3d;}
  .sr-item .snip{flex:1 0 100%;margin-top:1px;font-size:11.5px;line-height:1.65;color:#9c9280;
    overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;}
  .sr-empty{padding:14px 12px;font-size:13px;color:#a09786;}
  .sr-foot{padding:7px 10px 3px;font-size:11px;color:#b0a794;border-top:1px dashed var(--line);margin-top:4px;}
  .prail::-webkit-scrollbar{width:6px;}
  .prail::-webkit-scrollbar-thumb{background:#dbd1bb;border-radius:3px;}
  .prail::-webkit-scrollbar-track{background:transparent;}
  @media(max-width:1180px){
    .pwrap{display:flex;flex-direction:column-reverse;align-items:stretch;}
    .prail{position:static;flex:0 0 auto;width:auto;max-height:none;margin:0 0 18px;
      padding:7px 2px;background:transparent;border:none;border-bottom:1px dashed var(--line);
      border-radius:0;box-shadow:none;}
    .prail-hd{cursor:pointer;position:static;border-bottom:none;padding:0;margin-bottom:0;
      justify-content:center;letter-spacing:.1em;background:none;}
    .prail-hd em{margin-left:6px;}
    .prail-tg{display:inline;margin-left:6px;}
    .prail-list{display:none;margin-top:9px;border-top:1px dashed var(--line);padding-top:8px;}
    .prail.open .prail-list{display:block;max-height:44vh;overflow-y:auto;}
  }
  @media(max-width:820px){
    .app{display:block;}
    .sidebar{position:fixed;z-index:60;left:0;top:0;height:100vh;width:280px;flex:none;
      transform:translateX(-100%);transition:transform .25s;box-shadow:4px 0 24px rgba(0,0,0,.18);}
    .sidebar.open{transform:translateX(0);}
    .main{padding:0 14px 70px;}
    .mobile-bar{display:flex;position:sticky;top:0;z-index:30;background:var(--paper);
      border-bottom:1px solid var(--line);padding:9px 14px;align-items:center;justify-content:space-between;}
    .mobile-bar button{font-family:inherit;font-size:13px;padding:6px 12px;border:1px solid var(--line);
      background:var(--bg);border-radius:6px;cursor:pointer;color:var(--ink);}
    .topbar{top:0;}
    .search{flex:1 1 100%;order:3;margin-left:0;min-width:0;}
    .search kbd{display:none;}
    .search input{padding-right:12px;}
    .sr-panel{width:100%;max-width:none;left:0;right:auto;}
    .author-cover h1{font-size:28px;} .home-hero h1{font-size:29px;}
  }
"""

JS = r"""
(function(){
  var pages=[].slice.call(document.querySelectorAll('.page'));

  /* ---- 为每一篇生成独立的侧边目录栏 ---- */
  function txt(el){
    if(!el) return '';
    var c=el.cloneNode(true);
    [].slice.call(c.querySelectorAll('.num,.tag,.note')).forEach(function(x){
      if(x.parentNode) x.parentNode.removeChild(x);
    });
    return c.textContent.replace(/\s+/g,' ').trim();
  }
  function buildRail(page){
    var wrap=document.createElement('div'); wrap.className='pwrap';
    var body=document.createElement('div'); body.className='pbody';
    while(page.firstChild){ body.appendChild(page.firstChild); }
    var rail=document.createElement('nav'); rail.className='prail';
    var hd=document.createElement('div'); hd.className='prail-hd';
    var list=document.createElement('div'); list.className='prail-list';
    var nodes=[].slice.call(body.querySelectorAll('h2,section.stage,.author-card,.poem,h3.jc-grade'));
    var items=[], seq=0;
    nodes.forEach(function(n){
      var lv=0, label='', kind='section';
      if(n.tagName==='H2'){
        if(n.closest('nav.toc')) return;
        if(n.parentNode&&n.parentNode.classList&&n.parentNode.classList.contains('stage')) return;
        label=txt(n); lv=1;
      }else if(n.tagName==='SECTION'&&n.classList.contains('stage')){
        label=txt(n.querySelector('h2'))||txt(n); lv=1;
      }else if(n.classList.contains('author-card')){
        kind='author';
        var ps=n.querySelectorAll('.poem');
        label=(txt(n.querySelector('h3'))||'作者').replace(/（[^）]{0,28}）\s*$/,'').trim();
        if(ps.length===1){
          var pt=ps[0].querySelector('.ptitle');
          if(pt) label+=' · '+txt(pt).replace(/[《》]/g,'');
          ps[0].setAttribute('data-nora','1');
        }
        lv=2;
      }else if(n.classList.contains('poem')){
        if(n.getAttribute('data-nora')) return;
        label=txt(n.querySelector('.ptitle'))||'作品';
        lv=(n.closest('.author-card')?3:2); kind='poem';
      }else if(n.classList.contains('jc-grade')){ lv=2; label=txt(n); }
      if(!label) return;
      if(!n.id) n.id=page.id+'-n'+(seq++);
      items.push({id:n.id,level:lv,label:label,kind:kind,alias:(n.getAttribute('data-alias')||'')});
    });
    var t=document.createElement('span'); t.textContent='本篇目录';
    var c=document.createElement('em'); c.textContent=items.length+' 节';
    var tg=document.createElement('i'); tg.className='prail-tg'; tg.textContent='展开';
    hd.appendChild(t); hd.appendChild(c); hd.appendChild(tg);
    items.forEach(function(it){
      var d=document.createElement('div'); d.className='l'+it.level;
      var a=document.createElement('a');
      a.setAttribute('href','#'+it.id); a.setAttribute('data-jump',it.id);
      a.setAttribute('title',it.label); a.setAttribute('data-kind',it.kind);
      if(it.alias) a.setAttribute('data-alias',it.alias);
      a.textContent=it.label;
      d.appendChild(a); list.appendChild(d);
    });
    rail.appendChild(hd); rail.appendChild(list);
    wrap.appendChild(body); wrap.appendChild(rail);
    page.appendChild(wrap);
    hd.addEventListener('click',function(){
      rail.classList.toggle('open');
      tg.textContent=rail.classList.contains('open')?'收起':'展开';
    });
  }
  pages.forEach(buildRail);

  /* ---- 全局检索索引（复用每篇目录栏的锚点） ---- */
  function snorm(t){
    return String(t).replace(/[《》〈〉·・：:，,。、；;（）()【】\[\]「」“”‘’"'！!？?—\-…\s\u00b7]/g,'').toLowerCase();
  }
  /* 作者的字号别称：搜「青莲居士」「东坡」「稼轩」也能命中 */
  var ALIAS={
    '篇目总索引':'教材篇目总索引 总索引 篇目索引 作者索引 速查 篇目速查',
    '全篇顺序索引':'教材全篇顺序索引 教材顺序索引 册次索引 课本顺序 教材顺序 顺序索引',
    '编例与说明':'编例 体例 说明 凡例',
    '李白':'李太白 太白 青莲居士 诗仙 谪仙人 李十二 醉仙',
    '杜甫':'杜子美 子美 少陵野老 诗圣 杜工部 老杜 少陵',
    '白居易':'白乐天 乐天 香山居士 醉吟先生 白香山 白傅',
    '苏轼':'苏东坡 东坡 东坡居士 苏子瞻 子瞻 苏文忠 眉山',
    '辛弃疾':'辛幼安 幼安 稼轩 稼轩居士 辛稼轩 词中之龙',
    '李清照':'李易安 易安 易安居士 漱玉 李清照',
    '王维':'王摩诘 摩诘 诗佛 辋川 王右丞',
    '李商隐':'李义山 义山 玉溪生 樊南生 无题诗人',
    '杜牧':'杜牧之 牧之 樊川 樊川居士 小杜',
    '韩愈':'韩退之 退之 昌黎 韩昌黎 韩文公 昌黎先生',
    '柳宗元':'柳子厚 子厚 柳河东 河东先生 柳柳州',
    '欧阳修':'欧阳永叔 永叔 醉翁 六一居士 欧阳文忠 庐陵',
    '王安石':'王介甫 介甫 半山 半山老人 王文公 临川',
    '范仲淹':'范希文 希文 范文正 范文正公',
    '陆游':'陆务观 务观 放翁 陆放翁 龟堂',
    '陶渊明':'陶潜 陶元亮 元亮 五柳先生 靖节 陶靖节',
    '屈原':'屈平 屈灵均 灵均 三闾大夫',
    '曹操':'曹孟德 孟德 魏武帝 曹阿瞒',
    '曹植':'曹子建 子建 陈王 陈思王',
    '嵇康':'嵇叔夜 叔夜 嵇中散 竹林七贤',
    '阮籍':'阮嗣宗 嗣宗 阮步兵',
    '刘禹锡':'刘梦得 梦得 刘宾客 诗豪',
    '孟浩然':'孟襄阳 襄阳 孟山人 孟夫子',
    '贺知章':'贺季真 季真 四明狂客 贺监',
    '温庭筠':'温飞卿 飞卿 温八叉 花间词人',
    '李煜':'李后主 后主 南唐后主 违命侯',
    '柳永':'柳耆卿 耆卿 柳三变 三变 柳屯田 白衣卿相',
    '周邦彦':'周美成 美成 清真居士 周清真',
    '姜夔':'姜白石 白石道人 姜尧章 尧章',
    '秦观':'秦少游 少游 淮海居士 秦七',
    '晏殊':'晏同叔 同叔 晏元献',
    '晏几道':'晏叔原 叔原 小山 晏小山',
    '杨万里':'杨廷秀 诚斋 诚斋先生 杨诚斋',
    '文天祥':'文履善 文宋瑞 宋瑞 文文山 文山',
    '关汉卿':'关已斋 已斋叟 曲圣 元曲四大家',
    '王实甫':'王德信 德信 西厢 元曲四大家',
    '马致远':'马东篱 东篱 东篱先生 曲状元',
    '汤显祖':'汤义仍 义仍 玉茗堂 临川先生 东方莎士比亚',
    '孔尚任':'孔聘之 聘之 岸堂 云亭山人 南洪北孔',
    '洪昇':'洪昉思 昉思 稗畦 南洪北孔',
    '蒲松龄':'蒲留仙 留仙 剑臣 柳泉居士 聊斋先生 聊斋',
    '吴敬梓':'吴敏轩 敏轩 吴文木 文木老人 秦淮寓客',
    '曹雪芹':'曹梦阮 梦阮 曹霑 雪芹 芹溪 红楼',
    '罗贯中':'罗本 湖海散人 三国演义作者',
    '施耐庵':'施子安 子安 耐庵',
    '吴承恩':'吴汝忠 汝忠 射阳山人 西游作者',
    '冯梦龙':'冯犹龙 犹龙 龙子犹 墨憨斋 三言编者',
    '归有光':'归熙甫 熙甫 震川 震川先生',
    '袁宏道':'袁中郎 中郎 石公 公安派',
    '龚自珍':'龚璱人 璱人 定庵 定盦 龚定庵',
    '梁启超':'梁任公 任公 饮冰室主人 饮冰子',
    '毛泽东':'毛润之 润之 主席诗人',
    '戴望舒':'雨巷诗人',
    '徐志摩':'徐章垿 志摩 新月派',
    '闻一多':'闻家骅 一多 新月派',
    '艾青':'蒋海澄 艾青',
    '舒婷':'龚佩瑜 舒婷 朦胧诗',
    '海子':'查海生 海子',
    '荀子':'荀况 荀卿 孙卿 荀子',
    '庄子':'庄周 南华真人 蒙庄',
    '老子':'李耳 老聃 聃 太上老君 道德经作者',
    '孔子':'孔丘 仲尼 孔夫子 至圣先师 夫子',
    '孟子':'孟轲 子舆 亚圣 邹孟子',
    '墨子':'墨翟 翟',
    '韩非':'韩非子 韩非',
    '李斯':'李通古 通古',
    '司马迁':'司马子长 子长 太史公 史迁 太史令',
    '班固':'班孟坚 孟坚 班兰台',
    '贾谊':'贾生 贾长沙 贾太傅',
    '诸葛亮':'诸葛孔明 孔明 卧龙 武侯 诸葛武侯',
    '王勃':'王子安 子安 王勃',
    '骆宾王':'骆观光 观光',
    '陈子昂':'陈伯玉 伯玉 陈拾遗',
    '张若虚':'张若虚',
    '高适':'高达夫 达夫 高常侍',
    '岑参':'岑嘉州 嘉州',
    '王昌龄':'王少伯 少伯 七绝圣手 王龙标',
    '王之涣':'王季凌 季凌',
    '李贺':'李长吉 长吉 诗鬼 李昌谷',
    '刘长卿':'刘文房 文房 五言长城',
    '韦应物':'韦苏州 韦江州',
    '孟郊':'孟东野 东野 诗囚',
    '贾岛':'贾浪仙 浪仙 诗奴 贾长江',
    '元稹':'元微之 微之 元九',
    '杜荀鹤':'杜彦之 彦之',
    '李绅':'李公垂 公垂 短李',
    '张志和':'张子同 玄真子 烟波钓徒',
    '林逋':'林君复 和靖先生 梅妻鹤子',
    '苏洵':'苏明允 明允 老泉',
    '苏辙':'苏子由 子由 颍滨遗老',
    '曾巩':'曾子固 子固 南丰先生',
    '黄庭坚':'黄鲁直 鲁直 山谷道人 山谷 江西诗派',
    '岳飞':'岳鹏举 鹏举 岳武穆',
    '朱自清':'朱自清 佩弦',
    '鲁迅':'周树人 豫才 鲁迅',
    '老舍':'舒庆春 舍予 老舍',
    '茅盾':'沈德鸿 雁冰 茅盾',
    '巴金':'李尧棠 芾甘 巴金',
    '冰心':'谢婉莹 冰心',
    '朱光潜':'孟实 朱光潜',
    '沈从文':'沈岳焕 从文 边城作者'
  };
  /* 出处别名：从 pmeta 的《书名·篇名》里取篇名，使《北冥有鱼》也能用「逍遥游」搜到 */
  var SRC_SKIP={'全唐诗':1,'全宋词':1,'全宋诗':1,'宋史':1,'史记':1,'汉书':1,'文选':1,'古诗源':1};
  function srcAlias(el){
    var pm=el?el.querySelector('.pmeta'):null;
    if(!pm) return '';
    var t=pm.textContent, out=[], m, re=/《([^》]{2,24})》/g;
    while((m=re.exec(t))){
      var s=m[1], parts=s.split(/[·・]/), tail=parts.length>1?parts[parts.length-1]:s;
      if(!tail||tail.length>14||SRC_SKIP[tail]) continue;
      out.push(tail);
    }
    return out.join(' ');
  }
  var INDEX=[], PGNAME={};
  (function(){
    var pname=PGNAME;
    [].slice.call(document.querySelectorAll('.toc-group a[data-target]')).forEach(function(a){
      pname[a.getAttribute('data-target')]=a.textContent.replace(/\s+/g,' ').trim();
    });
    pages.forEach(function(pg){
      var pl=pname[pg.id]||pg.id, plb=pl.replace(/（[^）]*）/g,'').trim();
      INDEX.push({p:pg.id,a:'',label:pl,kind:'page',ctx:pl,alias:ALIAS[plb]||ALIAS[pl]||''});
      [].slice.call(pg.querySelectorAll('.prail a[data-jump]')).forEach(function(a){
        var id=a.getAttribute('data-jump'), kind=a.getAttribute('data-kind')||'section';
        var label=a.textContent.trim(), al=a.getAttribute('data-alias')||'';
        var base=label.split(' · ')[0];
        if(kind==='author'){
          if(ALIAS[base]) al=(al?al+' ':'')+ALIAS[base];
          if(ALIAS[label]) al=(al?al+' ':'')+ALIAS[label];
        }
        if(kind==='poem'){
          var s=srcAlias(document.getElementById(id));
          if(s) al=(al?al+' ':'')+s;
        }
        INDEX.push({p:pg.id,a:id,label:label,kind:kind,ctx:pl,alias:al});
      });
    });
  })();

  /* ---- 正文检索索引（惰性构建：诗篇卡 / 作者卡 / 表格行） ---- */
  var TINDEX=null;
  function buildTIndex(){
    TINDEX=[]; var seq=0;
    function cellLabel(tr){
      var tds=[].slice.call(tr.children);
      for(var i=0;i<tds.length;i++){
        if(/《|》/.test(tds[i].textContent)) return tds[i].textContent.replace(/\s+/g,' ').trim().slice(0,30);
      }
      return (tds[1]||tds[0]||{textContent:''}).textContent.replace(/\s+/g,' ').trim().slice(0,30);
    }
    function push(pg,el,label,kind){
      if(!el.id){ el.id=pg.id+'-t'+(seq++); }
      var t=snorm(el.textContent||'');
      if(t.length<6) return;
      TINDEX.push({p:pg.id,a:el.id,label:label||'本段',kind:kind,text:t,
        raw:(el.textContent||'').replace(/\s+/g,' ').trim()});
    }
    pages.forEach(function(pg){
      [].slice.call(pg.querySelectorAll('.poem')).forEach(function(el){
        var tt=el.querySelector('.ptitle');
        push(pg,el,tt?txt(tt).replace(/[《》]/g,''):'作品','poem');
      });
      [].slice.call(pg.querySelectorAll('.author-card')).forEach(function(el){
        push(pg,el,(txt(el.querySelector('h3'))||'作者').replace(/（[^）]{0,28}）\s*$/,'').trim(),'author');
      });
      [].slice.call(pg.querySelectorAll('table tr')).forEach(function(tr){
        if(!tr.querySelector('td')) return;
        push(pg,tr,cellLabel(tr),'table');
      });
    });
  }
  function snip(it,q){
    var raw=it.raw||'', probe='';
    for(var k=Math.min(q.length,10);k>=2;k--){
      if(raw.indexOf(q.slice(0,k))>=0){ probe=q.slice(0,k); break; }
    }
    if(!probe) return raw.slice(0,28)+'…';
    var i=raw.indexOf(probe);
    var s=Math.max(0,i-12), e=Math.min(raw.length,i+q.length+16);
    return (s>0?'…':'')+raw.slice(s,e)+(e<raw.length?'…':'');
  }

  /* ---- 搜索栏 ---- */
  (function(){
    var box=document.getElementById('searchBox');
    if(!box) return;
    var input=document.getElementById('q'), panel=document.getElementById('srPanel');
    var KIND={page:'分页',author:'诗人',poem:'诗篇',section:'章节',table:'篇目'};
    var sel=-1, cur=[];
    function norm(t){ return snorm(t); }
    function rank(it,q){
      var l=norm(it.label), c=norm(it.ctx), a=norm(it.alias||''), s=-1, own=false;
      if(!q) return null;
      if(l===q){s=100;own=true;}
      else if(l.indexOf(q)===0){s=82;own=true;}
      else if(l.indexOf(q)>0){s=64;own=true;}
      else if(a&&a.indexOf(q)>=0){
        // 别名命中：整段别名相等权重更高，避免「李白页」被「李十二」类长串稀释
        s=(norm(it.alias).split(' ').indexOf(q)>=0)?76:58; own=true;
      }
      else if(c.indexOf(q)>=0){s=34;}
      if(s<0) return null;
      s+=(it.kind==='page'?9:it.kind==='author'?5:it.kind==='poem'?3:0);
      return {s:s-it.label.length*0.02,own:own};
    }
    function esc(t){return String(t).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c];});}
    function hl(text,q){
      var i=String(text).toLowerCase().indexOf(String(q).toLowerCase());
      if(i<0) return esc(text);
      return esc(text.slice(0,i))+'<mark>'+esc(text.slice(i,i+q.length))+'</mark>'+esc(text.slice(i+q.length));
    }
    function draw(q){
      var qq=norm(q);
      if(!qq){ panel.style.display='none'; panel.innerHTML=''; sel=-1; cur=[]; return; }
      var own=[], byPage=[];
      INDEX.forEach(function(it){
        var r=rank(it,qq);
        if(!r) return;
        (r.own?own:byPage).push({s:r.s,it:it});
      });
      own.sort(function(a,b){return b.s-a.s;});
      byPage.sort(function(a,b){return b.s-a.s;});
      var extra=own.length<6?byPage.slice(0,Math.max(0,10-own.length)):[];
      var hits=own.concat(extra);
      // 直接命中不足时，回落到正文检索（名句、篇目表、作者卡内的评述都能搜到）
      if(own.length<8&&qq.length>=2){
        if(!TINDEX) buildTIndex();
        var seen={}; hits.forEach(function(h){ seen[h.it.p+'|'+h.it.a]=1; });
        var cands=[];
        for(var i=0;i<TINDEX.length;i++){
          var b=TINDEX[i];
          if(seen[b.p+'|'+b.a]) continue;
          var pos=b.text.indexOf(qq);
          if(pos<0) continue;
          // 命中越靠前（多在篇名/正文/名句处）越优先，避免评述里的顺带一提压过原篇
          cands.push({b:b,pos:pos,rel:pos/Math.max(1,b.text.length)});
        }
        cands.sort(function(x,y){ return (x.rel-y.rel)||(x.pos-y.pos); });
        cands.slice(0,8).forEach(function(c){
          var b=c.b; seen[b.p+'|'+b.a]=1;
          hits.push({s:18,it:{p:b.p,a:b.a,label:b.label,kind:b.kind,ctx:PGNAME[b.p]||'',
            _snip:'正文：'+snip(b,qq)}});
        });
      }
      cur=hits.slice(0,40).map(function(h){return h.it;});
      sel=cur.length?0:-1;
      if(!cur.length){
        panel.innerHTML='<div class="sr-empty">没有找到“'+esc(q)+'”，试试作者名、篇名或诗句中的几个字</div>';
        panel.style.display='block'; return;
      }
      var html='';
      cur.forEach(function(it,i){
        var tag=KIND[it.kind]||'章节';
        html+='<div class="sr-item'+(i===0?' on':'')+'" data-i="'+i+'">'+
              '<i class="sr-tag k-'+it.kind+'">'+tag+'</i>'+
              '<b>'+hl(it.label,q)+'</b>'+
              (it.kind==='page'?'':'<em>'+esc(it.ctx)+'</em>')+
              (it._snip?'<span class="snip">'+hl(it._snip,q)+'</span>':'')+
              '</div>';
      });
      panel.innerHTML=html+'<div class="sr-foot">共 '+hits.length+' 条结果 · ↑↓ 选择 · Enter 打开</div>';
      panel.style.display='block';
    }
    function pick(i){
      var it=cur[i]; if(!it) return;
      show(it.p,true,it.a);
      panel.style.display='none';
      input.blur();
    }
    input.addEventListener('input',function(){draw(input.value);});
    input.addEventListener('focus',function(){ if(input.value.trim()) draw(input.value); });
    input.addEventListener('keydown',function(e){
      if(e.key==='ArrowDown'||e.key==='ArrowUp'){
        if(!cur.length) return;
        e.preventDefault();
        sel=(sel+(e.key==='ArrowDown'?1:-1)+cur.length)%cur.length;
        [].slice.call(panel.querySelectorAll('.sr-item')).forEach(function(el,i){
          el.classList.toggle('on',i===sel);
          if(i===sel&&el.scrollIntoView) el.scrollIntoView({block:'nearest'});
        });
      }else if(e.key==='Enter'){
        e.preventDefault(); if(sel>=0) pick(sel);
      }else if(e.key==='Escape'){
        panel.style.display='none'; input.blur();
      }
    });
    panel.addEventListener('mousedown',function(e){
      var el=e.target.closest?e.target.closest('.sr-item'):null;
      if(!el) return;
      e.preventDefault();
      pick(parseInt(el.getAttribute('data-i'),10));
    });
    document.addEventListener('click',function(e){
      if(!box.contains(e.target)) panel.style.display='none';
    });
    document.addEventListener('keydown',function(e){
      if(e.key==='/'&&e.target.tagName!=='INPUT'&&e.target.tagName!=='TEXTAREA'){
        e.preventDefault(); input.focus(); input.select();
      }
    });
  })();

  /* ---- 侧栏高亮当前所在小节 ---- */
  var raf=null;
  function spy(){
    raf=null;
    var page=document.querySelector('.page.active'); if(!page) return;
    var rail=page.querySelector('.prail'); if(!rail) return;
    var as=[].slice.call(rail.querySelectorAll('a[data-jump]'));
    if(!as.length) return;
    var cur=null;
    for(var i=0;i<as.length;i++){
      var el=document.getElementById(as[i].getAttribute('data-jump'));
      if(!el) continue;
      if(el.getBoundingClientRect().top<=150) cur=as[i]; else break;
    }
    as.forEach(function(a){a.classList.toggle('on',a===cur);});
    if(cur){
      var rr=cur.getBoundingClientRect(), pr=rail.getBoundingClientRect();
      if(rr.top<pr.top+6) rail.scrollTop+=rr.top-pr.top-8;
      else if(rr.bottom>pr.bottom-6) rail.scrollTop+=rr.bottom-pr.bottom+8;
    }
  }
  function scheduleSpy(){ if(!raf) raf=requestAnimationFrame(spy); }
  window.addEventListener('scroll',scheduleSpy,{passive:true});
  window.addEventListener('resize',scheduleSpy);

  var ids=pages.map(function(p){return p.id;});
  var links=[].slice.call(document.querySelectorAll('.toc-group a'));
  var crumb=document.getElementById('crumb');
  var prev=document.getElementById('prevBtn'),next=document.getElementById('nextBtn');
  var sidebar=document.getElementById('sidebar');
  function currentId(){var p=document.querySelector('.page.active');return p?p.id:ids[0];}
  function jump(anchor){
    if(!anchor) return;
    var el=document.getElementById(anchor);
    if(!el) return;
    try{ el.scrollIntoView({behavior:'auto',block:'start'}); }
    catch(e){ el.scrollIntoView(); }
  }
  function parseGo(v){var p=String(v||'').split('::');return [p[0],p[1]||''];}
  function show(id,push,anchor){
    if(ids.indexOf(id)<0) return false;
    pages.forEach(function(p){p.classList.toggle('active',p.id===id);});
    links.forEach(function(a){a.classList.toggle('active',a.getAttribute('data-target')===id);});
    var i=ids.indexOf(id);
    prev.disabled=(i===0); next.disabled=(i===ids.length-1);
    var a=links.filter(function(x){return x.getAttribute('data-target')===id;})[0];
    crumb.textContent='当前：'+(a?a.textContent.trim():'总览');
    var want='#'+id+(anchor?'::'+anchor:'');
    if(push!==false && location.hash!==want) history.pushState(null,'',want);
    if(anchor){setTimeout(function(){jump(anchor);},60); setTimeout(function(){jump(anchor);},400);} else {window.scrollTo(0,0);}
    sidebar.classList.remove('open');
    var act=links.filter(function(x){return x.classList.contains('active');})[0];
    if(act&&act.scrollIntoView) act.scrollIntoView({block:'nearest'});
    var pr=document.getElementById(id);
    pr=pr?pr.querySelector('.prail'):null;
    if(pr) pr.scrollTop=0;
    scheduleSpy();
    return true;
  }
  links.forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();show(a.getAttribute('data-target'));});});
  document.querySelectorAll('[data-goto]').forEach(function(el){el.addEventListener('click',function(e){
    e.preventDefault(); var g=parseGo(el.getAttribute('data-goto')); show(g[0],true,g[1]);
  });});
  Array.prototype.forEach.call(document.querySelectorAll('.sub-toc a,[data-jump]'),function(el){
    el.addEventListener('click',function(e){
      e.preventDefault();
      var t=el.getAttribute('data-jump')||(el.getAttribute('href')||'').replace(/^#/,'');
      var rl=el.closest('.prail');
      if(rl&&rl.classList.contains('open')){
        rl.classList.remove('open');
        var tg=rl.querySelector('.prail-tg'); if(tg) tg.textContent='展开';
      }
      if(t) jump(t);
    });
  });
  prev.addEventListener('click',function(){var i=ids.indexOf(currentId());if(i>0)show(ids[i-1]);});
  next.addEventListener('click',function(){var i=ids.indexOf(currentId());if(i<ids.length-1)show(ids[i+1]);});
  document.getElementById('topBtn').addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
  document.getElementById('menuBtn').addEventListener('click',function(){sidebar.classList.toggle('open');});
  sidebar.addEventListener('click',function(e){if(e.target===sidebar)sidebar.classList.remove('open');});
  window.addEventListener('popstate',function(){var g=parseGo(location.hash.slice(1));show(g[0],false,g[1]);});
  window.addEventListener('hashchange',function(){
    var g=parseGo(location.hash.slice(1));
    if(!show(g[0],false,g[1])){var el=document.getElementById(g[0]);if(el)el.scrollIntoView({behavior:'smooth'});}
  });
  document.addEventListener('keydown',function(e){
    if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA')return;
    var i=ids.indexOf(currentId());
    if(e.key==='ArrowLeft'&&i>0)show(ids[i-1]);
    if(e.key==='ArrowRight'&&i<ids.length-1)show(ids[i+1]);
  });
  var init=parseGo(location.hash.slice(1)||ids[0]);
  show(init[0],false,init[1]);
  window.addEventListener('load',scheduleSpy);
})();
"""

# (id, group, label)
PAGES = [
 ("home","导览","首页 · 全书总览"),
 ("indexall","索引 · 教材篇目","篇目总索引（按作者）"),
 ("jiaocai","索引 · 教材篇目","全篇顺序索引（按册次）"),
 ("xiaowen","小学 · 文言启蒙","小学文言启蒙（11篇）"),
 ("quyuan","先秦两汉","屈原与《楚辞》"),
 ("shijing","先秦两汉","《诗经》与民间歌谣"),
 ("zhuzi","先秦两汉","先秦诸子散文"),
 ("hanprose","先秦两汉","两汉史传与辞赋"),
 ("taoyuanming","魏晋南北朝","陶渊明"),
 ("caocao","魏晋南北朝","曹操与建安诗人"),
 ("weijinprose","魏晋南北朝","魏晋南北朝散文"),
 ("libai","隋唐 · 重点作家","李白（全书详解）"),
 ("dufu","隋唐 · 重点作家","杜甫"),
 ("wangwei","隋唐 · 重点作家","王维"),
 ("baijuyi","隋唐 · 重点作家","白居易"),
 ("lihe","隋唐 · 重点作家","李贺"),
 ("shangyin","隋唐 · 重点作家","李商隐"),
 ("dumu","隋唐 · 重点作家","杜牧"),
 ("tangchu","隋唐 · 作家合篇","初唐四杰与陈子昂"),
 ("tangsheng","隋唐 · 作家合篇","盛唐山水与边塞诗人"),
 ("tangwan","隋唐 · 作家合篇","中晚唐诗人"),
 ("tangguwen","隋唐 · 作家合篇","唐代古文：韩柳"),
 ("sushi","宋 · 重点作家","苏轼"),
 ("liqingzhao","宋 · 重点作家","李清照"),
 ("luyou","宋 · 重点作家","陆游"),
 ("xinqiji","宋 · 重点作家","辛弃疾"),
 ("wanganshi","宋 · 重点作家","王安石"),
 ("fanzhongyan","宋 · 重点作家","范仲淹"),
 ("ouyangxiu","宋 · 重点作家","欧阳修"),
 ("songci","宋 · 作家合篇","两宋词人"),
 ("songshi","宋 · 作家合篇","宋代诗人"),
 ("songwen","宋 · 作家合篇","宋代散文"),
 ("yuanqu","元明清近代","元曲作家"),
 ("mingqingwen","元明清近代","明清散文"),
 ("mingqingshi","元明清近代","明清诗词"),
 ("novel","元明清近代","古代白话小说（9篇）"),
 ("mao","元明清近代","毛泽东"),
 ("xiandai","近现代","近现代诗词（14篇）"),
 ("xuanxiu","高中选修 · 专题研讨","中华传统文化专题研讨（选修）"),
 ("method","附录","编例与说明"),
]

toc=[]
last_group=None
for pid,grp,label in PAGES:
    if grp!=last_group:
        toc.append('  <div class="toc-group"><div class="gt">%s</div>'%grp)
        last_group=grp
    toc.append('    <a href="#%s" data-target="%s">%s</a>'%(pid,pid,label))
toc.append('  </div>')
toc="\n".join(toc)

parts_html={}
for fn in os.listdir(PARTS):
    if fn.endswith(".html"):
        parts_html[fn]=io.open(os.path.join(PARTS,fn),encoding="utf-8").read()

bodies=[]
for pid,grp,label in PAGES:
    if pid=="libai":
        bodies.append('<section class="page" id="libai">'+libai_inner+parts_html.get("libai_extra.html","")+'</section>')
    else:
        bodies.append('<section class="page" id="%s">%s</section>'%(pid,parts_html.get(pid+".html","<p>待补充</p>")))
bodies="\n".join(bodies)

doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>统编教材古代作家文学集成 · 分页版</title>
<style>%s
%s</style>
</head>
<body>
<div class="app">
 <aside class="sidebar" id="sidebar">
  <div class="brand"><b>统编教材 · 古代作家集成</b><span>小学 / 初中 / 高中 · 分页阅读版</span></div>
%s
 </aside>
 <main class="main">
  <div class="mobile-bar"><button id="menuBtn">☰ 目录</button><span style="font-size:12px;color:#8a8378">古代作家文学集成</span></div>
  <div class="topbar">
    <div class="crumb" id="crumb"></div>
    <div class="search" id="searchBox">
      <input id="q" type="text" autocomplete="off" spellcheck="false" placeholder="搜诗人、篇名或诗句">
      <kbd>/</kbd>
      <div class="sr-panel" id="srPanel"></div>
    </div>
    <div class="nav-btns"><button id="prevBtn">← 上一篇</button><button id="topBtn">回到顶部</button><button id="nextBtn">下一篇 →</button></div>
  </div>
%s
 </main>
</div>
<script>%s</script>
</body>
</html>
"""%(css,EXTRA_CSS,toc,bodies,JS)

io.open(OUT,"w",encoding="utf-8").write(doc)
print("生成:",OUT)
print("页面数:",len(PAGES),"  字节:",len(doc.encode('utf-8')))
missing=[p for p in parts_html if p[:-5] not in [x[0] for x in PAGES] and p!="libai_extra.html"]
print("片段文件:",len(parts_html),"  冗余:",missing)
