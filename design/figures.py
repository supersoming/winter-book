# -*- coding: utf-8 -*-
"""원고의 [그림 NN-k] 자리를 채우는 SVG 생성기. python3 design/figures.py → manuscript/figures/*.svg"""
import math, os
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'manuscript', 'figures')
INK = 'currentColor'
ROSE, SAGE, PERI = '#E07A95', '#5EAE88', '#8A84E2'
P_ROSE, P_SAGE, P_PERI, P_LEMON, P_SKY = '#FFB5C2', '#C6F0D6', '#DABDFF', '#FFF1B5', '#B5E6F7'
FONT = "font-family:'IBM Plex Sans KR','Apple SD Gothic Neo',sans-serif"

class C:
    def __init__(s, w, h, label=''):
        s.w, s.h, s.label, s.parts = w, h, label, []
    def add(s, x): s.parts.append(x); return s
    # 기본 도형
    def line(s, x1, y1, x2, y2, sw=1.6, color=INK, dash=None, arrow=False, arrow2=False, op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        m = ' marker-end="url(#ah)"' if arrow else ''
        m2 = ' marker-start="url(#ahs)"' if arrow2 else ''
        st = f' style="color:{color}"' if color != INK else ''
        return s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{d}{m}{m2} opacity="{op}"{st}/>')
    def vec(s, x1, y1, x2, y2, color=ROSE, sw=2.4, label=None, lx=0, ly=0, size=12):
        s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" marker-end="url(#ah)" style="color:{color}"/>')
        if label: s.text((x1+x2)/2+lx, (y1+y2)/2+ly, label, size=size, color=color, weight=700)
        return s
    def text(s, x, y, t, size=12, anchor='middle', color=INK, weight=400, italic=False, op=1, rotate=0):
        st = f"{FONT};font-size:{size}px;font-weight:{weight}" + (";font-style:italic" if italic else "")
        r = f' transform="rotate({rotate} {x} {y})"' if rotate else ''
        return s.add(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" dominant-baseline="middle" fill="{color}" style="{st}" opacity="{op}"{r}>{t}</text>')
    def rect(s, x, y, w, h, fill='none', stroke=INK, sw=1.6, rx=0, op=1, dash=None, color=None):
        if color: stroke = color
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}" opacity="{op}"{d}/>')
    def circle(s, x, y, r, fill='none', stroke=INK, sw=1.6, op=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"{d}/>')
    def poly(s, pts, fill='none', stroke=INK, sw=1.6, op=1, close=True, dash=None, color=None):
        if color: stroke = color
        p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        tag = 'polygon' if close else 'polyline'
        return s.add(f'<{tag} points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" opacity="{op}"{d}/>')
    def path(s, d, fill='none', stroke=INK, sw=1.6, op=1, dash=None, arrow=False, color=None):
        if color: stroke = color
        da = f' stroke-dasharray="{dash}"' if dash else ''
        m = ' marker-end="url(#ah)"' if arrow else ''
        st = f' style="color:{stroke}"' if stroke != INK else ''
        return s.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" opacity="{op}"{da}{m}{st}/>')
    # 부품
    def block(s, x, y, w, h, label='', fill=P_ROSE, size=12):
        s.rect(x, y, w, h, fill=fill, sw=1.4)
        if label: s.text(x+w/2, y+h/2, label, size=size, weight=600)
        return s
    def ground(s, x1, x2, y, hatch=True):
        s.line(x1, y, x2, y, sw=1.8)
        if hatch:
            for x in range(int(x1), int(x2), 12): s.line(x+8, y, x, y+8, sw=1, op=0.6)
        return s
    def dot(s, x, y, r=3.5, color=INK): return s.circle(x, y, r, fill=color, stroke='none')
    def label_box(s, x, y, t, size=11, color=INK):
        return s.text(x, y, t, size=size, color=color, weight=600)
    def svg(s):
        defs = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="currentColor"/></marker>'
                '<marker id="ahs" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M10 0 L0 5 L10 10 Z" fill="currentColor"/></marker></defs>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" role="img" aria-label="{s.label}" '
                f'style="max-width:100%;height:auto;display:block;color:#443E5C">{defs}{"".join(s.parts)}</svg>')

class G:
    """데이터 좌표 → 픽셀 그래프."""
    def __init__(s, c, x0, y0, w, h, xmax, ymax, xl='', yl='', ymin=0, xmin=0):
        s.c, s.x0, s.y0, s.w, s.h, s.xmax, s.ymax, s.ymin, s.xmin = c, x0, y0, w, h, xmax, ymax, ymin, xmin
        s.xl, s.yl = xl, yl
    def px(s, x): return s.x0 + (x - s.xmin) / (s.xmax - s.xmin) * s.w
    def py(s, y): return s.y0 + s.h - (y - s.ymin) / (s.ymax - s.ymin) * s.h
    def pt(s, x, y): return (s.px(x), s.py(y))
    def axes(s, xt=(), yt=()):
        c = s.c; oy = s.py(0) if s.ymin < 0 else s.y0 + s.h
        c.line(s.x0, oy, s.x0 + s.w + 14, oy, sw=1.4, arrow=True)
        c.line(s.x0, s.y0 + s.h, s.x0, s.y0 - 14, sw=1.4, arrow=True)
        if s.xl: c.text(s.x0 + s.w + 22, oy, s.xl, size=12, italic=True, anchor='start')
        if s.yl: c.text(s.x0, s.y0 - 24, s.yl, size=12, italic=True)
        for x, lab in xt:
            c.line(s.px(x), oy - 3, s.px(x), oy + 3, sw=1.2); c.text(s.px(x), oy + 14, str(lab), size=11)
        for y, lab in yt:
            c.line(s.x0 - 3, s.py(y), s.x0 + 3, s.py(y), sw=1.2); c.text(s.x0 - 12, s.py(y), str(lab), size=11, anchor='end')
        return s
    def line(s, pts, color=INK, sw=2.2, dash=None):
        s.c.poly([s.pt(x, y) for x, y in pts], stroke=color, sw=sw, close=False, dash=dash); return s
    def area(s, pts, fill=P_ROSE, op=0.75):
        base = [(pts[-1][0], 0), (pts[0][0], 0)]
        s.c.poly([s.pt(x, y) for x, y in list(pts) + base], fill=fill, stroke='none', op=op); return s
    def guide(s, x, y, both=True):
        c = s.c; px, py = s.pt(x, y)
        c.line(px, s.py(0), px, py, sw=1, dash='3 3', op=0.7)
        if both: c.line(s.x0, py, px, py, sw=1, dash='3 3', op=0.7)
        return s
    def dot(s, x, y, color=INK): s.c.dot(*s.pt(x, y), color=color); return s

FIGS = {}
def fig(fid, w, h, label):
    def deco(fn):
        def build():
            c = C(w, h, label); fn(c); return c.svg()
        FIGS[fid] = build; return fn
    return deco

# ---------------- Δ00 ----------------
@fig('00-1', 420, 170, '같은 크기 5 N의 힘 두 개, 동쪽과 북쪽')
def _(c):
    c.dot(90, 120); c.vec(90, 120, 190, 120, label='5 N (동쪽)', ly=18)
    c.dot(290, 130); c.vec(290, 130, 290, 30, label='5 N (북쪽)', lx=44)
    c.text(210, 20, '길이는 같고 방향만 다르다', size=12, weight=600)

@fig('00-2', 520, 220, '동쪽 3과 북쪽 4의 합이 5가 되는 두 방법')
def _(c):
    # 꼬리-머리
    o = (40, 180); c.dot(*o)
    c.vec(40, 180, 160, 180, label='3', ly=16); c.vec(160, 180, 160, 20, label='4', lx=14)
    c.vec(40, 180, 160, 20, color=PERI, label='합 5', lx=-28, ly=-4)
    c.text(100, 205, '꼬리에 머리 잇기', size=12, weight=600)
    # 평행사변형
    c.dot(310, 180)
    c.vec(310, 180, 430, 180, label='3', ly=16); c.vec(310, 180, 310, 20, label='4', lx=-12)
    c.line(430, 180, 430, 20, sw=1.2, dash='4 3', op=0.7); c.line(310, 20, 430, 20, sw=1.2, dash='4 3', op=0.7)
    c.vec(310, 180, 430, 20, color=PERI, label='합 5', lx=26, ly=-6)
    c.text(370, 205, '평행사변형의 대각선', size=12, weight=600)

@fig('00-3', 360, 240, 'x–t 그래프에서 기울기 3 m/s를 읽는 삼각형')
def _(c):
    g = G(c, 60, 30, 240, 160, 5, 15, 't (s)', 'x (m)').axes([(4, 4)], [(12, 12)])
    g.line([(0, 0), (4.6, 13.8)]); g.guide(4, 12)
    c.line(*g.pt(0, 0), *g.pt(4, 0), sw=2.2, color=ROSE); c.line(*g.pt(4, 0), *g.pt(4, 12), sw=2.2, color=ROSE)
    c.text(g.px(2), g.py(0) - 12, 'Δt = 4 s', size=11, color=ROSE, weight=700)
    c.text(g.px(4) + 34, g.py(6), 'Δx = 12 m', size=11, color=ROSE, weight=700)
    c.text(g.px(1.4), g.py(10), '기울기 = 12/4 = 3 m/s', size=12, weight=600, anchor='start')

@fig('00-4', 380, 220, '문제 6의 v–t 그래프: 직사각형 30 m와 삼각형 15 m')
def _(c):
    g = G(c, 60, 30, 260, 150, 11, 8, 't (s)', 'v (m/s)').axes([(5, 5), (10, 10)], [(6, 6)])
    g.area([(0, 6), (5, 6)], fill=P_ROSE); g.area([(5, 6), (10, 0)], fill=P_PERI)
    g.line([(0, 6), (5, 6), (10, 0)])
    c.text(g.px(2.5), g.py(3), '6 × 5 = 30', size=12, weight=600); c.text(g.px(6.6), g.py(1.8), '½·5·6 = 15', size=12, weight=600)

# ---------------- Δ01 ----------------
@fig('01-1', 460, 120, '수직선 위 A(−2 m)에서 B(+5 m)로 갈 때 변위 +7 m')
def _(c):
    c.line(30, 70, 440, 70, sw=1.6, arrow=True)
    for x in range(-3, 7):
        px = 230 + x * 40; c.line(px, 66, px, 74, sw=1.2); c.text(px, 90, str(x), size=11)
    c.text(230, 108, 'O (원점)', size=11, weight=600); c.text(450, 70, 'x (m)', size=11, anchor='start', italic=True)
    c.dot(150, 70, color=ROSE); c.text(150, 48, 'A', size=13, weight=700, color=ROSE)
    c.dot(430, 70, color=PERI); c.text(430, 48, 'B', size=13, weight=700, color=PERI)
    c.vec(150, 30, 430, 30, color=PERI, label='변위 Δx = 5 − (−2) = +7 m', ly=-14, size=11)

@fig('01-2', 380, 230, '곡선 x–t 그래프에서 두 순간의 접선 기울기')
def _(c):
    g = G(c, 60, 30, 260, 150, 10, 10, 't', 'x').axes([(2, 't₁'), (7, 't₂')], [])
    pts = [(t, 10 * (1 - math.exp(-t / 3.5))) for t in [i * 0.25 for i in range(41)]]
    g.line(pts)
    for t, col in [(2, ROSE), (7, PERI)]:
        x = 10 * (1 - math.exp(-t / 3.5)); k = 10 / 3.5 * math.exp(-t / 3.5)
        c.line(*g.pt(t - 1.5, x - 1.5 * k), *g.pt(t + 1.5, x + 1.5 * k), sw=2, color=col); g.dot(t, x, color=col); g.guide(t, x, both=False)
    c.text(g.px(2.2), g.py(9.2), '가파름 → 빠르다', size=11, color=ROSE, weight=600, anchor='start')
    c.text(g.px(5.6), g.py(6.6), '완만함 → 느리다', size=11, color=PERI, weight=600, anchor='start')

@fig('01-3', 420, 220, '원운동에서 속력이 같아도 속도 방향이 바뀌므로 Δv가 중심을 향한다')
def _(c):
    cx, cy, r = 150, 115, 80
    c.circle(cx, cy, r, sw=1.2, dash='5 4', op=0.7); c.dot(cx, cy, r=2.5)
    a1, a2 = math.radians(-60), math.radians(0)
    for a, lab in [(a1, 'v₁'), (a2, 'v₂')]:
        px, py = cx + r * math.cos(a), cy + r * math.sin(a); tx, ty = -math.sin(a), math.cos(a)
        c.dot(px, py); c.vec(px, py, px + 55 * tx, py + 55 * ty, label=lab, lx=14 if lab == 'v₂' else 12, ly=-10)
    # 벡터 뺄셈
    ox, oy = 320, 70
    c.vec(ox, oy, ox - 55 * math.sin(a1) * 0 + 55 * (-math.sin(a1)), oy + 55 * math.cos(a1), color=INK, sw=1.8, label='v₁', lx=-16)
    c.vec(ox, oy, ox + 55 * (-math.sin(a2)), oy + 55 * math.cos(a2), color=INK, sw=1.8, label='v₂', lx=14)
    x1, y1 = ox + 55 * (-math.sin(a1)), oy + 55 * math.cos(a1); x2, y2 = ox + 55 * (-math.sin(a2)), oy + 55 * math.cos(a2)
    c.vec(x1, y1, x2, y2, color=ROSE, label='Δv', lx=22, ly=4)
    c.text(320, 185, '속력은 같지만 방향이 달라', size=11, weight=600); c.text(320, 200, 'Δv ≠ 0 → 가속도 있음', size=11, weight=600, color=ROSE)

@fig('01-4', 380, 220, '문제 7의 x–t 그래프: 0→12 m, 정지, 12→0 m')
def _(c):
    g = G(c, 60, 30, 260, 150, 10, 14, 't (s)', 'x (m)').axes([(3, 3), (5, 5), (9, 9)], [(12, 12)])
    g.line([(0, 0), (3, 12), (5, 12), (9, 0)]); g.guide(3, 12); g.guide(5, 12, both=False)

# ---------------- Δ02 ----------------
@fig('02-1', 360, 420, '정지에서 등가속도로 출발한 물체의 a–t, v–t, x–t 그래프')
def _(c):
    for i, (yl, pts, lab) in enumerate([('a', [(0, 5), (5, 5)], '수평선'), ('v', [(0, 0), (5, 9)], '직선, 기울기 a'), ('x', [(t, 0.36 * t * t) for t in [k * 0.5 for k in range(11)]], '포물선')]):
        g = G(c, 60, 30 + i * 135, 180, 90, 5.5, 10, 't', yl).axes()
        g.line(pts); c.text(250, 75 + i * 135, lab, size=11, weight=600, anchor='start')

@fig('02-2', 380, 230, 'v–t 사다리꼴을 직사각형 v₀t와 삼각형 ½at²로 나눈 그림')
def _(c):
    g = G(c, 70, 30, 240, 150, 6, 12, 't', 'v').axes([(5, 't')], [(3, 'v₀'), (10, 'v')])
    g.area([(0, 3), (5, 3)], fill=P_ROSE); g.area([(0, 3), (5, 10)], fill=P_PERI)
    c.poly([g.pt(0, 3), g.pt(5, 3), g.pt(5, 3)], fill='none')
    g.line([(0, 3), (5, 10)]); g.line([(0, 3), (5, 3)], sw=1.2, dash='4 3'); g.guide(5, 10)
    c.text(g.px(2.5), g.py(1.5), 'v₀t', size=13, weight=700); c.text(g.px(3.6), g.py(5.2), '½at²', size=13, weight=700)

@fig('02-3', 360, 240, '자유 낙하하는 공의 0.1 s 간격 위치와 v–t 직선')
def _(c):
    x = 70; c.line(x, 20, x, 225, sw=1, op=0.4)
    for i in range(6):
        y = 28 + 6.5 * i * i + 3 * i; c.circle(x, y, 6, fill=P_ROSE, sw=1.2)
        if i != 1: c.text(x + 20, y, f'{i * 0.1:.1f} s', size=10, anchor='start')
    c.text(x, 238, '간격이 점점 벌어진다', size=11, weight=600)
    g = G(c, 200, 40, 120, 150, 0.6, 6, 't', 'v').axes([(0.5, 0.5)], [(5, 5)]); g.line([(0, 0), (0.55, 5.5)])
    c.text(260, 225, '기울기 = g', size=11, weight=600)

@fig('02-4', 380, 220, '예제 1의 v–t 그래프: 2에서 10 m/s, 사다리꼴 넓이 24 m')
def _(c):
    g = G(c, 60, 30, 260, 150, 5, 12, 't (s)', 'v (m/s)').axes([(4, 4)], [(2, 2), (10, 10)])
    g.area([(0, 2), (4, 10)], fill=P_ROSE); g.line([(0, 2), (4, 10)]); g.guide(4, 10)
    c.text(g.px(2.2), g.py(3.2), '½(2+10)·4 = 24 m', size=12, weight=600)

@fig('02-5', 380, 230, '예제 3: A의 삼각형 넓이와 B의 직사각형 넓이가 t = 12 s에서 같아진다')
def _(c):
    g = G(c, 60, 30, 260, 150, 14, 28, 't (s)', 'v (m/s)').axes([(12, 12)], [(12, 12), (24, 24)])
    g.area([(0, 12), (12, 12)], fill=P_PERI, op=0.5); g.area([(0, 0), (12, 24)], fill=P_ROSE, op=0.5)
    g.line([(0, 12), (13.5, 12)], color=PERI); g.line([(0, 0), (13.5, 27)], color=ROSE); g.guide(12, 24)
    c.text(g.px(3), g.py(15), 'B: 12 × 12 = 144', size=11, weight=600, color=PERI, anchor='start')
    c.text(g.px(8.5), g.py(5), 'A: ½·12·24 = 144', size=11, weight=600, color=ROSE, anchor='start')

@fig('02-6', 380, 220, '문제 6의 사다리꼴 v–t 그래프')
def _(c):
    g = G(c, 60, 30, 260, 150, 11, 10, 't (s)', 'v (m/s)').axes([(2, 2), (6, 6), (10, 10)], [(8, 8)])
    g.area([(0, 0), (2, 8), (6, 8), (10, 0)], fill=P_ROSE, op=0.5); g.line([(0, 0), (2, 8), (6, 8), (10, 0)]); g.guide(2, 8, both=False); g.guide(6, 8, both=False)

# ---------------- Δ03 ----------------
@fig('03-1', 320, 200, '책상 위 책: 중력과 수직항력이 크기가 같아 알짜힘 0')
def _(c):
    c.ground(60, 260, 150); c.block(120, 100, 80, 50, '책', fill=P_LEMON)
    c.vec(160, 125, 160, 185, label='mg', lx=26, ly=14); c.vec(160, 125, 160, 65, color=PERI, label='N', lx=-18)
    c.text(160, 25, '알짜힘 = N − mg = 0', size=12, weight=600)

@fig('03-2', 360, 220, '수평면 위 상자의 자유 물체 그림: N, mg, F, f')
def _(c):
    c.ground(40, 320, 170); c.block(140, 110, 80, 60, '', fill=P_LEMON)
    c.vec(180, 140, 180, 60, color=PERI, label='N', lx=-16); c.vec(180, 140, 180, 205, label='mg', lx=24)
    c.vec(220, 140, 310, 140, label='F (당김)', ly=-16); c.vec(140, 140, 80, 140, color=SAGE, label='f (마찰)', ly=-16)
    c.text(180, 30, '수직: N = mg   수평: F − f = ma', size=12, weight=600)

@fig('03-3', 480, 230, '말과 수레를 따로 본 자유 물체 그림: 짝힘은 서로 다른 물체에 작용한다')
def _(c):
    c.ground(20, 460, 170)
    c.block(60, 110, 120, 60, '수레', fill=P_LEMON); c.block(280, 100, 130, 70, '말', fill=P_SAGE)
    c.vec(180, 125, 250, 125, label='말이 당김', ly=-14, size=11); c.vec(60, 140, 15, 140, color=SAGE, label='마찰', ly=-14, size=11)
    c.vec(280, 155, 210, 155, color=PERI, label='수레가 당김', ly=14, size=11); c.vec(345, 165, 440, 165, color=INK, label='땅이 밈', ly=-14, size=11)
    c.text(120, 200, '수레: 말의 힘 > 마찰 → 앞으로', size=11, weight=600); c.text(345, 200, '말: 땅의 힘 > 수레의 힘 → 앞으로', size=11, weight=600)

@fig('03-4', 360, 170, '맞닿은 A(2 kg)와 B(3 kg)를 10 N으로 미는 그림')
def _(c):
    c.ground(30, 330, 130); c.block(120, 80, 70, 50, 'A 2 kg'); c.block(190, 65, 90, 65, 'B 3 kg', fill=P_PERI)
    c.vec(50, 105, 118, 105, label='10 N', ly=-14)
    c.text(180, 30, '마찰 없음', size=11, op=0.7)

@fig('03-5', 360, 160, '실로 연결된 A(1 kg)와 B(2 kg), B를 6 N으로 당김')
def _(c):
    c.ground(30, 330, 120); c.block(70, 75, 60, 45, 'A 1 kg'); c.block(190, 65, 80, 55, 'B 2 kg', fill=P_PERI)
    c.line(130, 97, 190, 97, sw=1.6); c.text(160, 84, '실', size=10, op=0.7)
    c.vec(270, 92, 335, 92, label='6 N', ly=-14)

# ---------------- Δ04 ----------------
def pulley_two(c, cx, top, left, right, lfill=P_ROSE, rfill=P_PERI):
    c.line(cx, top - 30, cx, top, sw=1.4); c.circle(cx, top + 14, 14, fill='#FFFFFF', sw=1.6); c.dot(cx, top + 14, r=2)
    c.line(cx - 14, top + 14, cx - 14, top + 70, sw=1.6); c.line(cx + 14, top + 14, cx + 14, top + 110, sw=1.6)
    c.block(cx - 38, top + 70, 48, 40, left, fill=lfill, size=11); c.block(cx - 10, top + 110, 48, 40, right, fill=rfill, size=11)

@fig('04-1', 300, 240, '도르래에 3 kg과 2 kg을 매단 그림, 3 kg이 내려간다')
def _(c):
    pulley_two(c, 150, 40, '3 kg', '2 kg')
    c.vec(90, 130, 90, 180, label='a', lx=-12, size=12); c.vec(210, 190, 210, 140, label='a', lx=12, size=12)
    c.text(150, 225, '(+) 방향: 3 kg 내려감', size=11, weight=600)

@fig('04-2', 380, 240, '빗면 위 물체의 중력을 빗면 방향과 수직 방향으로 분해')
def _(c):
    th = math.radians(30); ox, oy = 40, 200; L = 300
    c.poly([(ox, oy), (ox + L, oy), (ox + L, oy - L * math.tan(th))], fill=P_SKY, op=0.5, sw=1.4)
    c.text(ox + 60, oy - 12, 'θ', size=13, italic=True)
    bx, by = ox + 170, oy - 170 * math.tan(th); ux, uy = math.cos(th), -math.sin(th); nx, ny = -math.sin(th), -math.cos(th)
    pts = [(bx, by), (bx + 44 * ux, by + 44 * uy), (bx + 44 * ux + 32 * nx, by + 44 * uy + 32 * ny), (bx + 32 * nx, by + 32 * ny)]
    c.poly(pts, fill=P_LEMON, sw=1.4)
    gx, gy = bx + 22 * ux + 16 * nx, by + 22 * uy + 16 * ny
    c.vec(gx, gy, gx, gy + 90, label='mg', lx=-16, ly=28)
    c.vec(gx, gy, gx - 45 * ux, gy - 45 * uy, color=ROSE, label='mg sinθ', lx=-42, ly=6, size=11)
    c.vec(gx, gy, gx - 78 * nx, gy - 78 * ny, color=ROSE, label='mg cosθ', lx=46, ly=8, size=11)
    c.vec(gx, gy, gx + 78 * nx, gy + 78 * ny, color=PERI, label='N', lx=-12)

@fig('04-3', 380, 220, '미는 힘과 마찰력: 정지 마찰은 미는 힘만큼, 최대를 넘으면 운동 마찰로')
def _(c):
    g = G(c, 60, 30, 260, 150, 10, 10, '미는 힘', '마찰력').axes()
    g.line([(0, 0), (6, 6)], color=ROSE); g.line([(6, 6), (6, 4.5)], sw=1.4, dash='3 3'); g.line([(6, 4.5), (9.5, 4.5)], color=PERI)
    g.dot(6, 6, color=ROSE); c.text(g.px(3.4), g.py(4.4), '정지 마찰 (기울기 1)', size=11, color=ROSE, weight=600, anchor='start')
    c.text(g.px(6.2), g.py(6.9), '최대 정지 마찰력 μₛN', size=11, weight=600, anchor='start'); c.text(g.px(7.8), g.py(3.6), '운동 마찰 μₖN', size=11, color=PERI, weight=600)

@fig('04-4', 340, 200, '책상 위 4 kg 물체가 도르래 너머 1 kg 추에 연결됨')
def _(c):
    c.ground(30, 250, 120); c.block(90, 70, 80, 50, '4 kg', fill=P_LEMON)
    c.circle(262, 95, 12, fill='#FFFFFF'); c.dot(262, 95, r=2); c.line(170, 95, 262, 83, sw=1.5); c.line(274, 95, 274, 150, sw=1.5)
    c.line(250, 120, 250, 180, sw=1.8); c.block(252, 150, 44, 36, '1 kg', size=11)

# ---------------- Δ05 ----------------
@fig('05-1', 420, 180, '경첩 축에서 먼 곳과 가까운 곳에 같은 힘을 줄 때의 돌림힘')
def _(c):
    c.dot(60, 90, r=5); c.text(60, 115, '경첩(축)', size=11); c.line(60, 90, 360, 90, sw=8, color=P_LEMON); c.line(60, 90, 360, 90, sw=1.2)
    c.vec(340, 90, 340, 30, label='F', lx=14); c.line(60, 140, 340, 140, sw=1, dash='4 3'); c.text(200, 155, 'r 큼 → 돌림힘 큼', size=11, color=ROSE, weight=600)
    c.vec(110, 90, 110, 30, color=PERI, label='F', lx=-14); c.text(110, 12, 'r 작음 → 돌림힘 작음', size=11, color=PERI, weight=600, anchor='start')

def beam(c, x0, x1, y, loads, supports, labels_top=True):
    c.line(x0, y, x1, y, sw=10, color=P_LEMON); c.line(x0, y, x1, y, sw=1.4)
    for x, lab in supports:
        c.poly([(x, y + 5), (x - 14, y + 30), (x + 14, y + 30)], fill='#FFFFFF', sw=1.4); c.text(x, y + 44, lab, size=11, weight=600)
    for x, lab, col in loads:
        c.vec(x, y - 60, x, y - 8, color=col, label=lab, lx=0, ly=-40 if labels_top else 0, size=11)

@fig('05-2', 460, 200, '4 m 막대 위 1 m 지점의 600 N 사람과 중앙의 막대 무게 200 N, 받침 A·B')
def _(c):
    beam(c, 60, 400, 120, [(145, '600 N', ROSE), (230, '200 N', INK)], [(60, 'A'), (400, 'B')])
    c.vec(60, 170, 60, 130, color=PERI, label='Rₐ', lx=-22); c.vec(400, 170, 400, 130, color=PERI, label='Rʙ', lx=22)
    for x, t in [(60, '0'), (145, '1 m'), (230, '2 m'), (400, '4 m')]: c.text(x, 100 - 70, t, size=10, op=0.7)

@fig('05-3', 420, 220, '조금 기울인 상자는 돌아오고, 많이 기울인 상자는 넘어진다')
def _(c):
    for i, (ang, ok) in enumerate([(12, True), (38, False)]):
        cx = 110 + i * 220; c.ground(cx - 80, cx + 80, 180)
        a = math.radians(ang); w, h = 70, 90; px, py = cx - 30, 180
        pts = [(0, 0), (w, 0), (w, -h), (0, -h)]
        rp = [(px + x * math.cos(a) - y * math.sin(a), py + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
        c.poly(rp, fill=P_LEMON, sw=1.4)
        gx, gy = px + (w / 2) * math.cos(a) - (-h / 2) * math.sin(a), py + (w / 2) * math.sin(a) + (-h / 2) * math.cos(a)
        c.dot(gx, gy, color=ROSE); c.line(gx, gy, gx, 180, sw=1.4, dash='4 3', color=ROSE)
        c.text(cx, 205, '받침면 안 → 돌아옴' if ok else '받침면 밖 → 넘어짐', size=11, weight=600, color=SAGE if ok else ROSE)

@fig('05-4', 460, 200, '6 m 막대: A(0 m), 물체 900 N(2 m), 막대 무게 300 N(3 m), B(5 m)')
def _(c):
    beam(c, 50, 410, 120, [(170, '900 N', ROSE), (230, '300 N', INK)], [(50, 'A'), (350, 'B')])
    for x, t in [(50, '0'), (170, '2 m'), (230, '3 m'), (350, '5 m'), (410, '6 m')]: c.text(x, 30, t, size=10, op=0.7)

@fig('05-5', 380, 260, '벽에 기댄 사다리: 아래 끝을 축으로, 무게는 중앙, 벽의 힘은 위 끝에서 수평')
def _(c):
    c.line(60, 20, 60, 230, sw=3); c.ground(60, 340, 230)
    bx, by = 260, 230; tx, ty = 60, 230 - 200 * math.tan(math.radians(53))
    ty = max(ty, 40); c.line(bx, by, tx, ty, sw=6, color=P_LEMON); c.line(bx, by, tx, ty, sw=1.4)
    mx, my = (bx + tx) / 2, (by + ty) / 2; c.vec(mx, my, mx, my + 70, label='500 N', lx=30)
    c.vec(tx, ty, tx + 70, ty, color=PERI, label='벽의 힘 F', ly=-14, size=11); c.dot(bx, by, r=5, color=ROSE); c.text(bx + 30, by - 12, '축', size=11, color=ROSE, weight=600)
    c.vec(bx, by, bx - 70, by, color=SAGE, label='마찰', ly=14, size=11); c.text(225, 218, '53°', size=12, italic=True)

# ---------------- Δ06 ----------------
@fig('06-1', 340, 200, '충돌할 때의 F–t 그래프: 산 모양 아래 넓이가 충격량')
def _(c):
    g = G(c, 60, 30, 230, 130, 10, 10, 't', 'F').axes()
    pts = [(t, 9 * math.exp(-((t - 5) ** 2) / 1.6)) for t in [i * 0.25 for i in range(41)]]
    g.area(pts, fill=P_ROSE); g.line(pts); c.text(g.px(5), g.py(3), '넓이 = 충격량 = Δp', size=12, weight=600)

@fig('06-2', 420, 200, '같은 충격량: 딱딱한 바닥은 높고 좁게, 에어백은 낮고 넓게')
def _(c):
    g = G(c, 60, 30, 320, 130, 12, 10, 't', 'F').axes()
    hard = [(t, 9 * math.exp(-((t - 3) ** 2) / 0.35)) for t in [i * 0.1 for i in range(61)]]
    soft = [(t, 3 * math.exp(-((t - 7.5) ** 2) / 3.2)) for t in [i * 0.1 for i in range(41, 121)]]
    g.area(hard, fill=P_ROSE); g.line(hard, color=ROSE); g.area(soft, fill=P_PERI); g.line(soft, color=PERI)
    c.text(g.px(3), g.py(9.6), '딱딱한 바닥: F 큼, Δt 짧음', size=11, color=ROSE, weight=600, anchor='start')
    c.text(g.px(7.5), g.py(4.2), '에어백: F 작음, Δt 긺', size=11, color=PERI, weight=600)
    c.text(g.px(6), g.py(-1.9), '두 넓이는 같다', size=11, weight=600)

@fig('06-3', 420, 210, '정지한 두 사람이 서로 밀면 반대 방향으로, 운동량 크기가 같게 밀려난다')
def _(c):
    c.ground(20, 400, 100, hatch=False); c.text(210, 25, '밀기 전: p = 0', size=12, weight=600)
    c.block(150, 50, 50, 50, '60 kg', fill=P_SAGE, size=11); c.block(220, 60, 40, 40, '40 kg', fill=P_LEMON, size=11)
    c.ground(20, 400, 190, hatch=False); c.text(210, 118, '민 후: 60v₁ + 40v₂ = 0', size=12, weight=600)
    c.block(70, 140, 50, 50, '60 kg', fill=P_SAGE, size=11); c.block(300, 150, 40, 40, '40 kg', fill=P_LEMON, size=11)
    c.vec(70, 165, 30, 165, label='v₁', ly=-14); c.vec(340, 170, 395, 170, label='v₂ = 1.5v₁', ly=-14, size=11)

@fig('06-4', 340, 200, '문제 8의 삼각형 F–t 그래프: 0.4 s, 최대 100 N')
def _(c):
    g = G(c, 60, 30, 230, 130, 0.5, 120, 't (s)', 'F (N)').axes([(0.2, 0.2), (0.4, 0.4)], [(100, 100)])
    g.area([(0, 0), (0.2, 100), (0.4, 0)], fill=P_ROSE); g.line([(0, 0), (0.2, 100), (0.4, 0)]); g.guide(0.2, 100)

# ---------------- Δ07 ----------------
@fig('07-1', 520, 190, '일이 양수인 경우와 0인 두 경우')
def _(c):
    for i, (t, sub) in enumerate([('밀어서 옮김', 'W = Fs > 0'), ('들고 가만히', 's = 0 → W = 0'), ('들고 수평 이동', 'F ⊥ s → W = 0')]):
        x = 30 + i * 170; c.ground(x, x + 150, 130, hatch=False)
        if i == 0:
            c.block(x + 30, 85, 45, 45, '', fill=P_LEMON); c.vec(x + 75, 107, x + 130, 107, label='F', ly=-14); c.line(x + 52, 140, x + 120, 140, sw=1.2, arrow=True); c.text(x + 86, 152, 's', size=11, italic=True)
        else:
            c.block(x + 50, 40, 45, 45, '', fill=P_LEMON); c.vec(x + 72, 62, x + 72, 20, color=PERI, label='F', lx=14)
            if i == 2: c.line(x + 20, 140, x + 130, 140, sw=1.2, arrow=True); c.text(x + 75, 152, 's', size=11, italic=True)
        c.text(x + 75, 172, t, size=11, weight=600); c.text(x + 75, 15, sub, size=11, color=ROSE, weight=600)

@fig('07-2', 340, 200, '용수철의 F–x 그래프: 삼각형 넓이가 ½kx²')
def _(c):
    g = G(c, 60, 30, 230, 130, 10, 10, 'x', 'F').axes([(8, 'x')], [(8, 'kx')])
    g.area([(0, 0), (8, 8)], fill=P_ROSE); g.line([(0, 0), (9.5, 9.5)]); g.guide(8, 8)
    c.text(g.px(5.6), g.py(2), '½·x·kx = ½kx²', size=12, weight=600)

@fig('07-3', 460, 240, '롤러코스터 세 위치의 운동 에너지와 퍼텐셜 에너지 막대: 합은 일정')
def _(c):
    c.path('M30 60 C 90 60, 110 190, 180 190 S 250 90, 310 100 S 400 200, 440 200', sw=2.4)
    for x, y, K, U, lab in [(30, 60, 0, 100, '꼭대기'), (180, 190, 100, 0, '바닥'), (310, 100, 55, 45, '언덕')]:
        c.dot(x, y, color=ROSE); bx = x + 18 if x < 100 else x - 14; base = y - 16 if x > 100 else y + 60
        c.rect(bx, base - U * 0.5, 12, U * 0.5, fill=P_PERI, stroke='none'); c.rect(bx + 14, base - K * 0.5, 12, K * 0.5, fill=P_ROSE, stroke='none')
        c.text(x, y + 16 if x > 100 else y - 14, lab, size=10, weight=600)
    c.rect(360, 20, 12, 12, fill=P_PERI, stroke='none'); c.text(378, 26, 'U = mgh', size=11, anchor='start')
    c.rect(360, 38, 12, 12, fill=P_ROSE, stroke='none'); c.text(378, 44, 'K = ½mv²', size=11, anchor='start')

@fig('07-4', 420, 170, '에너지 전환 사슬: 100 → 80 → 64, 단계마다 새어 나간 몫')
def _(c):
    for i, (v, lab) in enumerate([(100, '공급 100'), (80, '1단계 후 80'), (64, '2단계 후 64')]):
        x = 40 + i * 130; c.rect(x, 40, 100, 90, fill=P_SAGE, stroke='none', op=0.35); c.rect(x, 130 - v * 0.9, 100, v * 0.9, fill=P_SAGE, stroke='none')
        c.text(x + 50, 150, lab, size=11, weight=600)
        if i < 2: c.line(x + 104, 85, x + 126, 85, sw=1.4, arrow=True); c.text(x + 115, 70, '×0.8', size=10, color=ROSE, weight=600)
    c.text(210, 20, '옅은 부분이 열로 새어 나간 몫', size=11, op=0.8)

# ---------------- Δ08 ----------------
def radial(c, cx, cy, out=True, n=8, r1=12, r2=40, col=INK):
    for k in range(n):
        a = 2 * math.pi * k / n; x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a); x2, y2 = cx + r2 * math.cos(a), cy + r2 * math.sin(a)
        if out: c.line(x1, y1, x2, y2, sw=1.2, arrow=True, color=col)
        else: c.line(x2, y2, x1, y1, sw=1.2, arrow=True, color=col)

@fig('08-1', 520, 170, '전기력선 네 가지: (+) 점전하, (−) 점전하, (+)(−) 쌍, 평행판')
def _(c):
    c.circle(70, 80, 11, fill=P_ROSE); c.text(70, 80, '+', size=14, weight=700); radial(c, 70, 80, True)
    c.circle(190, 80, 11, fill=P_SKY); c.text(190, 80, '−', size=14, weight=700); radial(c, 190, 80, False)
    c.circle(290, 80, 10, fill=P_ROSE); c.text(290, 80, '+', size=13, weight=700); c.circle(370, 80, 10, fill=P_SKY); c.text(370, 80, '−', size=13, weight=700)
    for dy in (-38, -20, 0, 20, 38):
        c.path(f'M300 {80 + dy * 0.2:.0f} Q 330 {80 + dy * 1.6:.0f} 360 {80 + dy * 0.2:.0f}', sw=1.2, arrow=True)
    c.line(420, 40, 500, 40, sw=3, color=ROSE); c.line(420, 120, 500, 120, sw=3, color='#6C9BD2')
    for x in (432, 452, 472, 492): c.line(x, 46, x, 114, sw=1.2, arrow=True)
    for x, t in [(70, '(+) 바깥으로'), (190, '(−) 안쪽으로'), (330, '(+)(−) 쌍'), (460, '평행판: 균일')]: c.text(x, 155, t, size=11, weight=600)

@fig('08-2', 440, 220, '평행판 사이의 전기력선(아래로)과 등전위면(수평선), 두 전하가 받는 힘')
def _(c):
    c.line(60, 40, 320, 40, sw=4, color=ROSE); c.text(340, 40, '+ 전위 높음', size=11, anchor='start')
    c.line(60, 180, 320, 180, sw=4, color='#6C9BD2'); c.text(340, 180, '− 전위 0', size=11, anchor='start')
    for x in (90, 130, 250, 290): c.line(x, 48, x, 172, sw=1.2, arrow=True, op=0.8)
    for y in (75, 110, 145): c.line(60, y, 320, y, sw=1, dash='4 3', op=0.6)
    c.text(28, 110, '등전위면', size=10, anchor='middle', rotate=-90, op=0.8)
    c.circle(170, 100, 9, fill=P_ROSE); c.text(170, 100, '+', size=12, weight=700); c.vec(170, 110, 170, 150, label='F', lx=12)
    c.circle(215, 125, 9, fill=P_SKY); c.text(215, 125, '−', size=12, weight=700); c.vec(215, 115, 215, 75, color=PERI, label='F', lx=12)

# ---------------- Δ09 ----------------
def resistor(c, x, y, w=40, label=''):
    c.rect(x, y - 7, w, 14, fill='#FFFFFF', sw=1.4)
    if label: c.text(x + w / 2, y - 16, label, size=11, weight=600)
def battery(c, x, y, label=''):
    c.line(x - 8, y - 12, x - 8, y + 12, sw=2.2); c.line(x + 6, y - 6, x + 6, y + 6, sw=1.4)
    if label: c.text(x, y + 26, label, size=11, weight=600)

@fig('09-1', 460, 190, '직렬은 길이 하나라 전류가 같고, 병렬은 두 갈래라 전압이 같다')
def _(c):
    # 직렬
    c.rect(30, 40, 170, 110, sw=1.4); battery(c, 115, 150, 'V'); resistor(c, 60, 40, 40, 'R₁'); resistor(c, 130, 40, 40, 'R₂')
    c.line(30, 95, 30, 85, sw=1.2, arrow=True); c.text(18, 95, 'I', size=11, italic=True, weight=600)
    c.text(115, 175, '직렬: 전류 같음', size=11, weight=600)
    # 병렬
    c.rect(270, 40, 170, 110, sw=1.4); battery(c, 355, 150, 'V'); c.line(300, 40, 300, 150, sw=1.4); c.line(410, 40, 410, 150, sw=1.4)
    resistor(c, 335, 40, 40, 'R₁'); resistor(c, 335, 95, 40, 'R₂'); c.line(300, 95, 335, 95, sw=1.4); c.line(375, 95, 410, 95, sw=1.4)
    c.line(270, 100, 270, 88, sw=1.2, arrow=True); c.text(258, 95, 'I', size=11, italic=True, weight=600)
    c.line(315, 40, 327, 40, sw=1.2, arrow=True); c.line(315, 95, 327, 95, sw=1.2, arrow=True); c.text(318, 68, 'I₁', size=10, weight=600); c.text(318, 116, 'I₂', size=10, weight=600)
    c.text(355, 175, '병렬: 전압 같음', size=11, weight=600)

@fig('09-2', 460, 200, '멀티탭에 병렬로 꽂힌 세 기기: 각 가지 전류가 공통 전선에 합쳐진다')
def _(c):
    c.rect(30, 60, 400, 24, fill=P_LEMON, sw=1.4); c.text(230, 72, '멀티탭 전선 · 허용 전류 16 A', size=11, weight=600)
    c.line(0, 72, 30, 72, sw=2.4, color=ROSE); c.text(14, 56, '220 V', size=10)
    for i, (lab, cur) in enumerate([('히터 2000 W', '9.1 A'), ('드라이어 1500 W', '6.8 A'), ('주전자 1200 W', '5.5 A')]):
        x = 90 + i * 130; c.line(x, 84, x, 120, sw=1.4); c.rect(x - 45, 120, 90, 40, fill='#FFFFFF', sw=1.4); c.text(x, 140, lab, size=10, weight=600)
        c.line(x + 8, 116, x + 8, 92, sw=1.2, arrow=True, color=ROSE); c.text(x + 24, 104, cur, size=10, color=ROSE, weight=600, anchor='start')
    c.text(230, 185, '총 전류 = 9.1 + 6.8 + 5.5 = 21.4 A > 16 A', size=12, color=ROSE, weight=700)

@fig('09-3', 520, 210, '평행판 축전기: 전지 연결 유지 시 전하 절반, 전지 분리 시 전압 두 배')
def _(c):
    for i, (d, q, v, sub, batt) in enumerate([(30, 8, '10 V', '(가) 거리 d', True), (60, 4, '10 V', '(나) 전지 연결, 2d', True), (60, 8, '20 V', '(다) 전지 분리, 2d', False)]):
        x = 30 + i * 170; y = 90
        c.line(x, y - d / 2, x + 90, y - d / 2, sw=3, color=ROSE); c.line(x, y + d / 2, x + 90, y + d / 2, sw=3, color='#6C9BD2')
        for k in range(q):
            px = x + 8 + k * (74 / max(q - 1, 1)); c.text(px, y - d / 2 - 9, '+', size=10, weight=700, color=ROSE); c.text(px, y + d / 2 + 10, '−', size=10, weight=700, color='#6C9BD2')
        if batt:
            c.line(x + 90, y - d / 2, x + 130, y - d / 2, sw=1.2); c.line(x + 130, y - d / 2, x + 130, y - 12, sw=1.2)
            c.line(x + 90, y + d / 2, x + 130, y + d / 2, sw=1.2); c.line(x + 130, y + d / 2, x + 130, y + 12, sw=1.2)
            c.line(x + 122, y - 12, x + 138, y - 12, sw=2.2); c.line(x + 125, y + 12, x + 135, y + 12, sw=1.4)
        else:
            c.line(x + 90, y - d / 2, x + 112, y - d / 2, sw=1.2); c.line(x + 90, y + d / 2, x + 112, y + d / 2, sw=1.2); c.text(x + 126, y, '끊김', size=9, op=0.7)
        c.text(x + 60, 170, sub, size=11, weight=600); c.text(x + 60, 188, f'V = {v}', size=11, color=PERI, weight=600)

@fig('09-4', 340, 170, '예제 1 회로: 12 V 전지, 2 Ω 직렬, 3 Ω과 6 Ω 병렬')
def _(c):
    c.rect(30, 30, 280, 110, sw=1.4); battery(c, 60, 140, '12 V'); resistor(c, 100, 30, 40, '2 Ω')
    c.line(200, 30, 200, 140, sw=1.4); c.line(280, 30, 280, 140, sw=1.4); c.line(280, 85, 200, 85, sw=1.4)
    resistor(c, 220, 30, 40, '3 Ω'); resistor(c, 220, 85, 40, '6 Ω')
    c.line(30, 95, 30, 83, sw=1.2, arrow=True); c.text(18, 88, 'I', size=11, italic=True, weight=600)

# ---------------- Δ10 ----------------
@fig('10-1', 480, 180, '강자성·상자성·반자성의 원자 자석 배열')
def _(c):
    c.vec(240, 22, 300, 22, color=PERI, label='외부 자기장', lx=-90, size=11)
    for i, (t, angs, L) in enumerate([('강자성', [0] * 9, 18), ('상자성', [10, -25, 5, 30, -10, 15, -30, 0, 20], 11), ('반자성', [180, 170, 190, 175, 185, 180, 172, 188, 180], 9)]):
        x0 = 40 + i * 150
        for k, a in enumerate(angs):
            cx, cy = x0 + 20 + (k % 3) * 40, 60 + (k // 3) * 32; r = math.radians(a)
            c.line(cx - L * math.cos(r), cy - L * math.sin(r), cx + L * math.cos(r), cy + L * math.sin(r), sw=2, arrow=True, color=ROSE if i == 0 else INK)
        c.text(x0 + 60, 165, t, size=12, weight=600)

@fig('10-2', 520, 220, '직선 전류, 원형 전류, 솔레노이드가 만드는 자기장과 오른손 규칙')
def _(c):
    # 직선
    c.dot(90, 100, r=7, color=ROSE); c.circle(90, 100, 7, stroke='#FFFFFF', sw=1.5); c.text(90, 100, '•', size=12, color='#FFFFFF', weight=700)
    for r in (22, 40, 58): c.circle(90, 100, r, sw=1.2, op=0.8); c.path(f'M{90 + r} 100 A {r} {r} 0 0 0 {90 + r * 0.7:.0f} {100 - r * 0.7:.0f}', sw=1.2, arrow=True)
    c.text(90, 180, '직선 전류(종이 밖으로)', size=11, weight=600); c.text(90, 196, '동심원, 반시계', size=10, op=0.8)
    # 원형
    c.path('M230 100 A 40 20 0 1 1 310 100 A 40 20 0 1 1 230 100', sw=2.2, color=ROSE); c.line(270, 130, 270, 62, sw=1.6, arrow=True); c.text(270, 50, 'B', size=12, weight=700, italic=True)
    c.text(270, 180, '원형 전류', size=11, weight=600); c.text(270, 196, '중심을 뚫는 자기장', size=10, op=0.8)
    # 솔레노이드
    for k in range(6): c.path(f'M{380 + k * 20} 120 A 10 22 0 0 1 {390 + k * 20} 78', sw=1.8, color=ROSE)
    for y in (88, 100, 112): c.line(372, y, 508, y, sw=1.2, arrow=True)
    c.text(372, 66, 'S', size=12, weight=700); c.text(508, 66, 'N', size=12, weight=700)
    c.text(440, 180, '솔레노이드', size=11, weight=600); c.text(440, 196, '안쪽에 나란한 자기장', size=10, op=0.8)

@fig('10-3', 360, 210, '말굽자석 사이의 도선: 자기장 아래, 전류 오른쪽, 힘은 앞(종이 밖)')
def _(c):
    c.rect(100, 20, 160, 40, fill=P_ROSE, sw=1.4); c.text(180, 40, 'N', size=14, weight=700)
    c.rect(100, 160, 160, 40, fill=P_SKY, sw=1.4); c.text(180, 180, 'S', size=14, weight=700)
    for x in (130, 180, 230): c.line(x, 64, x, 156, sw=1.2, arrow=True, op=0.7)
    c.text(268, 110, 'B', size=12, italic=True, weight=700, anchor='start')
    c.line(60, 110, 300, 110, sw=3.5, color=INK); c.vec(200, 110, 290, 110, label='I', ly=14)
    c.circle(180, 110, 11, fill='#FFFFFF', sw=1.8, stroke=ROSE); c.dot(180, 110, r=3, color=ROSE); c.text(180, 132, 'F (종이 밖으로)', size=11, color=ROSE, weight=600)

@fig('10-4', 380, 220, '자기장 속 사각 코일: 두 변이 반대 힘을 받아 돌림힘이 생긴다')
def _(c):
    c.rect(40, 30, 40, 160, fill=P_ROSE, sw=1.2); c.text(60, 110, 'N', size=13, weight=700)
    c.rect(300, 30, 40, 160, fill=P_SKY, sw=1.2); c.text(320, 110, 'S', size=13, weight=700)
    for y in (60, 110, 160): c.line(84, y, 296, y, sw=1, arrow=True, op=0.5)
    c.poly([(130, 70), (250, 70), (250, 150), (130, 150)], sw=2.6, color=INK)
    c.vec(130, 110, 130, 50, label='F', lx=-14); c.vec(250, 110, 250, 170, label='F', lx=14)
    c.path('M175 40 A 25 12 0 0 1 205 40', sw=1.4, arrow=True); c.text(190, 22, '회전', size=11, weight=600)
    c.text(130, 178, '전류 ↑', size=10); c.text(250, 42, '전류 ↓', size=10)

# ---------------- Δ11 ----------------
def coil(c, x, y, n=5, w=16, h=40, color=INK):
    for k in range(n): c.path(f'M{x + k * w} {y + h / 2} A {w / 2} {h / 2} 0 0 1 {x + (k + 1) * w} {y + h / 2}', sw=1.8, color=color)
def magnet(c, x, y, w=70, h=26, flip=False):
    c.rect(x, y, w / 2, h, fill=P_SKY if flip else P_ROSE, sw=1.2); c.rect(x + w / 2, y, w / 2, h, fill=P_ROSE if flip else P_SKY, sw=1.2)
    c.text(x + w / 4, y + h / 2, 'S' if flip else 'N', size=12, weight=700); c.text(x + 3 * w / 4, y + h / 2, 'N' if flip else 'S', size=12, weight=700)

@fig('11-1', 520, 190, 'N극이 다가오면 코일이 N극을 만들어 밀고, 멀어지면 S극을 만들어 붙잡는다')
def _(c):
    for i, (t, pole, arrow_dir, cur) in enumerate([('다가올 때', 'N', 1, '전류 ↻'), ('멀어질 때', 'S', -1, '전류 ↺')]):
        x = 30 + i * 250; magnet(c, x, 60, flip=True)  # 오른쪽이 N
        if arrow_dir > 0: c.vec(x + 78, 73, x + 112, 73)
        else: c.vec(x - 6, 73, x - 40, 73)
        coil(c, x + 130, 53, n=5); c.text(x + 128, 40, pole, size=13, weight=700, color=ROSE); c.text(x + 210, 40, 'S' if pole == 'N' else 'N', size=13, weight=700, color=PERI)
        c.text(x + 170, 118, cur, size=11, weight=600); c.text(x + 120, 160, t, size=12, weight=600)
        c.text(x + 120, 178, '코일이 변화를 방해한다', size=10, op=0.8)

@fig('11-2', 520, 250, '자기장 속에서 도는 코일 네 장면과 유도 전류의 사인 곡선')
def _(c):
    for i, (ang, lab) in enumerate([(0, '0°'), (90, '90°'), (180, '180°'), (270, '270°')]):
        x = 60 + i * 120; c.line(x - 40, 60, x + 40, 60, sw=1, arrow=True, op=0.5); c.text(x + 48, 60, 'B', size=10, italic=True, anchor='start')
        a = math.radians(ang); w = 30 * abs(math.cos(a)); c.rect(x - max(w, 3), 35, max(2 * w, 6), 50, fill=P_LEMON, sw=1.4) if ang % 180 == 0 else c.rect(x - 3, 35, 6, 50, fill=P_LEMON, sw=1.4)
        c.text(x, 105, lab, size=11, weight=600)
    g = G(c, 60, 130, 400, 90, 4, 1, 't', 'I', ymin=-1).axes()
    g.line([(t, math.sin(math.pi * t / 2 + math.pi / 2)) for t in [k * 0.05 for k in range(81)]], color=ROSE)
    c.text(280, 240, '반 바퀴마다 방향이 바뀐다 → 교류', size=11, weight=600)

@fig('11-3', 440, 190, '충전 패드 코일의 변하는 자기장이 휴대전화 코일에 유도 전류를 만든다')
def _(c):
    c.rect(60, 120, 320, 40, fill=P_SAGE, sw=1.4, rx=4); c.text(220, 172, '충전 패드 (교류 전류)', size=11, weight=600); coil(c, 140, 120, n=10, w=16, h=30, color=ROSE)
    c.rect(100, 30, 240, 44, fill='#FFFFFF', sw=1.4, rx=6); c.text(220, 22, '휴대전화 (수전 코일 → 배터리)', size=11, weight=600); coil(c, 150, 44, n=9, w=16, h=22, color=PERI)
    for x in (150, 220, 290): c.path(f'M{x} 118 C {x - 20} 100, {x - 20} 80, {x} 76', sw=1.2, dash='4 3', arrow=True, op=0.8); c.path(f'M{x + 20} 76 C {x + 40} 80, {x + 40} 100, {x + 20} 118', sw=1.2, dash='4 3', op=0.8)
    c.text(392, 90, '변하는', size=10, anchor='start'); c.text(392, 104, '자기장', size=10, anchor='start')

@fig('11-4', 460, 200, '자기장 영역에 들어가고, 지나고, 나오는 사각 도선의 유도 전류')
def _(c):
    c.rect(150, 40, 200, 120, fill=P_SKY, sw=1.2, op=0.6)
    for x in range(165, 350, 28):
        for y in range(55, 160, 28): c.text(x, y, '×', size=12, op=0.6)
    for i, (x, lab, cur) in enumerate([(110, '들어갈 때', '반시계'), (250, '지날 때', '0'), (330, '나올 때', '시계')]):
        c.rect(x - 30, 70, 60, 60, sw=2.2, color=INK if cur != '0' else '#999')
        c.text(x, 150, lab, size=11, weight=600); c.text(x, 168, f'전류 {cur}', size=11, color=ROSE if cur != '0' else INK, weight=700)
        if cur == '반시계': c.path(f'M{x + 14} 92 A 16 16 0 1 0 {x + 14} 108', sw=1.4, arrow=True, color=ROSE)
        if cur == '시계': c.path(f'M{x - 14} 92 A 16 16 0 1 1 {x - 14} 108', sw=1.4, arrow=True, color=ROSE)
    c.line(60, 25, 120, 25, sw=1.4, arrow=True); c.text(90, 12, '도선 이동 방향', size=10)

# ---------------- Δ12 ----------------
@fig('12-1', 560, 230, '이중 슬릿: 두 슬릿에서 스크린 각 점까지의 경로차가 밝고 어두움을 정한다')
def _(c):
    c.line(120, 30, 120, 200, sw=6, color=INK); c.rect(117, 100, 6, 10, fill='#FFFFFF', stroke='none'); c.rect(117, 130, 6, 10, fill='#FFFFFF', stroke='none')
    c.text(100, 105, 'S₁', size=11, anchor='end', weight=600); c.text(100, 135, 'S₂', size=11, anchor='end', weight=600)
    c.line(380, 30, 380, 200, sw=4, color=INK); c.text(380, 215, '스크린', size=11)
    for x in (40, 60, 80): c.line(x, 40, x, 195, sw=1.2, op=0.5)
    c.text(60, 215, '빛 (파장 λ)', size=11)
    for y, lab, col in [(120, 'O 경로차 0 · 밝음', SAGE), (80, 'P 경로차 λ/2 · 어두움', INK), (45, 'Q 경로차 λ · 밝음', SAGE)]:
        c.line(120, 105, 380, y, sw=1.2, color=col, op=0.9); c.line(120, 135, 380, y, sw=1.2, color=col, op=0.9)
        c.dot(380, y, color=col); c.text(392, y, lab, size=10, anchor='start', weight=600, color=col)

@fig('12-2', 460, 220, '공기에서 물로 들어갈 때는 법선 쪽으로, 물에서 공기로 나갈 때는 법선에서 멀어진다')
def _(c):
    for i, (top, bot, a1, a2, cap) in enumerate([('공기 n=1', '물 n=1.33', 50, 35, '공기 → 물: θ₂ < θ₁'), ('물 n=1.33', '공기 n=1', 35, 50, '물 → 공기: θ₂ > θ₁')]):
        x = 30 + i * 230; cx, cy = x + 100, 110
        c.rect(x, 110, 200, 80, fill=P_SKY if i == 0 else 'none', stroke='none', op=0.5); c.rect(x, 30, 200, 80, fill=P_SKY if i == 1 else 'none', stroke='none', op=0.5)
        c.line(x, 110, x + 200, 110, sw=1.6); c.line(cx, 35, cx, 185, sw=1, dash='4 3', op=0.7)
        r1, r2 = math.radians(a1), math.radians(a2)
        c.line(cx - 70 * math.sin(r1), cy - 70 * math.cos(r1), cx, cy, sw=2.2, color=ROSE, arrow=True)
        c.line(cx, cy, cx + 70 * math.sin(r2), cy + 70 * math.cos(r2), sw=2.2, color=ROSE, arrow=True)
        c.text(cx - 22, cy - 40, 'θ₁', size=11, italic=True); c.text(cx + 22, cy + 42, 'θ₂', size=11, italic=True)
        c.text(x + 8, 42, top, size=10, anchor='start', op=0.8); c.text(x + 8, 180, bot, size=10, anchor='start', op=0.8)
        c.text(cx, 208, cap, size=11, weight=600)

def lens(c, cx, cy, h=70):
    c.path(f'M{cx} {cy - h} Q {cx + 18} {cy} {cx} {cy + h} Q {cx - 18} {cy} {cx} {cy - h}', fill=P_SKY, sw=1.4, op=0.9)

@fig('12-3', 520, 300, '볼록 렌즈: 물체가 2f 밖이면 작은 거꾸로 실상, 초점 안이면 큰 바로 허상')
def _(c):
    # (가)
    cx, cy, f = 250, 80, 40; c.line(40, cy, 500, cy, sw=1, op=0.6); lens(c, cx, cy, 50)
    for k, lab in [(-1, 'F'), (1, 'F'), (-2, '2F'), (2, '2F')]: c.dot(cx + k * f, cy, r=2.5); c.text(cx + k * f, cy + 14, lab, size=9)
    ox, oh = cx - 3 * f, 30; c.vec(ox, cy, ox, cy - oh, color=INK, sw=2, label='물체', lx=-20, size=10)
    ix, ih = cx + 1.5 * f, -15; c.vec(ix, cy, ix, cy - ih, color=ROSE, sw=2, label='실상', lx=22, size=10)
    c.line(ox, cy - oh, cx, cy - oh, sw=1.2, color=SAGE); c.line(cx, cy - oh, ix, cy - ih, sw=1.2, color=SAGE)
    c.line(ox, cy - oh, ix, cy - ih, sw=1.2, color=SAGE); c.line(ox, cy - oh, cx, cy + oh / 2, sw=1.2, color=SAGE); c.line(cx, cy + oh / 2, ix, cy - ih, sw=1.2, color=SAGE)
    c.text(90, 25, '(가) 물체가 2f 밖 → 작은 거꾸로 실상', size=11, weight=600, anchor='start')
    # (나)
    cy = 220; c.line(40, cy, 500, cy, sw=1, op=0.6); lens(c, cx, cy, 50)
    for k, lab in [(-1, 'F'), (1, 'F')]: c.dot(cx + k * f, cy, r=2.5); c.text(cx + k * f, cy + 14, lab, size=9)
    ox, oh = cx - 0.6 * f, 24; c.vec(ox, cy, ox, cy - oh, color=INK, sw=2, label='물체', lx=18, ly=6, size=10)
    ix, ih = cx - 1.5 * f, 60; c.vec(ix, cy, ix, cy - ih, color=ROSE, sw=2, label='허상', lx=-20, size=10)
    # 광선 1: 축에 나란히 → 반대쪽 초점 방향으로
    c.line(ox, cy - oh, cx, cy - oh, sw=1.2, color=SAGE); c.line(cx, cy - oh, cx + 150, cy - oh + 150 * (oh / f), sw=1.2, color=SAGE)
    # 광선 2: 중심 통과 직진
    k = oh / (cx - ox); c.line(ox, cy - oh, cx + 150, cy + 150 * k, sw=1.2, color=SAGE)
    # 연장선(점선)이 같은 쪽에서 만남
    c.line(ix, cy - ih, cx, cy - oh, sw=1.2, color=SAGE, dash='4 3'); c.line(ix, cy - ih, ox, cy - oh, sw=1.2, color=SAGE, dash='4 3')
    c.text(90, 165, '(나) 물체가 초점 안 → 큰 바로 허상 (돋보기)', size=11, weight=600, anchor='start')

# ---------------- Δ13 ----------------
@fig('13-1', 380, 230, '광전 효과: 최대 운동 에너지는 진동수에 직선으로 비례, 밝기와 무관')
def _(c):
    g = G(c, 70, 30, 250, 150, 10, 10, 'f', 'K', ymin=-4).axes([(4, 'f₀')], [])
    g.line([(0, -4), (9.5, 5.5)], color=ROSE); g.line([(0, -4), (4, 0)], color=ROSE, dash='4 3')
    g.dot(4, 0, color=ROSE); g.dot(7, 3, color=INK); g.dot(7, 3, color=INK)
    c.text(g.px(0) - 8, g.py(-4), '−W', size=11, anchor='end', weight=600)
    c.text(g.px(6.2), g.py(6.2), '기울기 = h', size=11, weight=600, anchor='start')
    c.text(g.px(7.3), g.py(2.2), '밝기 달라도 같은 점', size=10, anchor='start', op=0.8)

@fig('13-2', 480, 170, '광자를 하나씩 보내도 점이 쌓이면 간섭무늬가 된다')
def _(c):
    import random
    random.seed(7)
    for i, n in enumerate([10, 100, 2000]):
        x0 = 30 + i * 150; c.rect(x0, 20, 130, 110, sw=1.2)
        for _ in range(n):
            while True:
                u = random.random(); p = (1 + math.cos(u * 6 * math.pi)) / 2
                if random.random() < p: break
            c.circle(x0 + 4 + u * 122, 24 + random.random() * 102, 1.2 if n > 100 else 2, fill=INK, stroke='none', op=0.7)
        c.text(x0 + 65, 150, f'광자 {n}개', size=11, weight=600)

@fig('13-3', 460, 200, '광학 현미경과 전자 현미경: 파장이 짧을수록 작은 것을 본다')
def _(c):
    for i, (t, wl, res, src, col) in enumerate([('광학 현미경', '가시광선 ~500 nm', '분해능 ~200 nm', '유리 렌즈', P_LEMON), ('전자 현미경', '전자 물질파 ~0.005 nm', '분해능 ~0.1 nm', '자기 렌즈(코일)', P_PERI)]):
        x = 40 + i * 230; c.rect(x, 30, 190, 130, fill=col, stroke='none', op=0.5, rx=6)
        c.text(x + 95, 50, t, size=13, weight=700); c.text(x + 95, 78, wl, size=11); c.text(x + 95, 100, res, size=11, weight=600, color=ROSE); c.text(x + 95, 122, src, size=11)
        c.text(x + 95, 178, '파장 ≈ 볼 수 있는 최소 크기', size=10, op=0.8)

# ---------------- Δ14 ----------------
@fig('14-1', 460, 250, '수소 원자 에너지 준위와 n=2로 떨어지는 전이가 내는 가시광선')
def _(c):
    levels = [(1, -13.6), (2, -3.4), (3, -1.51), (4, -0.85)]
    def py(E): return 30 + math.sqrt(max(0, -E) / 13.6) * 190
    c.line(60, 225, 60, 30, sw=1.2, arrow=True); c.text(60, 18, 'E (eV)', size=11)
    for n, E in levels:
        y = py(E); c.line(80, y, 260, y, sw=2); c.text(275, y, f'n = {n}   {E} eV', size=10, anchor='start')
    c.line(80, py(0), 260, py(0), sw=1, dash='4 3', op=0.6); c.text(275, py(0), 'n = ∞   0 (이온화)', size=10, anchor='start', op=0.7)
    for n, col, lab, x, ty in [(3, '#E05A5A', '3→2 빨강 656 nm', 120, 14), (4, '#3FA7C9', '4→2 청록 486 nm', 200, 28)]:
        c.line(x, py(dict(levels)[n]), x, py(-3.4), sw=2.2, color=col, arrow=True); c.text(x, py(-3.4) + ty, lab, size=9, color=col, weight=600)
    c.text(170, 242, '준위 간격은 위로 갈수록 좁아진다 (눈금은 비례가 아님)', size=10, op=0.8)

@fig('14-2', 480, 210, '도체·반도체·절연체의 에너지띠: 띠틈의 크기가 전기 전도를 정한다')
def _(c):
    for i, (t, gap, note) in enumerate([('도체', -14, '띠가 겹친다'), ('반도체', 22, '띠틈 좁음 ~1 eV'), ('절연체', 44, '띠틈 넓음')]):
        x = 40 + i * 150; top = 40; vb_top = 110 + gap
        c.rect(x, top, 100, 70 - 0 if gap >= 0 else 70, fill=P_SKY, stroke='none', op=0.8); c.text(x + 50, top + 14, '전도띠', size=10, weight=600)
        c.rect(x, vb_top, 100, 178 - vb_top, fill=P_ROSE, stroke='none', op=0.8); c.text(x + 50, vb_top + 13, '원자가 띠', size=10, weight=600)
        if gap > 0: c.vec(x + 120, vb_top, x + 120, top + 70, color=INK, sw=1.4); c.text(x + 126, (vb_top + top + 70) / 2, '띠틈', size=9, anchor='start')
        for k in range(8): c.dot(x + 10 + k * 12, min(vb_top + 28 + (k % 2) * 10, 170), r=2.2)
        if i == 0:
            for k in range(4): c.dot(x + 14 + k * 24, top + 40, r=2.2)
        if i == 1: c.dot(x + 60, top + 50, r=2.2)
        c.text(x + 50, 198, f'{t} · {note}', size=10, weight=600)

@fig('14-3', 460, 200, '규소 격자에 인(n형)과 붕소(p형)를 섞으면 남는 전자 또는 빈자리가 생긴다')
def _(c):
    for i, (t, dop, mark, sub) in enumerate([('n형', 'P', '전자', '인: 결합 전자 5개 → 하나 남음'), ('p형', 'B', '양공', '붕소: 결합 전자 3개 → 자리 하나 빔')]):
        x0 = 40 + i * 230
        for r in range(3):
            for k in range(3):
                cx, cy = x0 + 30 + k * 60, 40 + r * 50; lab = dop if (r, k) == (1, 1) else 'Si'
                c.circle(cx, cy, 13, fill=P_LEMON if lab == 'Si' else (P_SKY if i == 0 else P_ROSE), sw=1.2); c.text(cx, cy, lab, size=10, weight=600)
                if k < 2: c.line(cx + 13, cy, cx + 47, cy, sw=1)
                if r < 2: c.line(cx, cy + 13, cx, cy + 37, sw=1)
        if i == 0: c.dot(x0 + 108, 76, r=4, color=PERI); c.text(x0 + 122, 74, '남는 전자', size=9, anchor='start', color=PERI, weight=600)
        else: c.circle(x0 + 108, 76, 4, stroke=ROSE, sw=1.6); c.text(x0 + 122, 74, '양공', size=9, anchor='start', color=ROSE, weight=600)
        c.text(x0 + 90, 178, f'{t} · {sub}', size=10, weight=600)

@fig('14-4', 500, 210, 'p–n 접합: 순방향에서만 전류가 흐르고, 교류를 넣으면 한 방향만 남는다(정류)')
def _(c):
    for i, (t, ok, pl, pr) in enumerate([('순방향', True, '+', '−'), ('역방향', False, '−', '+')]):
        x = 30 + i * 170; c.rect(x, 60, 60, 50, fill=P_ROSE, sw=1.2); c.text(x + 30, 85, 'p', size=13, weight=700)
        c.rect(x + 60, 60, 60, 50, fill=P_SKY, sw=1.2); c.text(x + 90, 85, 'n', size=13, weight=700)
        c.rect(x + 60 - (3 if ok else 9), 60, (6 if ok else 18), 50, fill='#FFFFFF', stroke='none', op=0.9)
        c.text(x - 12, 85, pl, size=13, weight=700); c.text(x + 132, 85, pr, size=13, weight=700)
        if ok: c.vec(x + 10, 130, x + 110, 130, label='전류 흐름', ly=14, size=10)
        else: c.text(x + 60, 134, '전류 거의 0', size=10, weight=600, op=0.8)
        c.text(x + 60, 40, t, size=11, weight=600)
    g = G(c, 380, 40, 100, 60, 4, 1, 't', '입력', ymin=-1).axes(); g.line([(t, math.sin(math.pi * t)) for t in [k * 0.05 for k in range(81)]], color=INK, sw=1.4)
    g2 = G(c, 380, 125, 100, 60, 4, 1, 't', '출력', ymin=-1).axes(); g2.line([(t, max(0, math.sin(math.pi * t))) for t in [k * 0.05 for k in range(81)]], color=ROSE, sw=1.8)
    c.text(430, 200, '정류', size=11, weight=600)

# ---------------- Δ15 ----------------
@fig('15-1', 540, 220, '빛 시계: 우주선 안에서는 수직 왕복, 지구에서 보면 더 긴 지그재그')
def _(c):
    # 안
    c.line(60, 40, 140, 40, sw=4); c.line(60, 170, 140, 170, sw=4); c.line(100, 166, 100, 46, sw=1.6, color=ROSE, arrow=True); c.line(104, 46, 104, 166, sw=1.6, color=ROSE, arrow=True)
    c.text(100, 195, '우주선 안: 거리 2L', size=11, weight=600); c.text(118, 105, 'L', size=11, italic=True, anchor='start')
    # 지구
    for dx in (0, 80, 160): c.line(230 + dx, 40, 310 + dx, 40, sw=4, op=0.35 if dx else 1); c.line(230 + dx, 170, 310 + dx, 170, sw=4, op=0.35 if dx else 1)
    c.line(270, 166, 350, 46, sw=1.6, color=ROSE, arrow=True); c.line(350, 46, 430, 166, sw=1.6, color=ROSE, arrow=True)
    c.vec(300, 20, 380, 20, color=PERI, label='우주선 v', ly=-12, size=10)
    c.text(350, 195, '지구에서: 거리 > 2L, 속력은 같은 c → 시간이 더 걸린다', size=11, weight=600)

@fig('15-2', 480, 220, '뮤온: 지구는 시간 팽창으로, 뮤온은 길이 수축으로 같은 결론에 이른다')
def _(c):
    for i, (t, H, sub1, sub2) in enumerate([('지구 관점', 128, '대기 10 km', '뮤온 수명 2 → 14 μs'), ('뮤온 관점', 22, '대기 1.4 km (수축)', '수명 2 μs 그대로')]):
        x = 40 + i * 240; c.rect(x, 170 - H, 180, H, fill=P_SKY, stroke='none', op=0.6); c.ground(x, x + 180, 170, hatch=False)
        c.text(x + 90, 16, t, size=12, weight=700); c.text(x + 150, 170 - H - 8, sub1, size=10, weight=600)
        c.dot(x + 90, 170 - H + 4, r=4, color=ROSE); c.vec(x + 90, 170 - H + 10, x + 90, 160, color=ROSE, label='0.99c', lx=26, size=10)
        c.text(x + 90, 195, sub2, size=11, color=PERI, weight=600); c.text(x + 90, 212, '→ 지표에 도달', size=10, weight=600)

# ---------------- 총정리 연결도 ----------------
def node(c, x, y, w, h, title, sub='', fill=P_ROSE):
    c.rect(x, y, w, h, fill=fill, stroke='none', rx=4, op=0.85); c.text(x + w / 2, y + (h / 2 if not sub else h / 2 - 8), title, size=11, weight=700)
    if sub: c.text(x + w / 2, y + h / 2 + 9, sub, size=9, op=0.85)

@fig('R1-1', 560, 300, '힘과 에너지 개념 연결도: 그래프에서 F = ma를 거쳐 보존 법칙으로')
def _(c):
    node(c, 20, 20, 110, 44, 'Δ00 · Δ01', '벡터, 그래프, Δ'); node(c, 170, 20, 110, 44, 'Δ02', '등가속도, v–t 넓이')
    node(c, 225, 120, 110, 50, 'Δ03  F = ma', '힘은 속도를 바꾼다', fill=P_LEMON)
    node(c, 20, 220, 120, 44, 'Δ04', '계 나누기, 빗면, 마찰'); node(c, 170, 220, 110, 44, 'Δ05', 'ΣF = 0, Στ = 0'); node(c, 320, 220, 110, 44, 'Δ06', 'FΔt = Δp')
    node(c, 430, 120, 110, 50, 'Δ07', 'Fs = ΔK, 에너지 보존', fill=P_PERI)
    c.line(130, 42, 168, 42, sw=1.4, arrow=True); c.text(149, 30, 'a = Δv/Δt', size=9)
    c.line(225, 64, 265, 118, sw=1.4, arrow=True); c.text(228, 96, 'a 에 F 를 붙임', size=9, anchor='start')
    c.line(255, 170, 100, 218, sw=1.4, arrow=True); c.line(270, 170, 232, 218, sw=1.4, arrow=True); c.line(300, 170, 360, 218, sw=1.4, arrow=True)
    c.line(335, 145, 428, 145, sw=1.4, arrow=True); c.text(382, 133, '× 거리', size=9); c.text(400, 200, '× 시간 → Δ06', size=9)
    c.text(280, 285, '시간이 나오면 공식 · 힘이 나오면 F = ma · 처음과 나중만 있으면 보존', size=10, weight=600)

@fig('R2-1', 560, 260, '전기와 자기 연결도: 전하 → 전기장 → 전류 → 자기장 → 유도')
def _(c):
    node(c, 20, 100, 90, 50, '전하', 'Δ08 전기장·전위', fill=P_LEMON); node(c, 150, 100, 110, 50, 'Δ09', '전위차 → 전류, 축전기')
    node(c, 300, 40, 110, 46, 'Δ10 ①', '전류 → 자기장', fill=P_SAGE); node(c, 300, 160, 110, 46, 'Δ10 ②', '자기장 → 전류에 힘', fill=P_SAGE)
    node(c, 440, 100, 110, 50, 'Δ11', '변하는 자기장 → 전류', fill=P_PERI)
    c.line(110, 125, 148, 125, sw=1.4, arrow=True); c.text(129, 113, 'V', size=9, italic=True)
    c.line(260, 118, 298, 70, sw=1.4, arrow=True); c.line(260, 132, 298, 178, sw=1.4, arrow=True)
    c.line(410, 63, 480, 98, sw=1.4, arrow=True); c.text(455, 68, 'B 를 바꾸면', size=9, anchor='start')
    c.line(410, 183, 480, 152, sw=1.4, arrow=True); c.text(455, 190, '전동기', size=9, anchor='start')
    c.line(495, 100, 495, 30, sw=1.2, dash='4 3', arrow=True); c.text(495, 18, '발전기 · 무선 충전', size=9)
    c.text(280, 240, '있으면 힘(Δ10), 변하면 전류(Δ11)', size=10, weight=600)

@fig('R3-1', 560, 260, '빛과 물질 연결도: 파동 → 입자 → hf = ΔE, 그리고 c 불변')
def _(c):
    node(c, 20, 40, 120, 50, 'Δ12', '간섭 = 파동, 굴절·렌즈', fill=P_LEMON); node(c, 190, 40, 120, 50, 'Δ13', '광전 효과 = 입자, λ = h/mv')
    node(c, 360, 40, 130, 50, 'Δ14', '준위·띠틈 → 광자', fill=P_SAGE); node(c, 190, 160, 120, 50, 'Δ15', 'c 불변 → 시간·길이', fill=P_PERI)
    c.line(140, 65, 188, 65, sw=1.4, arrow=True); c.text(164, 53, '이중성', size=9); c.line(310, 65, 358, 65, sw=1.4, arrow=True); c.text(334, 53, 'E = hf', size=9)
    c.line(60, 90, 220, 158, sw=1.2, dash='4 3', arrow=True); c.text(110, 140, '빛의 속력 c', size=9, anchor='start')
    c.text(280, 240, '밝기는 광자 수, 진동수는 광자 하나의 에너지', size=10, weight=600)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for fid, build in FIGS.items():
        open(os.path.join(OUT, f'{fid}.svg'), 'w', encoding='utf-8').write(build())
    print(len(FIGS), 'figures')
