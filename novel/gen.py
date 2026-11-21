# -*- coding: utf-8 -*-
"""生成 parts/novel.html：古代白话小说九篇（五下名著单元 · 七上 · 九上）。"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'xuanxiu'))
import gen as XG          # xuanxiu/gen.py：verse_html、dims_html
sys.path.insert(0, HERE)  # 之后再让 data* 能找到 wt
import data1 as D1
import data2 as D2
import data3 as D3

def author_html(a):
    grid = "".join('    <div class="m"><b>%s</b>%s</div>\n' % (k, v) for k, v in a["grid"])
    paras = "".join("  <p>%s</p>\n" % p for p in a["ps"])
    toc = ""
    if a.get("toc"):
        toc = '  <div class="cardtoc"><b>本页细读：</b>%s</div>\n' % "".join(
            '<a href="#%s">%s</a>' % (i, t) for i, t in a["toc"])
    if a.get("教材"):
        paras += "  <p><b>教材篇目：</b>%s</p>\n" % a["教材"]
    if a.get("learn"):
        paras += "  <p><b>学习要点：</b>%s</p>\n" % a["learn"]
    return ('<div class="author-card" id="%s">\n'
            '  <h3>%s <span class="tag %s">%s</span></h3>\n'
            '  <div class="mini-grid">\n%s  </div>\n%s%s</div>\n'
            % (a["id"], a["name"], a["tag"][0], a["tag"][1], grid, paras, toc))

def piece_html(p):
    note = '  <div class="note">%s</div>\n' % p["note"] if p.get("note") else ""
    return ('<div class="poem" id="%s">\n'
            '  <div class="ptitle">%s <span class="tag %s">%s</span></div>\n'
            '  <div class="pmeta">%s</div>\n'
            '  <div class="verse">%s</div>\n%s%s\n</div>\n'
            % (p["id"], p["title"], p["tag"][0], p["tag"][1], p["meta"],
               XG.verse_html(p["paras"]), XG.dims_html(p["dims"]), note))

UNITS = [
    ("nv-1", "施耐庵：景阳冈 · 智取生辰纲", D1.A_SHINAIAN, [D3.P_JINGYANG, D1.P_SHUIHU]),
    ("nv-2", "罗贯中：草船借箭 · 三顾茅庐", D2.A_LUOGUANZHONG, [D3.P_CAOCHUAN, D2.P_SANGUO]),
    ("nv-3", "吴承恩：猴王出世 · 小圣施威降大圣", D3.A_WUCHENGEN, [D3.P_HOUWANG, D3.P_XIAOSHENG]),
    ("nv-4", "吴敬梓：范进中举", D1.A_WUJINGZI, [D1.P_RULIN]),
    ("nv-5", "曹雪芹：红楼春趣 · 刘姥姥进大观园", D2.A_CAOXUEQIN, [D3.P_CHUNQU, D2.P_HONGLOU]),
]

def build():
    out = []
    out.append("""<header class="author-cover">
  <div class="eyebrow">五下 · 七上 · 九上 · 名著与小说单元</div>
  <h1>古代白话小说</h1>
  <div class="sub">《三国演义》《水浒传》《西游记》《儒林外史》《红楼梦》 · 九篇节选细读</div>
  <div class="badges">
    <span class="tag tag-book">教材·小学至初中</span>
    <span class="tag tag-shi">史实</span>
    <span class="tag tag-chuan">传说</span>
    <span class="tag tag-guan">学界观点</span>
  </div>
</header>

<div class="sub-toc">
  <b>本篇目录</b>
  <a href="#nv-intro">白话小说怎么来的</a>
  <a href="#nv-read">九篇怎么读</a>
  <a href="#nv-1">施耐庵</a>
  <a href="#nv-2">罗贯中</a>
  <a href="#nv-3">吴承恩</a>
  <a href="#nv-4">吴敬梓</a>
  <a href="#nv-5">曹雪芹</a>
  <a href="#nv-learn">总学习要点</a>
</div>

<div class="lead">
中国古代小说有两条脉：一条是文言，从六朝志怪、唐传奇到《聊斋志异》，写给读书人看；一条是白话，从唐宋“说话”人的底本、元代的平话，到元末明初的章回体，说给市井听。本页收的九篇，正走在这条白话的脉上——<b>《三国演义》《水浒传》成于元末明初，《西游记》成于明代中叶，《儒林外史》《红楼梦》成于清代中期</b>，前后四百年，从“讲故事”走到了“写人心”。九篇分属三个学段：五年级下名著单元的《草船借箭》《景阳冈》《猴王出世》《红楼春趣》是初见，七年级上的《小圣施威降大圣》是斗法的想象，九年级上第六单元的《智取生辰纲》《范进中举》《三顾茅庐》《刘姥姥进大观园》才是按“长篇小说”来读。教材所取都是节选或改写，本页按原文对应段落收录，起讫在篇首注明。
</div>

<h2 id="nv-intro"><span class="num">01</span>白话小说怎么来的：从“说话”到“章回”</h2>
<p>宋代汴梁、临安的瓦舍勾栏里，有专门“说话”的艺人，分小说、讲史、说经等家数。他们把故事写成底本，叫“话本”；话本流传久了，有人把它们连缀、扩充，就成了长篇。元末明初，<b>章回体</b>定型：全书分回，每回有对仗的回目，回末留一句“且听下回分解”，这正是当年说话人收钱歇场的遗迹。</p>
<div class="info-grid">
  <div class="info-box"><h4>五个里程碑</h4><p><b>《三国演义》</b>以史为骨、以文为肉，定型了中国人对三国人物的想象；<b>《水浒传》</b>把“官逼民反”写成因果链，人物语言一人一副嗓子；<b>《西游记》</b>以神魔写人间，想象有严格的逻辑；<b>《儒林外史》</b>首创长篇讽刺，冷眼看士林；<b>《红楼梦》</b>把世情小说推到顶点，以一家之盛衰写一代之幻灭。五部书分别擅长史、侠、幻、讽、情。</p></div>
  <div class="info-box"><h4>与五册的衔接</h4><p>五年级下第二单元是“古典名著之旅”，四篇都是改写或节选，重在“初见”；七年级上《小圣施威降大圣》进入原文的斗法想象；九年级上第六单元才正式按“长篇小说”来读。此后高中必修下册第七单元整本书阅读《红楼梦》，本书另有<a data-goto="xuanxiu" style="cursor:pointer">选修页</a>收录《诸葛亮舌战群儒》《匡超人》《施润泽滩阙遇友》，可与之对看。</p></div>
</div>

<h2 id="nv-read"><span class="num">02</span>九篇怎么读：三把尺子</h2>
<p>第一把尺子量<b>回目</b>。章回体的回目是一副对联，二十字内把这一回的两件事说尽，读回目可知结构。第二把尺子量<b>白描</b>。白话小说极少心理描写，人物的心思全靠言语与动作显出来——胡屠户扯衣襟、张飞要拿麻绳缚人、刘姥姥念“老刘老刘”、武松“一步步挨下冈子来”，都是动作说话。第三把尺子量<b>世态</b>。这九篇没有一篇是单纯讲故事：借箭写智与忌，打虎写勇与怕，出世写自由，春趣写盛衰，斗法写强中更有强中手，智取写不义之财与人心向背，中举写制度与炎凉，三顾写求贤与际遇，游园写贫富与体面。</p>
<div class="aside"><b>一点提醒：</b>教材所收多是节选，长篇的妙处往往在节选之外。读完一篇，不妨顺着回目往下翻两回——借箭之后是黄盖受刑、火烧赤壁，打虎之后是杀嫂、刺配、上梁山，出世之后是出海求道、大闹天宫，春趣之后是抄检大观园，智取之后是梁山泊义士尊晁盖，中举之后是范进母亲喜极而死，三顾之后是博望坡第一把火，游园之后是刘姥姥给巧姐取名。这些“后文”才是作者真正要说的结局。</div>
""")

    for i, (anchor, title, a, pieces) in enumerate(UNITS, 1):
        out.append('<h2 id="%s"><span class="num">%02d</span>%s</h2>\n' % (anchor, i + 2, title))
        if a:
            out.append(author_html(a))
        for p in pieces:
            out.append(piece_html(p))

    out.append("""<h2 id="nv-learn"><span class="num">08</span>总学习要点：九篇共通的五件事</h2>
<div class="info-grid">
  <div class="info-box"><h4>一 · 长篇小说要“整本看”</h4><p>节选像一扇窗，看得见屋里，看不见屋子在村子里的位置。读节选时至少要知道：这一段在全书第几回、前后发生了什么、人物的结局如何。教材的“阅读提示”往往点出这些，别跳过。</p></div>
  <div class="info-box"><h4>二 · 人物靠语言立起来</h4><p>杨志的急、胡屠户的势利、张飞的莽、刘姥姥的世故、武松的倔、孙悟空的顽，没有一句是作者直接评价的，全是人物自己说出来的。练习时可以遮住提示语，只读对话，猜是谁在说话——猜得准，说明人物立住了。</p></div>
  <div class="info-box"><h4>三 · 环境不是背景板</h4><p>智取里的“热”、三顾里的“雪”与“松”、游园里的“软烟罗”、中举里的“猪油”与“大肠”、景阳冈的“日色渐落”、借箭的“大雾”，都是推动情节或标明身份的东西。写环境就是写人。</p></div>
  <div class="info-box"><h4>四 · 讽刺与悲悯是一体两面</h4><p>《儒林外史》笑范进，也怜范进；《红楼梦》写刘姥姥的丑，也写她的体面与智慧。讽刺的对象从来不是某个可笑的人，而是把人变成这样的那个制度与环境。</p></div>
  <div class="info-box"><h4>五 · 五部书的五种“看”</h4><p>《三国》看“智”如何改变格局，《水浒》看“义”如何被逼出来，《西游》看“心”如何被收束，《儒林》看“名”如何扭曲人心，《红楼》看“盛”如何走向衰。五种看法合起来，就是中国古典小说对人与社会的基本判断。</p></div>
  <div class="info-box"><h4>版本说明</h4><p>本页原文据通行本系统校录：《三国演义》毛本第四十六、三十八回，《水浒传》百二十回袁无涯本第二十三回、百回本第十六回，《西游记》明世德堂本第一、六回，《儒林外史》卧闲草堂本第三回，《红楼梦》程乙本系统第四十、七十回。五年级四篇教材为改写或删节，本页收原文对应段落，与课文文字有出入（如《草船借箭》课文把“却说鲁肃领了周瑜言语”改写为“周瑜看到诸葛亮挺有才干，心里很妒忌”），已在各篇篇首注明。</p></div>
</div>
""")
    html = "\n".join(out)
    io.open(os.path.join(ROOT, 'parts', 'novel.html'), 'w', encoding='utf-8').write(html)
    print('生成 parts/novel.html  %d 字符' % len(html))

if __name__ == '__main__':
    build()
