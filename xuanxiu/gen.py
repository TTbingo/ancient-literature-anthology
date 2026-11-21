# -*- coding: utf-8 -*-
"""生成 parts/xuanxiu.html：高中选修《中华传统文化专题研讨》全册细读。"""
import io, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
import d1, d2, d3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def esc(t):
    return t

def verse_html(paras):
    return "<br><br>".join(paras)

def dims_html(dims):
    out = []
    for k, v in dims:
        out.append('  <div class="dim"><span class="k">%s</span><span class="v">%s</span></div>' % (k, v))
    return "\n".join(out)

def author_html(a):
    grid = "".join('    <div class="m"><b>%s</b>%s</div>\n' % (k, v) for k, v in a["grid"])
    toc = ""
    if a.get("toc"):
        toc = '  <div class="cardtoc"><b>本页细读：</b>%s</div>\n' % "".join(
            '<a href="#%s">%s</a>' % (i, t) for i, t in a["toc"])
    paras = "".join("  <p>%s</p>\n" % p for p in a["ps"])
    return ('<div class="author-card" id="%s">\n'
            '  <h3>%s <span class="tag %s">%s</span></h3>\n'
            '  <div class="mini-grid">\n%s  </div>\n%s%s</div>\n'
            % (a["id"], a["h"], a.get("tagcls", "tag-book"), a.get("tag", "教材·高中选修"), grid, paras, toc))

def piece_html(p):
    alias = (' data-alias="%s"' % p["alias"]) if p.get("alias") else ""
    if p.get("kind") == "link":
        return ('<div class="poem" id="%s"%s>\n'
                '  <div class="ptitle">%s <span class="tag tag-book">%s</span></div>\n'
                '  <div class="pmeta">%s</div>\n'
                '  <div class="verse">%s</div>\n%s\n</div>\n'
                % (p["sid"], alias, p["title"], p.get("tag", "教材·高中选修"), p["pmeta"],
                   p["text"], dims_html(p["dims"])))
    body = verse_html(p["text"])
    note = ""
    if p.get("note"):
        note = '  <div class="note">%s</div>\n' % p["note"]
    return ('<div class="poem" id="%s"%s>\n'
            '  <div class="ptitle">%s <span class="tag tag-book">%s</span></div>\n'
            '  <div class="pmeta">%s</div>\n'
            '  <div class="verse">%s</div>\n%s%s\n</div>\n'
            % (p["sid"], alias, p["title"], p.get("tag", "教材·高中选修"), p["pmeta"], body, dims_html(p["dims"]), note))

def build():
    out = []
    out.append("""<header class="author-cover">
  <div class="eyebrow">高中选修 · 中华传统文化专题研讨 · 全册细读</div>
  <h1>中华传统文化专题研讨</h1>
  <div class="sub">统编高中语文选修课程用书 · 六单元二十课 · 先秦至明清</div>
  <div class="badges">
    <span class="tag tag-book">教材·高中选修</span>
    <span class="tag tag-shi">史实</span>
    <span class="tag tag-guan">学界观点</span>
  </div>
</header>

<div class="sub-toc">
  <b>本篇目录</b>
  <a href="#xu-intro">选修怎么读</a>
  <a href="#xu-u1">一 · 进德修身</a>
  <a href="#xu-u2">二 · 道法自然</a>
  <a href="#xu-u3">三 · 兴观群怨</a>
  <a href="#xu-u4">四 · 叙事传统</a>
  <a href="#xu-u5">五 · 乐山乐水</a>
  <a href="#xu-u6">六 · 市井风流</a>
  <a href="#xu-learn">总学习要点</a>
</div>

<div class="lead">
《中华传统文化专题研讨》是统编高中语文六册选修课程用书之一，与必修、选择性必修五册相衔接：五册按"文体—人文主题"编次，此书则按<b>六个文化专题</b>重组，把散见于各册的经典重新归拢到"修身—哲思—诗教—叙事—山水—市井"六条脉络上。全书二十课，自《老子》《庄子》起，经《毛诗序》《文心雕龙》《诗品》，到《滕王阁序》《黄冈竹楼记》，再落到《东京梦华录》《帝京景物略》与"三言""二拍"一脉的市井书写——既有思想的骨架，也有文章的肌理，更有城市与日常的烟火气。本页逐课收录<b>原文与七维度解析</b>，长篇章若教材本身即为节选，均注明节选范围。
</div>

<h2 id="xu-intro"><span class="num">00</span>选修怎么读：从"专题"进入经典</h2>
<p>与必修、选择性必修不同，这本选修用书不追求"篇篇精讲"，而是要人顺着专题读出一部文化史的头绪。六个单元其实回答了六个问题：<b>人如何立身</b>（进德修身）、<b>世界如何生成</b>（道法自然）、<b>诗何以能观</b>（兴观群怨）、<b>故事如何讲述</b>（叙事传统）、<b>山水如何被看见</b>（乐山乐水）、<b>市井如何入文</b>（市井风流）。前两单元立其本，中两单元辨其体，后两单元广其境。</p>
<div class="info-grid">
  <div class="info-box"><h4>与五册的衔接</h4><p>《老子》四章、《庄子》五石之瓠见选择性必修上册；《滕王阁序》见旧人教版必修五，统编五册未列正选而在此书第五单元；《廉颇蔺相如列传》与选择性必修中册《屈原列传》同属史传一脉；《柳毅传》《匡超人》《施润泽滩阙遇友》则补上了五册未及的小说史段落。</p></div>
  <div class="info-box"><h4>阅读建议</h4><p>一、先读单元导语与"单元研讨任务"，带着问题读原文；二、文言难点不必逐字死抠，先把握"这一篇在说什么事、用什么法"；三、六单元读毕，回头把"道法自然"与"乐山乐水"对看，把"兴观群怨"与"市井风流"对看，专题之间的呼应才是这本书的真正结构。</p></div>
</div>

<h2 id="xu-u1"><span class="num">01</span>第一单元 · 进德修身：《论语》整本书阅读</h2>
<p>本单元不选单篇，而以<b>《论语》整本书阅读</b>为任务：由"作品导读"入手，通读全书二十篇，梳理"仁—礼—君子"三个核心概念，再自选专题（如"孔门弟子群像""论学与论政""《论语》中的情境对话"）作研讨。教材所重不在语录记诵，而在<b>把语录还原为对话现场</b>——同一问题，孔子对颜渊、子路、司马牛的回答各不相同，差异处正是人物性格与教育方法所在。</p>
<div class="aside"><b>与本书其他分页的关系：</b>《论语》十二章（选择性必修上册）与孔门语录的细读，见「先秦诸子散文」页；本单元作为整本书阅读，不再重复选篇，读法上与那一页互为表里。</div>

""")
    # 单元二至六
    for unit in (d1.UNIT2, d1.UNIT3, d2.UNIT4, d3.UNIT5, d3.UNIT6):
        out.append(unit["head"])
        for kind, obj in unit["items"]:
            if kind == "a":
                out.append(author_html(obj))
            else:
                out.append(piece_html(obj))
        if unit.get("tail"):
            out.append(unit["tail"])
    out.append(d3.LEARN)
    html = "\n".join(out)
    import crosslink
    html, st = crosslink.process(html)
    io.open(os.path.join(ROOT, "parts", "xuanxiu.html"), "w", encoding="utf-8").write(html)
    print("生成 parts/xuanxiu.html  %d 字符  交叉链接 %s" % (len(html), st))

if __name__ == "__main__":
    build()
