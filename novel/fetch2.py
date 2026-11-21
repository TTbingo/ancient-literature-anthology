# -*- coding: utf-8 -*-
import io,os,time,urllib.parse,urllib.request
T={
 "huoban":"夢溪筆談/卷18",
 "chenshe":"史記/卷048",
 "dedao":"孟子/公孫丑下",
 "caochuan":"三國演義/第046回",
 "jingyang":"水滸傳 (100回本)/第023回",
 "houwang":"西遊記/第001回",
 "chunqu":"紅樓夢/第070回",
 "xiaosheng":"西遊記/第006回",
}
os.makedirs("tmp",exist_ok=True)
for k,t in T.items():
    fn="tmp/%s.raw"%k
    if os.path.exists(fn) and os.path.getsize(fn)>500:
        print("skip",k,os.path.getsize(fn)); continue
    url="https://zh.wikisource.org/w/index.php?title=%s&action=raw"%urllib.parse.quote(t.replace(" ","_"))
    for attempt in range(3):
        try:
            r=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 study-build"})
            s=urllib.request.urlopen(r,timeout=40).read().decode("utf-8","ignore")
            io.open(fn,"w",encoding="utf-8").write(s)
            print("ok",k,len(s)); break
        except Exception as e:
            print("retry",k,attempt,e); time.sleep(4)
    time.sleep(2.0)
