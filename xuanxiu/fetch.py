# -*- coding: utf-8 -*-
import io,os,re,sys,time,urllib.parse,urllib.request

OUT="src"
TITLES={
 "laozi":"道德經",
 "zhuangzi_rensheng":"莊子/人間世",
 "zhuangzi_yingdiwang":"莊子/應帝王",
 "zhuangzi_zhile":"莊子/至樂",
 "huainanzi_yuandao":"淮南子/原道訓",
 "huainanzi_xiuwu":"淮南子/修務訓",
 "jijuejiaoshu":"與山巨源絕交書",
 "maoshixu":"毛詩序",
 "wenxin_mingzhi":"文心雕龍/明詩",
 "shipinxu":"詩品序",
 "yuanyuan":"原詩",
 "yuyuanjiushu":"與元九書",
 "renjiancihua":"人間詞話",
 "lianpolinxiangru":"史記/卷081",
 "liuyizhuan":"柳毅傳",
 "sanguo43":"三國演義/第043回",
 "rulinnwaishi16":"儒林外史/第016回",
 "rulinnwaishi17":"儒林外史/第017回",
 "huanggangzhulou":"黃岡竹樓記",
 "linquangaozhi":"林泉高致",
 "xiake_ma":  "徐霞客遊記/楚遊日記",
 "dongjingmenghualu2":"東京夢華錄/卷二",
 "dongjingmenghualu5":"東京夢華錄/卷五",
 "dijingjingwulue2":"帝京景物略/卷二",
 "gaozuhuanxiang":"般涉調·哨遍·高祖還鄉",
 "shirunze":"醒世恆言/第18卷",
 "liujingting":"柳敬亭傳",
 "malingzhuan":"馬伶傳",
}
def strip(html):
    m=re.search(r'<div[^>]*class="[^"]*mw-parser-output[^"]*"[^>]*>',html)
    if not m: return None
    seg=html[m.end():]
    cut=seg.find('<div class="printfooter"')
    if cut>0: seg=seg[:cut]
    seg=re.sub(r'<style.*?</style>','',seg,flags=re.S)
    seg=re.sub(r'<script.*?</script>','',seg,flags=re.S)
    seg=re.sub(r'<table.*?</table>','',seg,flags=re.S)
    seg=re.sub(r'<sup.*?</sup>','',seg,flags=re.S)
    seg=re.sub(r'<(p|div|br|li)[^>]*>','\n',seg)
    seg=re.sub(r'<[^>]+>','',seg)
    seg=seg.replace('&nbsp;',' ').replace('&amp;','&').replace('&quot;','"').replace('&lt;','<').replace('&gt;','>')
    lines=[re.sub(r'[ \t]+',' ',l).strip() for l in seg.split('\n')]
    lines=[l for l in lines if l and not l.startswith('姊妹计划')]
    return '\n'.join(lines)

for k,t in TITLES.items():
    fn=os.path.join(OUT,k+'.txt')
    if os.path.exists(fn): continue
    url="https://zh.wikisource.org/zh-hans/"+urllib.parse.quote(t.replace(' ','_'))
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 study-build'})
        html=urllib.request.urlopen(req,timeout=30).read().decode('utf-8','ignore')
        txt=strip(html)
        if not txt:
            print("MISS",k,t); continue
        io.open(fn,'w',encoding='utf-8').write(txt)
        print("OK  %-22s %6d  %s"%(k,len(txt),txt[:40].replace('\n','|')))
    except Exception as e:
        print("ERR ",k,t,type(e).__name__)
    time.sleep(0.7)
