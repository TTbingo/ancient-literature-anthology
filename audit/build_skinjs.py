# -*- coding: utf-8 -*-
"""重建 parts/skin.js：色标从屈原三篇扩展到全书 376 篇。
题材归类来源（均取原题材索引，不新造语义）：
  1) 题材分类索引 ticai.html 已收录的篇目 -> 精确归类
  2) 其余篇目 -> 按该篇「题材主题」原文中的题材关键词归入 12 类
  3) 屈原三篇 -> 保留用户已确认的色标（索引未收录）
保留原有：色带、首页解读、名句加粗、解析区原版样式。
"""
import io

TOPICS = """  // 12 题材来自第三篇索引；一题材一传统色（取 dir-2 原色谱，无重复）
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
"""

# 关键词按优先级排列（具体 -> 泛化），词均来自题材索引各类「主要内容/常见意象/思想感情」原文
KW = [
    (1,  ['送别','赠答','怀友','惜别','赠友','送友人','离别','饯别','酬赠','酬答','赠序']),
    (2,  ['边塞','征战','从军','军旅','边关','戍边','出征','战争','战事','战斗','作战','行军','长征','抗日']),
    (3,  ['羁旅','思乡','旅愁','乡愁','漂泊','客居','游子','念家','怀旧','怀乡','行役','羁愁']),
    (4,  ['山水','田园','隐逸','闲适','山林','写景','纪游','春景','秋景','江景','咏雨','山行','草堂','花期','自然','风光','登临','登楼','访隐','山居','西湖','题画']),
    (5,  ['咏史','怀古','古迹','吊古','借古讽今','史论','以秦','历史规律','兴亡','赤壁']),
    (6,  ['咏物','托物','借物','喻人','寄意','音乐题材','技艺','咏蝉','咏梅','咏黄河','咏秋','咏暮春','咏西湖','自喻']),
    (7,  ['爱情','闺情','闺怨','相思','情爱','男女','悼亡','望月怀人']),
    (8,  ['忧国','伤时','家国','国破','忧民','时事','诗史','悯民','乱离','变革','图强','兴国','纳谏','捷报','抗清','怨刺','劳役','改革']),
    (9,  ['言志','抒怀','抱负','壮志','理想','胸臆','豪情','志向','情怀','气概','建设','宏图','歌唱','呼唤','志业','使命','自勉','进取','革命意志','托付','担当','忧怀','确认生命','绝笔']),
    (10, ['说理','劝学','哲理','学习','寓言','道理','论证','阐发','启示','为人处世','学习方法','科技','说明文','工序','论辩','驳论文','教育论文','表奏','政论','公文','论说文','推演','互为因果','归一','四端','恻隐']),
    (11, ['叙事','写人','记人','人物','记言','言行','史传','记事','讽谏','待客','迎客','传记','过程','赞其','劫取','石猴','孙悟空','候客','宴集','泛舟','主客问答']),
    (12, ['节令','童趣','儿童','节日','岁时','民俗','农事','春日','人间烟火','采莲','水乡']),
]

kw_js = "  // 关键词均取题材索引各类原文用词，按具体->泛化排序；不新造语义\n  var kw=[\n"
for idx, words in KW:
    kw_js += "    [" + str(idx) + ",[" + ",".join("'" + w + "'" for w in words) + "]],\n"
kw_js += "  ];\n"

GLOBAL = r'''
  // ---- 全书作品题材色标：索引精确归类 > 题材主题原文关键词 > 屈原三篇人工确认 ----
  // 从题材索引提取「作品id -> 类序号」精确映射（代表作品均可点击直达）
  var exact={};
  [].slice.call(document.querySelectorAll('#ticai .cat')).forEach(function(cat,i){
    [].slice.call(cat.querySelectorAll('.works a[data-goto]')).forEach(function(a){
      var g=a.getAttribute('data-goto')||'', p=g.split('::')[1];
      if(p) exact[p]=i+1;
    });
  });
  // 屈原三篇：用户已确认的色标（题材索引未收录，保留原配色）
  var override={
    'p-lisao-qu':8,      // 忧国伤时 / 墨
    'p-guoshang-qu':2,   // 边塞征战 / 绛
    'p-xiangfuren-qu':7  // 爱情闺情 / 桃夭
  };
  // 神话/寓言/文言短篇：题材索引第11类「叙事写人——以事立人，寓褒于叙」
  var NARRA=['p-shouzhu','p-jingwei','p-wangrong','p-nangying','p-tiechu','p-guren',
    'p-maodun','p-yangshi','p-daishong','p-yuexia','libai-n3','libai-n4'];
  NARRA.forEach(function(id){override[id]=11;});
  // 其余无「题材主题」维度的残篇：按作品块自身文字归入原题材类
  var FALLBACK={
    'p-wangwei-hua':4,          // 画/山水 -> 山水田园
    'p-zhouyeshuo-zhashenxing':10, // 说理 -> 说理劝学
    'p-huangtingjian-qingpingyue':9,// 抒怀 -> 抒怀言志
    'p-yuzhongzaji-fangbao':4,  // 景物 -> 山水田园
    'p-nananjun':2,             // 从军 -> 边塞征战
    'p-xiaohong-mupan':1,       // 凭吊亡友 -> 送别赠友
    'p-duanzhang':10,           // 哲思 -> 说理劝学
    'p-tongyi':10,              // 推演归一 -> 说理劝学
    'p-eriduoxuefeng':9,        // 所见所感 -> 抒怀言志
    'p-ludi-fengyuyin':8,       // 时代风雨忧怀 -> 忧国伤时
    'p-shenyimo-yueye':9,       // 月夜所见 -> 抒怀言志
    'p-xu-huainanzi':10,'p-xu-juejiaoshu':10,'p-xu-maoshixu':10,
    'p-xu-shezhan':10,'p-xu-kuangchaoren':10,'p-xu-zhulou':10,
    'p-xu-gaozu':5,'p-xu-shirunze':5,  // 淮南子/尺牍/历史 -> 说理劝学或咏史怀古
    'p-jishierlang-hanyu':11  // 祭文追忆家常 -> 叙事写人
  };
  Object.keys(FALLBACK).forEach(function(id){if(!override[id])override[id]=FALLBACK[id];});
  function kwClass(txt){
    if(!txt) return 0;
    for(var i=0;i<kw.length;i++){
      var ws=kw[i][1];
      for(var j=0;j<ws.length;j++) if(txt.indexOf(ws[j])>=0) return kw[i][0];
    }
    return 0;
  }
  function themeText(el){
    var dims=[].slice.call(el.querySelectorAll('.dim'));
    for(var i=0;i<dims.length;i++){
      var k=dims[i].querySelector('.k'), v=dims[i].querySelector('.v');
      if(k && v && k.textContent.trim()==='题材主题') return v.textContent||'';
    }
    return '';
  }
  var labeled=0, fromIndex=0, fromKw=0, fromOverride=0, unclassified=[];
  [].slice.call(document.querySelectorAll('.poem')).forEach(function(el){
    var pid=el.id, n=0;
    if(override[pid]){ n=override[pid]; fromOverride++; }
    else if(exact[pid]){ n=exact[pid]; fromIndex++; }
    else { n=kwClass(themeText(el)); if(n) fromKw++; }
    if(!n){ unclassified.push(pid); return; }  // 无题材归类：保留默认中性色条，不显示色标
    var t=topics[n-1];
    var title=el.querySelector('.ptitle');
    if(title && !el.querySelector('.idmark')){
      var d=document.createElement('div'); d.className='idmark';
      d.innerHTML='<i style="background:'+t[2]+'"></i><b>'+t[1]+'</b>｜'+t[0];
      title.insertAdjacentElement('beforebegin',d);
    }
    el.setAttribute('data-chip',t[1]);
    el.style.setProperty('--chip-c',t[2]);
    el.style.setProperty('--chip-t',t[3]);
    el.style.setProperty('--tint',t[2]+'0d');  // hex8 低透明度底纹，色相同题材
    labeled++;
  });
  window.__d2Label={labeled:labeled,fromIndex:fromIndex,fromKw:fromKw,
    fromOverride:fromOverride,unclassified:unclassified};
'''

src = io.open('audit/skin_head.txt', encoding='utf-8').read() if False else None
# 组装：原文件的头部（IIFE 开始 + topics）用新 TOPICS 替换，色带/detail 段保留，屈原 mark 段替换为 GLOBAL
import os
base = 'audit/skin.js.before-global' if os.path.exists('audit/skin.js.before-global') else 'parts/skin.js'
old = io.open(base, encoding='utf-8').read()
start = old.index('(function(){')
topics_start = old.index('  // 12 题材来自第三篇索引')
band_start = old.index('  function bandHTML(mode){')
band_end = old.index('  // 屈原三篇：题材色标') if '  // 屈原三篇：题材色标' in old else old.index('  // ---- 全书作品题材色标')
tail_i = old.index('  // 名句类解读：')

head = old[start:topics_start]
band = old[band_start:band_end]   # 含 bandHTML/detailHTML/addBand 定义 + home/quyuan 调用
# 只保留首页色带：移除屈原页上方常驻色卡（其余色标/色带/样式一律不动）
import re as _re
band, _n = _re.subn(r"  var qy=document\.getElementById\('quyuan'\);\s*\n\s*if\(qy\) addBand\(qy,'\.author-cover','page'\);\s*\n?", '', band)
assert _n == 1, '未找到屈原页色带调用（n=%d），请检查备份文件' % _n
tail = old[tail_i:]

out = head + TOPICS + band + kw_js + GLOBAL + '\n' + tail
io.open('parts/skin.js', 'w', encoding='utf-8').write(out)
print('skin.js 重建完成，字符数:', len(out))
