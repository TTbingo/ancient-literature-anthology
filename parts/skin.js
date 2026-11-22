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
      return '<button class="d2-bar'+(i===0?' on':'')+'" data-i="'+i+'" style="--c:'+t[2]+';--t:'+t[3]+'" title="'+t[0]+'">'+
             '<span class="vname">'+t[0]+'</span></button>';
    }).join('');
    // 色名第二系统已砍：只保留题材名，坐标只显示题材名
    // 坐标说明只在首页出现（首页就地切换解读）；正文页点色块直达题材页，不需要也不该显示
    var coord=(mode==='home')?'<div class="d2-coord">当前坐标 · <b>'+topics[0][0]+'</b></div>':'';
    return '<div class="d2-band-shell"><div class="d2-band-scroll"><nav class="d2-band">'+bars+'</nav></div>'+
      '<div class="d2-band-meta">'+coord+'</div></div>';
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
    box.querySelector('.d2-td-line').textContent=d.desc;
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
      if(coordB) coordB.textContent=t[0];
      if(detail){ fillDetail(detail,i); return; }  // 首页：就地解读，不跳走
      var link=[].slice.call(document.querySelectorAll('[data-goto]')).filter(function(x){
        return x.getAttribute('data-goto')==='ticai::tc-'+String(i+1).padStart(2,'0');
      })[0];
      if(link) link.click();                       // 正文页：保持简洁，点色块直达题材页
    });
  }
  var home=document.getElementById('home');
  if(home) addBand(home,'.home-hero','home');
  // 关键词均取题材索引各类原文用词，按具体->泛化排序；不新造语义
  var kw=[
    [1,['送别','赠答','怀友','惜别','赠友','送友人','离别','饯别','酬赠','酬答','赠序']],
    [2,['边塞','征战','从军','军旅','边关','戍边','出征','战争','战事','战斗','作战','行军','长征','抗日']],
    [3,['羁旅','思乡','旅愁','乡愁','漂泊','客居','游子','念家','怀旧','怀乡','行役','羁愁']],
    [4,['山水','田园','隐逸','闲适','山林','写景','纪游','春景','秋景','江景','咏雨','山行','草堂','花期','自然','风光','登临','登楼','访隐','山居','西湖','题画']],
    [5,['咏史','怀古','古迹','吊古','借古讽今','史论','以秦','历史规律','兴亡','赤壁']],
    [6,['咏物','托物','借物','喻人','寄意','音乐题材','技艺','咏蝉','咏梅','咏黄河','咏秋','咏暮春','咏西湖','自喻']],
    [7,['爱情','闺情','闺怨','相思','情爱','男女','悼亡','望月怀人']],
    [8,['忧国','伤时','家国','国破','忧民','时事','诗史','悯民','乱离','变革','图强','兴国','纳谏','捷报','抗清','怨刺','劳役','改革']],
    [9,['言志','抒怀','抱负','壮志','理想','胸臆','豪情','志向','情怀','气概','建设','宏图','歌唱','呼唤','志业','使命','自勉','进取','革命意志','托付','担当','忧怀','确认生命','绝笔']],
    [10,['说理','劝学','哲理','学习','寓言','道理','论证','阐发','启示','为人处世','学习方法','科技','说明文','工序','论辩','驳论文','教育论文','表奏','政论','公文','论说文','推演','互为因果','归一','四端','恻隐']],
    [11,['叙事','写人','记人','人物','记言','言行','史传','记事','讽谏','待客','迎客','传记','过程','赞其','劫取','石猴','孙悟空','候客','宴集','泛舟','主客问答']],
    [12,['节令','童趣','儿童','节日','岁时','民俗','农事','春日','人间烟火','采莲','水乡']],
  ];

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
      d.innerHTML='<i style="background:'+t[2]+'"></i>'+t[0];
      title.insertAdjacentElement('beforebegin',d);
    }
    el.setAttribute('data-chip',t[0]);
    el.style.setProperty('--chip-c',t[2]);
    el.style.setProperty('--chip-t',t[3]);
    el.style.setProperty('--tint',t[2]+'0d');  // hex8 低透明度底纹，色相同题材
    labeled++;
  });
  window.__d2Label={labeled:labeled,fromIndex:fromIndex,fromKw:fromKw,
    fromOverride:fromOverride,unclassified:unclassified};

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

  // ---- 七维解析分组：语境 / 细读 / 回响（只包结构，一字不改） ----
  // 三组是阅读动作的顺序，不是题材分类；组内 dim 保持原版紧凑横排
  var GROUPS=[
    {name:'语境', keys:['创作背景','题材主题','出处与背景']},
    {name:'细读', keys:['情感脉络','意象与语言','艺术手法','原文疏解','寓意与人物',
                        '说理与人物','内容与结构','说明顺序','论证层次']},
    {name:'回响', keys:['名句释义','文学意义','学习要点','名句与学习要点']}
  ];
  function groupIdx(k){
    for(var i=0;i<GROUPS.length;i++) if(GROUPS[i].keys.indexOf(k)>=0) return i;
    return 1;  // 非标准维度兜底归细读，保证一篇不丢
  }
  var grpTotal=0, grpPoems=0, grpFallback=0;
  [].slice.call(document.querySelectorAll('.poem')).forEach(function(poem){
    if(poem.querySelector('.dgroup')) return;
    var verse=poem.querySelector('.verse');
    if(!verse) return;
    var dims=[].slice.call(poem.querySelectorAll(':scope > .dim'));
    if(!dims.length) return;
    var buckets={0:[],1:[],2:[]};
    dims.forEach(function(d){
      var k=d.querySelector('.k');
      if(!k){ buckets[1].push(d); return; }
      var t=k.textContent.trim(), i=groupIdx(t);
      var known=GROUPS[0].keys.indexOf(t)>=0||GROUPS[1].keys.indexOf(t)>=0||GROUPS[2].keys.indexOf(t)>=0;
      if(!known) grpFallback++;
      buckets[i].push(d);
    });
    var boxes=[];
    GROUPS.forEach(function(g,i){
      if(!buckets[i].length) return;
      var box=document.createElement('div'); box.className='dgroup';
      var hd=document.createElement('div'); hd.className='dgroup-hd'; hd.textContent=g.name;
      box.appendChild(hd);
      buckets[i].forEach(function(d){
        if(i===2 && d.querySelector('.k') && d.querySelector('.k').textContent.trim()==='名句释义')
          d.classList.add('dgroup-mingju');
        box.appendChild(d);  // appendChild 已从原位置移走，不要再 removeChild
      });
      boxes.push(box); grpTotal++;
    });
    if(!boxes.length) return;
    var ref=verse;
    boxes.forEach(function(bx){ ref.insertAdjacentElement('afterend',bx); ref=bx; });
    grpPoems++;
  });
  window.__d2Groups={poems:grpPoems,groups:grpTotal,fallback:grpFallback};
})();
