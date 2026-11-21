const { chromium } = require('playwright');
const path=require('path');
(async()=>{
 const file='file:///'+path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g,'/');
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1440,height:950}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto(file,{waitUntil:'load'}); await p.waitForTimeout(700);
 // 触发建索引后检查 id 唯一性
 await p.evaluate(()=>{const i=document.getElementById('q');i.value='测试建索引';i.dispatchEvent(new Event('input',{bubbles:true}));});
 const dup=await p.evaluate(()=>{
   const m={},dups=[]; document.querySelectorAll('[id]').forEach(e=>{ if(m[e.id]) dups.push(e.id); m[e.id]=1; });
   return {total:Object.keys(m).length,dups:dups.slice(0,6),dupN:dups.length};
 });
 console.log('运行后id', JSON.stringify(dup));
 // 常见检索词是否都有结果
 const qs=['静夜思','将进酒','春望','登高','赤壁赋','滕王阁序','陈情表','师说','劝学','岳阳楼记','醉翁亭记','爱莲说','陋室铭','出师表','阿房宫赋','六国论','兰亭集序','归去来兮辞','逍遥游','促织','窦娥冤','长亭送别','三顾茅庐','范进中举','草船借箭','猴王出世','景阳冈','红楼春趣','小圣施威降大圣','滕王阁序','老子','庄子','论语','孟子','屈原','陶渊明','杜甫','李白','苏轼','李清照','辛弃疾','陆游','关汉卿','王实甫','曹雪芹','鲁迅','毛泽东','雨巷','再别康桥','雷雨','哈姆莱特','青莲居士','东坡','稼轩','易安','诗圣','诗仙','报任安书'];
 const empty=[];
 for (const q of qs) {
   const r=await p.evaluate(q=>{const i=document.getElementById('q');i.value=q;i.dispatchEvent(new Event('input',{bubbles:true}));
     return [...document.querySelectorAll('#srPanel .sr-item')].length;},q);
   if(!r) empty.push(q);
 }
 console.log('无结果词:', empty.length?empty:'无');
 // 空查询与失焦
 await p.evaluate(()=>{const i=document.getElementById('q');i.value='';i.dispatchEvent(new Event('input',{bubbles:true}));});
 console.log('清空后隐藏:', await p.evaluate(()=>getComputedStyle(document.getElementById('srPanel')).display));
 console.log('JS错误', errs.length, errs.slice(0,3));
 await b.close();
})();
