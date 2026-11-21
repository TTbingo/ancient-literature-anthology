# -*- coding: utf-8 -*-
"""把 wikisource 抓取的原文清洗、切片，供 gen.py 组装 HTML。"""
import io, os, re

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
_cache = {}

def raw(key):
    if key not in _cache:
        _cache[key] = io.open(os.path.join(SRC, key + ".txt"), encoding="utf-8").read()
    return _cache[key]

FOOT = ("此作品在全世界都属于公有领域", "此北宋作品在全世界都属于公有领域",
        "此唐朝作品在全世界都属于公有领域", "Public domainPublic domainfalsefalse")

def _basic(t):
    for f in FOOT:
        i = t.find(f)
        if i > 0:
            t = t[:i]
    t = t.replace("&#160;", "").replace("\u00a0", "")
    t = re.sub(r"下载\s*\n维基文库，自由的图书馆\s*\n", "", t)
    t = re.sub(r"^<\s*[^\n]{0,30}\n", "", t, count=1)
    t = re.sub(r"\[编辑\]", "", t)
    t = re.sub(r"提示：本文的主题不是[^\n]*\n?", "", t)
    t = re.sub(r"参阅维基百科中的：[^\n]*\n?", "", t)
    # 校勘小注：X有版本作“Y”，误。 / 虚一作“和”
    t = re.sub(r"[^\s，。；]{1,3}有版本作“[^”]{1,8}”，(?:误|非)。", "", t)
    t = re.sub(r"[^\s，。；]{0,2}一作“[^”]{1,8}”", "", t)
    t = re.sub(r"[^\s，。；]{0,2}一作[^\s，。；]{1,6}[，。；]", r"\g<0>".replace("\\g<0>",""), t)
    t = t.replace("。。", "。")
    return t

def paras(key):
    """返回段落列表（去掉空行、导航、注释行）。"""
    t = _basic(raw(key))
    out = []
    for line in t.split("\n"):
        s = line.strip()
        if not s:
            continue
        if s.startswith("〈") or s.startswith("（") and s.endswith("）"):
            continue
        if re.match(r"^[①-⑳]", s):
            continue
        if re.match(r"^[一二三四五六七八九十百]+$", s):
            continue
        s = s.lstrip("■　 ")
        if s in ("内篇上", "内篇下", "外篇上", "外篇下", "卷五·传状类"):
            continue
        out.append(s)
    return out

def joinwrap(key):
    """把硬折行（每行约40字）合并成自然段：段以句末标点结尾。"""
    ps = paras(key)
    buf = ""
    res = []
    for s in ps:
        buf += s
        if re.search(r"[。！？：”’】]$", s) or s.endswith("；"):
            res.append(buf); buf = ""
    if buf.strip():
        res.append(buf)
    return res

def split_long(p, n=4):
    """把超长段落按句末标点切成每段约 n 句。"""
    if len(p) <= 260:
        return [p]
    sents = re.findall(r"[^。！？]*[。！？]”?", p)
    if not sents:
        return [p]
    out, cur = [], ""
    cnt = 0
    for s in sents:
        cur += s; cnt += 1
        if cnt >= n and len(cur) >= 120:
            out.append(cur); cur = ""; cnt = 0
    if cur.strip():
        out.append(cur)
    return out

def flat(key, n=4, joiner=None):
    ps = joinwrap(key) if joiner == "wrap" else paras(key)
    res = []
    for p in ps:
        res.extend(split_long(p, n))
    return res

def between(key, start, end=None, n=4):
    """按首尾标记截取（含 start，含 end）。"""
    ps = flat(key, n)
    txt = "\n".join(ps)
    i = txt.find(start)
    if i < 0:
        raise SystemExit("找不到起点 %s / %s" % (key, start))
    j = len(txt)
    if end:
        k = txt.find(end, i)
        if k < 0:
            raise SystemExit("找不到终点 %s / %s" % (key, end))
        j = k + len(end)
    return [x for x in txt[i:j].split("\n") if x.strip()]

def head_chars(key, n, n_sent=4):
    """从头截取 n 字（在句末断开），末尾加省略号标注。"""
    ps = flat(key, n_sent)
    txt = "".join(ps)
    if len(txt) <= n:
        return ps
    cut = txt.rfind("。", 0, n)
    txt = txt[:cut + 1] + "……"
    return [x for x in split_long(txt, n_sent) if x.strip()]

def chapters(key, nums):
    """道德經（王弼本）：按“X章”取经文，剔除王弼注（〈 〉）。"""
    t = _basic(raw(key))
    lines = t.split("\n")
    cn = "零一二三四五六七八九十"
    def num2cn(n):
        if n <= 10:
            return "十" if n == 10 else cn[n]
        if n < 20:
            return "十" + cn[n - 10]
        if n % 10 == 0:
            return cn[n // 10] + "十"
        return cn[n // 10] + "十" + cn[n % 10]
    out = []
    for n in nums:
        tag = num2cn(n) + "章"
        idx = None
        for i, l in enumerate(lines):
            if l.strip().startswith(tag):
                idx = i; break
        if idx is None:
            raise SystemExit("找不到 %s" % tag)
        body = []
        for l in lines[idx + 1:]:
            s = l.strip()
            if re.match(r"^[零一二三四五六七八九十]+章", s):
                break
            if not s or s.startswith("〈") or s.startswith("（"):
                continue
            body.append(s)
        out.append((n, "".join(body)))
    return out

def numbered(key, nums):
    """人間詞話：按“一 标题”编号取则（返回 (号, 文)）。"""
    t = _basic(raw(key))
    lines = [l.strip() for l in t.split("\n") if l.strip()]
    cn = "零一二三四五六七八九十"
    def num2cn(n):
        if n <= 10:
            return "十" if n == 10 else cn[n]
        if n < 20:
            return "十" + cn[n - 10]
        if n % 10 == 0:
            return cn[n // 10] + "十"
        return cn[n // 10] + "十" + cn[n % 10]
    res = []
    for n in nums:
        tag = num2cn(n) + " "
        idx = None
        for i, l in enumerate(lines):
            if l.startswith(tag):
                idx = i; break
        if idx is None:
            raise SystemExit("找不到第 %d 则" % n)
        body = []
        for l in lines[idx + 1:]:
            if re.match(r"^[零一二三四五六七八九十]+ ", l):
                break
            if re.match(r"^[①-⑳]", l):
                continue
            body.append(l)
        res.append((n, "".join(body)))
    return res

def tocs(key, n):
    """取前 n 则（每则以“一/二/一一…”编号开头），返回 [(编号, 正文)]。"""
    t = _basic(raw(key))
    lines = [l.strip() for l in t.split("\n") if l.strip()]
    res, i = [], 0
    while i < len(lines) and len(res) < n:
        m = re.match(r"^([一二三四五六七八九十]{1,3})\s+(.+)$", lines[i])
        if not m:
            i += 1
            continue
        head, body = m.group(1), []
        i += 1
        while i < len(lines) and not re.match(r"^[一二三四五六七八九十]{1,3}\s+\S", lines[i]):
            if not re.match(r"^[①-⑳]", lines[i]):
                body.append(lines[i])
            i += 1
        txt = "".join(body)
        txt = re.sub(r"[①-⑳]", "", txt)
        res.append((head, txt))
    return res
