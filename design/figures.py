# -*- coding: utf-8 -*-
"""원고 그림 생성기 v2. 교과서 도식 수준: 입체 물체, 부드러운 배경, 색 구분 화살표, 이탤릭 수학 라벨.
python3 design/figures.py → manuscript/figures/*.svg"""
import math, os, random
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'manuscript', 'figures')

INK = '#3B3652'; MUTED = '#7C7791'
RED, BLUE, GREEN, PURPLE, ORANGE = '#E0455B', '#2F6FD6', '#2E9E6A', '#7C5CD6', '#F08C2E'
WOOD, WOOD_T, WOOD_S = '#F2C078', '#F9DDA6', '#D9A252'
STEEL, STEEL_T, STEEL_S = '#B8BED0', '#E2E6F0', '#8C93A8'
ROSEF, BLUEF, GREENF, LEMONF, PURPLEF = '#FFD1DA', '#CFE0FF', '#CFF0DD', '#FFF1B8', '#E3D9FF'
SANS = "font-family:'IBM Plex Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif"
SERIF = "font-family:'Times New Roman','Nanum Myeongjo','Apple Myungjo',serif"

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class C:
    def __init__(s, fid, w, h, label=''):
        s.fid, s.w, s.h, s.label = fid.replace('-', ''), w, h, label; s.parts = []; s.defs = []; s.n = 0
    def uid(s, p): s.n += 1; return f'{p}{s.fid}{s.n}'
    def add(s, x): s.parts.append(x); return s
    # ---------- gradients ----------
    def lgrad(s, c1, c2, angle=90, stops=None):
        i = s.uid('g'); a = math.radians(angle); x2, y2 = 50 + 50 * math.cos(a), 50 + 50 * math.sin(a); x1, y1 = 100 - x2, 100 - y2
        st = stops or [(0, c1), (1, c2)]
        s.defs.append(f'<linearGradient id="{i}" x1="{x1:.0f}%" y1="{y1:.0f}%" x2="{x2:.0f}%" y2="{y2:.0f}%">' + ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in st) + '</linearGradient>')
        return f'url(#{i})'
    def rgrad(s, c1, c2, cx=35, cy=35):
        i = s.uid('r'); s.defs.append(f'<radialGradient id="{i}" cx="{cx}%" cy="{cy}%" r="70%"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient>'); return f'url(#{i})'
    def shadow(s):
        i = s.uid('s'); s.defs.append(f'<filter id="{i}" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#3B3652" flood-opacity="0.18"/></filter>'); return f'url(#{i})'
    # ---------- primitives ----------
    def line(s, x1, y1, x2, y2, sw=1.6, color=INK, dash=None, arrow=False, op=1, cap='round'):
        d = f' stroke-dasharray="{dash}"' if dash else ''; m = f' marker-end="url(#{s.mk(color)})"' if arrow else ''
        return s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="{cap}"{d}{m} opacity="{op}"/>')
    def mk(s, color):
        key = 'm' + color.strip('#')
        if not any(f'id="{key}{s.fid}"' in d for d in s.defs):
            s.defs.append(f'<marker id="{key}{s.fid}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0.5 L10 5 L0 9.5 Q3 5 0 0.5 Z" fill="{color}"/></marker>')
        return key + s.fid
    def vec(s, x1, y1, x2, y2, color=RED, sw=3, label=None, lx=0, ly=0, size=14, halo=True):
        if halo: s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#FFFFFF" stroke-width="{sw + 4}" stroke-linecap="round" opacity="0.85"/>')
        s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" marker-end="url(#{s.mk(color)})"/>')
        if label: s.mlabel((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, color=color, size=size)
        return s
    def text(s, x, y, t, size=12, anchor='middle', color=INK, weight=400, italic=False, op=1, rotate=0, serif=False, halo=False):
        st = f"{SERIF if serif else SANS};font-size:{size}px;font-weight:{weight}" + (";font-style:italic" if italic else "")
        r = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ''
        if halo: s.add(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" dominant-baseline="middle" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" fill="none" style="{st}" opacity="0.9"{r}>{esc(t)}</text>')
        return s.add(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" dominant-baseline="middle" fill="{color}" style="{st}" opacity="{op}"{r}>{esc(t)}</text>')
    def mlabel(s, x, y, t, color=INK, size=14, anchor='middle'):
        """수학 라벨: 이탤릭 세리프 + 흰 테두리"""
        return s.text(x, y, t, size=size, anchor=anchor, color=color, italic=True, serif=True, weight=700, halo=True)
    def cap(s, x, y, t, size=11.5, color=INK, anchor='middle', weight=600): return s.text(x, y, t, size=size, anchor=anchor, color=color, weight=weight)
    def note(s, x, y, t, size=10.5, anchor='middle'): return s.text(x, y, t, size=size, anchor=anchor, color=MUTED, weight=500)
    def rect(s, x, y, w, h, fill='none', stroke=INK, sw=1.4, rx=0, op=1, dash=None, filt=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''; f = f' filter="{filt}"' if filt else ''
        return s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}" opacity="{op}"{d}{f}/>')
    def circle(s, x, y, r, fill='none', stroke=INK, sw=1.4, op=1, dash=None, filt=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''; f = f' filter="{filt}"' if filt else ''
        return s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"{d}{f}/>')
    def ellipse(s, x, y, rx, ry, fill='none', stroke=INK, sw=1.4, op=1):
        return s.add(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')
    def poly(s, pts, fill='none', stroke=INK, sw=1.4, op=1, close=True, dash=None, filt=None):
        p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts); d = f' stroke-dasharray="{dash}"' if dash else ''; f = f' filter="{filt}"' if filt else ''
        return s.add(f'<{"polygon" if close else "polyline"} points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" opacity="{op}"{d}{f}/>')
    def path(s, d, fill='none', stroke=INK, sw=1.6, op=1, dash=None, arrow=False, filt=None):
        da = f' stroke-dasharray="{dash}"' if dash else ''; m = f' marker-end="url(#{s.mk(stroke)})"' if arrow else ''; f = f' filter="{filt}"' if filt else ''
        return s.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" opacity="{op}"{da}{m}{f}/>')
    def dot(s, x, y, r=3.5, color=INK): return s.circle(x, y, r, fill=color, stroke='none')
    # ---------- 부품 ----------
    def panel(s, x=0, y=0, w=None, h=None, tint='#F5F3FA'):
        w = w or s.w; h = h or s.h
        return s.rect(x, y, w, h, fill=s.lgrad('#FFFFFF', tint, 90), stroke='none', rx=14)
    def ground(s, x1, x2, y, h=14, color='#DCD7E6'):
        s.rect(x1, y, x2 - x1, h, fill=s.lgrad(color, '#FFFFFF', 90), stroke='none'); return s.line(x1, y, x2, y, sw=1.6, color='#9E97B4')
    def box3d(s, x, y, w, h, d=12, face=WOOD, top=WOOD_T, side=WOOD_S, label='', size=13, lcolor=INK, shadow=True):
        f = s.shadow() if shadow else None
        s.poly([(x, y), (x + d, y - d), (x + w + d, y - d), (x + w, y)], fill=top, stroke=side, sw=1)
        s.poly([(x + w, y), (x + w + d, y - d), (x + w + d, y + h - d), (x + w, y + h)], fill=side, stroke=side, sw=1)
        s.rect(x, y, w, h, fill=s.lgrad(face, side, 0, [(0, face), (0.85, face), (1, side)]), stroke=side, sw=1, filt=f)
        if label: s.text(x + w / 2, y + h / 2, label, size=size, weight=700, color=lcolor)
        return s
    def ball(s, x, y, r, color=RED, label='', size=12):
        light = '#FFFFFF'; s.circle(x, y, r, fill=s.rgrad(light, color, 35, 30), stroke=color, sw=1, filt=s.shadow())
        if label: s.text(x, y + r + 12, label, size=size, weight=600)
        return s
    def cylinder(s, x, y, w, h, color=STEEL, side=STEEL_S, top=STEEL_T, label=''):
        s.rect(x, y, w, h, fill=s.lgrad(top, side, 0, [(0, side), (0.25, top), (0.6, color), (1, side)]), stroke='none')
        s.ellipse(x + w / 2, y + h, w / 2, w / 8, fill=side, stroke='none'); s.ellipse(x + w / 2, y, w / 2, w / 8, fill=top, stroke=side, sw=1)
        if label: s.text(x + w / 2, y + h / 2, label, size=12, weight=700)
        return s
    def pulley(s, x, y, r=18):
        s.circle(x, y, r, fill=s.rgrad(STEEL_T, STEEL_S, 40, 40), stroke=STEEL_S, sw=1.2, filt=s.shadow()); s.circle(x, y, r * 0.35, fill=STEEL_S, stroke='none'); s.circle(x, y, 2.5, fill=INK, stroke='none'); return s
    def rope(s, x1, y1, x2, y2): return s.line(x1, y1, x2, y2, sw=2.2, color='#8A7A66')
    def cart(s, x, y, w, h, label='', face=BLUEF, side='#8FAEE8'):
        s.box3d(s, x, y, w, h, d=10, face=face, top='#EAF1FF', side=side, label=label) if False else None
        s.rect(x, y, w, h, fill=s.lgrad(face, side, 0, [(0, face), (0.8, face), (1, side)]), stroke=side, sw=1.2, rx=4, filt=s.shadow())
        for wx in (x + w * 0.25, x + w * 0.75): s.circle(wx, y + h + 6, 7, fill=s.rgrad('#9EA4B5', '#4A5063'), stroke='#3B3652', sw=1); s.circle(wx, y + h + 6, 2, fill='#FFF', stroke='none')
        if label: s.text(x + w / 2, y + h / 2, label, size=13, weight=700)
        return s
    def spring(s, x1, y, x2, n=8, amp=8, color='#6E6A80'):
        step = (x2 - x1) / (n * 2); pts = [(x1, y)]
        for k in range(1, n * 2): pts.append((x1 + k * step, y + (amp if k % 2 else -amp)))
        pts.append((x2, y)); return s.poly(pts, close=False, stroke=color, sw=2.2)
    def wall(s, x, y1, y2, side='left'):
        s.rect(x - 8 if side == 'left' else x, y1, 8, y2 - y1, fill='#C9C4D6', stroke='none')
        for yy in range(int(y1), int(y2), 10): s.line(x - 8 if side == 'left' else x, yy + 10, x if side == 'left' else x + 8, yy, sw=1, color='#8F89A6')
        return s
    def magnet(s, x, y, w, h, flip=False, vertical=False):
        n, so = ('#E0455B', '#2F6FD6') if not flip else ('#2F6FD6', '#E0455B')
        if vertical:
            s.rect(x, y, w, h / 2, fill=s.lgrad(n, '#B8203A' if n == RED else '#1F4FA8', 0), stroke='none', rx=2); s.rect(x, y + h / 2, w, h / 2, fill=s.lgrad(so, '#1F4FA8' if so == BLUE else '#B8203A', 0), stroke='none', rx=2)
            s.text(x + w / 2, y + h / 4, 'N' if not flip else 'S', size=13, weight=800, color='#FFF'); s.text(x + w / 2, y + 3 * h / 4, 'S' if not flip else 'N', size=13, weight=800, color='#FFF')
        else:
            s.rect(x, y, w / 2, h, fill=s.lgrad('#FFFFFF', n, 90, [(0, '#FF9AA8' if n == RED else '#8FB3FF'), (0.4, n), (1, n)]), stroke='none', rx=2); s.rect(x + w / 2, y, w / 2, h, fill=s.lgrad('#FFFFFF', so, 90, [(0, '#8FB3FF' if so == BLUE else '#FF9AA8'), (0.4, so), (1, so)]), stroke='none', rx=2)
            s.text(x + w / 4, y + h / 2, 'N' if not flip else 'S', size=13, weight=800, color='#FFF'); s.text(x + 3 * w / 4, y + h / 2, 'S' if not flip else 'N', size=13, weight=800, color='#FFF')
        return s.rect(x, y, w, h, fill='none', stroke='#3B3652', sw=0.8, rx=2, op=0.5)
    def coil(s, x, y, n=6, w=14, h=36, color='#C9822E', horizontal=True):
        for k in range(n):
            if horizontal: s.path(f'M{x + k * w} {y + h / 2} C {x + k * w} {y - h * 0.15}, {x + (k + 1) * w} {y - h * 0.15}, {x + (k + 1) * w} {y + h / 2}', sw=2.4, stroke=color); s.path(f'M{x + (k + 1) * w} {y + h / 2} C {x + (k + 1) * w} {y + h * 1.15}, {x + k * w} {y + h * 1.15}, {x + k * w} {y + h / 2}', sw=2.4, stroke=color, op=0.35)
        return s
    def lens(s, cx, cy, h=70, w=18): return s.path(f'M{cx} {cy - h} Q {cx + w} {cy} {cx} {cy + h} Q {cx - w} {cy} {cx} {cy - h}', fill=s.lgrad('#EAF4FF', '#B9D6F5', 0), stroke='#6FA5DC', sw=1.4)
    def resistor(s, x, y, w=44, label='', vertical=False):
        if vertical: s.rect(x - 7, y, 14, w, fill='#FFF', stroke=INK, sw=1.4)
        else: s.rect(x, y - 7, w, 14, fill='#FFF', stroke=INK, sw=1.4)
        if label: s.text(x + (w / 2 if not vertical else 22), y - (16 if not vertical else -w / 2), label, size=12, weight=600, anchor='middle' if not vertical else 'start')
        return s
    def battery(s, x, y, label='', vertical=False):
        if vertical: s.line(x - 12, y - 6, x + 12, y - 6, sw=2.6); s.line(x - 6, y + 6, x + 6, y + 6, sw=1.6); s.text(x + 18, y - 8, '+', size=11, weight=700, anchor='start')
        else: s.line(x - 6, y - 12, x - 6, y + 12, sw=2.6); s.line(x + 6, y - 6, x + 6, y + 6, sw=1.6); s.text(x - 8, y - 18, '+', size=11, weight=700)
        if label: s.text(x, y + (26 if not vertical else 0) + (0 if not vertical else 0), label, size=12, weight=600, anchor='middle' if not vertical else 'start') if not vertical else s.text(x + 18, y + 10, label, size=12, weight=600, anchor='start')
        return s
    def person(s, x, y, h=60, color='#5B7BB5'):
        """단순 인물 실루엣(측면). 머리·몸·다리"""
        r = h * 0.13; s.circle(x, y - h + r, r, fill='#F2C9A8', stroke='none')
        s.path(f'M{x - h * 0.12} {y - h + 2.2 * r} L{x + h * 0.12} {y - h + 2.2 * r} L{x + h * 0.1} {y - h * 0.4} L{x - h * 0.1} {y - h * 0.4} Z', fill=color, stroke='none')
        s.line(x - h * 0.05, y - h * 0.4, x - h * 0.12, y, sw=h * 0.09, color='#3B4A6B', cap='round'); s.line(x + h * 0.05, y - h * 0.4, x + h * 0.14, y, sw=h * 0.09, color='#3B4A6B', cap='round')
        return s
    def svg(s):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" role="img" aria-label="{esc(s.label)}" style="max-width:100%;height:auto;display:block">'
                f'<defs>{"".join(s.defs)}</defs>{"".join(s.parts)}</svg>')

class G:
    """데이터 좌표 → 픽셀 그래프 (격자, 축, 영역 채움)"""
    def __init__(s, c, x0, y0, w, h, xmax, ymax, xl='', yl='', ymin=0, xmin=0, grid=True):
        s.c, s.x0, s.y0, s.w, s.h, s.xmax, s.ymax, s.ymin, s.xmin, s.xl, s.yl, s.grid = c, x0, y0, w, h, xmax, ymax, ymin, xmin, xl, yl, grid
    def px(s, x): return s.x0 + (x - s.xmin) / (s.xmax - s.xmin) * s.w
    def py(s, y): return s.y0 + s.h - (y - s.ymin) / (s.ymax - s.ymin) * s.h
    def pt(s, x, y): return (s.px(x), s.py(y))
    def axes(s, xt=(), yt=(), gx=None, gy=None):
        c = s.c; oy = s.py(0) if s.ymin < 0 else s.y0 + s.h
        c.rect(s.x0, s.y0, s.w, s.h, fill='#FFFFFF', stroke='none', op=0.6)
        if s.grid:
            gx = gx or [x for x, _ in xt]; gy = gy or [y for y, _ in yt]
            for x in gx: c.line(s.px(x), s.y0, s.px(x), s.y0 + s.h, sw=0.8, color='#DCD8E6')
            for y in gy: c.line(s.x0, s.py(y), s.x0 + s.w, s.py(y), sw=0.8, color='#DCD8E6')
        c.line(s.x0, oy, s.x0 + s.w + 16, oy, sw=1.6, arrow=True); c.line(s.x0, s.y0 + s.h, s.x0, s.y0 - 16, sw=1.6, arrow=True)
        if s.xl: c.mlabel(s.x0 + s.w + 30, oy, s.xl, size=14)
        if s.yl: c.mlabel(s.x0, s.y0 - 30, s.yl, size=14)
        for x, lab in xt: c.line(s.px(x), oy - 3, s.px(x), oy + 3, sw=1.2); c.text(s.px(x), oy + 15, str(lab), size=11.5, serif=True)
        for y, lab in yt: c.line(s.x0 - 3, s.py(y), s.x0 + 3, s.py(y), sw=1.2); c.text(s.x0 - 12, s.py(y), str(lab), size=11.5, anchor='end', serif=True)
        if not (s.ymin < 0): c.text(s.x0 - 8, oy + 14, 'O', size=11, serif=True, italic=True)
        return s
    def line(s, pts, color=INK, sw=2.6, dash=None): s.c.poly([s.pt(x, y) for x, y in pts], stroke=color, sw=sw, close=False, dash=dash); return s
    def area(s, pts, color=ROSEF, dark=None, op=0.9):
        base = [(pts[-1][0], 0), (pts[0][0], 0)]; fill = s.c.lgrad(color, dark or color, 90, [(0, color), (1, dark or color)])
        s.c.poly([s.pt(x, y) for x, y in list(pts) + base], fill=fill, stroke='none', op=op); return s
    def guide(s, x, y, both=True):
        c = s.c; px, py = s.pt(x, y); c.line(px, s.py(0), px, py, sw=1, dash='3 3', color=MUTED)
        if both: c.line(s.x0, py, px, py, sw=1, dash='3 3', color=MUTED)
        return s
    def dot(s, x, y, color=INK, r=4): s.c.circle(*s.pt(x, y), r, fill='#FFF', stroke=color, sw=2.2); return s

FIGS = {}
def fig(fid, w, h, label):
    def deco(fn):
        def build():
            c = C(fid, w, h, label); fn(c); return c.svg()
        FIGS[fid] = build; return fn
    return deco

# ================= Δ00 =================
@fig('00-1', 440, 190, '같은 크기 5 N의 힘 두 개, 동쪽과 북쪽')
def _(c):
    c.panel()
    c.ball(100, 120, 16, color='#5B7BB5'); c.vec(118, 120, 218, 120, label='F = 5 N', ly=22, size=13); c.note(168, 158, '동쪽')
    c.ball(320, 130, 16, color='#5B7BB5'); c.vec(320, 112, 320, 32, label='F = 5 N', lx=44, size=13); c.note(348, 130, '북쪽', anchor='start')
    c.cap(220, 24, '길이(크기)는 같고 방향만 다르다', size=12.5)

@fig('00-2', 560, 240, '동쪽 3과 북쪽 4의 합이 5가 되는 두 방법')
def _(c):
    c.panel()
    for i, (title, para) in enumerate([('꼬리에 머리 잇기', False), ('평행사변형의 대각선', True)]):
        ox, oy = 60 + i * 280, 190
        for gx in range(0, 5): c.line(ox + gx * 40, oy, ox + gx * 40, oy - 160, sw=0.8, color='#E4E0EC')
        for gy in range(0, 5): c.line(ox, oy - gy * 40, ox + 160, oy - gy * 40, sw=0.8, color='#E4E0EC')
        c.dot(ox, oy, r=4)
        if not para:
            c.vec(ox, oy, ox + 120, oy, color=BLUE, label='3', ly=18); c.vec(ox + 120, oy, ox + 120, oy - 160, color=BLUE, label='4', lx=16)
        else:
            c.vec(ox, oy, ox + 120, oy, color=BLUE, label='3', ly=18); c.vec(ox, oy, ox, oy - 160, color=BLUE, label='4', lx=-16)
            c.line(ox + 120, oy, ox + 120, oy - 160, sw=1.2, dash='5 4', color=MUTED); c.line(ox, oy - 160, ox + 120, oy - 160, sw=1.2, dash='5 4', color=MUTED)
        c.vec(ox, oy, ox + 120, oy - 160, color=RED, sw=3.5, label='합 5', lx=-34, ly=-6, size=15)
        c.cap(ox + 80, oy + 32, title, size=12.5)

@fig('00-3', 400, 260, 'x–t 그래프에서 기울기 3 m/s를 읽는 삼각형')
def _(c):
    c.panel(); g = G(c, 70, 40, 250, 170, 5, 15, 't (s)', 'x (m)').axes([(1, 1), (2, 2), (3, 3), (4, 4)], [(3, 3), (6, 6), (9, 9), (12, 12)])
    g.line([(0, 0), (4.6, 13.8)], color=BLUE); g.guide(4, 12); g.dot(4, 12, color=BLUE)
    c.line(*g.pt(0, 0), *g.pt(4, 0), sw=3, color=RED); c.line(*g.pt(4, 0), *g.pt(4, 12), sw=3, color=RED)
    c.mlabel(g.px(2), g.py(0) - 14, 'Δt = 4 s', color=RED, size=13); c.mlabel(g.px(4) + 40, g.py(6), 'Δx = 12 m', color=RED, size=13)
    c.cap(g.px(1.2), g.py(2.2), '기울기 = 12 ÷ 4 = 3 m/s', size=12.5, anchor='start')

@fig('00-4', 420, 240, '문제 6의 v–t 그래프: 직사각형 30 m와 삼각형 15 m')
def _(c):
    c.panel(); g = G(c, 70, 40, 280, 160, 11, 8, 't (s)', 'v (m/s)').axes([(5, 5), (10, 10)], [(2, 2), (4, 4), (6, 6)])
    g.area([(0, 6), (5, 6)], color=ROSEF, dark='#FFB5C2'); g.area([(5, 6), (10, 0)], color=PURPLEF, dark='#C9B8FF'); g.line([(0, 6), (5, 6), (10, 0)], color=BLUE)
    c.cap(g.px(2.5), g.py(3), '6 × 5 = 30 m', size=13); c.cap(g.px(6.7), g.py(1.8), '½ × 5 × 6 = 15 m', size=13)

# ================= Δ01 =================
@fig('01-1', 500, 150, '수직선 위 A(−2 m)에서 B(+5 m)로 갈 때 변위 +7 m')
def _(c):
    c.panel(); base = 100
    c.line(30, base, 470, base, sw=2, arrow=True)
    for x in range(-3, 7):
        px = 250 + x * 40; c.line(px, base - 5, px, base + 5, sw=1.4); c.text(px, base + 20, str(x), size=12, serif=True)
    c.cap(250, base + 38, 'O (원점)', size=11); c.mlabel(484, base - 16, 'x (m)', size=13)
    c.ball(170, base - 14, 11, color=RED); c.mlabel(170, base - 40, 'A', color=RED); c.ball(450, base - 14, 11, color=PURPLE); c.mlabel(450, base - 40, 'B', color=PURPLE)
    c.vec(184, base - 62, 436, base - 62, color=PURPLE, label='Δx = 5 − (−2) = +7 m', ly=-18, size=13)

@fig('01-2', 420, 250, '곡선 x–t 그래프에서 두 순간의 접선 기울기')
def _(c):
    c.panel(); g = G(c, 70, 40, 280, 160, 10, 10, 't', 'x', grid=False).axes([(2, 't₁'), (7, 't₂')], [])
    pts = [(t, 10 * (1 - math.exp(-t / 3.5))) for t in [i * 0.25 for i in range(41)]]; g.line(pts, color=BLUE)
    for t, col, lab in [(2, RED, '가파름 → 빠르다'), (7, PURPLE, '완만함 → 느리다')]:
        x = 10 * (1 - math.exp(-t / 3.5)); k = 10 / 3.5 * math.exp(-t / 3.5)
        c.line(*g.pt(t - 1.6, x - 1.6 * k), *g.pt(t + 1.6, x + 1.6 * k), sw=2.6, color=col); g.dot(t, x, color=col); g.guide(t, x, both=False)
        c.cap(g.px(t) + (14 if t > 5 else -14), g.py(x) - (22 if t > 5 else -30), lab, color=col, anchor='start' if t > 5 else 'end', size=11.5)

@fig('01-3', 460, 230, '원운동에서 속력이 같아도 속도 방향이 바뀌므로 Δv가 중심을 향한다')
def _(c):
    c.panel(); cx, cy, r = 150, 120, 82
    c.circle(cx, cy, r, sw=1.4, dash='6 5', stroke=MUTED); c.dot(cx, cy, r=3)
    a1, a2 = math.radians(-70), math.radians(-10)
    for a, lab in [(a1, 'v₁'), (a2, 'v₂')]:
        px, py = cx + r * math.cos(a), cy + r * math.sin(a); tx, ty = -math.sin(a), math.cos(a)
        c.ball(px, py, 9, color='#5B7BB5'); c.vec(px, py, px + 62 * tx, py + 62 * ty, color=BLUE, label=lab, lx=16, ly=-8)
    ox, oy = 330, 60
    v1 = (62 * -math.sin(a1), 62 * math.cos(a1)); v2 = (62 * -math.sin(a2), 62 * math.cos(a2))
    c.vec(ox, oy, ox + v1[0], oy + v1[1], color=BLUE, sw=2.2, label='v₁', lx=-16, halo=False); c.vec(ox, oy, ox + v2[0], oy + v2[1], color=BLUE, sw=2.2, label='v₂', lx=16, halo=False)
    c.vec(ox + v1[0], oy + v1[1], ox + v2[0], oy + v2[1], color=RED, label='Δv', lx=22, ly=8)
    c.cap(330, 185, '속력은 같지만 방향이 달라', size=11.5); c.cap(330, 203, 'Δv ≠ 0 → 가속도가 있다', color=RED, size=11.5)

@fig('01-4', 420, 240, '문제 7의 x–t 그래프: 0→12 m, 정지, 12→0 m')
def _(c):
    c.panel(); g = G(c, 70, 40, 280, 160, 10, 14, 't (s)', 'x (m)').axes([(3, 3), (5, 5), (9, 9)], [(4, 4), (8, 8), (12, 12)])
    g.line([(0, 0), (3, 12), (5, 12), (9, 0)], color=BLUE); g.guide(3, 12); g.guide(5, 12, both=False); g.dot(3, 12, color=BLUE); g.dot(5, 12, color=BLUE)

# ================= Δ02 =================
@fig('02-1', 380, 460, '정지에서 등가속도로 출발한 물체의 a–t, v–t, x–t 그래프')
def _(c):
    c.panel()
    for i, (yl, pts, lab, col) in enumerate([('a', [(0, 5), (5, 5)], '수평선', GREEN), ('v', [(0, 0), (5, 9)], '직선, 기울기 = a', BLUE), ('x', [(t, 0.36 * t * t) for t in [k * 0.5 for k in range(11)]], '포물선', PURPLE)]):
        g = G(c, 70, 40 + i * 145, 190, 100, 5.5, 10, 't', yl, grid=False).axes(); g.line(pts, color=col)
        c.cap(290, 90 + i * 145, lab, anchor='start', color=col, size=12.5)

@fig('02-2', 420, 250, 'v–t 사다리꼴을 직사각형 v₀t와 삼각형 ½at²로 나눈 그림')
def _(c):
    c.panel(); g = G(c, 80, 40, 260, 160, 6, 12, 't', 'v', grid=False).axes([(5, 't')], [(3, 'v₀'), (10, 'v')])
    g.area([(0, 3), (5, 3)], color=ROSEF, dark='#FFB5C2'); g.area([(0, 3), (5, 10)], color=PURPLEF, dark='#C9B8FF')
    g.line([(0, 3), (5, 10)], color=BLUE); g.line([(0, 3), (5, 3)], sw=1.4, dash='5 4', color=MUTED); g.guide(5, 10)
    c.mlabel(g.px(2.5), g.py(1.5), 'v₀t', size=15); c.mlabel(g.px(3.7), g.py(5.3), '½at²', size=15)

@fig('02-3', 420, 270, '자유 낙하하는 공의 0.1 s 간격 위치와 v–t 직선')
def _(c):
    c.panel(); x = 80; c.line(x, 22, x, 240, sw=1, color='#CFCADB'); c.ground(30, 150, 240)
    for i in range(6):
        y = 30 + 6.6 * i * i + 3 * i; c.ball(x, y, 7, color=RED)
        if i != 1: c.text(x + 18, y, f'{i * 0.1:.1f} s', size=10.5, anchor='start', serif=True)
    c.cap(90, 258, '간격이 점점 벌어진다', size=11.5)
    g = G(c, 230, 50, 140, 160, 0.6, 6, 't', 'v', grid=False).axes([(0.5, 0.5)], [(5, 5)]); g.line([(0, 0), (0.55, 5.5)], color=BLUE)
    c.cap(300, 245, '기울기 = g', size=12, color=BLUE)

@fig('02-4', 420, 240, '예제 1의 v–t 그래프: 2에서 10 m/s, 사다리꼴 넓이 24 m')
def _(c):
    c.panel(); g = G(c, 70, 40, 280, 160, 5, 12, 't (s)', 'v (m/s)').axes([(2, 2), (4, 4)], [(2, 2), (6, 6), (10, 10)])
    g.area([(0, 2), (4, 10)], color=ROSEF, dark='#FFB5C2'); g.line([(0, 2), (4, 10)], color=BLUE); g.guide(4, 10); g.dot(4, 10, color=BLUE)
    c.cap(g.px(2.2), g.py(3.4), '½(2 + 10) × 4 = 24 m', size=13)

@fig('02-5', 420, 250, '예제 3: A의 삼각형 넓이와 B의 직사각형 넓이가 t = 12 s에서 같아진다')
def _(c):
    c.panel(); g = G(c, 70, 40, 280, 160, 14, 28, 't (s)', 'v (m/s)').axes([(6, 6), (12, 12)], [(12, 12), (24, 24)])
    g.area([(0, 12), (12, 12)], color=PURPLEF, op=0.6); g.area([(0, 0), (12, 24)], color=ROSEF, op=0.6)
    g.line([(0, 12), (13.5, 12)], color=PURPLE); g.line([(0, 0), (13.5, 27)], color=RED); g.guide(12, 24); g.dot(12, 24, color=RED); g.dot(12, 12, color=PURPLE)
    c.cap(g.px(1), g.py(15.5), 'B: 12 × 12 = 144 m', color=PURPLE, anchor='start', size=12); c.cap(g.px(7.5), g.py(4.5), 'A: ½ × 12 × 24 = 144 m', color=RED, anchor='start', size=12)

@fig('02-6', 420, 240, '문제 6의 사다리꼴 v–t 그래프')
def _(c):
    c.panel(); g = G(c, 70, 40, 280, 160, 11, 10, 't (s)', 'v (m/s)').axes([(2, 2), (6, 6), (10, 10)], [(4, 4), (8, 8)])
    g.area([(0, 0), (2, 8), (6, 8), (10, 0)], color=ROSEF, dark='#FFB5C2', op=0.7); g.line([(0, 0), (2, 8), (6, 8), (10, 0)], color=BLUE); g.guide(2, 8, both=False); g.guide(6, 8, both=False)

# ================= Δ03 =================
@fig('03-1', 360, 230, '책상 위 책: 중력과 수직항력이 크기가 같아 알짜힘 0')
def _(c):
    c.panel(); c.rect(60, 160, 240, 14, fill=c.lgrad(WOOD_T, WOOD_S, 90), stroke=WOOD_S, sw=1, rx=2)
    for lx in (80, 280): c.rect(lx - 6, 174, 12, 40, fill=WOOD_S, stroke='none')
    c.box3d(140, 118, 80, 42, d=10, face='#C96B7A', top='#E39AA7', side='#9E4B5A', label='책', lcolor='#FFF')
    c.vec(180, 139, 180, 205, color=RED, label='mg', lx=26, ly=12); c.vec(180, 139, 180, 62, color=BLUE, label='N', lx=-18)
    c.cap(180, 28, '알짜힘 = N − mg = 0', size=13)

@fig('03-2', 400, 250, '수평면 위 상자의 자유 물체 그림: N, mg, F, f')
def _(c):
    c.panel(); c.ground(40, 360, 190)
    c.box3d(150, 130, 80, 60, d=12, label='')
    c.vec(190, 160, 190, 70, color=BLUE, label='N', lx=-18); c.vec(190, 160, 190, 235, color=RED, label='mg', lx=26, ly=12)
    c.vec(230, 160, 330, 160, color=RED, label='F', ly=-18); c.vec(150, 160, 80, 160, color=GREEN, label='f', ly=-18)
    c.cap(200, 30, '수직: N = mg     수평: F − f = ma', size=12.5)

@fig('03-3', 540, 250, '말과 수레를 따로 본 자유 물체 그림: 짝힘은 서로 다른 물체에 작용한다')
def _(c):
    c.panel(); c.ground(20, 520, 190)
    c.cart(60, 130, 130, 54, label='수레', face=LEMONF, side='#E0C860'); c.box3d(320, 110, 130, 80, d=12, face='#8FA9D8', top='#C4D4F2', side='#5F7AB5', label='말', lcolor='#FFF')
    c.vec(190, 145, 270, 145, color=RED, label='말이 당김', ly=-18, size=12); c.vec(60, 165, 14, 165, color=GREEN, label='마찰', ly=-16, size=12)
    c.vec(320, 165, 240, 165, color=PURPLE, label='수레가 당김', ly=16, size=12); c.vec(385, 186, 480, 186, color=RED, label='땅이 밈', ly=-16, lx=30, size=12)
    c.cap(125, 225, '수레: 말의 힘 > 마찰 → 앞으로', size=11.5); c.cap(385, 225, '말: 땅의 힘 > 수레의 힘 → 앞으로', size=11.5)

@fig('03-4', 400, 200, '맞닿은 A(2 kg)와 B(3 kg)를 10 N으로 미는 그림')
def _(c):
    c.panel(); c.ground(30, 370, 150)
    c.box3d(140, 100, 66, 50, d=10, label='A 2 kg', face=ROSEF, top='#FFE4E9', side='#E39AA7'); c.box3d(206, 84, 90, 66, d=10, label='B 3 kg', face=PURPLEF, top='#F0EAFF', side='#B9A5F0')
    c.vec(60, 125, 138, 125, color=RED, label='10 N', ly=-18); c.note(200, 32, '마찰 없음')

@fig('03-5', 400, 190, '실로 연결된 A(1 kg)와 B(2 kg), B를 6 N으로 당김')
def _(c):
    c.panel(); c.ground(30, 370, 140)
    c.box3d(80, 96, 60, 44, d=10, label='A 1 kg', face=ROSEF, top='#FFE4E9', side='#E39AA7'); c.box3d(210, 84, 80, 56, d=10, label='B 2 kg', face=PURPLEF, top='#F0EAFF', side='#B9A5F0')
    c.rope(140, 118, 210, 118); c.note(175, 104, '실'); c.vec(290, 112, 360, 112, color=RED, label='6 N', ly=-18)

# ================= Δ04 =================
@fig('04-1', 340, 280, '도르래에 3 kg과 2 kg을 매단 그림, 3 kg이 내려간다')
def _(c):
    c.panel(); c.rect(120, 20, 100, 8, fill='#C9C4D6', stroke='none'); c.line(170, 28, 170, 44, sw=2, color='#8F89A6'); c.pulley(170, 72, 30)
    c.rope(140, 72, 140, 150); c.rope(200, 72, 200, 190)
    c.box3d(112, 150, 56, 48, d=9, face=ROSEF, top='#FFE4E9', side='#E39AA7', label='3 kg'); c.box3d(176, 190, 48, 40, d=9, face=PURPLEF, top='#F0EAFF', side='#B9A5F0', label='2 kg')
    c.vec(96, 160, 96, 215, color=GREEN, label='a', lx=-14); c.vec(250, 225, 250, 170, color=GREEN, label='a', lx=14)
    c.cap(170, 262, '(+) 방향: 3 kg 내려감', size=11.5)

@fig('04-2', 440, 280, '빗면 위 물체의 중력을 빗면 방향과 수직 방향으로 분해')
def _(c):
    c.panel(); th = math.radians(30); ox, oy = 40, 240; L = 340
    c.poly([(ox, oy), (ox + L, oy), (ox + L, oy - L * math.tan(th))], fill=c.lgrad('#DDEAF8', '#B7CFEE', 90), stroke='#8FB0DA', sw=1.2)
    c.path(f'M{ox + 70} {oy} A 70 70 0 0 0 {ox + 70 * math.cos(th):.1f} {oy - 70 * math.sin(th):.1f}', sw=1.2, stroke=MUTED); c.mlabel(ox + 88, oy - 14, 'θ', size=14)
    bx, by = ox + 190, oy - 190 * math.tan(th); ux, uy = math.cos(th), -math.sin(th); nx, ny = -math.sin(th), -math.cos(th)
    pts = [(bx, by), (bx + 50 * ux, by + 50 * uy), (bx + 50 * ux + 36 * nx, by + 50 * uy + 36 * ny), (bx + 36 * nx, by + 36 * ny)]
    c.poly(pts, fill=c.lgrad(WOOD_T, WOOD, 60), stroke=WOOD_S, sw=1.2, filt=c.shadow())
    gx, gy = bx + 25 * ux + 18 * nx, by + 25 * uy + 18 * ny
    c.vec(gx, gy, gx, gy + 96, color=RED, label='mg', lx=-18, ly=30)
    c.vec(gx, gy, gx - 48 * ux, gy - 48 * uy, color=ORANGE, label='mg sinθ', lx=-48, ly=6, size=13)
    c.vec(gx, gy, gx - 83 * nx, gy - 83 * ny, color=ORANGE, label='mg cosθ', lx=48, ly=10, size=13)
    c.vec(gx, gy, gx + 83 * nx, gy + 83 * ny, color=BLUE, label='N', lx=-14)
    c.line(gx - 48 * ux, gy - 48 * uy, gx, gy + 96, sw=1, dash='4 3', color=MUTED); c.line(gx - 83 * nx, gy - 83 * ny, gx, gy + 96, sw=1, dash='4 3', color=MUTED)

@fig('04-3', 420, 250, '미는 힘과 마찰력: 정지 마찰은 미는 힘만큼, 최대를 넘으면 운동 마찰로')
def _(c):
    c.panel(); g = G(c, 70, 40, 280, 160, 10, 10, '미는 힘', '마찰력', grid=False).axes()
    g.line([(0, 0), (6, 6)], color=RED); g.line([(6, 6), (6, 4.5)], sw=1.4, dash='3 3', color=MUTED); g.line([(6, 4.5), (9.5, 4.5)], color=PURPLE)
    g.dot(6, 6, color=RED); g.guide(6, 6, both=True)
    c.cap(g.px(3.4), g.py(2.2), '정지 마찰 (기울기 1)', color=RED, anchor='start', size=11.5)
    c.cap(g.px(6.2), g.py(7.2), '최대 정지 마찰력 μₛN', anchor='start', size=11.5); c.cap(g.px(7.8), g.py(3.6), '운동 마찰 μₖN', color=PURPLE, size=11.5)
    c.text(g.x0 - 30, g.py(4.5), 'μₖN', size=11, serif=True, italic=True, anchor='end'); c.text(g.x0 - 30, g.py(6), 'μₛN', size=11, serif=True, italic=True, anchor='end')

@fig('04-4', 380, 230, '책상 위 4 kg 물체가 도르래 너머 1 kg 추에 연결됨')
def _(c):
    c.panel(); c.rect(40, 150, 240, 12, fill=c.lgrad(WOOD_T, WOOD_S, 90), stroke=WOOD_S, sw=1, rx=2); c.rect(60, 162, 10, 50, fill=WOOD_S, stroke='none'); c.rect(250, 162, 10, 50, fill=WOOD_S, stroke='none')
    c.box3d(100, 98, 90, 52, d=10, label='4 kg'); c.pulley(292, 138, 14)
    c.rope(190, 124, 292, 124); c.rope(306, 138, 306, 176); c.cylinder(292, 176, 28, 34, label='1 kg')
    c.vec(140, 80, 200, 80, color=GREEN, label='a', ly=-16); c.vec(330, 176, 330, 214, color=GREEN, label='a', lx=14)

# ================= Δ05 =================
@fig('05-1', 460, 210, '경첩 축에서 먼 곳과 가까운 곳에 같은 힘을 줄 때의 돌림힘')
def _(c):
    c.panel(); c.rect(60, 96, 340, 28, fill=c.lgrad(WOOD_T, WOOD, 90), stroke=WOOD_S, sw=1, rx=3); c.circle(60, 110, 8, fill=STEEL, stroke=STEEL_S, sw=1.4); c.dot(60, 110, r=2.5)
    c.note(60, 140, '경첩(축)'); c.circle(376, 110, 5, fill=STEEL_S, stroke='none')
    c.vec(370, 96, 370, 40, color=RED, label='F', lx=16); c.line(60, 156, 370, 156, sw=1.4, color=RED); c.line(60, 150, 60, 162, sw=1.4, color=RED); c.line(370, 150, 370, 162, sw=1.4, color=RED); c.cap(215, 172, 'r 큼 → 돌림힘 큼', color=RED)
    c.vec(120, 96, 120, 40, color=PURPLE, label='F', lx=-16); c.line(60, 80, 120, 80, sw=1.4, color=PURPLE); c.cap(140, 40, 'r 작음 → 돌림힘 작음', color=PURPLE, anchor='start')

def beam(c, x0, x1, y, loads, supports, marks):
    c.rect(x0, y - 7, x1 - x0, 14, fill=c.lgrad(WOOD_T, WOOD, 90), stroke=WOOD_S, sw=1, rx=2, filt=c.shadow())
    for x, lab in supports:
        c.poly([(x, y + 8), (x - 16, y + 36), (x + 16, y + 36)], fill=c.lgrad(STEEL_T, STEEL_S, 90), stroke=STEEL_S, sw=1.2); c.cap(x, y + 50, lab, size=12)
    for x, lab, col in loads: c.vec(x, y - 70, x, y - 10, color=col, label=lab, lx=30, ly=-12, size=13)
    for x, t in marks: c.text(x, y - 84, t, size=10.5, color=MUTED, serif=True)

@fig('05-2', 500, 220, '4 m 막대 위 1 m 지점의 600 N 사람과 중앙의 막대 무게 200 N, 받침 A·B')
def _(c):
    c.panel(); beam(c, 70, 430, 130, [(160, '600 N', RED), (250, '200 N', INK)], [(70, 'A'), (430, 'B')], [(70, '0'), (160, '1 m'), (250, '2 m'), (430, '4 m')])
    c.vec(70, 200, 70, 145, color=BLUE, label='Rₐ', lx=-22); c.vec(430, 200, 430, 145, color=BLUE, label='Rʙ', lx=22)

@fig('05-3', 460, 240, '조금 기울인 상자는 돌아오고, 많이 기울인 상자는 넘어진다')
def _(c):
    c.panel()
    for i, (ang, ok) in enumerate([(12, True), (40, False)]):
        cx = 120 + i * 230; c.ground(cx - 90, cx + 90, 190)
        a = math.radians(ang); w, h = 74, 96; px, py = cx - 30, 190
        pts = [(0, 0), (w, 0), (w, -h), (0, -h)]
        rp = [(px + x * math.cos(a) - y * math.sin(a), py + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
        c.poly(rp, fill=c.lgrad(WOOD_T, WOOD, 60), stroke=WOOD_S, sw=1.2, filt=c.shadow())
        gx, gy = px + (w / 2) * math.cos(a) - (-h / 2) * math.sin(a), py + (w / 2) * math.sin(a) + (-h / 2) * math.cos(a)
        c.circle(gx, gy, 5, fill=RED, stroke='#FFF', sw=1.5); c.line(gx, gy, gx, 190, sw=1.6, dash='5 4', color=RED); c.circle(gx, 190, 3, fill=RED, stroke='none')
        c.cap(cx, 218, '받침면 안 → 돌아온다' if ok else '받침면 밖 → 넘어진다', color=GREEN if ok else RED, size=12)

@fig('05-4', 500, 220, '6 m 막대: A(0 m), 물체 900 N(2 m), 막대 무게 300 N(3 m), B(5 m)')
def _(c):
    c.panel(); beam(c, 60, 440, 130, [(187, '900 N', RED), (250, '300 N', INK)], [(60, 'A'), (377, 'B')], [(60, '0'), (187, '2 m'), (250, '3 m'), (377, '5 m'), (440, '6 m')])

@fig('05-5', 420, 290, '벽에 기댄 사다리: 아래 끝을 축으로, 무게는 중앙, 벽의 힘은 위 끝에서 수평')
def _(c):
    c.panel(); c.wall(70, 20, 250, 'left'); c.ground(70, 380, 250)
    bx, by = 270, 250; th = math.radians(53); L = 250; tx, ty = bx - L * math.cos(th), by - L * math.sin(th)
    for k in (0, 1): c.line(bx - 6 + 12 * k, by, tx - 6 + 12 * k, ty, sw=5, color=WOOD_S)
    for k in range(1, 6):
        f = k / 6; x, y = bx + (tx - bx) * f, by + (ty - by) * f; c.line(x - 8, y, x + 8, y, sw=3, color=WOOD)
    mx, my = (bx + tx) / 2, (by + ty) / 2; c.vec(mx, my, mx, my + 76, color=RED, label='500 N', lx=34)
    c.vec(tx, ty, tx + 76, ty, color=BLUE, label='F (벽)', ly=-16, size=12); c.circle(bx, by, 6, fill=RED, stroke='#FFF', sw=1.5); c.cap(bx + 34, by - 14, '축', color=RED)
    c.vec(bx, by, bx - 76, by, color=GREEN, label='마찰', ly=16, size=12); c.path(f'M{bx - 40} {by} A 40 40 0 0 0 {bx - 40 * math.cos(th):.1f} {by - 40 * math.sin(th):.1f}', sw=1.2, stroke=MUTED); c.mlabel(bx - 56, by - 22, '53°', size=12)

# ================= Δ06 =================
@fig('06-1', 380, 230, '충돌할 때의 F–t 그래프: 산 모양 아래 넓이가 충격량')
def _(c):
    c.panel(); g = G(c, 70, 40, 260, 150, 10, 10, 't', 'F', grid=False).axes()
    pts = [(t, 9 * math.exp(-((t - 5) ** 2) / 1.6)) for t in [i * 0.25 for i in range(41)]]
    g.area(pts, color=ROSEF, dark='#FFB5C2'); g.line(pts, color=RED); c.cap(g.px(5), g.py(3), '넓이 = 충격량 = Δp', size=13)

@fig('06-2', 460, 230, '같은 충격량: 딱딱한 바닥은 높고 좁게, 에어백은 낮고 넓게')
def _(c):
    c.panel(); g = G(c, 70, 40, 340, 150, 12, 10, 't', 'F', grid=False).axes()
    hard = [(t, 9 * math.exp(-((t - 3) ** 2) / 0.35)) for t in [i * 0.1 for i in range(61)]]
    soft = [(t, 3 * math.exp(-((t - 7.5) ** 2) / 3.2)) for t in [i * 0.1 for i in range(41, 121)]]
    g.area(hard, color=ROSEF, dark='#FFB5C2'); g.line(hard, color=RED); g.area(soft, color=PURPLEF, dark='#C9B8FF'); g.line(soft, color=PURPLE)
    c.cap(g.px(3.3), g.py(9.6), '딱딱한 바닥: F 큼, Δt 짧음', color=RED, anchor='start', size=11.5); c.cap(g.px(7.5), g.py(4.3), '에어백: F 작음, Δt 긺', color=PURPLE, size=11.5)
    c.cap(g.px(6), g.py(-2.2), '두 넓이는 같다', size=12)

@fig('06-3', 460, 250, '정지한 두 사람이 서로 밀면 반대 방향으로, 운동량 크기가 같게 밀려난다')
def _(c):
    c.panel(); c.rect(20, 20, 420, 100, fill='#EEF4FF', stroke='none', rx=8); c.rect(20, 130, 420, 100, fill='#EEF4FF', stroke='none', rx=8)
    c.cap(230, 34, '밀기 전: p = 0', size=12.5); c.person(200, 112, 62, color='#5B7BB5'); c.person(258, 112, 50, color='#E29A4F'); c.line(40, 112, 420, 112, sw=1.2, color='#B9C6E8')
    c.cap(230, 144, '민 후: 60v₁ + 40v₂ = 0', size=12.5); c.person(120, 222, 62, color='#5B7BB5'); c.person(340, 222, 50, color='#E29A4F'); c.line(40, 222, 420, 222, sw=1.2, color='#B9C6E8')
    c.vec(96, 190, 46, 190, color=BLUE, label='v₁', ly=-16); c.vec(364, 195, 424, 195, color=BLUE, label='v₂ = 1.5v₁', ly=-16, size=12)
    c.note(120, 240, '60 kg'); c.note(340, 240, '40 kg')

@fig('06-4', 380, 230, '문제 8의 삼각형 F–t 그래프: 0.4 s, 최대 100 N')
def _(c):
    c.panel(); g = G(c, 70, 40, 260, 150, 0.5, 120, 't (s)', 'F (N)').axes([(0.2, 0.2), (0.4, 0.4)], [(50, 50), (100, 100)])
    g.area([(0, 0), (0.2, 100), (0.4, 0)], color=ROSEF, dark='#FFB5C2'); g.line([(0, 0), (0.2, 100), (0.4, 0)], color=RED); g.guide(0.2, 100); g.dot(0.2, 100, color=RED)

# ================= Δ07 =================
@fig('07-1', 560, 220, '일이 양수인 경우와 0인 두 경우')
def _(c):
    c.panel()
    for i, (t, sub) in enumerate([('밀어서 옮김', 'W = Fs > 0'), ('들고 가만히', 's = 0 → W = 0'), ('들고 수평 이동', 'F ⊥ s → W = 0')]):
        x = 30 + i * 180; c.ground(x, x + 160, 160)
        if i == 0:
            c.box3d(x + 34, 112, 48, 48, d=8); c.vec(x + 90, 136, x + 146, 136, color=RED, label='F', ly=-16); c.line(x + 58, 178, x + 130, 178, sw=1.4, arrow=True, color=BLUE); c.mlabel(x + 94, 192, 's', color=BLUE, size=13)
        else:
            c.person(x + 60, 160, 78, color='#5B7BB5'); c.box3d(x + 76, 84, 40, 34, d=7); c.vec(x + 96, 100, x + 96, 60, color=RED, label='F', lx=14)
            if i == 2: c.line(x + 40, 178, x + 130, 178, sw=1.4, arrow=True, color=BLUE); c.mlabel(x + 85, 192, 's', color=BLUE, size=13)
        c.cap(x + 80, 208, t, size=11.5); c.cap(x + 80, 22, sub, color=RED, size=11.5)

@fig('07-2', 380, 230, '용수철의 F–x 그래프: 삼각형 넓이가 ½kx²')
def _(c):
    c.panel(); g = G(c, 70, 40, 260, 150, 10, 10, 'x', 'F', grid=False).axes([(8, 'x')], [(8, 'kx')])
    g.area([(0, 0), (8, 8)], color=ROSEF, dark='#FFB5C2'); g.line([(0, 0), (9.5, 9.5)], color=RED); g.guide(8, 8); g.dot(8, 8, color=RED)
    c.cap(g.px(5.6), g.py(2), '½ · x · kx = ½kx²', size=13)

@fig('07-3', 500, 260, '롤러코스터 세 위치의 운동 에너지와 퍼텐셜 에너지 막대: 합은 일정')
def _(c):
    c.panel(); c.path('M30 70 C 90 70, 110 200, 180 200 S 250 95, 320 105 S 420 215, 470 215', sw=3, stroke='#8F89A6')
    c.path('M30 74 C 90 74, 110 204, 180 204 S 250 99, 320 109 S 420 219, 470 219', sw=1.2, stroke='#C9C4D6')
    for x, y, K, U, lab, bx, base in [(30, 70, 0, 100, '꼭대기', 48, 62), (180, 200, 100, 0, '바닥', 168, 190), (320, 105, 55, 45, '언덕', 300, 96)]:
        c.cart(x - 14, y - 22, 28, 16, face=RED, side='#B8203A'); bx = x + 22; base = y - 14
        c.rect(bx, base - U * 0.45, 12, U * 0.45, fill=PURPLE, stroke='none', rx=2); c.rect(bx + 14, base - K * 0.45, 12, K * 0.45, fill=RED, stroke='none', rx=2)
        c.cap(x, y + 26 if x != 30 else y + 40, lab, size=11)
    c.rect(400, 26, 12, 12, fill=PURPLE, stroke='none', rx=2); c.mlabel(420, 32, 'U = mgh', size=13, anchor='start'); c.rect(400, 46, 12, 12, fill=RED, stroke='none', rx=2); c.mlabel(420, 52, 'K = ½mv²', size=13, anchor='start')

@fig('07-4', 460, 190, '에너지 전환 사슬: 100 → 80 → 64, 단계마다 새어 나간 몫')
def _(c):
    c.panel()
    for i, (v, lab) in enumerate([(100, '공급 100'), (80, '1단계 후 80'), (64, '2단계 후 64')]):
        x = 50 + i * 140; c.rect(x, 40, 100, 100, fill='#DDEFE4', stroke='none', rx=4); c.rect(x, 140 - v, 100, v, fill=c.lgrad('#6FCB98', '#3BA36A', 90), stroke='none', rx=4)
        c.cap(x + 50, 160, lab, size=11.5); c.text(x + 50, 140 - v / 2, str(v), size=15, weight=800, color='#FFF')
        if i < 2: c.line(x + 106, 90, x + 134, 90, sw=1.8, arrow=True, color=RED); c.cap(x + 120, 72, '× 0.8', color=RED, size=11)
    c.note(230, 22, '옅은 부분이 열로 새어 나간 몫')

# ================= Δ08 =================
def charge(c, x, y, r, pos=True, size=14):
    col, dark = (RED, '#B8203A') if pos else (BLUE, '#1F4FA8')
    c.circle(x, y, r, fill=c.rgrad('#FFFFFF', col, 35, 30), stroke=dark, sw=1, filt=c.shadow()); c.text(x, y + 0.5, '+' if pos else '−', size=size, weight=800, color='#FFF')
def radial(c, cx, cy, out=True, n=8, r1=14, r2=46, col=INK):
    for k in range(n):
        a = 2 * math.pi * k / n; x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a); x2, y2 = cx + r2 * math.cos(a), cy + r2 * math.sin(a)
        c.line(*( (x1, y1, x2, y2) if out else (x2, y2, x1, y1) ), sw=1.4, arrow=True, color=col)

@fig('08-1', 560, 190, '전기력선 네 가지: (+) 점전하, (−) 점전하, (+)(−) 쌍, 평행판')
def _(c):
    c.panel(); radial(c, 75, 85, True); charge(c, 75, 85, 12, True); radial(c, 200, 85, False); charge(c, 200, 85, 12, False)
    for dy in (-42, -22, 0, 22, 42): c.path(f'M312 {85 + dy * 0.18:.0f} Q 350 {85 + dy * 1.7:.0f} 388 {85 + dy * 0.18:.0f}', sw=1.4, arrow=True)
    charge(c, 305, 85, 11, True); charge(c, 395, 85, 11, False)
    c.rect(450, 40, 90, 8, fill=c.lgrad('#FF9AA8', RED, 90), stroke='none', rx=2); c.rect(450, 122, 90, 8, fill=c.lgrad(BLUE, '#8FB3FF', 90), stroke='none', rx=2)
    for x in (462, 484, 506, 528): c.line(x, 50, x, 120, sw=1.4, arrow=True)
    for x, t in [(75, '(+) 바깥으로'), (200, '(−) 안쪽으로'), (350, '(+)(−) 쌍'), (495, '평행판: 균일')]: c.cap(x, 168, t, size=11.5)

@fig('08-2', 480, 240, '평행판 사이의 전기력선(아래로)과 등전위면(수평선), 두 전하가 받는 힘')
def _(c):
    c.panel(); c.rect(60, 40, 280, 10, fill=c.lgrad('#FF9AA8', RED, 90), stroke='none', rx=2); c.cap(352, 45, '+  전위 높음', anchor='start')
    c.rect(60, 190, 280, 10, fill=c.lgrad(BLUE, '#8FB3FF', 90), stroke='none', rx=2); c.cap(352, 195, '−  전위 0', anchor='start')
    for x in (90, 130, 270, 310): c.line(x, 52, x, 188, sw=1.4, arrow=True, color='#8A84A8')
    for y in (85, 120, 155): c.line(60, y, 340, y, sw=1.2, dash='6 4', color=PURPLE, op=0.8)
    c.text(36, 120, '등전위면', size=10.5, color=PURPLE, rotate=-90, weight=600)
    charge(c, 180, 100, 11, True); c.vec(180, 112, 180, 158, color=RED, label='F', lx=14)
    charge(c, 230, 140, 11, False); c.vec(230, 128, 230, 82, color=BLUE, label='F', lx=14)

# ================= Δ09 =================
def wire(c, pts, cur=None):
    c.poly(pts, close=False, sw=2, stroke=INK)
def bulb(c, x, y, r=10):
    c.circle(x, y, r, fill=c.rgrad('#FFF7C2', LEMONF), stroke=INK, sw=1.4); c.path(f'M{x - r * 0.6} {y + r * 0.6} L{x + r * 0.6} {y - r * 0.6} M{x - r * 0.6} {y - r * 0.6} L{x + r * 0.6} {y + r * 0.6}', sw=1.2)

@fig('09-1', 520, 220, '직렬은 길이 하나라 전류가 같고, 병렬은 두 갈래라 전압이 같다')
def _(c):
    c.panel()
    # 직렬
    wire(c, [(40, 60), (40, 170), (230, 170), (230, 60), (40, 60)]); c.battery(c, 135, 170, 'V') if False else None
    c.battery(135, 170); c.mlabel(135, 150, 'V', size=13); c.resistor(70, 60, 44, 'R₁'); c.resistor(150, 60, 44, 'R₂')
    c.line(40, 125, 40, 105, sw=1.6, arrow=True, color=RED); c.mlabel(26, 115, 'I', color=RED)
    c.cap(135, 205, '직렬: 전류 같음', size=12)
    # 병렬
    wire(c, [(300, 60), (300, 170), (490, 170), (490, 60), (300, 60)]); c.battery(395, 170); c.mlabel(395, 150, 'V', size=13)
    wire(c, [(335, 60), (335, 115), (455, 115), (455, 60)]); c.resistor(373, 60, 44, 'R₁'); c.resistor(373, 115, 44, 'R₂')
    c.line(300, 125, 300, 105, sw=1.6, arrow=True, color=RED); c.mlabel(286, 115, 'I', color=RED)
    c.line(345, 60, 362, 60, sw=1.4, arrow=True, color=RED); c.line(345, 115, 362, 115, sw=1.4, arrow=True, color=RED); c.mlabel(352, 46, 'I₁', color=RED, size=12); c.mlabel(352, 130, 'I₂', color=RED, size=12)
    c.cap(395, 205, '병렬: 전압 같음', size=12)

@fig('09-2', 520, 230, '멀티탭에 병렬로 꽂힌 세 기기: 각 가지 전류가 공통 전선에 합쳐진다')
def _(c):
    c.panel(); c.rect(40, 60, 440, 34, fill=c.lgrad('#FFFFFF', '#E9E5F0', 90), stroke='#B9B3C9', sw=1.2, rx=6, filt=c.shadow()); c.cap(260, 77, '멀티탭 · 허용 전류 16 A (3520 W)', size=12)
    c.line(0, 77, 40, 77, sw=4, color=RED); c.note(18, 60, '220 V')
    for i, (lab, cur, col) in enumerate([('히터 2000 W', '9.1 A', '#E29A4F'), ('드라이어 1500 W', '6.8 A', '#5B7BB5'), ('주전자 1200 W', '5.5 A', '#3BA36A')]):
        x = 110 + i * 150; c.rect(x - 9, 94, 18, 10, fill='#B9B3C9', stroke='none'); c.line(x, 104, x, 136, sw=2)
        c.rect(x - 50, 136, 100, 44, fill=c.lgrad('#FFFFFF', col, 90, [(0, '#FFFFFF'), (1, col)]), stroke=col, sw=1.2, rx=6, filt=c.shadow()); c.cap(x, 158, lab, size=11, color='#3B3652')
        c.line(x + 12, 134, x + 12, 108, sw=1.6, arrow=True, color=RED); c.mlabel(x + 32, 121, cur, color=RED, size=12, anchor='start')
    c.cap(260, 208, '총 전류 = 9.1 + 6.8 + 5.5 = 21.4 A  >  16 A', color=RED, size=13)

@fig('09-3', 560, 230, '평행판 축전기: 전지 연결 유지 시 전하 절반, 전지 분리 시 전압 두 배')
def _(c):
    c.panel()
    for i, (d, q, v, sub, batt) in enumerate([(30, 8, '10 V', '(가) 거리 d', True), (60, 4, '10 V', '(나) 전지 연결, 2d', True), (60, 8, '20 V', '(다) 전지 분리, 2d', False)]):
        x = 36 + i * 180; y = 100
        c.rect(x, y - d / 2 - 4, 96, 8, fill=c.lgrad('#FF9AA8', RED, 90), stroke='none', rx=2); c.rect(x, y + d / 2 - 4, 96, 8, fill=c.lgrad(BLUE, '#8FB3FF', 90), stroke='none', rx=2)
        for k in range(q):
            px = x + 8 + k * (80 / max(q - 1, 1)); c.text(px, y - d / 2 - 14, '+', size=11, weight=800, color=RED); c.text(px, y + d / 2 + 14, '−', size=11, weight=800, color=BLUE)
        if batt:
            wire(c, [(x + 96, y - d / 2), (x + 140, y - d / 2), (x + 140, y - 6)]); wire(c, [(x + 96, y + d / 2), (x + 140, y + d / 2), (x + 140, y + 6)])
            c.battery(x + 140, y, vertical=True)
        else:
            wire(c, [(x + 96, y - d / 2), (x + 116, y - d / 2)]); wire(c, [(x + 96, y + d / 2), (x + 116, y + d / 2)]); c.note(x + 134, y, '분리')
        c.cap(x + 60, 186, sub, size=11.5); c.cap(x + 60, 206, f'V = {v}', color=PURPLE, size=12)

@fig('09-4', 380, 200, '예제 1 회로: 12 V 전지, 2 Ω 직렬, 3 Ω과 6 Ω 병렬')
def _(c):
    c.panel(); wire(c, [(40, 40), (40, 160), (340, 160), (340, 40), (40, 40)]); c.battery(70, 160, '12 V'); c.resistor(110, 40, 44, '2 Ω')
    wire(c, [(220, 40), (220, 100), (300, 100), (300, 40)]); c.resistor(238, 40, 44, '3 Ω'); c.resistor(238, 100, 44, '6 Ω')
    c.line(40, 115, 40, 95, sw=1.6, arrow=True, color=RED); c.mlabel(26, 105, 'I', color=RED)

# ================= Δ10 =================
@fig('10-1', 520, 200, '강자성·상자성·반자성의 원자 자석 배열')
def _(c):
    c.panel(); c.vec(200, 24, 320, 24, color=PURPLE, label='외부 자기장', lx=-110, size=12)
    for i, (t, angs, L, col) in enumerate([('강자성', [0] * 9, 20, RED), ('상자성', [10, -25, 5, 30, -10, 15, -30, 0, 20], 12, INK), ('반자성', [180, 170, 190, 175, 185, 180, 172, 188, 180], 10, INK)]):
        x0 = 40 + i * 165; c.rect(x0, 44, 140, 116, fill='#FFFFFF', stroke='#E4E0EC', sw=1, rx=8)
        for k, a in enumerate(angs):
            cx, cy = x0 + 26 + (k % 3) * 44, 70 + (k // 3) * 36; r = math.radians(a)
            c.circle(cx, cy, 13, fill=ROSEF if i == 0 else '#F1EFF6', stroke='none')
            c.line(cx - L * math.cos(r), cy - L * math.sin(r), cx + L * math.cos(r), cy + L * math.sin(r), sw=2.4, arrow=True, color=col)
        c.cap(x0 + 70, 180, t, size=12.5)

@fig('10-2', 560, 240, '직선 전류, 원형 전류, 솔레노이드가 만드는 자기장과 오른손 규칙')
def _(c):
    c.panel()
    for r in (24, 44, 64): c.circle(95, 110, r, sw=1.3, stroke='#8A84A8'); c.path(f'M{95 + r} 110 A {r} {r} 0 0 0 {95 + r * 0.71:.0f} {110 - r * 0.71:.0f}', sw=1.3, arrow=True, stroke='#8A84A8')
    c.circle(95, 110, 9, fill=c.rgrad('#FFFFFF', RED), stroke='#B8203A', sw=1); c.dot(95, 110, r=2.5, color='#FFF')
    c.cap(95, 198, '직선 전류 (종이 밖으로)', size=11.5); c.note(95, 214, '동심원, 반시계')
    c.path('M235 110 A 45 22 0 1 1 325 110', sw=3, stroke=RED); c.path('M325 110 A 45 22 0 1 1 235 110', sw=3, stroke=RED, op=0.35); c.line(280, 150, 280, 62, sw=1.8, arrow=True, color='#8A84A8'); c.mlabel(280, 48, 'B', size=14)
    c.cap(280, 198, '원형 전류', size=11.5); c.note(280, 214, '중심을 뚫는 자기장')
    c.coil(390, 92, n=7, w=20, h=40); [c.line(378, y, 548, y, sw=1.4, arrow=True, color='#8A84A8') for y in (100, 112, 124)]
    c.text(384, 70, 'S', size=13, weight=800, color=BLUE); c.text(542, 70, 'N', size=13, weight=800, color=RED)
    c.cap(465, 198, '솔레노이드', size=11.5); c.note(465, 214, '안쪽에 나란한 자기장, 오른손')

@fig('10-3', 400, 240, '말굽자석 사이의 도선: 자기장 아래, 전류 오른쪽, 힘은 앞(종이 밖)')
def _(c):
    c.panel(); c.magnet(110, 22, 180, 44, vertical=False) if False else None
    c.rect(110, 22, 180, 42, fill=c.lgrad('#FF9AA8', RED, 90), stroke='#B8203A', sw=1, rx=3); c.text(200, 43, 'N', size=15, weight=800, color='#FFF')
    c.rect(110, 178, 180, 42, fill=c.lgrad(BLUE, '#8FB3FF', 90), stroke='#1F4FA8', sw=1, rx=3); c.text(200, 199, 'S', size=15, weight=800, color='#FFF')
    for x in (140, 200, 260): c.line(x, 68, x, 174, sw=1.3, arrow=True, color='#8A84A8')
    c.mlabel(300, 92, 'B', size=14, anchor='start')
    c.line(60, 120, 340, 120, sw=5, color='#C9822E'); c.vec(220, 120, 330, 120, color=RED, label='I', ly=16, halo=False)
    c.circle(200, 120, 12, fill='#FFF', stroke=GREEN, sw=2.2); c.dot(200, 120, r=3.5, color=GREEN); c.cap(200, 146, 'F (종이 밖으로)', color=GREEN, size=12)

@fig('10-4', 420, 240, '자기장 속 사각 코일: 두 변이 반대 힘을 받아 돌림힘이 생긴다')
def _(c):
    c.panel(); c.rect(40, 36, 44, 168, fill=c.lgrad('#FF9AA8', RED, 0), stroke='#B8203A', sw=1, rx=3); c.text(62, 120, 'N', size=15, weight=800, color='#FFF')
    c.rect(336, 36, 44, 168, fill=c.lgrad(BLUE, '#8FB3FF', 0), stroke='#1F4FA8', sw=1, rx=3); c.text(358, 120, 'S', size=15, weight=800, color='#FFF')
    for y in (70, 120, 170): c.line(88, y, 332, y, sw=1.2, arrow=True, color='#8A84A8', op=0.7)
    c.poly([(140, 80), (280, 80), (280, 160), (140, 160)], sw=4, stroke='#C9822E')
    c.vec(140, 120, 140, 58, color=GREEN, label='F', lx=-14); c.vec(280, 120, 280, 182, color=GREEN, label='F', lx=14)
    c.path('M185 42 A 30 14 0 0 1 235 42', sw=1.6, arrow=True, stroke=PURPLE); c.cap(210, 24, '회전', color=PURPLE)
    c.note(140, 176, '전류 ↑'); c.note(280, 66, '전류 ↓')

# ================= Δ11 =================
@fig('11-1', 560, 220, 'N극이 다가오면 코일이 N극을 만들어 밀고, 멀어지면 S극을 만들어 붙잡는다')
def _(c):
    c.panel()
    for i, (t, pole, d, cur) in enumerate([('다가올 때', 'N', 1, '전류 ↻'), ('멀어질 때', 'S', -1, '전류 ↺')]):
        x = 36 + i * 280; c.magnet(x, 76, 84, 30, flip=True)
        if d > 0: c.vec(x + 92, 91, x + 128, 91, color=BLUE)
        else: c.vec(x - 6, 91, x - 34, 91, color=BLUE)
        c.coil(x + 140, 72, n=6, w=16, h=40); c.text(x + 136, 52, pole, size=14, weight=800, color=RED if pole == 'N' else BLUE); c.text(x + 240, 52, 'S' if pole == 'N' else 'N', size=14, weight=800, color=BLUE if pole == 'N' else RED)
        c.cap(x + 188, 140, cur, size=12); c.cap(x + 130, 180, t, size=12.5); c.note(x + 130, 198, '코일이 변화를 방해한다')

@fig('11-2', 560, 280, '자기장 속에서 도는 코일 네 장면과 유도 전류의 사인 곡선')
def _(c):
    c.panel()
    for i, (ang, lab) in enumerate([(0, '0°'), (90, '90°'), (180, '180°'), (270, '270°')]):
        x = 80 + i * 130; c.line(x - 50, 66, x + 50, 66, sw=1.3, arrow=True, color='#8A84A8'); c.mlabel(x + 60, 66, 'B', size=12, anchor='start')
        w = 32 if ang % 180 == 0 else 4; c.rect(x - w, 36, 2 * w, 60, fill=c.lgrad(LEMONF, '#E0C860', 0), stroke='#C9A83A', sw=1.2, rx=2)
        c.cap(x, 116, lab, size=11.5)
    g = G(c, 70, 156, 440, 90, 4, 1, 't', 'I', ymin=-1, grid=False).axes()
    g.line([(t, math.cos(math.pi * t / 2)) for t in [k * 0.05 for k in range(81)]], color=RED)
    c.cap(290, 268, '반 바퀴마다 방향이 바뀐다 → 교류', size=12)

@fig('11-3', 480, 220, '충전 패드 코일의 변하는 자기장이 휴대전화 코일에 유도 전류를 만든다')
def _(c):
    c.panel(); c.rect(60, 150, 360, 44, fill=c.lgrad('#FFFFFF', '#D8E9DE', 90), stroke='#9CC7AE', sw=1.2, rx=8, filt=c.shadow()); c.cap(240, 210, '충전 패드 (교류 전류)', size=11.5); c.coil(140, 150, n=12, w=17, h=30, color='#C9822E')
    c.rect(110, 30, 260, 54, fill=c.lgrad('#FFFFFF', '#E6E2F1', 90), stroke='#9E97B4', sw=1.2, rx=10, filt=c.shadow()); c.cap(240, 22, '휴대전화 (수전 코일 → 배터리)', size=11.5); c.coil(160, 46, n=10, w=16, h=24, color=PURPLE)
    for x in (160, 240, 320): c.path(f'M{x} 148 C {x - 26} 130, {x - 26} 102, {x} 86', sw=1.4, dash='5 4', arrow=True, stroke=BLUE); c.path(f'M{x + 22} 86 C {x + 48} 102, {x + 48} 130, {x + 22} 148', sw=1.4, dash='5 4', stroke=BLUE, op=0.7)
    c.cap(436, 110, '변하는', color=BLUE, anchor='start', size=11); c.cap(436, 124, '자기장', color=BLUE, anchor='start', size=11)

@fig('11-4', 500, 230, '자기장 영역에 들어가고, 지나고, 나오는 사각 도선의 유도 전류')
def _(c):
    c.panel(); c.rect(160, 40, 220, 130, fill='#DCE8FA', stroke='#9EB8E0', sw=1, rx=6)
    for x in range(178, 380, 28):
        for y in range(56, 168, 28): c.text(x, y, '×', size=13, color='#6F8FC4')
    for i, (x, lab, cur) in enumerate([(118, '들어갈 때', '반시계'), (270, '지날 때', '0'), (360, '나올 때', '시계')]):
        c.rect(x - 32, 72, 64, 64, sw=3, stroke='#C9822E' if cur != '0' else '#B9B3C9', rx=2)
        c.cap(x, 190, lab, size=11.5); c.cap(x, 208, f'전류 {cur}', color=RED if cur != '0' else MUTED, size=12)
        if cur == '반시계': c.path(f'M{x + 16} 94 A 18 18 0 1 0 {x + 16} 114', sw=1.8, arrow=True, stroke=RED)
        if cur == '시계': c.path(f'M{x - 16} 94 A 18 18 0 1 1 {x - 16} 114', sw=1.8, arrow=True, stroke=RED)
    c.vec(50, 24, 120, 24, color=BLUE, label='도선 이동', ly=-14, size=12)

# ================= Δ12 =================
@fig('12-1', 600, 250, '이중 슬릿: 두 슬릿에서 스크린 각 점까지의 경로차가 밝고 어두움을 정한다')
def _(c):
    c.panel(); c.rect(24, 30, 90, 190, fill=c.lgrad('#FFF6D6', '#FFFFFF', 0), stroke='none')
    for x in (40, 62, 84, 106): c.line(x, 40, x, 210, sw=1.2, color='#E0B84A', op=0.8)
    c.cap(70, 234, '빛 (파장 λ)', size=11.5)
    c.rect(134, 30, 8, 190, fill=c.lgrad(STEEL_T, STEEL_S, 0), stroke=STEEL_S, sw=1); c.rect(133, 104, 10, 10, fill='#FFF', stroke='none'); c.rect(133, 136, 10, 10, fill='#FFF', stroke='none')
    c.mlabel(120, 109, 'S₁', size=12, anchor='end'); c.mlabel(120, 141, 'S₂', size=12, anchor='end')
    c.rect(420, 30, 10, 190, fill=c.lgrad(STEEL_T, STEEL_S, 0), stroke=STEEL_S, sw=1); c.cap(425, 234, '스크린', size=11.5)
    for y, lab, col in [(125, 'O  경로차 0 · 밝음', GREEN), (85, 'P  경로차 λ/2 · 어두움', MUTED), (48, 'Q  경로차 λ · 밝음', GREEN)]:
        c.line(138, 109, 420, y, sw=1.4, color=col); c.line(138, 141, 420, y, sw=1.4, color=col)
        c.circle(425, y, 5, fill='#FFF7C2' if col == GREEN else '#DAD6E4', stroke=col, sw=1.6); c.cap(440, y, lab, anchor='start', color=col, size=11.5)
    for y in (162, 200): c.circle(425, y, 5, fill='#FFF7C2', stroke=GREEN, sw=1.6)

@fig('12-2', 500, 240, '공기에서 물로 들어갈 때는 법선 쪽으로, 물에서 공기로 나갈 때는 법선에서 멀어진다')
def _(c):
    c.panel()
    for i, (top, bot, a1, a2, cap, water_top) in enumerate([('공기 n = 1', '물 n = 1.33', 50, 35, '공기 → 물: θ₂ < θ₁', False), ('물 n = 1.33', '공기 n = 1', 35, 50, '물 → 공기: θ₂ > θ₁', True)]):
        x = 30 + i * 240; cx, cy = x + 110, 120
        c.rect(x, 30, 220, 90, fill=c.lgrad('#DCEBFA', '#B7D3F0', 90) if water_top else '#FFFFFF', stroke='none', rx=6)
        c.rect(x, 120, 220, 90, fill=c.lgrad('#B7D3F0', '#DCEBFA', 90) if not water_top else '#FFFFFF', stroke='none', rx=6)
        c.line(x, 120, x + 220, 120, sw=1.6, color='#6FA5DC'); c.line(cx, 36, cx, 204, sw=1.2, dash='5 4', color=MUTED)
        r1, r2 = math.radians(a1), math.radians(a2)
        c.line(cx - 78 * math.sin(r1), cy - 78 * math.cos(r1), cx, cy, sw=3, color=RED, arrow=True); c.line(cx, cy, cx + 78 * math.sin(r2), cy + 78 * math.cos(r2), sw=3, color=RED, arrow=True)
        c.path(f'M{cx} {cy - 34} A 34 34 0 0 0 {cx - 34 * math.sin(r1):.1f} {cy - 34 * math.cos(r1):.1f}', sw=1.2, stroke=MUTED); c.mlabel(cx - 24, cy - 46, 'θ₁', size=12)
        c.path(f'M{cx} {cy + 34} A 34 34 0 0 0 {cx + 34 * math.sin(r2):.1f} {cy + 34 * math.cos(r2):.1f}', sw=1.2, stroke=MUTED); c.mlabel(cx + 26, cy + 48, 'θ₂', size=12)
        c.note(x + 10, 44, top, anchor='start'); c.note(x + 10, 198, bot, anchor='start'); c.cap(cx, 226, cap, size=11.5)

@fig('12-3', 560, 320, '볼록 렌즈: 물체가 2f 밖이면 작은 거꾸로 실상, 초점 안이면 큰 바로 허상')
def _(c):
    c.panel(); cx, f = 270, 42
    for j, (cy, title) in enumerate([(84, '(가) 물체가 2f 밖 → 작은 거꾸로 실상'), (236, '(나) 물체가 초점 안 → 큰 바로 허상 (돋보기)')]):
        c.line(40, cy, 540, cy, sw=1.2, color='#9E97B4'); c.lens(cx, cy, 52); c.cap(60, cy - 66, title, anchor='start', size=11.5)
        for k, lab in ([(-1, 'F'), (1, 'F'), (-2, '2F'), (2, '2F')] if j == 0 else [(-1, 'F'), (1, 'F')]): c.dot(cx + k * f, cy, r=3); c.text(cx + k * f, cy + 14, lab, size=10, serif=True, italic=True)
        if j == 0:
            ox, oh = cx - 3 * f, 30; ix, ih = cx + 1.5 * f, -15
            c.vec(ox, cy, ox, cy - oh, color=INK, sw=2.4, label='물체', lx=-24, size=11); c.vec(ix, cy, ix, cy - ih, color=RED, sw=2.4, label='실상', lx=24, size=11)
            c.line(ox, cy - oh, cx, cy - oh, sw=1.3, color=ORANGE); c.line(cx, cy - oh, ix, cy - ih, sw=1.3, color=ORANGE)
            c.line(ox, cy - oh, ix, cy - ih, sw=1.3, color=ORANGE); c.line(ox, cy - oh, cx, cy + oh / 2, sw=1.3, color=ORANGE); c.line(cx, cy + oh / 2, ix, cy - ih, sw=1.3, color=ORANGE)
        else:
            ox, oh = cx - 0.6 * f, 24; ix, ih = cx - 1.5 * f, 60
            c.vec(ox, cy, ox, cy - oh, color=INK, sw=2.4, label='물체', lx=22, ly=8, size=11); c.vec(ix, cy, ix, cy - ih, color=RED, sw=2.4, label='허상', lx=-24, size=11)
            c.line(ox, cy - oh, cx, cy - oh, sw=1.3, color=ORANGE); c.line(cx, cy - oh, cx + 120, cy - oh + 120 * (oh / f), sw=1.3, color=ORANGE)
            k = oh / (cx - ox); c.line(ox, cy - oh, cx + 60, cy + 60 * k, sw=1.3, color=ORANGE)
            c.line(ix, cy - ih, cx, cy - oh, sw=1.3, color=ORANGE, dash='5 4'); c.line(ix, cy - ih, ox, cy - oh, sw=1.3, color=ORANGE, dash='5 4')
            c.circle(cx + 150, cy - 40, 9, fill='#FFF', stroke=INK, sw=1.4); c.dot(cx + 150, cy - 40, r=3); c.note(cx + 150, cy - 58, '눈')

# ================= Δ13 =================
@fig('13-1', 420, 260, '광전 효과: 최대 운동 에너지는 진동수에 직선으로 비례, 밝기와 무관')
def _(c):
    c.panel(); g = G(c, 80, 40, 270, 170, 10, 10, 'f', 'K', ymin=-4, grid=False).axes([(4, 'f₀')], [])
    g.line([(0, -4), (9.5, 5.5)], color=RED); g.line([(0, -4), (4, 0)], color=RED, dash='5 4', sw=1.6)
    g.dot(4, 0, color=RED); g.dot(7, 3, color=INK); c.mlabel(g.px(0) - 10, g.py(-4), '−W', anchor='end', size=13)
    c.cap(g.px(6.4), g.py(6.4), '기울기 = h', anchor='start', size=12); c.note(g.px(7.3), g.py(2.2), '밝기가 달라도 같은 점', anchor='start')
    c.cap(g.px(1.2), g.py(-2.2), '전자가 안 나옴', anchor='start', size=11, color=MUTED); c.cap(g.px(5), g.py(-2.2), '전자가 나옴', anchor='start', size=11, color=RED)

@fig('13-2', 520, 190, '광자를 하나씩 보내도 점이 쌓이면 간섭무늬가 된다')
def _(c):
    c.panel(); random.seed(7)
    for i, n in enumerate([10, 100, 2000]):
        x0 = 36 + i * 160; c.rect(x0, 24, 140, 118, fill='#1F1B2E', stroke='none', rx=6)
        for _ in range(n):
            while True:
                u = random.random(); pr = (1 + math.cos(u * 6 * math.pi)) / 2
                if random.random() < pr: break
            c.circle(x0 + 4 + u * 132, 28 + random.random() * 110, 1.4 if n > 100 else 2.2, fill='#FFE97A', stroke='none', op=0.85)
        c.cap(x0 + 70, 164, f'광자 {n}개', size=11.5)

@fig('13-3', 520, 230, '광학 현미경과 전자 현미경: 파장이 짧을수록 작은 것을 본다')
def _(c):
    c.panel()
    for i, (t, wl, res, src, col, dark) in enumerate([('광학 현미경', '가시광선 ~500 nm', '분해능 ~200 nm', '유리 렌즈', '#FFF6D6', '#E0B84A'), ('전자 현미경', '전자 물질파 ~0.005 nm', '분해능 ~0.1 nm', '자기 렌즈(코일)', '#E9E3FF', '#8A84E2')]):
        x = 40 + i * 250; c.rect(x, 30, 200, 150, fill=c.lgrad('#FFFFFF', col, 90), stroke=dark, sw=1.2, rx=10, filt=c.shadow())
        c.cap(x + 100, 54, t, size=14); c.cap(x + 100, 84, wl, size=11.5, weight=500); c.cap(x + 100, 108, res, size=12.5, color=RED); c.cap(x + 100, 132, src, size=11.5, weight=500)
        if i == 0: c.lens(x + 100, 160, 12, 5)
        else: c.coil(x + 70, 152, n=4, w=15, h=16)
    c.note(270, 208, '파장 ≈ 볼 수 있는 최소 크기. 파장이 짧을수록 더 작은 것을 본다')

# ================= Δ14 =================
@fig('14-1', 500, 270, '수소 원자 에너지 준위와 n=2로 떨어지는 전이가 내는 가시광선')
def _(c):
    c.panel(); levels = [(1, -13.6), (2, -3.4), (3, -1.51), (4, -0.85)]
    def py(E): return 34 + math.sqrt(max(0, -E) / 13.6) * 200
    c.line(70, 244, 70, 30, sw=1.6, arrow=True); c.mlabel(70, 18, 'E (eV)', size=13)
    for n, E in levels:
        y = py(E); c.line(90, y, 290, y, sw=2.4, color=INK); c.text(304, y, f'n = {n}', size=11.5, serif=True, italic=True, anchor='start'); c.text(360, y, f'{E} eV', size=11.5, serif=True, anchor='start')
    c.line(90, py(0), 290, py(0), sw=1.2, dash='5 4', color=MUTED); c.text(304, py(0), 'n = ∞', size=11.5, serif=True, italic=True, anchor='start', color=MUTED); c.text(360, py(0), '0 (이온화)', size=11, serif=True, anchor='start', color=MUTED)
    for n, col, lab, x, ty in [(3, '#E05A5A', '3→2  빨강 656 nm', 130, 16), (4, '#3FA7C9', '4→2  청록 486 nm', 210, 32)]:
        c.line(x, py(dict(levels)[n]), x, py(-3.4) - 2, sw=2.6, color=col, arrow=True); c.cap(x, py(-3.4) + ty, lab, size=10.5, color=col)
    c.note(190, 258, '준위 간격은 위로 갈수록 좁아진다 (눈금은 비례가 아님)')

@fig('14-2', 520, 230, '도체·반도체·절연체의 에너지띠: 띠틈의 크기가 전기 전도를 정한다')
def _(c):
    c.panel()
    for i, (t, gap, note) in enumerate([('도체', -14, '띠가 겹친다'), ('반도체', 22, '띠틈 좁음 ~1 eV'), ('절연체', 44, '띠틈 넓음')]):
        x = 44 + i * 160; top = 40; vb_top = 110 + gap
        c.rect(x, top, 110, 70, fill=c.lgrad('#EAF2FF', '#BFD4FF', 90), stroke='#9EB8E0', sw=1, rx=4); c.cap(x + 55, top + 14, '전도띠', size=10.5)
        c.rect(x, vb_top, 110, 186 - vb_top, fill=c.lgrad('#FFD9E0', '#FFB5C2', 90), stroke='#E39AA7', sw=1, rx=4); c.cap(x + 55, vb_top + 13, '원자가 띠', size=10.5)
        if gap > 0: c.vec(x + 126, vb_top, x + 126, top + 70, color=INK, sw=1.6, halo=False); c.note(x + 132, (vb_top + top + 70) / 2, '띠틈', anchor='start')
        for k in range(8): c.circle(x + 12 + k * 13, min(vb_top + 30 + (k % 2) * 10, 176), 2.6, fill=BLUE, stroke='none')
        if i == 0:
            for k in range(4): c.circle(x + 18 + k * 26, top + 44, 2.6, fill=BLUE, stroke='none')
        if i == 1: c.circle(x + 60, top + 52, 2.6, fill=BLUE, stroke='none')
        c.cap(x + 55, 210, f'{t} · {note}', size=10.5)

@fig('14-3', 500, 230, '규소 격자에 인(n형)과 붕소(p형)를 섞으면 남는 전자 또는 빈자리가 생긴다')
def _(c):
    c.panel()
    for i, (t, dop, sub) in enumerate([('n형', 'P', '인: 결합 전자 5개 → 하나 남음'), ('p형', 'B', '붕소: 결합 전자 3개 → 자리 하나 빔')]):
        x0 = 40 + i * 250
        for r in range(3):
            for k in range(3):
                cx, cy = x0 + 36 + k * 64, 48 + r * 54; lab = dop if (r, k) == (1, 1) else 'Si'
                if k < 2: c.line(cx + 15, cy, cx + 49, cy, sw=1.4, color='#B9B3C9')
                if r < 2: c.line(cx, cy + 15, cx, cy + 39, sw=1.4, color='#B9B3C9')
                col = LEMONF if lab == 'Si' else (BLUEF if i == 0 else ROSEF); dark = '#E0C860' if lab == 'Si' else (BLUE if i == 0 else RED)
                c.circle(cx, cy, 15, fill=c.rgrad('#FFFFFF', col), stroke=dark, sw=1.2); c.text(cx, cy, lab, size=11, weight=700)
        if i == 0: c.circle(x0 + 118, 84, 4.5, fill=BLUE, stroke='#FFF', sw=1.5); c.cap(x0 + 132, 82, '남는 전자', anchor='start', color=BLUE, size=10.5)
        else: c.circle(x0 + 118, 84, 4.5, fill='#FFF', stroke=RED, sw=2); c.cap(x0 + 132, 82, '양공', anchor='start', color=RED, size=10.5)
        c.cap(x0 + 100, 206, f'{t} · {sub}', size=10.5)

@fig('14-4', 590, 230, 'p–n 접합: 순방향에서만 전류가 흐르고, 교류를 넣으면 한 방향만 남는다(정류)')
def _(c):
    c.panel()
    for i, (t, ok, pl, pr) in enumerate([('순방향', True, '+', '−'), ('역방향', False, '−', '+')]):
        x = 30 + i * 180; c.rect(x, 70, 62, 54, fill=c.lgrad('#FFD9E0', '#FFB5C2', 90), stroke='none', rx=3); c.text(x + 31, 97, 'p', size=15, weight=800, serif=True, italic=True)
        c.rect(x + 62, 70, 62, 54, fill=c.lgrad('#DCE8FA', '#BFD4FF', 90), stroke='none', rx=3); c.text(x + 93, 97, 'n', size=15, weight=800, serif=True, italic=True)
        c.rect(x + 62 - (3 if ok else 10), 70, (6 if ok else 20), 54, fill='#FFFFFF', stroke='none', op=0.95); c.rect(x, 70, 124, 54, fill='none', stroke='#9E97B4', sw=1, rx=3)
        c.text(x - 12, 97, pl, size=15, weight=800); c.text(x + 136, 97, pr, size=15, weight=800)
        if ok: c.vec(x + 10, 146, x + 114, 146, color=RED, label='전류 흐름', ly=16, size=11.5)
        else: c.note(x + 62, 150, '전류 거의 0')
        c.cap(x + 62, 48, t, size=12)
    g = G(c, 410, 40, 120, 60, 4, 1, 't', '', ymin=-1, grid=False).axes(); g.line([(t, math.sin(math.pi * t)) for t in [k * 0.05 for k in range(81)]], color=INK, sw=1.8); c.note(470, 26, '입력(교류)')
    g2 = G(c, 410, 130, 120, 60, 4, 1, 't', '', ymin=-1, grid=False).axes(); g2.line([(t, max(0, math.sin(math.pi * t))) for t in [k * 0.05 for k in range(81)]], color=RED, sw=2.2); c.note(470, 116, '출력(정류)')

# ================= Δ15 =================
@fig('15-1', 560, 240, '빛 시계: 우주선 안에서는 수직 왕복, 지구에서 보면 더 긴 지그재그')
def _(c):
    c.panel()
    c.rect(70, 44, 90, 8, fill=c.lgrad(STEEL_T, STEEL_S, 90), stroke='none', rx=2); c.rect(70, 178, 90, 8, fill=c.lgrad(STEEL_S, STEEL_T, 90), stroke='none', rx=2)
    c.line(112, 176, 112, 54, sw=2.2, color=ORANGE, arrow=True); c.line(118, 54, 118, 176, sw=2.2, color=ORANGE, arrow=True); c.mlabel(134, 115, 'L', size=13)
    c.cap(115, 214, '우주선 안: 거리 2L', size=12)
    for dx, op in ((0, 1), (95, 0.45), (190, 0.2)): c.rect(250 + dx, 44, 90, 8, fill=STEEL_S, stroke='none', rx=2, op=op); c.rect(250 + dx, 178, 90, 8, fill=STEEL_S, stroke='none', rx=2, op=op)
    c.line(295, 176, 390, 54, sw=2.2, color=ORANGE, arrow=True); c.line(390, 54, 485, 176, sw=2.2, color=ORANGE, arrow=True)
    c.vec(320, 26, 420, 26, color=BLUE, label='우주선 v', ly=-14, size=12)
    c.cap(390, 214, '지구에서: 거리 > 2L, 속력은 같은 c → 시간이 더 걸린다', size=12)

@fig('15-2', 520, 250, '뮤온: 지구는 시간 팽창으로, 뮤온은 길이 수축으로 같은 결론에 이른다')
def _(c):
    c.panel()
    for i, (t, H, sub1, sub2) in enumerate([('지구 관점', 130, '대기 10 km', '뮤온 수명 2 → 14 μs'), ('뮤온 관점', 24, '대기 1.4 km (수축)', '수명 2 μs 그대로')]):
        x = 40 + i * 260; c.rect(x, 190 - H, 200, H, fill=c.lgrad('#EAF4FF', '#BFD9F5', 90), stroke='none', rx=6); c.ground(x, x + 200, 190)
        c.cap(x + 100, 20, t, size=13); c.note(x + 160, 190 - H - 10, sub1)
        c.ball(x + 100, 190 - H + 6, 7, color=PURPLE); c.vec(x + 100, 190 - H + 16, x + 100, 180, color=PURPLE, label='0.99c', lx=30, size=12)
        c.cap(x + 100, 214, sub2, color=BLUE, size=12); c.cap(x + 100, 234, '→ 지표에 도달', size=11)

# ================= 총정리 연결도 =================
def node(c, x, y, w, h, title, sub='', fill=ROSEF, dark='#E39AA7'):
    c.rect(x, y, w, h, fill=c.lgrad('#FFFFFF', fill, 90), stroke=dark, sw=1.2, rx=8, filt=c.shadow()); c.text(x + w / 2, y + (h / 2 if not sub else h / 2 - 8), title, size=12, weight=700)
    if sub: c.text(x + w / 2, y + h / 2 + 9, sub, size=9.5, color=MUTED, weight=500)

@fig('R1-1', 600, 320, '힘과 에너지 개념 연결도: 그래프에서 F = ma를 거쳐 보존 법칙으로')
def _(c):
    c.panel(); node(c, 24, 24, 120, 48, 'Δ00 · Δ01', '벡터, 그래프, Δ'); node(c, 184, 24, 120, 48, 'Δ02', '등가속도, v–t 넓이')
    node(c, 240, 128, 120, 54, 'Δ03  F = ma', '힘은 속도를 바꾼다', fill=LEMONF, dark='#E0C860')
    node(c, 24, 236, 130, 48, 'Δ04', '계 나누기, 빗면, 마찰'); node(c, 184, 236, 120, 48, 'Δ05', 'ΣF = 0, Στ = 0'); node(c, 344, 236, 120, 48, 'Δ06', 'FΔt = Δp')
    node(c, 460, 128, 120, 54, 'Δ07', 'Fs = ΔK, 에너지 보존', fill=PURPLEF, dark='#B9A5F0')
    c.line(144, 48, 182, 48, sw=1.6, arrow=True); c.note(163, 34, 'a = Δv/Δt')
    c.line(244, 72, 285, 126, sw=1.6, arrow=True); c.note(248, 104, 'a 에 F 를 붙임', anchor='start')
    c.line(270, 182, 110, 234, sw=1.6, arrow=True); c.line(290, 182, 250, 234, sw=1.6, arrow=True); c.line(320, 182, 390, 234, sw=1.6, arrow=True)
    c.line(360, 155, 458, 155, sw=1.6, arrow=True); c.note(409, 141, '× 거리'); c.note(420, 210, '× 시간 → Δ06')
    c.cap(300, 304, '시간이 나오면 공식 · 힘이 나오면 F = ma · 처음과 나중만 있으면 보존', size=11)

@fig('R2-1', 600, 280, '전기와 자기 연결도: 전하 → 전기장 → 전류 → 자기장 → 유도')
def _(c):
    c.panel(); node(c, 24, 110, 96, 54, '전하', 'Δ08 전기장·전위', fill=LEMONF, dark='#E0C860'); node(c, 160, 110, 120, 54, 'Δ09', '전위차 → 전류, 축전기')
    node(c, 320, 44, 120, 50, 'Δ10 ①', '전류 → 자기장', fill=GREENF, dark='#8FD0AA'); node(c, 320, 176, 120, 50, 'Δ10 ②', '자기장 → 전류에 힘', fill=GREENF, dark='#8FD0AA')
    node(c, 470, 110, 116, 54, 'Δ11', '변하는 자기장 → 전류', fill=PURPLEF, dark='#B9A5F0')
    c.line(120, 137, 158, 137, sw=1.6, arrow=True); c.mlabel(139, 122, 'V', size=12)
    c.line(280, 128, 318, 76, sw=1.6, arrow=True); c.line(280, 146, 318, 194, sw=1.6, arrow=True)
    c.line(440, 68, 510, 108, sw=1.6, arrow=True); c.note(486, 74, 'B 를 바꾸면', anchor='start')
    c.line(440, 200, 510, 166, sw=1.6, arrow=True); c.note(486, 208, '전동기', anchor='start')
    c.line(528, 110, 528, 34, sw=1.4, dash='5 4', arrow=True); c.note(528, 20, '발전기 · 무선 충전')
    c.cap(300, 262, '있으면 힘(Δ10), 변하면 전류(Δ11)', size=11)

@fig('R3-1', 600, 280, '빛과 물질 연결도: 파동 → 입자 → hf = ΔE, 그리고 c 불변')
def _(c):
    c.panel(); node(c, 24, 44, 130, 54, 'Δ12', '간섭 = 파동, 굴절·렌즈', fill=LEMONF, dark='#E0C860'); node(c, 204, 44, 130, 54, 'Δ13', '광전 효과 = 입자, λ = h/mv')
    node(c, 384, 44, 140, 54, 'Δ14', '준위·띠틈 → 광자', fill=GREENF, dark='#8FD0AA'); node(c, 204, 170, 130, 54, 'Δ15', 'c 불변 → 시간·길이', fill=PURPLEF, dark='#B9A5F0')
    c.line(154, 71, 202, 71, sw=1.6, arrow=True); c.note(178, 56, '이중성'); c.line(334, 71, 382, 71, sw=1.6, arrow=True); c.mlabel(358, 56, 'E = hf', size=12)
    c.line(70, 98, 240, 168, sw=1.4, dash='5 4', arrow=True); c.note(120, 150, '빛의 속력 c', anchor='start')
    c.cap(300, 262, '밝기는 광자 수, 진동수는 광자 하나의 에너지', size=11)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for fid, build in FIGS.items(): open(os.path.join(OUT, f'{fid}.svg'), 'w', encoding='utf-8').write(build())
    print(len(FIGS), 'figures')
