# -*- coding: utf-8 -*-
"""파일럿: 문제집 그림 3장을 우리 스타일로 새로 그린다. python3 design/pilot.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figures import C, INK, MUTED, RED, BLUE, GREEN, PURPLE, ORANGE, WOOD, WOOD_T, WOOD_S, STEEL, STEEL_T, STEEL_S
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'manuscript', 'figures', 'pilot')
SKIN, SKIN_D, SKIN_L = '#F3C9A6', '#D9A47E', '#FBE3CF'

def klabel(c, x, y, t, color=INK, size=15, anchor='middle'):
    """한글 라벨: 굵은 고딕 + 흰 테두리"""
    return c.text(x, y, t, size=size, anchor=anchor, color=color, weight=700, halo=True)

def table(c, x, y, w, h=110, front=26):
    """책상 윗면(원근) + 앞면"""
    c.poly([(x, y + front), (x + w, y + front), (x + w - 30, y), (x + 30, y)], fill=c.lgrad('#F6E2B8', '#E8C98E', 90), stroke='#C9A25C', sw=1)
    c.rect(x, y + front, w, h, fill=c.lgrad('#E8C98E', '#D6B276', 90), stroke='#C9A25C', sw=1)
    c.line(x, y + front, x + w, y + front, sw=1.2, color='#B8904A')

def hand_grip(c, x, y, s=1.0, flip=False):
    """주먹 쥔 손(측면), 손목은 오른쪽. (x, y)는 잡는 지점"""
    g = c.lgrad(SKIN_L, SKIN, 90); k = -1 if flip else 1
    def X(dx): return x + k * dx * s
    # 손목/팔
    c.rect(X(52), y - 20 * s, 60 * s, 40 * s, fill=c.lgrad('#8FB3FF', '#5B7BB5', 90), stroke='none', rx=8 * s) if not flip else c.rect(X(112), y - 20 * s, 60 * s, 40 * s, fill=c.lgrad('#8FB3FF', '#5B7BB5', 90), stroke='none', rx=8 * s)
    # 손바닥
    c.path(f'M{X(14)} {y - 26 * s} Q {X(70)} {y - 34 * s} {X(70)} {y - 4 * s} Q {X(70)} {y + 30 * s} {X(24)} {y + 30 * s} Q {X(0)} {y + 26 * s} {X(0)} {y + 6 * s} Q {X(0)} {y - 22 * s} {X(14)} {y - 26 * s} Z', fill=g, stroke=SKIN_D, sw=1.2)
    # 말린 손가락 네 개
    for i in range(4):
        fy = y - 18 * s + i * 12 * s
        c.rect(X(-8), fy, 30 * s, 11 * s, fill=c.lgrad(SKIN_L, SKIN, 90), stroke=SKIN_D, sw=1, rx=5.5 * s)
    # 엄지
    c.path(f'M{X(10)} {y - 22 * s} Q {X(-6)} {y - 18 * s} {X(-4)} {y - 6 * s} Q {X(-2)} {y + 2 * s} {X(12)} {y + 2 * s}', fill=g, stroke=SKIN_D, sw=1.1)

def hand_point(c, x, y, s=1.0):
    """검지로 미는 손(측면), 손목은 왼쪽. (x, y)는 손끝"""
    g = c.lgrad(SKIN_L, SKIN, 90)
    c.rect(x - 150 * s, y - 16 * s, 70 * s, 40 * s, fill=c.lgrad('#8FB3FF', '#5B7BB5', 90), stroke='none', rx=8 * s)
    # 손바닥(주먹)
    c.path(f'M{x - 96 * s} {y - 22 * s} Q {x - 40 * s} {y - 30 * s} {x - 34 * s} {y - 2 * s} Q {x - 34 * s} {y + 34 * s} {x - 80 * s} {y + 34 * s} Q {x - 104 * s} {y + 30 * s} {x - 104 * s} {y + 6 * s} Q {x - 104 * s} {y - 18 * s} {x - 96 * s} {y - 22 * s} Z', fill=g, stroke=SKIN_D, sw=1.2)
    # 검지(펴짐)
    c.rect(x - 44 * s, y - 7 * s, 46 * s, 13 * s, fill=c.lgrad(SKIN_L, SKIN, 90), stroke=SKIN_D, sw=1.1, rx=6.5 * s)
    # 말린 손가락 셋
    for i in range(3):
        c.rect(x - 60 * s, y + 6 * s + i * 10 * s, 26 * s, 9 * s, fill=c.lgrad(SKIN_L, SKIN, 90), stroke=SKIN_D, sw=1, rx=4.5 * s)
    # 엄지
    c.path(f'M{x - 70 * s} {y - 22 * s} Q {x - 52 * s} {y - 30 * s} {x - 40 * s} {y - 16 * s} Q {x - 34 * s} {y - 8 * s} {x - 46 * s} {y - 6 * s}', fill=g, stroke=SKIN_D, sw=1.1)

def spring_scale(c, x1, x2, y):
    """용수철저울: 왼쪽 갈고리 x1, 오른쪽 고리 x2, 중심선 y"""
    L = x2 - x1
    # 갈고리
    c.path(f'M{x1 + 26} {y} C {x1 + 12} {y}, {x1 + 4} {y - 10}, {x1 + 6} {y - 16} C {x1 + 8} {y - 22}, {x1 + 16} {y - 20}, {x1 + 14} {y - 13}', sw=2.4, stroke='#6E6A80')
    c.line(x1 + 26, y, x1 + 40, y, sw=3, color='#6E6A80')
    # 통(투명)
    tx, tw = x1 + 40, L - 90
    c.rect(tx, y - 13, tw, 26, fill=c.lgrad('#FFFFFF', '#DCDAE6', 90, [(0, '#FFFFFF'), (0.5, '#F4F3F8'), (1, '#D5D2E0')]), stroke='#9E97B4', sw=1.2, rx=5)
    # 눈금
    for i in range(1, 10): c.line(tx + 14 + i * (tw - 28) / 9, y - 12, tx + 14 + i * (tw - 28) / 9, y - 12 + (7 if i % 5 == 0 else 4), sw=1, color='#8A84A8')
    # 안쪽 용수철 + 지시판
    c.spring(tx + 6, y + 3, tx + tw * 0.62, n=9, amp=4, color='#8A84A8'); c.rect(tx + tw * 0.62 - 3, y - 9, 6, 18, fill=RED, stroke='none', rx=1.5)
    # 끝 고리 + 봉
    c.rect(tx + tw, y - 4, 22, 8, fill='#8A84A8', stroke='none', rx=2); c.circle(x2 - 12, y, 10, fill='none', stroke='#6E6A80', sw=3)

figs = {}
def fig(fid, w, h, label):
    def deco(fn):
        def build():
            c = C('P' + fid, w, h, label); fn(c); return c.svg()
        figs[fid] = build; return fn
    return deco

@fig('1', 640, 280, '책상 위 상자를 용수철저울로 끌 때 작용하는 네 힘')
def _(c):
    c.panel(); table(c, 40, 150, 560, 100, front=24)
    bx, by, bw, bh = 120, 96, 96, 78
    c.box3d(bx, by, bw, bh, d=16, face=WOOD, top=WOOD_T, side=WOOD_S)
    spring_scale(c, bx + bw + 16, 470, 138); hand_grip(c, 470, 138, 1.0)
    cx, cy = bx + bw / 2, by + bh / 2
    c.vec(cx, cy, cx, 22, color=BLUE, sw=3.5); klabel(c, cx + 14, 30, '수직 항력', BLUE, anchor='start')
    c.vec(cx, cy, cx, 262, color=PURPLE, sw=3.5); klabel(c, cx + 14, 250, '중력', PURPLE, anchor='start')
    c.vec(bx, by + bh - 6, 30, by + bh - 6, color=GREEN, sw=3.5); klabel(c, 60, by + bh - 24, '마찰력', GREEN)
    c.vec(bx + bw + 16, cy + 30, bx + bw + 130, cy + 30, color=RED, sw=3.5); klabel(c, bx + bw + 74, cy + 54, '끌어당기는 힘', RED)

@fig('2', 560, 280, '책을 손가락으로 밀 때: 힘의 작용점, 방향, 크기')
def _(c):
    c.panel(); c.rect(40, 224, 480, 30, fill=c.lgrad('#F6E2B8', '#D6B276', 90), stroke='#C9A25C', sw=1); c.line(40, 224, 520, 224, sw=1.2, color='#B8904A')
    # 책(세워 둠): 앞면(표지) + 위쪽 책장 + 책등 왼쪽
    x, y, w, h = 236, 40, 118, 184
    c.rect(x - 14, y + 6, 14, h - 6, fill=c.lgrad('#3E8E5C', '#2C6B44', 0), stroke='none', rx=3)   # 책등
    c.rect(x, y, w, h, fill=c.lgrad('#8FCFA6', '#4FA46F', 90, [(0, '#9AD6B0'), (0.15, '#5FB27D'), (1, '#3E8E5C')]), stroke='#2C6B44', sw=1.2, rx=2)
    c.rect(x + 20, y + 24, w - 40, 30, fill='#FFFFFF', stroke='none', op=0.55, rx=2)
    c.rect(x + 2, y - 8, w - 4, 8, fill=c.lgrad('#FFFFFF', '#D8D4C8', 90), stroke='#B8B4A8', sw=0.8)   # 책장 윗면
    for k in range(6): c.line(x + 4, y - 7 + k * 1.3, x + w - 4, y - 7 + k * 1.3, sw=0.4, color='#B8B4A8')
    # 손가락
    py = y + h / 2; hand_point(c, x - 14, py, 1.0)
    c.circle(x - 14, py, 4.5, fill=RED, stroke='#FFF', sw=1.5)
    # 힘 화살표(작용점에서 책을 관통해 오른쪽으로)
    c.vec(x - 14, py, x + w + 60, py, color=RED, sw=4)
    klabel(c, x + w + 66, py, '힘의 방향', RED, anchor='start')
    c.line(x - 14, py - 6, x - 70, y + 26, sw=1.2, color=INK); klabel(c, x - 74, y + 18, '힘의 작용점', INK, anchor='end')
    c.path(f'M{x - 14} {py + 12} Q {x + (w + 46) / 2} {py + 54} {x + w + 46} {py + 12}', sw=1.4, dash='5 4', stroke=INK)
    klabel(c, x + (w + 32) / 2, py + 62, '힘의 크기', INK)

@fig('3', 720, 260, '줄로 상자를 당길 때: 줄이 물체를, 줄이 손을, 손이 줄을 당기는 힘')
def _(c):
    c.panel(); c.rect(30, 190, 660, 44, fill=c.lgrad('#E4E1EA', '#CFCBD9', 90), stroke='none'); c.line(30, 190, 690, 190, sw=1.6, color='#9E97B4')
    bx, by, bw, bh = 70, 112, 96, 78; c.box3d(bx, by, bw, bh, d=14, face=WOOD, top=WOOD_T, side=WOOD_S)
    ry = by + bh / 2 + 6
    c.rope(bx + bw, ry, 470, ry); hand_grip(c, 470, ry, 1.0)
    c.vec(bx + bw, ry, bx + bw + 96, ry, color=RED, sw=4); klabel(c, bx + bw + 40, 62, '줄이 물체를', RED); klabel(c, bx + bw + 40, 84, '당기는 힘', RED)
    c.vec(470, ry - 10, 380, ry - 10, color=PURPLE, sw=4); klabel(c, 392, 62, '줄이 손을', PURPLE); klabel(c, 392, 84, '당기는 힘', PURPLE)
    c.vec(470, ry + 10, 560, ry + 10, color=GREEN, sw=4); klabel(c, 590, 96, '손이 줄을', GREEN, anchor='start'); klabel(c, 590, 118, '당기는 힘', GREEN, anchor='start')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for fid, build in figs.items(): open(os.path.join(OUT, f'pilot-{fid}.svg'), 'w', encoding='utf-8').write(build())
    print(len(figs), 'pilot figures')
