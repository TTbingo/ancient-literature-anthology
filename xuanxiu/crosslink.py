# -*- coding: utf-8 -*-
"""交叉链接：把选修页作者卡「教材篇目」里的篇名，链到全站已有内容。

两类目标：
1. 必修 / 选择性必修五册中的篇目 → data-goto 跳到既有页面与卡片（锚点取自 parts/jiaocai.html）。
2. 本册选修篇目 → 跳到本页对应的作品卡（#p-xu-xxx）。

只处理「作者卡 · 教材篇目」段落与「与五册的衔接」说明盒，正文分析文字不动，
避免把行文中的书名误链成"这一篇的全文"。
"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 最外层书名号，容许内嵌一层（《〈老子〉四章》）；并容许书名号后紧跟数量词
# （教材惯写「《老子》十章」「《人间词话》十则」，数词在号外）
NAME_RE = re.compile(r'《[^《》]*(?:《[^》]*》[^《》]*)*》(?:[〇一二三四五六七八九十百千两]+[则章篇首节])?')


def norm(t):
    """去掉书名号、间隔号、标点与空白，用于篇名比对。"""
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'[《》〈〉·・：:，,。、（）()【】\[\]\s"“”‘’—－\-]', '', t).lower()


# 本頁各卡的教材篇名（卡标题常带卷次/调名，无法直接反推，故显式声明）
XU_TITLES = {
    '老子': 'p-xu-laozi',
    '老子十章': 'p-xu-laozi',
    '庄子寓言三则': 'p-xu-zhuangzi',
    '淮南子': 'p-xu-huainanzi',
    '淮南子二则': 'p-xu-huainanzi',
    '与山巨源绝交书': 'p-xu-juejiaoshu',
    '毛诗序': 'p-xu-maoshixu',
    '文心雕龙明诗': 'p-xu-shilun',
    '诗品序': 'p-xu-shilun',
    '原诗': 'p-xu-shilun',
    '与元九书': 'p-xu-yuyuanjiushu',
    '人间词话': 'p-xu-renjiancihua',
    '人间词话十则': 'p-xu-renjiancihua',
    '廉颇蔺相如列传': 'p-xu-lianpo',
    '柳毅传': 'p-xu-liuyi',
    '诸葛亮舌战群儒': 'p-xu-shezhan',
    '匡超人': 'p-xu-kuangchaoren',
    '滕王阁序': 'p-xu-tengwang',
    '黄冈竹楼记': 'p-xu-zhulou',
    '山水训': 'p-xu-shanshuixun',
    '山水训五则': 'p-xu-shanshuixun',
    '麻叶洞天': 'p-xu-mayee',
    '东角楼街巷': 'p-xu-shijingbiji',
    '民俗': 'p-xu-shijingbiji',
    '灯市': 'p-xu-shijingbiji',
    '高祖还乡': 'p-xu-gaozu',
    '施润泽滩阙遇友': 'p-xu-shirunze',
    '柳敬亭传': 'p-xu-liujingting',
    '马伶传': 'p-xu-maling',
}

# 个别篇目的全文在别的分页（本页只设链接卡），直接指向正文，少一次跳转
OVERRIDE = {
    '滕王阁序': 'tangchu::p-tengwangge-wangbo',
}

# 五册里确实没有独立卡片、只能留作纯文本的篇目（外部无内容可跳）
MISSING = set()   # 四篇小说已收录，此处留作以后标注缺篇用

# 「与五册的衔接」一段的行文把篇名写在书名号之外（《庄子》五石之瓠、《老子》四章），
# 单处硬编码最可靠
BOX_FIX = [
    ('《老子》四章', 'zhuzi::p-laozi-sizhang'),
    ('《庄子》五石之瓠', 'zhuzi::p-zhuangzi-wushizhihu'),
    ('《滕王阁序》', 'tangchu::p-tengwangge-wangbo'),
    ('《廉颇蔺相如列传》', 'xuanxiu::p-xu-lianpo'),
    ('《屈原列传》', 'hanprose::p-simaqian-qunyuanliezhuan'),
    ('《柳毅传》', 'xuanxiu::p-xu-liuyi'),
    ('《匡超人》', 'xuanxiu::p-xu-kuangchaoren'),
    ('《施润泽滩阙遇友》', 'xuanxiu::p-xu-shirunze'),
]


def jiaocai_map():
    """parts/jiaocai.html 里的 (篇名 → data-goto)，五册篇目的权威锚点表。"""
    p = os.path.join(ROOT, 'parts', 'jiaocai.html')
    s = io.open(p, encoding='utf-8').read()
    m = {}
    for g, t in re.findall(r'<a[^>]*data-goto="([^"]+)"[^>]*>(.*?)</a>', s, re.S):
        if '::' not in g:          # 只收具体篇目，跳过整页入口
            continue
        k = norm(t)
        if k:
            m.setdefault(k, g)
    return m


def xu_map(html):
    """本页作品卡：卡标题（去标签）+ data-alias + 手工表 → #卡 id。"""
    m = {}
    for mid, attrs, title in re.findall(
            r'<div class="poem" id="([^"]+)"([^>]*)>\s*<div class="ptitle">(.*?)</div>', html, re.S):
        title = re.sub(r'<span class="tag[^"]*">.*?</span>', '', title)
        k = norm(title)
        if k:
            m.setdefault(k, '#' + mid)
        a = re.search(r'data-alias="([^"]*)"', attrs or '')
        if a:
            for w in re.split(r'[\s　]+', a.group(1)):
                if w:
                    m.setdefault(norm(w), '#' + mid)
    for k, v in XU_TITLES.items():
        m[norm(k)] = '#' + v
    return m


def link_one(name, jmap, pmap, stats=None):
    """单个书名号片段 → 链接 HTML（无目标则原样返回）。"""
    k = norm(name)
    if k in OVERRIDE:
        if stats is not None:
            stats['五册'] = stats.get('五册', 0) + 1
        return '<a class="xlink" data-goto="%s" title="跳到已收录的全文与解析">%s</a>' % (OVERRIDE[k], name)
    if k in jmap:
        if stats is not None:
            stats['五册'] = stats.get('五册', 0) + 1
        return '<a class="xlink" data-goto="%s" title="跳到已收录的全文与解析">%s</a>' % (jmap[k], name)
    if k in pmap:
        if stats is not None:
            stats['本页'] = stats.get('本页', 0) + 1
        return '<a class="xlink" data-goto="xuanxiu::%s" title="跳到本页全文与解析">%s</a>' % (pmap[k].lstrip('#'), name)
    if k in MISSING:
        if stats is not None:
            stats['缺'] = stats.get('缺', 0) + 1
        return '<span class="xmiss" title="该篇在已收录的五册页与本页中都没有独立卡片">%s</span>' % name
    if stats is not None:
        stats['未匹配'] = stats.get('未匹配', 0) + 1
    return name


def process(html):
    jmap = jiaocai_map()
    pmap = xu_map(html)
    stats = {}

    # 1) 作者卡「教材篇目」段
    html = re.sub(r'(<p><b>教材篇目：</b>)(.*?)(</p>)',
                  lambda m: m.group(1) + NAME_RE.sub(
                      lambda mm: link_one(mm.group(0), jmap, pmap, stats), m.group(2)) + m.group(3),
                  html, flags=re.S)

    # 2) 「与五册的衔接」说明盒
    def fix_box(m):
        body = m.group(2)
        for lit, tgt in BOX_FIX:
            if tgt.startswith('#'):
                a = '<a class="xlink" data-goto="xuanxiu::%s" title="跳到本页全文与解析">%s</a>' % (tgt.lstrip('#'), lit)
            else:
                a = '<a class="xlink" data-goto="%s" title="跳到已收录的全文与解析">%s</a>' % (tgt, lit)
            body = body.replace(lit, a)
        return m.group(1) + body + m.group(3)

    html = re.sub(r'(<div class="info-box"><h4>与五册的衔接</h4><p>)(.*?)(</p></div>)',
                  fix_box, html, flags=re.S)
    return html, stats


if __name__ == '__main__':
    p = os.path.join(ROOT, 'parts', 'xuanxiu.html')
    s = io.open(p, encoding='utf-8').read()
    out, st = process(s)
    io.open(p, 'w', encoding='utf-8').write(out)
    print('交叉链接:', st, '字符', len(out))
