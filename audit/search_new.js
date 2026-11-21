  /* ---- 全局检索索引（复用每篇目录栏的锚点） ---- */
  function snorm(t){
    return String(t).replace(/[《》〈〉·・：:，,。、；;（）()【】\[\]「」“”‘’"'！!？?—\-…\s\u00b7]/g,'').toLowerCase();
  }
  /* 作者的字号别称：搜「青莲居士」「东坡」「稼轩」也能命中 */
  var ALIAS={
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
  var INDEX=[];
  (function(){
    var pname={};
    [].slice.call(document.querySelectorAll('.toc-group a[data-target]')).forEach(function(a){
      pname[a.getAttribute('data-target')]=a.textContent.replace(/\s+/g,' ').trim();
    });
    pages.forEach(function(pg){
      var pl=pname[pg.id]||pg.id;
      INDEX.push({p:pg.id,a:'',label:pl,kind:'page',ctx:pl,alias:ALIAS[pl]||''});
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
        var got=0;
        for(var i=0;i<TINDEX.length&&got<8;i++){
          var b=TINDEX[i];
          if(seen[b.p+'|'+b.a]) continue;
          if(b.text.indexOf(qq)<0) continue;
          seen[b.p+'|'+b.a]=1; got++;
          hits.push({s:18,it:{p:b.p,a:b.a,label:b.label,kind:b.kind,ctx:'正文命中',_snip:snip(b,qq)}});
        }
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

