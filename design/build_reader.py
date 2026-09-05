# -*- coding: utf-8 -*-
"""manuscript/*.md → 원고 열람 페이지 한 장. 사용: python3 design/build_reader.py <out.html>"""
import re, sys, os, glob, html
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AREA = {n: ('힘과 에너지', '#E07A95', '#FFF3F5', '') for n in ['00','01','02','03','04','05','06','07','08']}
AREA.update({n: ('전기와 자기', '#5EAE88', '#EEF8F2', '') for n in ['09','10','11','12']})
AREA.update({n: ('빛과 물질', '#8A84E2', '#F1F0FF', '') for n in ['13','14','15']})

def tex(s):
    """간단한 LaTeX → 읽을 수 있는 유니코드."""
    s = s.replace(r'\ ', ' ')
    s = re.sub(r'\\text\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\(d?frac)\{([^{}]*)\}\{([^{}]*)\}', r'(\2)/(\3)', s)
    s = re.sub(r'\\sqrt\{([^{}]*)\}', r'√(\1)', s)
    s = re.sub(r'\\vec\{([^{}]*)\}', r'\1⃗', s)
    s = re.sub(r'\\bar ([a-zA-Z])', r'\1̄', s)
    s = s.replace(r'\Delta', 'Δ').replace(r'\times', '×').replace(r'\neq', '≠').replace(r'\geq', '≥')
    s = re.sub(r'\^\{?2\}?', '²', s); s = re.sub(r'\^\{([^}]*)\}', r'<sup>\1</sup>', s)
    s = re.sub(r'_\{([^}]*)\}', r'<sub>\1</sub>', s); s = re.sub(r'_([a-zA-Z0-9])', r'<sub>\1</sub>', s)
    s = re.sub(r'\(([^()/]{1,3})\)/\(([^()/]{1,3})\)', r'\1/\2', s)
    return s.strip()

def pre(md):
    md = re.sub(r'\$\$(.+?)\$\$', lambda m: f'<div class="eq">{tex(m.group(1))}</div>', md, flags=re.S)
    md = re.sub(r'\$([^$\n]+?)\$', lambda m: f'<span class="m">{tex(m.group(1))}</span>', md)
    return md

BADGE = {'Δ0 출발선': 'start', 'Δ개념': 'concept', 'Δ예제': 'example', 'Δ연습': 'practice', 'Δ체크': 'check'}
GLYPH = {
 'start':   '<path d="M12 2.5 L19.5 16 L4.5 16 Z"/><path d="M2 21 H22"/><circle cx="4.5" cy="21" r="2" fill="currentColor" stroke="none"/>',
 'concept': '<path d="M13 4 L22 20 L4 20 Z"/><path d="M0.5 12 H9" stroke-width="2.6"/>',
 'example': '<path d="M10 4 L19 20 L1 20 Z"/><path d="M14 12 L23.5 6.5 M14 12 L23.5 12 M14 12 L23.5 17.5" stroke-width="1.8"/>',
 'practice':'<path d="M7 3 L12 11.5 L2 11.5 Z" stroke-width="1.8"/><path d="M17 3 L22 11.5 L12 11.5 Z" stroke-width="1.8"/><path d="M12 12.5 L17 21 L7 21 Z" stroke-width="1.8"/>',
 'check':   '<path d="M12 2.5 L21.5 19.5 L2.5 19.5 Z"/><path d="M8.5 14 L11 16.5 L16 10.5" stroke-width="2.4"/>',
 'answers': '<path d="M12 2 L23 21 L1 21 Z M12 8.5 L17.6 18 L6.4 18 Z" fill="currentColor" stroke="none" fill-rule="evenodd"/>',
}
def svg(k): return f'<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round">{GLYPH[k]}</svg>'

def post(h):
    # 코너 헤더 <h2>[Δ개념 1] 제목</h2>
    def h2(m):
        tag, rest = m.group(1), m.group(2)
        kind = next((v for k, v in BADGE.items() if tag.startswith(k)), None)
        if tag.startswith('정답'): kind = 'answers'
        num = re.search(r'(\d+)$', tag)
        badge = f'<span class="badge"><span class="bx">{svg(kind)}</span>{html.escape(tag if not num else tag[:num.start()].strip())}</span>' if kind else html.escape(tag)
        numb = f'<span class="num">{num.group(1)}</span>' if num and kind in ('concept','example') else ''
        lvl = re.search(r'(▲+)\s*$', rest)
        rest_txt = rest[:lvl.start()].strip() if lvl else rest.strip()
        lvltag = f'<span class="lvl">{lvl.group(1)}</span>' if lvl else ''
        return f'<h2 class="corner c-{kind}">{badge}{numb}<span class="ct">{rest_txt}</span>{lvltag}</h2>'
    h = re.sub(r'<h2>\[([^\]]+)\]\s*(.*?)</h2>', h2, h)
    # [정의] 등 h3
    h = re.sub(r'<h3>\[정의\]\s*(.*?)</h3>', r'<h3 class="def"><span class="eyebrow">정의</span> \1</h3>', h)
    h = re.sub(r'<h3>\[(이 단원의 Δ[^\]]*)\]\s*</h3>', r'<h3 class="eyebrow">\1</h3>', h)
    h = re.sub(r'<h3>\[단원 지도\]\s*</h3>', r'<h3 class="eyebrow">단원 지도</h3>', h)
    # 메모 / 자주 틀리는 곳
    h = re.sub(r'<blockquote>\s*<p><strong>\[(Δ메모|자주 틀리는 곳)\]</strong>\s*(.*?)</p>\s*</blockquote>', r'<aside class="note"><span class="eyebrow">\1</span><p>\2</p></aside>', h, flags=re.S)
    # 그림 자리
    h = re.sub(r'<p>\[그림 ([^\]]+)\]\s*(.*?)</p>', r'<figure class="fig"><span class="eyebrow">그림 \1</span><p>\2</p></figure>', h, flags=re.S)
    # 구분선 제거(코너 헤더가 이미 선을 가짐)
    h = h.replace('<hr />', '').replace('<hr>', '')
    # 단원 지도 한 줄: **1** A · **2** B · **3** C
    h = re.sub(r'<p>((?:<strong>\d</strong>[^<]*(?:·\s*)?){2,})</p>', lambda m: '<p class="map">' + re.sub(r'<strong>(\d)</strong>', r'<span class="pn">\1</span>', m.group(1)) + '</p>', h)
    # 출발선·체크 문항: ☐ 로 시작하는 줄을 문항마다 나눔
    h = re.sub(r'<p>(☐ <strong>.*?)</p>', lambda m: '<div class="qs">' + ''.join(f'<p class="q">{x.strip()}</p>' for x in re.split(r'\s*(?=☐ <strong>)', m.group(1)) if x.strip()) + '</div>', h, flags=re.S)
    h = re.sub(r'<p>(<strong>1</strong> .*?<strong>3</strong> .*?)</p>', lambda m: '<div class="qs">' + ''.join(f'<p class="q">{x.strip()}</p>' for x in re.split(r'(?=<strong>\d</strong> )', m.group(1)) if x.strip()) + '</div>', h, count=1, flags=re.S) if '</details>' not in h else h
    # 풀이 단계 ①②③④
    h = re.sub(r'<p>([①②③④⑤])\s*', r'<p class="step"><span class="sn">\1</span>', h)
    # 연습 문제 번호
    h = re.sub(r'<p><strong>(\d+)</strong>\s*(▲+)\s*', r'<p class="prob"><span class="pn">\1</span><span class="lvl">\2</span>', h)
    h = re.sub(r'<p><strong>(\d+)</strong>\s*', r'<p class="ans"><span class="pn">\1</span>', h)
    # 체크박스 문항
    h = h.replace('☐ <strong>', '<span class="box"></span><strong>')
    # 정답과 해설은 접기
    h = re.sub(r'(<h2 class="corner c-answers">.*?</h2>)(.*)$', r'<details class="answers"><summary>\1<span class="hint">펼치기</span></summary><div class="abody">\2</div></details>', h, flags=re.S)
    return h

def unit(path):
    src = open(path, encoding='utf-8').read()
    m = re.match(r'# (Δ\d\d) (.+)\n', src); code, title = m.group(1), m.group(2)
    meta = re.search(r'> 영역: (.+)\n> 한 줄: (.+)\n', src)
    body = src[meta.end():]
    h = markdown.markdown(pre(body), extensions=['tables'])
    h = post(h)
    n = code[1:]
    area, main, tint, _ = AREA.get(n, ('힘과 에너지', '#E07A95', '#FFF3F5', ''))
    return dict(code=code, n=n, title=title.replace(' — ', ' · '), meta=meta.group(1), line=meta.group(2), html=h, area=area, main=main, tint=tint)

units = [unit(p) for p in sorted(glob.glob(os.path.join(ROOT, 'manuscript', '*.md')))]
upcoming = [('Δ02','등가속도 운동과 그래프'),('Δ03','뉴턴 운동 법칙'),('Δ04','운동 법칙의 적용'),('Δ05','평형과 안정성'),('Δ06','운동량과 충격량'),('Δ07','일과 역학적 에너지'),('Δ08','열과 에너지'),('Δ09','전기장과 전위'),('Δ10','전류와 전기 회로'),('Δ11','전류의 자기 작용'),('Δ12','전자기 유도와 전자기파'),('Δ13','파동과 빛의 성질'),('Δ14','빛과 물질의 이중성'),('Δ15','원자와 에너지 준위')]
done = {u['code'] for u in units}

nav = ''.join(f'<a href="#{u["code"]}" class="nv"><span class="nc">{u["code"]}</span><span>{html.escape(u["title"].split(" · ")[0])}</span></a>' for u in units)
nav += ''.join(f'<span class="nv todo"><span class="nc">{c}</span><span>{t}</span></span>' for c, t in upcoming if c not in done)

sections = ''
for u in units:
    words = len(re.sub(r'<[^>]+>', '', u['html']).split())
    sections += f'''
<section class="unit" id="{u['code']}" style="--main:{u['main']};--tint:{u['tint']}">
  <header class="uh">
    <div class="uh-meta"><span class="nc">{u['code']}</span><span>{html.escape(u['meta'])}</span></div>
    <h1>{html.escape(u['title'])}</h1>
    <p class="line">{html.escape(u['line'])}</p>
  </header>
  <div class="body">{u['html']}</div>
</section>'''

page = f'''<title>델타 물리학 원고</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=Syne:wght@700;800&family=Gowun+Batang:wght@400;700&display=swap">
<style>
:root {{
  --paper:#FBFAFD; --ink:#443E5C; --muted:#7C7791; --rule:#E6E3EE; --soft:#F3F1F8; --tint-fallback:#FFF3F5;
  --bar:linear-gradient(90deg,#FFB5C2,#FFCFB0,#FFF1B5,#C6F0D6,#B5E6F7,#BFCBFF,#DABDFF);
  --sans:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif; --serif:"Gowun Batang","Nanum Myeongjo","Apple Myungjo",serif; --label:"Syne","IBM Plex Sans KR",sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --paper:#1B1A26; --ink:#ECE9F4; --muted:#A8A3BE; --rule:#34324A; --soft:#242336; }} }}
:root[data-theme="dark"] {{ --paper:#1B1A26; --ink:#ECE9F4; --muted:#A8A3BE; --rule:#34324A; --soft:#242336; }}
:root[data-theme="dark"] .unit, :root:not([data-theme="light"]) .unit {{ --tint:#2B2438; }}
:root[data-theme="light"] .unit {{ --tint:#FFF3F5; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--paper); color:var(--ink); font-family:var(--sans); font-size:15.5px; line-height:1.75; }}
.bar {{ height:10px; background:var(--bar); }}
.wrap {{ display:grid; grid-template-columns:220px minmax(0,720px); gap:56px; max-width:1060px; margin:0 auto; padding:36px 28px 96px; }}
nav {{ position:sticky; top:28px; align-self:start; display:flex; flex-direction:column; gap:2px; }}
.brand {{ display:flex; align-items:center; gap:8px; margin-bottom:18px; font-weight:700; font-size:14px; }}
.brand svg {{ display:block; }}
.nv {{ display:grid; grid-template-columns:44px 1fr; gap:8px; align-items:baseline; padding:6px 8px; border-radius:4px; color:var(--ink); text-decoration:none; font-size:13px; }}
.nv:hover {{ background:var(--soft); }}
.nv.todo {{ color:var(--muted); }}
.nc {{ font-family:var(--label); font-weight:800; font-size:12px; letter-spacing:.04em; color:var(--main,#E07A95); }}
.todo .nc {{ color:var(--muted); }}
.navhead {{ font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); font-weight:600; margin:14px 8px 6px; }}
.unit {{ padding-bottom:64px; margin-bottom:64px; border-bottom:1px solid var(--rule); }}
.unit:last-child {{ border-bottom:0; }}
.uh {{ display:flex; flex-direction:column; gap:10px; padding-bottom:22px; margin-bottom:28px; border-bottom:2px solid var(--ink); }}
.uh-meta {{ display:flex; gap:12px; font-size:12px; color:var(--muted); letter-spacing:.06em; }}
.uh-meta .nc {{ font-size:13px; }}
h1 {{ font-family:var(--serif); font-weight:700; font-size:34px; line-height:1.25; margin:0; letter-spacing:-.01em; text-wrap:balance; }}
.line {{ font-family:var(--serif); font-size:17px; color:var(--muted); margin:0; }}
.body h2.corner {{ display:flex; align-items:center; gap:10px; font-size:19px; font-weight:700; margin:48px 0 14px; padding-top:22px; border-top:1px solid var(--rule); letter-spacing:-.01em; }}
.badge {{ display:inline-flex; align-items:center; gap:8px; font-size:14px; font-weight:700; }}
.bx {{ width:26px; height:26px; background:var(--main); color:#fff; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0; }}
.num {{ width:26px; height:26px; background:var(--main); color:#fff; display:inline-flex; align-items:center; justify-content:center; font-family:var(--label); font-weight:800; font-size:14px; }}
.ct {{ flex:1; }}
.lvl {{ font-family:var(--label); font-size:11px; letter-spacing:.1em; color:var(--main); }}
.body h3 {{ font-size:15px; font-weight:700; margin:26px 0 8px; }}
.body h3.def {{ margin-top:22px; }}
.eyebrow {{ display:inline-block; font-size:11px; letter-spacing:.12em; font-weight:700; color:var(--muted); margin-right:6px; }}
.body p {{ margin:0 0 14px; max-width:66ch; text-wrap:pretty; }}
.body ul {{ padding-left:20px; margin:0 0 14px; }}
.body li {{ margin:4px 0; }}
.body strong {{ font-weight:700; }}
.eq {{ font-family:var(--label); font-size:20px; font-weight:700; padding:10px 16px; margin:8px 0 16px; background:var(--tint); border-left:3px solid var(--main); display:inline-block; }}
.m {{ font-family:var(--label); font-weight:700; font-size:.95em; }}
.body table {{ border-collapse:collapse; margin:8px 0 18px; font-size:14px; width:100%; max-width:640px; font-variant-numeric:tabular-nums; }}
.body th {{ text-align:left; font-size:11.5px; letter-spacing:.06em; color:var(--muted); font-weight:600; padding:6px 10px; border-bottom:1px solid var(--ink); }}
.body td {{ padding:8px 10px; border-bottom:1px solid var(--rule); vertical-align:top; }}
.tbl {{ overflow-x:auto; }}
.note {{ display:flex; flex-direction:column; gap:2px; margin:18px 0; padding:12px 16px; background:var(--soft); border-top:2px solid var(--main); font-size:14px; max-width:640px; }}
.note p {{ margin:0; }}
.fig {{ margin:16px 0 20px; padding:14px 16px; border:1px dashed var(--muted); color:var(--muted); font-size:13.5px; max-width:640px; }}
.fig p {{ margin:4px 0 0; color:var(--ink); }}
.step {{ display:flex; gap:10px; align-items:flex-start; }}
.sn {{ color:var(--main); font-weight:700; flex-shrink:0; }}
.prob, .ans {{ display:flex; flex-wrap:wrap; gap:0 10px; align-items:baseline; padding-top:10px; border-top:1px solid var(--rule); max-width:640px; }}
.pn {{ width:24px; height:24px; background:var(--main); color:#fff; display:inline-flex; align-items:center; justify-content:center; font-family:var(--label); font-weight:800; font-size:12px; flex-shrink:0; align-self:flex-start; margin-top:4px; }}
.ans .pn {{ background:transparent; color:var(--main); border:2px solid var(--main); }}
.map {{ display:flex; flex-wrap:wrap; gap:8px 10px; align-items:center; }} .map .pn {{ margin-top:0; align-self:center; }}
.qs {{ display:flex; flex-direction:column; gap:6px; margin-bottom:14px; }} .q {{ margin:0 !important; }}
.box {{ display:inline-block; width:14px; height:14px; border:1.5px solid var(--ink); vertical-align:-2px; margin-right:8px; }}
details.answers {{ margin-top:40px; }}
details.answers summary {{ list-style:none; cursor:pointer; display:flex; align-items:center; gap:14px; }}
details.answers summary::-webkit-details-marker {{ display:none; }}
details.answers summary h2 {{ margin:0; padding-top:22px; border-top:1px solid var(--rule); flex:1; }}
.hint {{ font-size:12px; color:var(--muted); padding-top:22px; }}
details[open] .hint {{ display:none; }}
.abody {{ padding-top:8px; }}
.abody .ans .pn {{ margin-top:6px; }}
@media (max-width:820px) {{ .wrap {{ grid-template-columns:1fr; gap:28px; }} nav {{ position:static; flex-direction:row; flex-wrap:wrap; gap:6px; }} .brand {{ width:100%; }} .navhead {{ display:none; }} .nv {{ grid-template-columns:auto; gap:4px; border:1px solid var(--rule); }} .nv span:last-child {{ display:none; }} }}
</style>
<div class="bar"></div>
<div class="wrap">
  <nav>
    <div class="brand"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 2 L23 21 L1 21 Z M12 8.5 L17.6 18 L6.4 18 Z" fill-rule="evenodd" fill="currentColor"/></svg>델타 물리학 · 원고</div>
    <div class="navhead">초고</div>
    {nav}
  </nav>
  <main>{sections}</main>
</div>
'''
page = page.replace('<table>', '<div class="tbl"><table>').replace('</table>', '</table></div>')
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'design', 'reader.html')
open(out, 'w', encoding='utf-8').write(page)
print('reader ->', out, f'({len(units)} units)')
