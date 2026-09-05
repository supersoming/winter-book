# -*- coding: utf-8 -*-
"""내지 페이지와 마크 시트 생성기. 실행하면 design/canvas/*.dc.html 을 다시 쓴다."""
import os
OUT = os.path.join(os.path.dirname(__file__), 'canvas')

SPEC = ['#FF3B3B', '#FF8A00', '#FFD600', '#22C55E', '#06B6D4', '#2563EB', '#8B5CF6']
AREAS = {
    'E': dict(name='힘과 에너지', rng='Δ01–08', g='linear-gradient(135deg, #FF3B3B, #FF8A00)', main='#FF5A36', tint='#FFF1EC', c1='#FF3B3B', c2='#FF8A00'),
    'M': dict(name='전기와 자기', rng='Δ09–12', g='linear-gradient(135deg, #16A34A, #84CC16)', main='#16A34A', tint='#EEFBF2', c1='#16A34A', c2='#84CC16'),
    'L': dict(name='빛과 물질',   rng='Δ13–15', g='linear-gradient(135deg, #2563EB, #8B5CF6)', main='#6D4AED', tint='#F1EEFF', c1='#2563EB', c2='#8B5CF6'),
}
FONT = "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@300;400;500;600;700&family=Syne:wght@500;700;800&display=swap\">"
SYNE = "'Syne', 'IBM Plex Sans KR', sans-serif"
BAR = "linear-gradient(90deg, #FF3B3B 0 14.28%, #FF8A00 14.28% 28.57%, #FFD600 28.57% 42.85%, #22C55E 42.85% 57.14%, #06B6D4 57.14% 71.42%, #2563EB 71.42% 85.71%, #8B5CF6 85.71% 100%)"

# ---------- 글리프 (24x24, stroke=currentColor) ----------
def glyph(kind, color='#FFFFFF', size=24, spectrum=False):
    s = f'stroke="{color}" stroke-width="2" fill="none" stroke-linejoin="round" stroke-linecap="round"'
    inner = {
        'mark':    f'<path d="M12 3 L21 19 L3 19 Z" {s}></path><path d="M1 11 H8" {s}></path><path d="M15.5 11 L23 7.5 M15.5 11 L23 11 M15.5 11 L23 14.5" {s} stroke-width="1.6"></path>',
        'start':   f'<path d="M12 2.5 L19.5 16 L4.5 16 Z" {s}></path><path d="M2 21 H22" {s}></path><circle cx="4.5" cy="21" r="2" fill="{color}" stroke="none"></circle>',
        'concept': f'<path d="M13 4 L22 20 L4 20 Z" {s}></path><path d="M0.5 12 H9" {s} stroke-width="2.6"></path>',
        'example': f'<path d="M10 4 L19 20 L1 20 Z" {s}></path><path d="M14 12 L23.5 6.5 M14 12 L23.5 12 M14 12 L23.5 17.5" {s} stroke-width="1.8"></path>',
        'practice':f'<path d="M7 3 L12 11.5 L2 11.5 Z" {s} stroke-width="1.8"></path><path d="M17 3 L22 11.5 L12 11.5 Z" {s} stroke-width="1.8"></path><path d="M12 12.5 L17 21 L7 21 Z" {s} stroke-width="1.8"></path>',
        'check':   f'<path d="M12 2.5 L21.5 19.5 L2.5 19.5 Z" {s}></path><path d="M8.5 14 L11 16.5 L16 10.5" {s} stroke-width="2.4"></path>',
    }
    if kind == 'weekly':
        bands = ''.join(f'<rect x="0" y="{2+i*2.6:.1f}" width="24" height="2.7" fill="{SPEC[i]}"></rect>' for i in range(7))
        inner = f'<defs><clipPath id="wk{size}"><path d="M12 2 L22 20 L2 20 Z"></path></clipPath></defs><g clip-path="url(#wk{size})">{bands}</g>'
    else:
        inner = inner[kind]
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" aria-hidden="true" style="display: block; flex-shrink: 0;">{inner}</svg>'

def badge(kind, area, label, size=28, gsize=18):
    a = AREAS[area]
    bg = '#0B0B0F' if kind == 'weekly' else a['g']
    return (f'<div style="display: inline-flex; align-items: center; gap: 8px;">'
            f'<div style="width: {size}px; height: {size}px; background: {bg}; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">{glyph(kind, size=gsize)}</div>'
            f'<div style="font-size: {int(size*0.54)}px; font-weight: 700; color: #0B0B0F; letter-spacing: -0.01em;">{label}</div></div>')

def numbadge(n, area, size=28):
    a = AREAS[area]
    return (f'<div style="width: {size}px; height: {size}px; background: {a["g"]}; color: #FFFFFF; display: flex; align-items: center; justify-content: center; '
            f'font-family: {SYNE}; font-size: {int(size*0.58)}px; font-weight: 800; flex-shrink: 0;">{n}</div>')

def stepnum(n, area, size=22):
    a = AREAS[area]
    return (f'<div style="width: {size}px; height: {size}px; border: 2px solid {a["main"]}; border-radius: 50%; color: {a["main"]}; display: flex; align-items: center; justify-content: center; '
            f'font-family: {SYNE}; font-size: {int(size*0.5)}px; font-weight: 800; flex-shrink: 0; box-sizing: border-box;">{n}</div>')

def difficulty(level, area, size=12):
    a = AREAS[area]
    tris = ''
    for i in range(3):
        fill = a['main'] if i < level else 'none'
        stroke = a['main'] if i < level else '#C8C8C8'
        tris += f'<svg viewBox="0 0 12 12" width="{size}" height="{size}" aria-hidden="true" style="display: block;"><path d="M6 1.5 L11 10.5 L1 10.5 Z" fill="{fill}" stroke="{stroke}" stroke-width="1.3" stroke-linejoin="round"></path></svg>'
    return f'<div style="display: flex; gap: 3px; align-items: center;">{tris}</div>'

def topbar(): return f'<div style="height: 10px; margin: 0 -52px 0 -52px; background: {BAR}; flex-shrink: 0;"></div>'

def page(body, w=710, h=971, pad='0 52px 40px 52px', bg='#FFFFFF', extra_style=''):
    return f'''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  {FONT}
  <style>
    body {{ margin: 0; font-family: "IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif; }}
    a {{ color: #0B0B0F; }} a:hover {{ color: #2563EB; }}
  </style>
</helmet>
<div style="position: relative; width: {w}px; height: {h}px; background: {bg}; color: #0B0B0F; box-sizing: border-box; padding: {pad}; display: flex; flex-direction: column; gap: 0; overflow: hidden; {extra_style}">
{body}
</div>
</x-dc>
</body>
</html>
'''

def runhead(left, right, area):
    a = AREAS[area]
    return (f'<div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; letter-spacing: 0.08em; color: #555555; padding: 30px 0 10px 0; border-bottom: 1px solid #E5E5E5;">'
            f'<div><span style="font-family: {SYNE}; font-weight: 700; color: {a["main"]};">{left[0]}</span> {left[1]}</div><div style="font-family: {SYNE}; letter-spacing: 0.2em; font-weight: 700;">{right}</div></div>')

def foot(pn):
    return (f'<div style="margin-top: auto; display: flex; justify-content: space-between; font-size: 11px; color: #555555; padding-top: 10px; border-top: 1px solid #E5E5E5;">'
            f'<div>델타 물리학 · 겨울</div><div style="font-family: {SYNE}; font-weight: 700;">{pn}</div></div>')

W = lambda name, html: open(os.path.join(OUT, name), 'w', encoding='utf-8').write(html)

# ================= 1. 마크 시트 =================
def marks_sheet():
    def cell(title, sub, content):
        return (f'<div style="display: flex; flex-direction: column; gap: 10px;"><div style="display: flex; flex-direction: column; gap: 2px;">'
                f'<div style="font-size: 13px; font-weight: 700;">{title}</div><div style="font-size: 11px; color: #555555; line-height: 1.5;">{sub}</div></div>{content}</div>')
    # 마스터 마크 3종
    master = f'''
    <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px;">
      <div style="height: 120px; background: #0B0B0F; display: flex; align-items: center; justify-content: center;">{glyph('mark', size=64)}</div>
      <div style="height: 120px; background: #FFFFFF; border: 1px solid #E5E5E5; box-sizing: border-box; display: flex; align-items: center; justify-content: center;">{glyph('mark', color='#0B0B0F', size=64)}</div>
      <div style="height: 120px; background: {AREAS['E']['g']}; display: flex; align-items: center; justify-content: center;">{glyph('mark', size=64)}</div>
      <div style="height: 120px; background: #FFFFFF; border: 1px solid #E5E5E5; box-sizing: border-box; display: flex; align-items: center; justify-content: center; gap: 14px;">{glyph('mark', color='#0B0B0F', size=40)}{glyph('mark', color='#0B0B0F', size=24)}{glyph('mark', color='#0B0B0F', size=16)}</div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; font-size: 11px; color: #555555;">
      <div>검정 바탕 · 흰색</div><div>흰 바탕 · 검정 1도</div><div>영역 그라데이션 위</div><div>최소 크기 16px (인쇄 4 mm)</div>
    </div>'''
    # 워드마크
    wordmark = f'''
    <div style="display: flex; align-items: center; gap: 28px; padding: 22px 24px; border: 1px solid #E5E5E5;">
      <div style="display: flex; align-items: center; gap: 12px;">{glyph('mark', color='#0B0B0F', size=44)}<div style="font-size: 30px; font-weight: 700; letter-spacing: -0.02em;">델타 물리학</div></div>
      <div style="width: 1px; height: 44px; background: #E5E5E5;"></div>
      <div style="display: flex; align-items: center; gap: 12px;">{glyph('mark', color='#0B0B0F', size=44)}<div style="font-family: {SYNE}; font-size: 22px; font-weight: 800; letter-spacing: 0.12em;">DELTA PHYSICS</div></div>
      <div style="width: 1px; height: 44px; background: #E5E5E5;"></div>
      <div style="display: flex; align-items: center; gap: 8px;">{glyph('mark', color='#0B0B0F', size=20)}<div style="font-size: 12px; font-weight: 700;">델타 물리학 · 겨울</div></div>
    </div>'''
    # 코너 배지 6종 × 영역 3색
    rows = ''
    for area in ['E', 'M', 'L']:
        a = AREAS[area]
        rows += (f'<div style="display: grid; grid-template-columns: 120px repeat(6, minmax(0, 1fr)); gap: 12px; align-items: center; padding: 12px 0; border-bottom: 1px solid #E5E5E5;">'
                 f'<div style="font-size: 12px; font-weight: 700;">{a["name"]}<div style="font-family: {SYNE}; font-weight: 700; font-size: 10px; color: {a["main"]};">{a["rng"]}</div></div>'
                 + badge('start', area, 'Δ0 출발선') + badge('concept', area, 'Δ개념') + badge('example', area, 'Δ예제')
                 + badge('practice', area, 'Δ연습') + badge('check', area, 'Δ체크') + badge('weekly', area, '주간 Δ') + '</div>')
    corners = f'<div style="display: flex; flex-direction: column; border-top: 2px solid #0B0B0F;">{rows}</div>'
    # 글리프 의미
    meaning = f'''
    <div style="display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 12px; font-size: 11px; line-height: 1.5; color: #555555;">
      <div><span style="font-weight: 700; color: #0B0B0F;">출발선</span> 프리즘 아래 출발선과 점. 아직 빛이 들어가기 전.</div>
      <div><span style="font-weight: 700; color: #0B0B0F;">개념</span> 백색광 한 줄기가 프리즘으로 들어간다.</div>
      <div><span style="font-weight: 700; color: #0B0B0F;">예제</span> 빛이 갈라져 나온다. 개념이 풀이로 펼쳐진다.</div>
      <div><span style="font-weight: 700; color: #0B0B0F;">연습</span> 프리즘 셋. 반복.</div>
      <div><span style="font-weight: 700; color: #0B0B0F;">체크</span> 프리즘 안에 체크.</div>
      <div><span style="font-weight: 700; color: #0B0B0F;">주간 Δ</span> 7색 띠로 채워진 프리즘. 검정 바탕 고정.</div>
    </div>'''
    # 번호 배지
    nums = ''
    for area in ['E', 'M', 'L']:
        nums += (f'<div style="display: flex; align-items: center; gap: 14px;">'
                 f'<div style="display: flex; align-items: center; gap: 8px;">{badge("concept", area, "Δ개념")}{numbadge(1, area)}</div>'
                 f'{numbadge(2, area)}{numbadge(3, area)}{numbadge(4, area)}'
                 f'<div style="width: 1px; height: 28px; background: #E5E5E5;"></div>'
                 f'<div style="display: flex; gap: 6px;">{stepnum(1, area)}{stepnum(2, area)}{stepnum(3, area)}</div>'
                 f'<div style="width: 1px; height: 28px; background: #E5E5E5;"></div>'
                 f'<div style="display: flex; gap: 10px;">{difficulty(1, area)}{difficulty(2, area)}{difficulty(3, area)}</div>'
                 f'<div style="width: 1px; height: 28px; background: #E5E5E5;"></div>'
                 f'<div style="font-family: {SYNE}; font-size: 40px; font-weight: 800; line-height: 1; background: {AREAS[area]["g"]}; -webkit-background-clip: text; background-clip: text; color: transparent;">{ {"E":"Δ03","M":"Δ09","L":"Δ13"}[area] }</div>'
                 f'</div>')
    numbers = f'<div style="display: flex; flex-direction: column; gap: 14px;">{nums}</div>'
    numbers_sub = ('<div style="display: grid; grid-template-columns: 1.2fr 0.8fr 0.9fr 0.5fr; gap: 12px; font-size: 11px; color: #555555; line-height: 1.5;">'
                   '<div><span style="font-weight: 700; color: #0B0B0F;">개념 번호 1·2·3</span> 코너 배지 뒤에 붙는 정사각 번호. 단원 지도와 본문 헤더에 같은 것을 쓴다.</div>'
                   '<div><span style="font-weight: 700; color: #0B0B0F;">풀이 단계 번호</span> 원형 외곽선. 예제 풀이 각 단계 앞.</div>'
                   '<div><span style="font-weight: 700; color: #0B0B0F;">난이도 ▲</span> 연습 문제 번호 옆. 채운 개수 1~3.</div>'
                   '<div><span style="font-weight: 700; color: #0B0B0F;">단원 번호</span> 영역 그라데이션 글자.</div></div>')
    body = f'''
  <div style="display: flex; flex-direction: column; gap: 6px; padding-top: 40px;">
    <div style="font-size: 22px; font-weight: 700;">로고 · 마크 체계</div>
    <div style="font-size: 13px; line-height: 1.6; color: #555555;">마스터 마크 하나(프리즘 + 들어오는 빛 + 나가는 빛 3줄)에서 코너 글리프 6종이 파생된다. 배지 바탕은 그 단원이 속한 영역의 그라데이션, 글리프는 항상 흰색 선. 주간 Δ만 검정 바탕 고정.</div>
  </div>
  <div style="display: flex; flex-direction: column; gap: 28px; padding-top: 24px;">
    {cell('1. 마스터 마크', '표지 뒷면, 책등, 판권, 워크북 등 모든 곳에 쓰는 기본형.', master)}
    {cell('2. 워드마크', '마크 + 글자 조합. 세 가지 크기.', wordmark)}
    {cell('3. 코너 배지 6종 × 영역 3색', '모든 코너 헤더는 이 배지로 시작한다.', corners + meaning)}
    {cell('4. 번호 체계', '개념 번호, 풀이 단계, 난이도, 단원 번호.', numbers + numbers_sub)}
  </div>'''
    W('Marks.dc.html', page(body, w=1000, h=1120, pad='0 40px 40px 40px'))

# ================= 2. 목차 =================
def contents():
    units = [('E', [('Δ00','출발선 · 벡터, 단위, 그래프 읽기'),('Δ01','운동의 표현'),('Δ02','등가속도 운동과 그래프'),('Δ03','뉴턴 운동 법칙'),('Δ04','운동 법칙의 적용'),('Δ05','평형과 안정성'),('Δ06','운동량과 충격량'),('Δ07','일과 역학적 에너지'),('Δ08','열과 에너지')]),
             ('M', [('Δ09','전기장과 전위'),('Δ10','전류와 전기 회로'),('Δ11','전류의 자기 작용'),('Δ12','전자기 유도와 전자기파')]),
             ('L', [('Δ13','파동과 빛의 성질'),('Δ14','빛과 물질의 이중성'),('Δ15','원자와 에너지 준위')])]
    blocks = ''
    for area, lst in units:
        a = AREAS[area]
        items = ''.join(f'<div style="display: flex; align-items: baseline; gap: 12px; padding: 5px 0;"><div style="font-family: {SYNE}; font-size: 12px; font-weight: 700; color: {a["main"]}; width: 40px;">{u}</div><div style="font-size: 13.5px; font-weight: 500;">{t}</div><div style="flex-grow: 1; border-bottom: 1px dotted #C8C8C8; margin: 0 4px 3px 4px;"></div><div style="font-family: {SYNE}; font-size: 11px; color: #555555; width: 22px; text-align: right;">[p]</div></div>' for u, t in lst)
        blocks += (f'<div style="display: flex; flex-direction: column; gap: 6px;">'
                   f'<div style="display: flex; align-items: center; gap: 12px; padding-bottom: 8px; border-bottom: 3px solid transparent; border-image: {a["g"]} 1;">'
                   f'<div style="font-family: {SYNE}; font-size: 12px; font-weight: 800; letter-spacing: 0.1em; color: {a["main"]};">{a["rng"]}</div><div style="font-size: 17px; font-weight: 700;">{a["name"]}</div></div>'
                   f'<div style="display: flex; flex-direction: column;">{items}</div></div>')
    body = f'''
  {topbar()}
  <div style="display: flex; justify-content: space-between; align-items: flex-end; padding: 34px 0 18px 0; border-bottom: 2px solid #0B0B0F;">
    <div style="display: flex; flex-direction: column; gap: 6px;"><div style="font-family: {SYNE}; font-size: 11px; letter-spacing: 0.24em; font-weight: 800; color: #555555;">CONTENTS</div><div style="font-size: 30px; font-weight: 700; letter-spacing: -0.02em;">차례</div></div>
    <div style="display: flex; align-items: center; gap: 8px;">{glyph('mark', color='#0B0B0F', size=22)}<div style="font-size: 12px; font-weight: 700;">15 UNITS / 10 WEEKS</div></div>
  </div>
  <div style="display: flex; flex-direction: column; gap: 22px; padding-top: 20px;">
    <div style="display: flex; align-items: center; gap: 12px; padding: 10px 0;"><div style="display: flex; gap: 8px;">{badge('weekly','E','주간 Δ')}</div><div style="flex-grow: 1; border-bottom: 1px dotted #C8C8C8;"></div><div style="font-family: {SYNE}; font-size: 11px; color: #555555;">[p]</div></div>
    {blocks}
  </div>
  {foot('3')}'''
    W('Contents.dc.html', page(body))

# ================= 3. 주간 Δ =================
def weekly():
    cols = ['#8B5CF6','#6D5BF0','#2563EB','#06B6D4','#22C55E','#84CC16','#FFD600','#FF8A00','#FF5A36','#FF3B3B']
    rows = ''
    for i in range(10):
        rows += (f'<div style="display: grid; grid-template-columns: 64px 1.3fr 0.7fr 1.6fr; gap: 0; border-bottom: 1px solid #E5E5E5; height: 58px;">'
                 f'<div style="background: {cols[i]}; color: {"#0B0B0F" if i in (6,) else "#FFFFFF"}; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: {SYNE}; font-weight: 800;"><div style="font-size: 9px; letter-spacing: 0.16em;">WEEK</div><div style="font-size: 20px; line-height: 1;">{i+1:02d}</div></div>'
                 f'<div style="border-right: 1px solid #E5E5E5;"></div><div style="border-right: 1px solid #E5E5E5;"></div><div></div></div>')
    body = f'''
  {topbar()}
  <div style="display: flex; justify-content: space-between; align-items: flex-end; padding: 34px 0 16px 0; border-bottom: 2px solid #0B0B0F;">
    <div style="display: flex; flex-direction: column; gap: 10px;">{badge('weekly','E','주간 Δ')}<div style="font-size: 28px; font-weight: 700; letter-spacing: -0.02em;">10주 변화량 기록</div></div>
    <div style="font-size: 12px; line-height: 1.6; color: #555555; text-align: right; width: 250px;">매주 마지막 수업이 끝나면 적는다.<br>10주가 지나면 이 표가 무지개가 된다.</div>
  </div>
  <div style="display: grid; grid-template-columns: 64px 1.3fr 0.7fr 1.6fr; gap: 0; padding: 10px 0 6px 0; font-size: 11px; letter-spacing: 0.06em; color: #555555; font-weight: 600;">
    <div></div><div style="padding-left: 10px;">끝낸 단원</div><div style="padding-left: 10px;">틀린 문제 수</div><div style="padding-left: 10px;">한 줄 Δ (이번 주 달라진 것)</div>
  </div>
  <div style="display: flex; flex-direction: column; border-top: 1px solid #0B0B0F;">{rows}</div>
  <div style="display: flex; align-items: center; gap: 10px; padding-top: 14px; font-size: 12px; color: #555555;">{glyph('mark', color='#0B0B0F', size=18)}<div>Δ00부터 Δ15까지, 색이 보라에서 빨강으로 바뀌는 동안 당신도 바뀐다.</div></div>
  {foot('6')}'''
    W('Weekly.dc.html', page(body))

# ================= 4. 단원 도입 (Δ03) =================
def opener():
    area = 'E'; a = AREAS[area]
    q = lambda n, t: (f'<div style="display: flex; gap: 12px; align-items: flex-start; font-size: 14px; line-height: 1.6;">'
                      f'<div style="width: 16px; height: 16px; border: 1.5px solid #0B0B0F; flex-shrink: 0; margin-top: 4px;"></div>'
                      f'<div><span style="font-family: {SYNE}; font-weight: 700; color: {a["main"]};">{n}</span>&nbsp; {t}</div></div>')
    body = f'''
  {topbar()}
  {runhead(('Δ03','힘과 에너지 · 3 / 8'), 'WEEK 2', area)}
  <div style="display: flex; flex-direction: column; gap: 4px; padding: 26px 0 22px 0; border-bottom: 2px solid #0B0B0F;">
    <div style="font-family: {SYNE}; font-size: 104px; line-height: 0.9; font-weight: 800; letter-spacing: -0.02em; background: {a["g"]}; -webkit-background-clip: text; background-clip: text; color: transparent;">Δ03</div>
    <div style="font-size: 34px; font-weight: 700; line-height: 1.2; letter-spacing: -0.01em; padding-top: 12px;">뉴턴 운동 법칙</div>
    <div style="font-size: 15px; line-height: 1.6; color: #555555;">힘은 물체를 움직이는 것이 아니라, 속도를 바꾸는 것이다.</div>
  </div>
  <div style="display: flex; flex-direction: column; gap: 14px; padding-top: 22px;">
    <div style="display: flex; align-items: center; gap: 12px;">{badge('start', area, 'Δ0 출발선')}<div style="font-size: 12px; color: #555555;">시작하기 전에, 지금 아는 만큼만 답한다</div></div>
    <div style="display: flex; flex-direction: column; gap: 10px;">
      {q(1, '책상 위에 놓인 책은 정지해 있다. 책에 작용하는 힘은 없는가, 아니면 있는데 합이 0인가?')}
      {q(2, '같은 힘으로 밀 때 2 kg 수레와 4 kg 수레의 가속도 비는 얼마인가?')}
      {q(3, '말이 수레를 당기는 힘과 수레가 말을 당기는 힘의 크기가 같다면, 수레는 왜 앞으로 가는가?')}
    </div>
  </div>
  <div style="display: flex; flex-direction: column; gap: 12px; padding-top: 24px;">
    <div style="display: flex; align-items: center; gap: 10px;"><div style="font-size: 16px; font-weight: 700;">이 단원의 Δ</div></div>
    <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0; border-top: 1px solid #0B0B0F; border-bottom: 1px solid #0B0B0F;">
      <div style="padding: 12px 14px 12px 0; border-right: 1px solid #E5E5E5; display: flex; flex-direction: column; gap: 8px;">
        <div style="font-size: 11px; letter-spacing: 0.08em; color: #555555; font-weight: 600;">단원 전</div>
        <div style="font-size: 13px; line-height: 1.6;">힘이 있어야 물체가 움직인다.</div>
        <div style="font-size: 13px; line-height: 1.6;">무거운 물체가 더 빨리 떨어진다.</div>
        <div style="font-size: 13px; line-height: 1.6;">작용과 반작용은 서로 상쇄된다.</div>
      </div>
      <div style="padding: 12px 0 12px 14px; display: flex; flex-direction: column; gap: 8px;">
        <div style="font-size: 11px; letter-spacing: 0.08em; color: {a["main"]}; font-weight: 600;">단원 후 (Δ체크에서 직접 채운다)</div>
        <div style="height: 21px; border-bottom: 1px dashed #F5B9A8;"></div><div style="height: 21px; border-bottom: 1px dashed #F5B9A8;"></div><div style="height: 21px; border-bottom: 1px dashed #F5B9A8;"></div>
      </div>
    </div>
  </div>
  <div style="display: flex; flex-direction: column; gap: 10px; margin-top: auto;">
    <div style="font-size: 11px; letter-spacing: 0.08em; color: #555555; font-weight: 600;">단원 지도</div>
    <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px;">
      <div style="display: flex; flex-direction: column; gap: 8px; padding-top: 10px; border-top: 3px solid transparent; border-image: {a["g"]} 1;"><div style="display: flex; align-items: center; gap: 8px;">{numbadge(1, area, 24)}<div style="font-size: 14px; font-weight: 700;">관성 법칙</div></div></div>
      <div style="display: flex; flex-direction: column; gap: 8px; padding-top: 10px; border-top: 3px solid transparent; border-image: {a["g"]} 1;"><div style="display: flex; align-items: center; gap: 8px;">{numbadge(2, area, 24)}<div style="font-size: 14px; font-weight: 700;">가속도 법칙</div></div></div>
      <div style="display: flex; flex-direction: column; gap: 8px; padding-top: 10px; border-top: 3px solid transparent; border-image: {a["g"]} 1;"><div style="display: flex; align-items: center; gap: 8px;">{numbadge(3, area, 24)}<div style="font-size: 14px; font-weight: 700;">작용 반작용 법칙</div></div></div>
    </div>
  </div>
  {foot('38')}'''
    W('Opener.dc.html', page(body))

# ================= 5. 개념 페이지 =================
def concept():
    area = 'E'; a = AREAS[area]
    step = lambda n, t: f'<div style="display: flex; gap: 10px; font-size: 13px; line-height: 1.65; align-items: flex-start;">{stepnum(n, area)}<div style="padding-top: 1px;">{t}</div></div>'
    body = f'''
  {topbar()}
  {runhead(('Δ03','뉴턴 운동 법칙'), 'Δ개념 2', area)}
  <div style="display: flex; gap: 26px; flex-grow: 1; padding-top: 22px;">
    <div style="display: flex; flex-direction: column; gap: 18px; flex-grow: 1; min-width: 0;">
      <div style="display: flex; flex-direction: column; gap: 10px;">
        <div style="display: flex; align-items: center; gap: 8px;">{badge('concept', area, 'Δ개념')}{numbadge(2, area)}</div>
        <div style="font-size: 26px; font-weight: 700; letter-spacing: -0.01em;">가속도 법칙</div>
      </div>
      <div style="font-size: 14px; line-height: 1.75; text-wrap: pretty;">물체에 알짜힘이 작용하면 물체는 알짜힘의 방향으로 가속된다. 가속도의 크기는 알짜힘에 비례하고 질량에 반비례한다. 여기서 "움직인다"가 아니라 "속도가 변한다"는 점이 핵심이다. 힘이 0이면 속도는 변하지 않을 뿐, 물체가 멈추는 것이 아니다.</div>
      <div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 20px; background: {a["tint"]}; border-top: 3px solid transparent; border-image: {a["g"]} 1;">
        <div style="font-size: 11px; letter-spacing: 0.08em; color: #555555; font-weight: 600;">정의</div>
        <div style="display: flex; align-items: center; gap: 24px;">
          <div style="font-family: {SYNE}; font-size: 30px; font-weight: 700;"><i>F</i> = <i>ma</i></div>
          <div style="font-size: 12px; line-height: 1.6; color: #555555;"><i>F</i> 알짜힘 [N] · <i>m</i> 질량 [kg] · <i>a</i> 가속도 [m/s²]</div>
        </div>
        <div style="font-size: 13px; line-height: 1.6;">1 N은 1 kg의 물체에 1 m/s²의 가속도를 만드는 힘이다.</div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 12px; border: 3px solid transparent; background: linear-gradient(#fff, #fff) padding-box, {a["g"]} border-box; padding: 16px 20px;">
        <div style="display: flex; align-items: center; gap: 10px;">{badge('example', area, 'Δ예제')}<div style="font-size: 14px; font-weight: 700;">두 물체를 함께 밀 때</div><div style="margin-left: auto;">{difficulty(2, area)}</div></div>
        <div style="font-size: 13.5px; line-height: 1.7;">마찰이 없는 수평면에 질량 2 kg인 물체 A와 3 kg인 물체 B가 맞닿아 놓여 있다. A를 10 N의 힘으로 B 쪽으로 밀 때, 두 물체의 가속도와 A가 B를 미는 힘의 크기를 구하시오.</div>
        <div style="display: flex; flex-direction: column; gap: 8px; padding-top: 10px; border-top: 1px dashed #F5B9A8;">
          {step(1, 'A와 B를 한 덩어리로 본다. 전체 질량 5 kg, 알짜힘 10 N이므로 <i>a</i> = 10 / 5 = 2 m/s².')}
          {step(2, 'B만 따로 본다. B에 작용하는 알짜힘은 A가 미는 힘뿐이다. <i>F</i> = 3 × 2 = 6 N.')}
          {step(3, '확인: A에는 10 N과 B가 미는 반작용 6 N이 반대로 작용하므로 알짜힘 4 N, 2 × 2 = 4 N. 맞다.')}
        </div>
      </div>
    </div>
    <div style="width: 150px; flex-shrink: 0; display: flex; flex-direction: column; gap: 18px; padding-top: 6px; border-left: 1px solid #E5E5E5; padding-left: 18px;">
      <div style="display: flex; flex-direction: column; gap: 6px;"><div style="display: flex; align-items: center; gap: 6px;">{glyph('mark', color=a['main'], size=14)}<div style="font-size: 10px; letter-spacing: 0.08em; color: #555555; font-weight: 600;">Δ메모</div></div><div style="font-size: 12px; line-height: 1.6;">"알짜힘"은 그 물체에 작용하는 모든 힘의 합. 계를 어떻게 잡느냐에 따라 알짜힘이 달라진다.</div></div>
      <div style="display: flex; flex-direction: column; gap: 6px;"><div style="font-size: 10px; letter-spacing: 0.08em; color: #555555; font-weight: 600;">자주 틀리는 곳</div><div style="font-size: 12px; line-height: 1.6;">B에 10 N이 그대로 전달된다고 생각하는 것. 힘은 "전달"되지 않고 각 물체마다 새로 따진다.</div></div>
      <div style="display: flex; flex-direction: column; gap: 6px;"><div style="font-size: 10px; letter-spacing: 0.08em; color: #555555; font-weight: 600;">연결</div><div style="font-size: 12px; line-height: 1.6;"><span style="font-family: {SYNE}; font-weight: 700; color: {a["main"]};">Δ04</span> 도르래·빗면에서 같은 방법으로 계를 나눈다.</div></div>
    </div>
  </div>
  {foot('41')}'''
    W('Concept.dc.html', page(body))

# ================= 6. 연습 =================
def practice():
    area = 'E'; a = AREAS[area]
    def prob(n, lvl, text, lines=3):
        blanks = ''.join('<div style="height: 22px; border-bottom: 1px solid #E5E5E5;"></div>' for _ in range(lines))
        return (f'<div style="display: flex; flex-direction: column; gap: 10px; padding: 14px 0; border-bottom: 1px solid #E5E5E5;">'
                f'<div style="display: flex; align-items: center; gap: 10px;">{numbadge(n, area, 24)}{difficulty(lvl, area)}</div>'
                f'<div style="font-size: 13.5px; line-height: 1.7;">{text}</div>{blanks}</div>')
    body = f'''
  {topbar()}
  {runhead(('Δ03','뉴턴 운동 법칙'), 'Δ연습', area)}
  <div style="display: flex; align-items: center; justify-content: space-between; padding: 22px 0 14px 0;">
    <div style="display: flex; align-items: center; gap: 12px;">{badge('practice', area, 'Δ연습')}<div style="font-size: 12px; color: #555555;">▲ 기본 · ▲▲ 표준 · ▲▲▲ 도전</div></div>
    <div style="font-size: 11px; color: #555555;">정답과 풀이 [p]</div>
  </div>
  <div style="display: flex; flex-direction: column; border-top: 2px solid #0B0B0F;">
    {prob(1, 1, '질량 4 kg인 물체에 12 N의 알짜힘이 작용한다. 가속도의 크기를 구하시오.', 2)}
    {prob(2, 1, '정지해 있던 2 kg 물체에 일정한 힘을 3초 동안 작용했더니 속력이 9 m/s가 되었다. 힘의 크기를 구하시오.', 2)}
    {prob(3, 2, '마찰이 없는 수평면에서 질량 1 kg인 A와 2 kg인 B를 실로 연결하고 B를 6 N으로 당긴다. 두 물체의 가속도와 실의 장력을 구하시오.', 3)}
    {prob(4, 3, '엘리베이터 바닥에 놓인 저울 위에 50 kg인 사람이 서 있다. 엘리베이터가 위로 2 m/s²로 가속할 때와 아래로 2 m/s²로 가속할 때 저울의 눈금(N)을 각각 구하고, 두 경우 사람에게 작용하는 힘을 화살표로 그리시오. (g = 10 m/s²)', 4)}
  </div>
  {foot('44')}'''
    W('Practice.dc.html', page(body))

# ================= 7. 체크 =================
def check():
    area = 'E'; a = AREAS[area]
    q = lambda n, t: (f'<div style="display: flex; flex-direction: column; gap: 6px; padding: 10px 0; border-bottom: 1px solid #E5E5E5;">'
                      f'<div style="display: flex; gap: 10px; font-size: 13.5px; line-height: 1.6;"><span style="font-family: {SYNE}; font-weight: 700; color: {a["main"]};">{n}</span><div>{t}</div></div>'
                      f'<div style="height: 22px; border-bottom: 1px solid #E5E5E5; margin-left: 20px;"></div></div>')
    body = f'''
  {topbar()}
  {runhead(('Δ03','뉴턴 운동 법칙'), 'Δ체크', area)}
  <div style="display: flex; align-items: center; gap: 12px; padding: 22px 0 14px 0;">{badge('check', area, 'Δ체크')}<div style="font-size: 12px; color: #555555;">출발선의 세 질문을 다시 푼다. 이번엔 이유까지.</div></div>
  <div style="display: flex; flex-direction: column; border-top: 2px solid #0B0B0F;">
    {q(1, '책상 위에 놓인 책은 정지해 있다. 책에 작용하는 힘은 없는가, 아니면 있는데 합이 0인가?')}
    {q(2, '같은 힘으로 밀 때 2 kg 수레와 4 kg 수레의 가속도 비는 얼마인가?')}
    {q(3, '말이 수레를 당기는 힘과 수레가 말을 당기는 힘의 크기가 같다면, 수레는 왜 앞으로 가는가?')}
  </div>
  <div style="display: flex; flex-direction: column; gap: 12px; padding-top: 24px;">
    <div style="font-size: 16px; font-weight: 700;">이 단원의 Δ · 단원 후</div>
    <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0; border-top: 1px solid #0B0B0F; border-bottom: 1px solid #0B0B0F;">
      <div style="padding: 12px 14px 12px 0; border-right: 1px solid #E5E5E5; display: flex; flex-direction: column; gap: 8px; color: #999999;">
        <div style="font-size: 11px; letter-spacing: 0.08em; font-weight: 600;">단원 전 (내가 믿었던 것)</div>
        <div style="font-size: 13px; line-height: 1.6;">힘이 있어야 물체가 움직인다.</div><div style="font-size: 13px; line-height: 1.6;">무거운 물체가 더 빨리 떨어진다.</div><div style="font-size: 13px; line-height: 1.6;">작용과 반작용은 서로 상쇄된다.</div>
      </div>
      <div style="padding: 12px 0 12px 14px; display: flex; flex-direction: column; gap: 8px;">
        <div style="font-size: 11px; letter-spacing: 0.08em; color: {a["main"]}; font-weight: 600;">단원 후 (지금 아는 것)</div>
        <div style="height: 21px; border-bottom: 1px solid #0B0B0F;"></div><div style="height: 21px; border-bottom: 1px solid #0B0B0F;"></div><div style="height: 21px; border-bottom: 1px solid #0B0B0F;"></div>
      </div>
    </div>
  </div>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; padding-top: 24px;">
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <div style="font-size: 12px; font-weight: 700;">틀린 연습 문제 번호</div>
      <div style="display: flex; gap: 8px;">{''.join(f'<div style="width: 34px; height: 34px; border: 1.5px solid #0B0B0F; display: flex; align-items: center; justify-content: center; font-family: {SYNE}; font-size: 12px; font-weight: 700; color: #BBBBBB;">{i}</div>' for i in range(1,7))}</div>
      <div style="font-size: 11px; color: #555555;">틀린 번호에 색을 칠한다.</div>
    </div>
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <div style="font-size: 12px; font-weight: 700;">이 단원의 나의 Δ</div>
      <div style="display: flex; gap: 12px; align-items: center;">
        {''.join(f'<svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true" style="display: block;"><path d="M12 3 L21.5 20 L2.5 20 Z" fill="none" stroke="#0B0B0F" stroke-width="1.6" stroke-linejoin="round"></path></svg>' for _ in range(3))}
        <div style="font-size: 11px; color: #555555; line-height: 1.5;">이해한 만큼 삼각형을 칠한다.<br>▲ 들었다 · ▲▲ 풀 수 있다 · ▲▲▲ 설명할 수 있다</div>
      </div>
    </div>
  </div>
  <div style="display: flex; flex-direction: column; gap: 8px; padding-top: 22px;">
    <div style="font-size: 12px; font-weight: 700;">한 줄 Δ</div>
    <div style="height: 26px; border-bottom: 1px solid #0B0B0F;"></div>
  </div>
  {foot('47')}'''
    W('Check.dc.html', page(body))

if __name__ == '__main__':
    marks_sheet(); contents(); weekly(); opener(); concept(); practice(); check()
    print('built')
