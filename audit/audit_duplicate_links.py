# -*- coding: utf-8 -*-
"""排查：①同名篇目被不同作者错链到同一目标；②作者卡片列篇目但无正文；③新增 id 存在性。"""
import io, re, glob, os, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(f):
    return io.open(os.path.join(BASE, f), encoding="utf-8").read()


# ---------- ① 同名篇目多作者指向 ----------
rows = []
for f in sorted(glob.glob(os.path.join(BASE, "parts", "*.html"))):
    s = io.open(f, encoding="utf-8").read()
    for tr in re.findall(r"<tr>(.*?)</tr>", s, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(tds) < 2:
            continue
        m = re.search(r'data-goto="([^"]+)"', tds[1])
        if not m:
            continue
        author = re.sub(r"<[^>]+>", "", tds[0]).strip()
        linktxt = re.sub(r"<[^>]+>", "", tds[1]).strip()
        rows.append((os.path.basename(f), author, linktxt, m.group(1)))

bytitle = collections.defaultdict(list)
for f, a, t, tg in rows:
    bytitle[t].append((a, tg, f))

print("=== ① 同名篇目多作者指向（人工复核：应为不同目标或明确区分）===")
found = 0
for t, lst in bytitle.items():
    authors = set(a for a, _, _ in lst)
    if len(authors) > 1:
        targets = set(tg for _, tg, _ in lst)
        flag = "  <== 同一目标，需复核" if len(targets) == 1 else "  (不同目标，正常)"
        print("【%s】%s" % (t, flag))
        for a, tg, f in lst:
            print("    %s -> %s (%s)" % (a, tg, f))
        found += 1
print("同名多作者条目数:", found)

# ---------- ② 新增 id 存在性与错链残留 ----------
prod = read("统编教材古代作家文学集成.html")
print("\n=== ② 新增作品块与错链残留 ===")
for pid in ["p-congjunxing-yangjiong", "p-liangzhouci-wanghan"]:
    print("  存在 %-28s: %s" % (pid, ('id="%s"' % pid) in prod))
bad = 'data-goto="tangsheng::p-congjunxing-wangchangling" class="tlink"'
# 仅统计杨炯表格那一行是否还有残留（王昌龄本页保留是正常的）
lines = [l for l in prod.splitlines() if "杨炯" in l and "从军行" in l and "data-goto" in l]
print("  杨炯表格行:")
for l in lines:
    print("   ", re.search(r'data-goto="([^"]+)"', l).group(1))

# jiaocai 四年级上凉州词
jc = read("parts/jiaocai.html")
seg = jc[jc.index("四年级上"):jc.index("六年级上")]
print("  四年级上段凉州词目标:", re.search(r'data-goto="([^"]*liangzhouci[^"]*)"', seg).group(1))
