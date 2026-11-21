# -*- coding: utf-8 -*-
"""重排附录总索引：篇名/作者名直达成链接，删去冗余列，按内容定宽。"""
import io, json, os, re, sys

BASE = r"D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析"
SRC = os.path.join(BASE, "parts", "indexall.html")
POEMS = json.load(io.open(os.path.join(BASE, "audit", "poems.json"), encoding="utf-8"))
AUTH = json.load(io.open(os.path.join(BASE, "audit", "authors.json"), encoding="utf-8"))

def clean(t):
    t = t.replace("《", "").replace("》", "").replace("〈", "").replace("〉", "")
    t = re.sub(r"[（(][^）)]*[）)]", "", t)
    t = t.replace("·", "").replace("・", "").replace("・", "").replace(" ", "")
    t = t.replace("并序", "").replace("节选", "")
    return t

def find_poem(page, title):
    key = clean(title)
    cands = [(pid, clean(t.split(" 教材")[0])) for pid, t in POEMS.get(page, [])]
    for pid, k in cands:
        if k == key:
            return pid
    for pid, k in cands:
        if k.startswith(key):
            return pid
    for pid, k in cands:
        if key.startswith(k) and len(k) >= 2:
            return pid
    for pid, k in cands:
        if key and (key in k or k in key) and len(key) >= 2:
            return pid
    return None

MISS = []
def poem_link(page, title, note=""):
    pid = find_poem(page, title)
    if not pid:
        MISS.append((page, title))
        return "%s%s" % (title, note)
    return '<span class="tt"><a data-goto="%s::%s" style="cursor:pointer">%s</a>%s</span>' % (page, pid, title, note)

def find_author(page, name):
    key = re.sub(r"[（(][^）)]*[）)]", "", name).strip()
    for aid, an in AUTH.get(page, []):
        if key in an or key in an.replace("《", "").replace("》", ""):
            return aid
    for aid, an in AUTH.get(page, []):
        if clean(key) and clean(key) in clean(an):
            return aid
    return None

MISSA = []
def author_link(page, name):
    aid = find_author(page, name)
    if not aid:
        MISSA.append((page, name))
        return name
    return '<a data-goto="%s::%s" style="cursor:pointer">%s</a>' % (page, aid, name)

def cell(items, page, sep="、"):
    out = []
    for it in items:
        if isinstance(it, tuple):
            out.append(poem_link(page, it[0], it[1]))
        elif it == "—":
            out.append("—")
        else:
            out.append(poem_link(page, it))
    return sep.join(out)

# ---------------- 01 专页 ----------------
XW = ["守株待兔", "精卫填海", "王戎不取道旁李", "囊萤夜读", "铁杵成针", "古人谈读书",
      "自相矛盾", "杨氏之子", "书戴嵩画牛", "学弈", "两小儿辩日"]
XD = ["少年中国说", "菩萨蛮·大柏地", "我爱这土地", "你是人间的四月天", "我看", "断章",
      "梅岭三章", "萧红墓畔口占", "统一", "海燕", "立在地球边上放号", "红烛",
      "峨日朵雪峰之侧", "致云雀"]

# ---------------- 02 重点作家 ----------------
MING = [
 ("李白", "libai",
  ["古朗月行", "静夜思", "赠汪伦", "望庐山瀑布", "夜宿山寺", "望天门山", "早发白帝城", "黄鹤楼送孟浩然", "独坐敬亭山"],
  ["闻王昌龄左迁龙标", "峨眉山月歌", "春夜洛城闻笛", "渡荆门送别", "送友人", "行路难", "月下独酌"],
  ["蜀道难", "将进酒", "梦游天姥吟留别"]),
 ("杜甫", "dufu",
  ["绝句二首", "春夜喜雨", "闻官军收河南河北"],
  ["望岳", "春望", "石壕吏", "茅屋为秋风所破歌"],
  ["登高", "蜀相", "客至", "登岳阳楼"]),
 ("苏轼", "sushi",
  ["饮湖上初晴后雨", "赠刘景文", "惠崇春江晚景", "题西林壁", "六月二十七日望湖楼醉书", "浣溪沙"],
  ["记承天寺夜游", "水调歌头", "江城子·密州出猎", "定风波"],
  ["念奴娇·赤壁怀古", "赤壁赋", "江城子·乙卯正月二十日夜记梦"]),
 ("白居易", "baijuyi",
  ["池上", "赋得古原草送别", "忆江南", "大林寺桃花", "暮江吟"],
  ["钱塘湖春行", "卖炭翁"],
  ["琵琶行并序"]),
 ("王维", "wangwei",
  ["画", "九月九日忆山东兄弟", "鹿柴", "送元二使安西", "鸟鸣涧", "山居秋暝"],
  ["竹里馆", "使至塞上"],
  ["山居秋暝"]),
 ("辛弃疾", "xinqiji",
  ["清平乐·村居", "西江月·夜行黄沙道中"],
  ["丑奴儿", "破阵子", "南乡子", "太常引"],
  ["永遇乐·京口北固亭怀古"]),
 ("陆游", "luyou",
  ["示儿", "秋夜将晓出篱门迎凉有感"],
  ["游山西村", "十一月四日风雨大作", "卜算子·咏梅"],
  ["书愤", "临安春雨初霁"]),
 ("李清照", "liqingzhao",
  ["夏日绝句"],
  ["如梦令", "渔家傲"],
  ["声声慢"]),
 ("王安石", "wanganshi",
  ["梅花", "元日", "书湖阴先生壁", "泊船瓜洲"],
  ["登飞来峰"],
  ["桂枝香·金陵怀古", "答司马谏议书"]),
 ("范仲淹", "fanzhongyan",
  ["江上渔者"],
  ["岳阳楼记", "渔家傲·秋思"],
  ["—"]),
 ("欧阳修", "ouyangxiu",
  ["—"],
  ["卖油翁", "醉翁亭记", "采桑子"],
  ["五代史伶官传序"]),
 ("李商隐", "shangyin",
  ["嫦娥"],
  ["夜雨寄北", "贾生", "无题"],
  ["锦瑟"]),
 ("杜牧", "dumu",
  ["山行", "清明", "江南春"],
  ["赤壁", "泊秦淮"],
  ["阿房宫赋"]),
 ("李贺", "lihe",
  ["马诗"],
  ["雁门太守行"],
  ["李凭箜篌引"]),
 ("陶渊明", "taoyuanming",
  ["—"],
  ["饮酒", "桃花源记"],
  ["归园田居", "归去来兮辞"]),
 ("屈原", "quyuan",
  ["—"],
  ["—"],
  [("离骚", "（节选）"), "国殇"]),
 ("毛泽东", "mao",
  ["七律·长征", "卜算子·咏梅"],
  ["—"],
  ["沁园春·长沙"]),
]

# ---------------- 03 合篇 ----------------
GROUPS = [
 ("诗经与民间歌谣", "shijing", ["《诗经》", "汉乐府", "北朝民歌", "《古诗十九首》"]),
 ("先秦诸子散文", "zhuzi", ["孔子", "孟子", "庄子", "荀子", "老子", "墨子", "列子", "吕氏春秋", "礼记"]),
 ("两汉史传与辞赋", "hanprose", ["司马迁", "班固", "贾谊", "李斯", "刘向", "《左传》", "汉赋", "魏征（唐，附列）"]),
 ("曹操与建安诗人", "caocao", ["曹操", "曹植", "刘桢", "王绩"]),
 ("魏晋南北朝散文", "weijinprose", ["郦道元", "陶弘景", "吴均", "王羲之", "刘义庆", "诸葛亮", "李密", "鲍照"]),
 ("初唐四杰与陈子昂", "tangchu", ["王勃", "杨炯", "卢照邻", "骆宾王", "陈子昂"]),
 ("盛唐山水与边塞", "tangsheng", ["孟浩然", "高适", "岑参", "王昌龄", "王之涣", "崔颢", "常建", "刘长卿", "韦应物", "王翰", "李益"]),
 ("中晚唐诗人", "tangwan", ["刘禹锡", "柳宗元", "韩愈", "温庭筠", "罗隐", "贾岛", "卢纶", "张继", "张志和", "胡令能", "李绅", "王建", "韩翃", "虞世南", "林杰", "袁枚", "高鼎", "查慎行"]),
 ("唐代古文：韩柳", "tangguwen", ["韩愈", "柳宗元"]),
 ("两宋词人", "songci", ["柳永", "晏殊", "秦观", "周邦彦", "姜夔", "张孝祥", "刘克庄", "朱敦儒", "陈与义", "李煜", "张若虚（唐，附列）"]),
 ("宋代诗人", "songshi", ["杨万里", "范成大", "叶绍翁", "曾几", "翁卷", "雷震", "卢钺", "林升", "朱熹", "赵师秀", "黄庭坚"]),
 ("宋代散文", "songwen", ["苏洵", "司马光", "沈括", "周敦颐", "宋濂", "苏辙", "曾巩"]),
 ("元曲作家", "yuanqu", ["马致远", "张养浩", "王磐", "关汉卿", "王实甫", "汤显祖（明，附列）"]),
 ("明清散文", "mingqingwen", ["归有光", "张岱", "蒲松龄", "姚鼐", "纪昀", "魏学洢", "林觉民", "方苞"]),
 ("明清诗词", "mingqingshi", ["于谦", "郑燮", "龚自珍", "纳兰性德", "唐寅", "王冕", "夏完淳", "秋瑾", "谭嗣同"]),
]

# ---------------- 04 课外延伸 ----------------
EXTEND = [
 ("libai", "李白专篇", "李白", ["宣州谢朓楼饯别校书叔云"]),
 ("quyuan", "屈原与楚辞", "屈原", ["湘夫人"]),
 ("shijing", "诗经与民间歌谣", "《古诗十九首》", [("涉江采芙蓉", "（此篇为正选，附列备查）")]),
 ("taoyuanming", "陶渊明", "陶渊明", ["杂诗其一"]),
 ("dufu", "杜甫", "杜甫", [("新婚别", "（三别之一）")]),
 ("tangchu", "初唐四杰", ["卢照邻", "骆宾王"], [("长安古意", "（节选）"), "在狱咏蝉"]),
 ("tangsheng", "盛唐山水与边塞", ["孟浩然", "高适", "王昌龄", "王之涣"],
  ["望洞庭湖赠张丞相", ("燕歌行", "（节选）"), "采莲曲", ("凉州词", "（黄河远上）")]),
 ("tangwan", "中晚唐诗人", "温庭筠", [("菩萨蛮", "（小山重叠金明灭）")]),
 ("tangguwen", "唐代古文：韩柳", ["韩愈", "柳宗元"], [("祭十二郎文", "（节选）"), "登柳州城楼"]),
 ("ouyangxiu", "欧阳修", "欧阳修", [("踏莎行", "（候馆梅残）")]),
 ("liqingzhao", "李清照", "李清照", ["一剪梅", "武陵春"]),
 ("xinqiji", "辛弃疾", "辛弃疾", ["菩萨蛮·书江西造口壁", "青玉案·元夕"]),
 ("songwen", "宋代散文", "曾巩", ["墨池记"]),
 ("songci", "两宋词人", "张若虚", [("春江花月夜", "（正选，附列备查）")]),
 ("songshi", "宋代诗人", "黄庭坚", [("登快阁", "（正选，附列备查）")]),
 ("yuanqu", "元曲作家", "汤显祖", [("游园【皂罗袍】", "（正选，附列备查）")]),
 ("mingqingwen", "明清散文", "方苞", [("狱中杂记", "（节选）")]),
 ("mao", "毛泽东", "毛泽东", ["沁园春·雪", "忆秦娥·娄山关", "七律·人民解放军占领南京"]),
]

def aus(cellv):
    if isinstance(cellv, list):
        return "、".join('<span class="tt">%s</span>' % n for n in cellv)
    return cellv

# ---------------- 06 小说 ----------------
NOVEL = [
 ("五下 · 5", "草船借箭", "p-sanguo-caochuan", "罗贯中《三国演义》第四十六回", "历史演义"),
 ("五下 · 6", "景阳冈", "p-shuihu-jingyang", "施耐庵《水浒传》第二十三回", "英雄传奇"),
 ("五下 · 7", "猴王出世", "p-xiyou-houwang", "吴承恩《西游记》第一回", "神魔小说"),
 ("五下 · 8", "红楼春趣", "p-honglou-chunqu", "曹雪芹《红楼梦》第七十回", "世情小说"),
 ("七上 · 21", "小圣施威降大圣", "p-xiyou-xiaosheng", "吴承恩《西游记》第六回", "神魔小说"),
 ("九上 · 22", "智取生辰纲", "p-shuihu-shengchengang", "施耐庵《水浒传》第十六回", "英雄传奇"),
 ("九上 · 23", "范进中举", "p-rulin-fanjin", "吴敬梓《儒林外史》第三回", "讽刺小说"),
 ("九上 · 24", "三顾茅庐", "p-sanguo-sangumaolu", "罗贯中《三国演义》第三十八回", "历史演义"),
 ("九上 · 25", "刘姥姥进大观园", "p-honglou-liulaolao", "曹雪芹《红楼梦》第四十回", "世情小说"),
]

old = io.open(SRC, encoding="utf-8").read()
# 保留第 05 节原文
m05 = re.search(r'(<h2 id="idx-xuanxiu".*?)(?=<h2 id="idx-novel")', old, re.S)
sec05 = m05.group(1)

L = []
L.append('''<header class="author-cover">
  <div class="eyebrow">附录 · 速查工具</div>
  <h1>教材篇目总索引</h1>
  <div class="sub">按作者汇总统编版小学、初中、高中语文教材古代作品篇目 · 点击篇名或作者名直达对应内容</div>
</header>

<div class="lead">
本索引把全书涉及的教材篇目按作者汇总，便于按图索骥。表中<b>作者名</b>可直达其专页或人物条目，<b>篇名</b>可直达该篇原文与解析。教材选篇在不同印次、地区间略有出入，此处依统编版常见目录整理，作学习梳理之用，不作版本定论。
</div>

<h2 id="idx-new"><span class="num">01</span>专页速查：小学文言与近现代诗词</h2>
<div class="aside"><b>提示：</b>若想按<b>课本册次</b>（小学一上→高中选必下）逐篇查阅并点击直达，请用附录中的<a data-goto="jiaocai" style="cursor:pointer">「教材顺序全篇索引」</a>页；本页则按<b>作者与学段</b>速查，篇名均可点击直达。</div>
<div class="tw">
<table class="t-new">
<colgroup><col style="width:158px"><col></colgroup>
  <tr><th>专页</th><th>收录内容</th></tr>
''')
L.append('  <tr><td><a data-goto="xiaowen" style="cursor:pointer">小学文言启蒙</a></td><td>%s（共11篇，均附完整原文）</td></tr>\n' % cell(XW, "xiaowen"))
L.append('  <tr><td><a data-goto="xiandai" style="cursor:pointer">近现代诗词</a></td><td>%s（共14篇，外国诗注译者）</td></tr>\n' % cell(XD, "xiandai"))
L.append('''</table>
</div>

<h2 id="idx-ming"><span class="num">02</span>重点作家篇目速查</h2>
<div class="aside"><b>用法：</b>十八位重点作家各有专页，点<b>作者名</b>进入该页通读生平与全部篇目；点<b>篇名</b>直接跳到那一首的原文与解析。同一篇目跨学段重出者，两处链接指向同一篇。</div>
<div class="tw">
<table class="t-ming">
<colgroup><col style="width:86px"><col style="width:34%"><col style="width:33%"><col></colgroup>
  <tr><th>作者</th><th>小学</th><th>初中</th><th>高中</th></tr>
''')
for name, page, a, b, c in MING:
    L.append('  <tr><td><a data-goto="%s" style="cursor:pointer"><b>%s</b></a></td><td>%s</td><td>%s</td><td>%s</td></tr>\n'
             % (page, name, cell(a, page), cell(b, page), cell(c, page)))
L.append('''</table>
</div>

<h2 id="idx-groups"><span class="num">03</span>合篇作者分组速查</h2>
<div class="aside"><b>用法：</b>合篇页一位作者一节，点<b>作者名</b>即跳到该页对应的人物条目与篇目清单。</div>
<div class="tw">
<table class="t-groups">
<colgroup><col style="width:182px"><col></colgroup>
  <tr><th>分页</th><th>涵盖作者（点击直达）</th></tr>
''')
for label, page, names in GROUPS:
    L.append('  <tr><td><a data-goto="%s" style="cursor:pointer">%s</a></td><td>%s</td></tr>\n'
             % (page, label, "、".join(author_link(page, n) for n in names)))
L.append('''</table>
</div>

<h2 id="idx-extend"><span class="num">04</span>课外延伸篇目速查</h2>
<p>以下篇目不在统编教材正选目录内，属常见课外延伸或不同版本选篇。全书已为每篇补全原文与七维度细读，点击<b>篇名</b>可直达该篇。</p>
<div class="tw">
<table class="t-extend">
<colgroup><col style="width:176px"><col style="width:150px"><col></colgroup>
  <tr><th>所在分页</th><th>作者</th><th>延伸篇目（点击直达）</th></tr>
''')
for page, label, author, items in EXTEND:
    L.append('  <tr><td><a data-goto="%s" style="cursor:pointer">%s</a></td><td>%s</td><td>%s</td></tr>\n'
             % (page, label, aus(author), cell(items, page)))
L.append('</table>\n</div>\n\n')
L.append(sec05)
L.append('''<h2 id="idx-novel"><span class="num">06</span>古代白话小说九篇（五年级下 · 七年级上 · 九年级上）</h2>
<div class="aside"><b>说明：</b>白话小说在教材里分三段出现：五年级下第二单元是"古典名著之旅"，四篇为改写或节选，重在初见；七年级上《小圣施威降大圣》进入原文的斗法想象；九年级上第六单元才是按长篇小说来读。九篇分属五部书，覆盖史、侠、幻、讽、情五条路。教材均取节选，故另设<a data-goto="novel" style="cursor:pointer">「古代白话小说」</a>专页，按原文对应段落收录并附七维度解析；节选之外的上下文在"创作背景"中补足。</div>
<div class="tw tw-fit">
<table class="t-novel">
  <tr><th>册次 · 课次</th><th>篇目（点击直达）</th><th>作者与出处</th><th>类型</th></tr>
''')
for grade, title, pid, src, kind in NOVEL:
    L.append('  <tr><td>%s</td><td><a data-goto="novel::%s" style="cursor:pointer">《%s》</a></td><td>%s</td><td>%s</td></tr>\n'
             % (grade, pid, title, src, kind))
L.append('''</table>
</div>

<div class="aside"><b>使用提示：</b>本表用于快速定位作者所在分页与学段分布。若需某篇作品的详细解析（创作背景、情感脉络、艺术手法等），请点击对应篇名进入细读。教材篇目以各校实际使用版本为准。凡标注"节选"者，均为原作篇幅过长而截取关键段落，已在对应卡片中注明节选范围；教材本身为全文的作品，全书一律呈现全文。</div>
''')

io.open(SRC, "w", encoding="utf-8").write("".join(L))
print("写出", SRC, os.path.getsize(SRC))
print("未匹配篇名:", len(MISS), MISS)
print("未匹配作者:", len(MISSA), MISSA)
