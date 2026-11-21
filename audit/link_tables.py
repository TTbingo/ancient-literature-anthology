# -*- coding: utf-8 -*-
"""把各页「教材篇目一览」表篇目列的作品名变成站内直达链接（试运行可加 --apply）"""
import io, json, os, re, sys

BASE = r"D:/workbuddy的工作空间/2026-11-20-18-22-04/李白诗词解析"
PARTS = os.path.join(BASE, "parts")
POEMS = json.load(io.open(os.path.join(BASE, "audit", "poems.json"), encoding="utf-8"))
SKIP = {"jiaocai", "indexall", "home", "method", "novel", "xuanxiu", "libai"}

def norm(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("《", "").replace("》", "").replace("〈", "").replace("〉", "")
    t = t.replace("〔", "").replace("〕", "").replace("【", "").replace("】", "")
    t = re.sub(r"[（(][^）)]*[）)]", "", t)
    t = re.sub(r"[\s·・、，,。：:；;“”\"'？?！!—\-…]", "", t)
    t = t.replace("并序", "").replace("节选", "").replace("全文", "")
    t = re.sub(r"其[一二三四五六七八九十]$", "", t)
    t = re.sub(r"之[一二三四五六七八九十]$", "", t)
    return t

def match(page, raw):
    key = norm(raw)
    if not key:
        return None
    cands = [(pid, norm(t.split(" 教材")[0])) for pid, t in POEMS.get(page, [])]
    exact = [c for c in cands if c[1] == key]
    if len(exact) == 1:
        return exact[0][0]
    pref = [c for c in cands if c[1].startswith(key) and len(c[1]) - len(key) <= 6]
    if len(pref) == 1:
        return pref[0][0]
    if len(pref) > 1:
        pref.sort(key=lambda c: len(c[1]))
        return pref[0][0]
    k2 = [c for c in cands if key.startswith(c[1]) and len(c[1]) >= 2]
    if len(k2) == 1:
        return k2[0][0]
    cont = [c for c in cands if key in c[1] and len(c[1]) - len(key) <= 4]
    if len(cont) == 1:
        return cont[0][0]
    return None

def match_global(raw):
    """本页没有时跨页找，且必须全站唯一，避免张冠李戴"""
    key = norm(raw)
    if not key:
        return None
    hits = []
    for pg, lst in POEMS.items():
        for pid, t in lst:
            k = norm(t.split(" 教材")[0])
            if k == key or k.startswith(key) or (key.startswith(k) and len(k) >= 2):
                hits.append((pg, pid, k))
    if not hits:
        return None
    best = [h for h in hits if h[2] == key] or hits
    pages = {h[0] for h in best}
    if len(pages) == 1:
        best.sort(key=lambda h: len(h[2]))
        return (best[0][0], best[0][1])
    return None

# 人工覆盖：篇目写法 -> (page, poem id)
OV = {
    ("dufu", "绝句"): "p-dufu-jueju",
    ("hanprose", "屈原列传"): "p-simaqian-qvyl" ,
}

def wrap(page, m):
    """把一个匹配替换为链接，保留括号说明"""
    return m.group(0)

def tokenize(cell):
    """返回 [(text, is_title, matched_id)]，按原顺序切分"""
    out = []
    pos = 0
    # 匹配《…》或 〔…〕《…》 结构
    for m in re.finditer(r"《[^》]{1,40}》", cell):
        if m.start() > pos:
            out.append([cell[pos:m.start()], False, None])
        out.append([m.group(0), True, None])
        pos = m.end()
    if pos < len(cell):
        out.append([cell[pos:], False, None])
    return out

def process(path, apply=False):
    key = os.path.basename(path)[:-5]
    s = io.open(path, encoding="utf-8").read()
    changed = [0, 0]
    def repl_table(tm):
        t = tm.group(0)
        hs = [re.sub("<[^>]+>", "", x).strip() for x in re.findall(r"<th[^>]*>(.*?)</th>", t, re.S)]
        if not any("篇目" in h for h in hs):
            return t
        if "篇目（点击直达）" in "".join(hs):
            return t
        idx = [i for i, h in enumerate(hs) if "篇目" in h][0]
        rows = list(re.finditer(r"<tr>(.*?)</tr>", t, re.S))
        out = t
        for r in reversed(rows):
            row = r.group(1)
            tds = list(re.finditer(r"<td[^>]*>(.*?)</td>", row, re.S))
            if len(tds) <= idx:
                continue
            cell = tds[idx].group(1)
            if "data-goto" in cell:
                continue
            parts = tokenize(cell)
            if not any(p[1] for p in parts):
                # 「词六首：西江月·井冈山、……」这类无书名号的单元格，按顿号拆
                m0 = re.match(r'^(.*?：)(.*)$', cell)
                if m0 and "、" in m0.group(2):
                    head, body = m0.group(1), m0.group(2)
                    pieces = []
                    for i, seg in enumerate(body.split("、")):
                        pid2 = match(key, seg)
                        if pid2:
                            pieces.append('<a data-goto="%s::%s" class="tlink">%s</a>' % (key, pid2, seg))
                        else:
                            pieces.append(seg)
                    newcell = [head + "、".join(pieces)]
                    newrow = row[:tds[idx].start(1)] + "".join(newcell) + row[tds[idx].end(1):]
                    out = out[:r.start(1)] + newrow + out[r.end(1):]
                    changed[0] += sum(1 for x in pieces if x.startswith("<a"))
                    changed[1] += sum(1 for x in pieces if not x.startswith("<a"))
                continue
            newcell = []
            for text, is_title, _ in parts:
                if not is_title:
                    newcell.append(text); continue
                inner = text[1:-1]
                pid = match(key, inner) or OV.get((key, norm(inner)))
                if isinstance(pid, str):
                    pid = (key, pid)
                if not pid:
                    pid = match_global(inner)
                if pid:
                    newcell.append('<a data-goto="%s::%s" class="tlink">%s</a>' % (pid[0], pid[1], text))
                    changed[0] += 1
                else:
                    newcell.append(text)
                    changed[1] += 1
            newrow = row[:tds[idx].start(1)] + "".join(newcell) + row[tds[idx].end(1):]
            out = out[:r.start(1)] + newrow + out[r.end(1):]
        return out
    new = re.sub(r"<table[^>]*>.*?</table>", repl_table, s, flags=re.S)
    return key, new, changed

if __name__ == "__main__":
    apply = "--apply" in sys.argv
    tot = [0, 0]
    for fn in sorted(os.listdir(PARTS)):
        if not fn.endswith(".html"): continue
        key = fn[:-5]
        if key in SKIP: continue
        key, new, ch = process(os.path.join(PARTS, fn))
        tot[0] += ch[0]; tot[1] += ch[1]
        if ch[0] or ch[1]:
            print("%-16s 链接 %3d  未匹配 %3d" % (key, ch[0], ch[1]))
        if apply and ch[0]:
            io.open(os.path.join(PARTS, fn), "w", encoding="utf-8").write(new)
    print("合计 链接 %d  未匹配 %d" % tuple(tot))
