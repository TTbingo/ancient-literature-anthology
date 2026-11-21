# -*- coding: utf-8 -*-
"""wikitext -> 段落列表（简体）"""
import io,re,os

MAP={}
_p=os.path.join(os.path.dirname(__file__),'..','xuanxiu','tmp','TSCharacters.txt')
if os.path.exists(_p):
    for ln in io.open(_p,encoding='utf-8'):
        a=ln.split()
        if len(a)>=2: MAP[a[0]]=a[1]

KEEP=set('著祇徵藉乾覆麼像俱沈坏彷蘋餔鵩絜駃騠氾魦爇巘摐騑騞樠薆')

def ts(t):
    out=[]
    for c in t:
        if c in MAP and c not in KEEP: out.append(MAP[c])
        else: out.append(c)
    return ''.join(out)

def clean(t):
    t=re.sub(r'\{\{header2.*?\}\}','',t,flags=re.S)
    t=re.sub(r'\{\{[^{}]*\}\}','',t)
    t=t.replace('----','')
    t=re.sub(r'-?\{([^{}]*)\}-',r'\1',t)      # -{云}-  -> 云
    t=re.sub(r'<ref[^>]*>.*?</ref>','',t,flags=re.S)
    t=re.sub(r'<[^>]+>','\n',t)
    t=re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]',r'\1',t)
    t=re.sub(r'\[\[([^\]]*)\]\]',r'\1',t)
    t=re.sub(r"'''?|''?",'',t)
    t=re.sub(r'^=+.*?=+$','',t,flags=re.M)
    t=re.sub(r'[ \t\u3000]+',' ',t)
    lines=[]
    for l in t.split('\n'):
        l=l.strip()
        if not l or l.startswith('{{') or l.startswith('|'): continue
        if re.fullmatch(r'[\-\s]*',l): continue
        lines.append(l)
    return lines

def load(name):
    return clean(io.open(os.path.join(os.path.dirname(__file__),'tmp',name+'.raw'),encoding='utf-8').read())

def find(lines,key,n=1):
    hits=[i for i,l in enumerate(lines) if key in l]
    return hits
