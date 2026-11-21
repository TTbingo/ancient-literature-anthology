const { chromium } = require('playwright');
(async () => {
  const b=await chromium.launch(); const p=await b.newPage();
  const url='file:///D:/workbuddy%E7%9A%84%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/2026-11-20-18-22-04/%E6%9D%8E%E7%99%BD%E8%AF%97%E8%AF%8D%E8%A7%A3%E6%9E%90/%E7%BB%9F%E7%BC%96%E6%95%99%E6%9D%90%E5%8F%A4%E4%BB%A3%E4%BD%9C%E5%AE%B6%E6%96%87%E5%AD%A6%E9%9B%86%E6%88%90.html';
  const cases=[['四年级下','卜算子·咏梅'],['八年级下','卜算子·咏梅'],['八年级上','渔家傲'],['九年级下','渔家傲·秋思'],['六年级下','浣溪沙'],['八年级上','浣溪沙'],['九年级下','浣溪沙'],['六年级下','清平乐']];
  await p.goto(url+'#jiaocai',{waitUntil:'load'}); await p.waitForTimeout(300);
  const all=await p.evaluate(()=>{
    const out=[];
    document.querySelectorAll('#jiaocai table.jc-table').forEach(tb=>{
      let h=tb.previousElementSibling;
      while(h && h.tagName!=='H3') h=h.previousElementSibling;
      const grade=h?h.textContent.trim():'?';
      tb.querySelectorAll('tr').forEach(tr=>{
        const a=tr.querySelector('a[data-goto]');
        if(a) out.push([grade,a.textContent.trim(),a.getAttribute('data-goto')]);
      });
    });
    return out;
  });
  console.log('索引条目总数:',all.length);
  for(const [g,n] of cases){
    const hit=all.filter(x=>x[0]===g && x[1].includes(n));
    console.log(g,n,'→',hit.length?hit.map(x=>x[2]).join(' | '):'未找到');
  }
  await b.close();
})();
