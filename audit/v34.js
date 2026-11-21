const { chromium } = require('playwright');
const path=require('path');
(async()=>{
 const file='file:///'+path.resolve('D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析/统编教材古代作家文学集成.html').replace(/\\/g,'/');
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1440,height:950}});
 await p.goto(file,{waitUntil:'load'}); await p.waitForTimeout(700);
 // 索引总量
 console.log('索引条目', await p.evaluate(()=>{
   let n=0, kind={};
   document.querySelectorAll('.prail a[data-jump]').forEach(a=>{n++;const k=a.getAttribute('data-kind');kind[k]=(kind[k]||0)+1;});
   return {n,kind,pages:document.querySelectorAll('section.page').length};
 }));
 const qs=['三顾茅庐','范进中举','长亭送别','活板','陈涉世家','得道多助','猴王出世','草船借箭','景阳冈','红楼春趣','小圣施威降大圣','滕王阁序','老子','庄子','淮南子','毛诗序','人间词话','柳毅传','匡超人','麻叶洞天','施润泽','柳敬亭','马伶','高祖还乡','山水训','黄冈竹楼记','廉颇蔺相如','与山巨源绝交书','与元九书','诗论三则','市井笔记','论语','井冈山','报任安书','稼说送张琥','赤壁赋','静夜思','登高','将进酒','使至塞上','出师表','岳阳楼记','醉翁亭记','爱莲说','陋室铭','劝学','师说','阿房宫赋','六国论','陈情表','兰亭集序','归去来兮辞','逍遥游','促织','窦娥冤','雷雨','哈姆莱特','沁园春','雨巷','再别康桥'];
 const rows=[];
 for (const q of qs) {
   const r=await p.evaluate(q=>{
     const i=document.getElementById('q');
     i.focus(); i.value=q; i.dispatchEvent(new Event('input',{bubbles:true}));
     const items=[...document.querySelectorAll('#srPanel .sr-item')].slice(0,4).map(el=>el.textContent.trim());
     const foot=document.querySelector('#srPanel .sr-foot')?.textContent||'';
     const empty=!!document.querySelector('#srPanel .sr-empty');
     return {items, foot, empty};
   }, q);
   rows.push([q, r]);
 }
 for (const [q,r] of rows) {
   const flag = (r.empty||r.items.length===0)?'【空】':'';
   console.log(flag+q+' → 共'+(r.foot.match(/共 (\d+) 条/)||[,'?'])[1]+' | '+r.items.slice(0,2).join(' ｜ '));
 }
 await b.close();
})();
