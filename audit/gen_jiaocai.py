# -*- coding: utf-8 -*-
"""生成「教材顺序全篇索引」页 jiaocai.html：按小学→初中→高中→近现代、逐学期列出，
每条篇目点击直达对应分页的具体作品卡片。"""
import io, os, re, sys
BASE = r"D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析"
sys.path.insert(0, os.path.join(BASE, "audit"))
from syllabus import XIAOXUE, CHUZHONG, GAOZHONG, JINXIANDAI

PAGELABEL = {
 "xiaowen":"小学文言启蒙","quyuan":"屈原与《楚辞》","shijing":"《诗经》与民间歌谣","zhuzi":"先秦诸子散文",
 "hanprose":"两汉史传与辞赋","taoyuanming":"陶渊明","caocao":"曹操与建安诗人","weijinprose":"魏晋南北朝散文",
 "libai":"李白","dufu":"杜甫","wangwei":"王维","baijuyi":"白居易","lihe":"李贺","shangyin":"李商隐","dumu":"杜牧",
 "tangchu":"初唐四杰与陈子昂","tangsheng":"盛唐山水与边塞诗人","tangwan":"中晚唐诗人","tangguwen":"唐代古文：韩柳",
 "sushi":"苏轼","liqingzhao":"李清照","luyou":"陆游","xinqiji":"辛弃疾","wanganshi":"王安石","fanzhongyan":"范仲淹",
 "ouyangxiu":"欧阳修","songci":"两宋词人","songshi":"宋代诗人","songwen":"宋代散文","yuanqu":"元曲作家",
 "mingqingwen":"明清散文","mingqingshi":"明清诗词","mao":"毛泽东","xiandai":"近现代诗词",
}

WENYAN = set("""守株待兔 精卫填海 王戎不取道旁李 囊萤夜读 铁杵成针 古人谈读书 自相矛盾 杨氏之子
书戴嵩画牛 学弈 两小儿辩日 司马光 伯牙鼓琴 咏雪 陈太丘与友期行 诫子书 狼 穿井得一人 杞人忧天
孙权劝学 陋室铭 河中石兽 答谢中书书 记承天寺夜游 与朱元思书 富贵不能淫 生于忧患死于安乐 愚公移山
周亚夫军细柳 桃花源记 小石潭记 核舟记 北冥有鱼 庄子与惠子游于濠梁之上 虽有嘉肴 大道之行也 马说
岳阳楼记 醉翁亭记 湖心亭看雪 鱼我所欲也 唐雎不辱使命 送东阳马生序 曹刿论战 邹忌讽齐王纳谏 出师表
论语十二章 三峡 爱莲说 劝学 师说 赤壁赋 登泰山记 子路曾皙冉有公西华侍坐 齐桓晋文之事 庖丁解牛
烛之武退秦师 鸿门宴 谏逐客书 与妻书 促织 谏太宗十思疏 答司马谏议书 阿房宫赋 六国论 大学之道
人皆有不忍人之心 老子四章 五石之瓠 兼爱 屈原列传 苏武传 过秦论 五代史伶官传序 陈情表 项脊轩志
兰亭集序 归去来兮辞 种树郭橐驼传 石钟山记""".split())

XIANDAI = set("""少年中国说 我爱这土地 乡愁 你是人间的四月天 我看 梅岭三章 海燕 月夜 萧红墓畔口占
断章 风雨 统一 立在地球边上放号 红烛 峨日朵雪峰之侧 致云雀""".split())

EXTRA_ID = {
 "绝句": ("dufu", "p-dufu-jueju"),
 "月夜": ("xiandai", "p-shenyimo-yueye"),
 "游园": ("yuanqu", "p-youyuan-tang"),
 "风雨": ("xiandai", "p-ludi-fengyuyin"),
 "论语十二章": ("zhuzi", "p-lunyu-xuan"),
 "老子四章": ("zhuzi", "p-laozi-sizhang"),
 "归去来兮辞": ("taoyuanming", "p-guiqulaixici-tym"),
 "临江仙·夜登小阁": ("songci", "p-chenyiyi-linjiangxian"),
}

# 同名词牌按学期区分，避免指向他人作品
GRADE_FIX = {
 ("六年级下", "浣溪沙"): ("sushi", "p-sushi-huanxisha"),
 ("八年级上", "浣溪沙"): ("songci", "p-yanshu-huanxisha"),
 ("九年级下", "浣溪沙"): ("mingqingshi", "p-nalanxingde-huanxisha"),
 ("六年级下", "清平乐"): ("songshi", "p-huangtingjian-qingpingyue"),
 ("八年级上", "渔家傲"): ("liqingzhao", "p-yujiaao-liqingzhao"),
 ("四年级下", "卜算子·咏梅"): ("mao", "p-mao-busuanzi-mei"),
 ("八年级下", "卜算子·咏梅"): ("luyou", "p-busuanzi-luyou"),
}

def norm(x):
    return re.sub(r'[《》（）()、，。·\s ・\-——？！：；【】]', '', x)

# 建立 篇名 -> (page, poemid)
m = {}
for pid in PAGELABEL:
    fn = os.path.join(BASE, "parts", pid + ".html")
    if not os.path.exists(fn): continue
    s = io.open(fn, encoding="utf-8").read()
    for mm in re.finditer(r'<div class="poem" id="([^"]+)">\s*<div class="ptitle">《([^》]+)》', s):
        m.setdefault(norm(mm.group(2)), (pid, mm.group(1)))
for src in ["李白诗词与人生历程系统解析.html", "parts/libai_extra.html"]:
    t = io.open(os.path.join(BASE, src), encoding="utf-8").read()
    for mm in re.finditer(r'<div class="poem" id="([^"]+)">\s*<div class="ptitle">《([^》]+)》', t):
        m.setdefault(norm(mm.group(2)), ("libai", mm.group(1)))
for k, v in EXTRA_ID.items():
    m[norm(k)] = v

BAD = {"月夜忆舍弟", "游园不值"}
keys = list(m.keys())
ONLYHEAD = {"长相思","浣溪沙","清平乐","渔家傲","采桑子","相见欢","如梦令","水调歌头","无题",
            "行香子","破阵子","满江红","定风波","太常引","声声慢","虞美人","鹊桥仙","望海潮","扬州慢","临江仙"}
def find(t, grade=""):
    if (grade, t) in GRADE_FIX: return GRADE_FIX[(grade, t)]
    n = norm(t)
    if n in EXTRA_ID: return EXTRA_ID[n]
    if n in m: return m[n]
    cand = [k for k in keys if k.startswith(n) and len(k) > len(n) and k not in BAD
            and re.match(r'^[【·—（(]', k[len(n):])]
    if not cand and t in ONLYHEAD:
        cand = [k for k in keys if k.startswith(n) and len(k) > len(n)]
    if cand:
        cand.sort(key=len)
        return m[cand[0]]
    return None

def genre(t):
    n = t.strip()
    if n in XIANDAI or n in ("七律·长征","菩萨蛮·大柏地","沁园春·雪","沁园春·长沙","忆秦娥·娄山关","七律·人民解放军占领南京"):
        return "现代诗" if n in XIANDAI else "近现代旧体"
    if n in WENYAN: return "文言文"
    return "古诗词"

def rows(items, grade):
    out = []
    for t in items:
        r = find(t, grade)
        g = genre(t)
        if r:
            page, pid = r
            lab = PAGELABEL.get(page, "李白")
            cell = '<a data-goto="%s::%s">《%s》</a>' % (page, pid, t)
        else:
            lab = "—"
            cell = '《%s》' % t
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (cell, g, lab))
    return "\n".join(out)

def block(grade, items, cnt=[0]):
    return '<h3 class="jc-grade">%s</h3>\n<table class="jc-table">\n<tr><th>篇目（点击直达）</th><th>体裁</th><th>所在篇章</th></tr>\n%s\n</table>\n' % (grade, rows(items, grade))

total = len(XIAOXUE) and sum(len(v) for v in XIAOXUE.values()) + sum(len(v) for v in CHUZHONG.values()) + sum(len(v) for v in GAOZHONG.values())
xx = "\n".join(block(g, v) for g, v in XIAOXUE.items())
cz = "\n".join(block(g, v) for g, v in CHUZHONG.items())
gz = "\n".join(block(g, v) for g, v in GAOZHONG.items())
xd = "\n".join(block(g, v) for g, v in JINXIANDAI.items())

html = """<header class="author-cover">
  <div class="eyebrow">附录 · 教材顺序全篇索引</div>
  <h1>教材全篇顺序索引</h1>
  <div class="sub">按小学、初中、高中课本先后逐册排列 · 点击篇名直达该篇全文与解析</div>
  <div class="badges"><span class="tag tag-book">教材·326篇</span><span class="tag tag-shi">统编版</span></div>
</header>

<div class="sub-toc">
  <b>本页导航</b>
  <a href="#jc-xiaoxue">小学（一上—六下）</a>
  <a href="#jc-chuzhong">初中（七上—九下）</a>
  <a href="#jc-gaozhong">高中（必修—选必）</a>
  <a href="#jc-xiandai">近现代与外国诗</a>
  <a href="#jc-howto">使用说明</a>
</div>

<h2 id="jc-howto"><span class="num">01</span>使用说明</h2>
<div class="info-grid">
  <div class="info-box"><h4>排序依据</h4><p>严格按统编版课本的册次与单元先后排列：小学自一年级上册起至六年级下册，初中自七年级上册至九年级下册，高中按必修上、必修下、选择性必修上中下的顺序。同一篇目在不同年级重复出现时，按出现位置分别列出。</p></div>
  <div class="info-box"><h4>点击直达</h4><p>篇名即链接，点击后自动切换到该作者分页，并滚动定位到该篇的作品卡片，可直接读到原文、创作背景、题材主题、情感脉络、意象与语言、艺术手法、名句释义、文学意义七项解析。标为"—"者说明该篇在本书中按篇目表收录，暂未单列细读。</p></div>
</div>

<h2 id="jc-xiaoxue"><span class="num">02</span>小学（一年级上—六年级下）</h2>
%s
<h2 id="jc-chuzhong"><span class="num">03</span>初中（七年级上—九年级下）</h2>
%s
<h2 id="jc-gaozhong"><span class="num">04</span>高中（必修与选择性必修）</h2>
%s
<h2 id="jc-xiandai"><span class="num">05</span>近现代旧体、现代诗与外国诗</h2>
%s
<div class="aside"><b>说明：</b>本索引是全书的总入口。若想按作者系统研读，请回「教材篇目总索引」页或直接使用左侧目录；若想按文学史时序通读，请从首页的"全书结构地图"进入。</div>
""" % (xx, cz, gz, xd)

io.open(os.path.join(BASE, "parts", "jiaocai.html"), "w", encoding="utf-8").write(html)
print("已生成 parts/jiaocai.html")
# 统计直达率
ALL = {}
for d in (XIAOXUE, CHUZHONG, GAOZHONG, JINXIANDAI):
    for g, v in d.items():
        for t in v: ALL.setdefault(t, g)
hit = 0
miss = []
for d in (XIAOXUE, CHUZHONG, GAOZHONG, JINXIANDAI):
    for g, v in d.items():
        for t in v:
            if find(t, g): hit += 1
            else: miss.append((g, t))
print("教材条目 %d，可直达 %d，未直达 %d" % (hit + len(miss), hit, len(miss)))
print("未直达：", miss)
