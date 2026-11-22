# -*- coding: utf-8 -*-
"""从成品原样复制生成预览：只叠加皮肤CSS + 屈原三篇新增题材色标。
原文、结构、导航、tag配色一字不动——脚本只做两处字符串插入。"""
import io, os

BASE = r"D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析"
SRC  = os.path.join(BASE, "统编教材古代作家文学集成.html")
OUT  = os.path.join(BASE, "design-demos", "preview-reading.html")

s = io.open(SRC, encoding="utf-8").read()

# ── 皮肤：只调底色与顶栏，字号层级/正文/tag配色/导航一律不动 ──
SKIN_CSS = r"""
  /* ===== 视觉皮肤（仅底色与顶栏，原文与排版结构不动）===== */
  :root{
    --bg:#F2EDE1;        /* 竹纸暖灰：比原 #f7f4ec 略沉静 */
    --paper:#FDFBF5;     /* 卡片微暖，仍亮于底，保持层次 */
  }
  /* 顶栏吸顶增强：实底 + 细阴影，滚动时更清晰（原已 sticky，此处只增强可读性） */
  .topbar{background:rgba(242,237,225,.97)!important;box-shadow:0 2px 10px rgba(60,50,35,.06);}
  /* 侧栏/章节栏跟随底色，仅微调，不动字号与结构 */
  .sidebar{background:#EAE3D2!important;}
  .prail,.prail-hd{background:#F7F3E8!important;}
  /* 新增：诗词标题上方的题材身份色标（原书无此元素，纯新增，不改任何原文） */
  .idmark{font-family:-apple-system,"PingFang SC",sans-serif;font-size:12.5px;
    color:#6b6455;margin:0 0 7px;display:flex;align-items:center;gap:7px;letter-spacing:.02em;}
  .idmark i{width:3px;height:15px;border-radius:1px;display:inline-block;flex:0 0 3px;}
  .idmark b{font-weight:700;color:var(--ink);}
"""

# 在 </style> 前插入（最后定义，优先级最高）
assert s.count("</style>") == 1, "style 块数量异常"
s = s.replace("</style>", SKIN_CSS + "\n</style>", 1)

# ── 新增题材色标：屈原三篇，插在各自 .ptitle 之前 ──
INJECT_JS = r"""
<script>
(function(){
  // 题材色取 dir-2.html 原有 12 色系；题材名取第三篇题材分类索引 12 类
  var mark={
    'p-lisao-qu':     ['#C8382A','朱','忧国伤时'],
    'p-guoshang-qu':  ['#9B2F2F','绛','边塞征战'],
    'p-xiangfuren-qu':['#8FBFA8','缥碧','爱情闺情']
  };
  Object.keys(mark).forEach(function(id){
    var el=document.getElementById(id);
    if(!el) return;
    var title=el.querySelector('.ptitle');
    if(!title || el.querySelector('.idmark')) return;   // 幂等
    var m=mark[id];
    var d=document.createElement('div');
    d.className='idmark';
    d.innerHTML='<i style="background:'+m[0]+'"></i><b>'+m[1]+'</b>｜'+m[2];
    el.insertBefore(d,title);
  });
})();
</script>
"""
assert s.count("</body>") == 1, "body 数量异常"
s = s.replace("</body>", INJECT_JS + "\n</body>", 1)

io.open(OUT, "w", encoding="utf-8").write(s)
print("生成:", OUT)
print("字节:", len(s.encode("utf-8")), "| 原成品:", len(io.open(SRC,encoding='utf-8').read().encode('utf-8')))
print("插入: SKIN_CSS 1处, INJECT_JS 1处; 原文与结构零改动")
