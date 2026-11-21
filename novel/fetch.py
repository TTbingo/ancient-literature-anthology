# -*- coding: utf-8 -*-
import io,os,re,urllib.parse,urllib.request

OUT="src"
TITLES={
 "shuihu16":"水滸傳/第016回",
 "rulin3":"儒林外史/第003回",
 "sanguo37":"三國演義/第037回",
 "sanguo38":"三國演義/第038回",
 "honglou40":"紅樓夢/第040回",
}
def strip(html):
    m=re.search(r'<div[^>]*class="[^"]*mw-parser-output[^"]*"[^>]*>',html)
    if not m: return None
    seg=html[m.end():]
    cut=seg.find('<div class="printfooter"')
    if cut>0: seg=seg[:cut]
    for pat in (r'<style.*?</style>',r'<script.*?</script>',r'<table.*?</table>',r'<sup.*?</sup>'):
        seg=re.sub(pat,'',seg,flags=re.S)
    seg=re.sub(r'<(p|div|br|li)[^>]*>','\n',seg)
    seg=re.sub(r'<[^>]+>','',seg)
    for a,b in (('&nbsp;',' '),('&amp;','&'),('&quot;','"'),('&lt;','<'),('&gt;','>')):
        seg=seg.replace(a,b)
    lines=[re.sub(r'[ \t]+',' ',l).strip() for l in seg.split('\n')]
    lines=[l for l in lines if l and not l.startswith('姊妹计划')]
    return '\n'.join(lines)

for k,t in TITLES.items():
    fn=os.path.join(OUT,k+'.txt')
    if os.path.exists(fn) and os.path.getsize(fn)>1000:
        print('skip',k,os.path.getsize(fn)); continue
    url="https://zh.wikisource.org/zh-hans/"+urllib.parse.quote(t.replace(' ','_'))
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 study-build'})
        html=urllib.request.urlopen(req,timeout=40).read().decode('utf-8','ignore')
        txt=strip(html)
        if not txt: print('EMPTY',k); continue
        io.open(fn,'w',encoding='utf-8').write(txt)
        print('ok',k,len(txt))
    except Exception as e:
        print('FAIL',k,e)
