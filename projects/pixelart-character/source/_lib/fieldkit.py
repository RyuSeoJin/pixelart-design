# -*- coding: utf-8 -*-
"""필드 스프라이트(치비)를 코드로 그릴 때 쓰는 이 프로젝트의 도우미입니다

공통 몸체와 캐릭터 파츠를 그리는 스크립트가 함께 씁니다. 도형 · 명암 · 외곽선은 중앙 `pixel-art`
모듈의 `pixkit`을 쓰고, 여기에는 이 프로젝트의 그리기 습관(형태 셰이딩 · 파츠 외곽선 규칙)만 둡니다.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.abspath(os.path.join(PROJECT, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "core", "modules", "pixel-art", "scripts"))

import pixkit  # noqa: E402
import spec as specmod  # noqa: E402
from PIL import Image  # noqa: E402

FIELD_SPEC = os.path.join(PROJECT, "spec", "design", "pixel-spec-field.json")
LIGHT = (-0.5, -0.6, 0.62)
_n = math.sqrt(sum(v * v for v in LIGHT))
LIGHT = tuple(v / _n for v in LIGHT)


def load_spec():
    return specmod.load(FIELD_SPEC)


def layer(sp, name):
    return pixkit.Layer(name, sp.width, sp.height)


def rect(lay, x0, y0, x1, y1, c):
    """모서리를 포함한 사각형 — pixkit.Layer에는 없어서 여기 둡니다."""
    lay.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], c)


def paint(sp, lay, draw, ramp, kind="sphere", max_step=3):
    """draw(tmp)가 색 1로 칠한 모양을 램프로 형태 셰이딩해 lay에 얹습니다(광원 왼쪽 위)."""
    tmp = layer(sp, "tmp")
    draw(tmp)
    pts = [(x, y) for y in range(sp.height) for x in range(sp.width) if tmp.px[y][x]]
    if not pts:
        return
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    cx, cy = (x0 + x1 + 1) / 2, (y0 + y1 + 1) / 2
    rx, ry = max((x1 - x0 + 1) / 2, .5), max((y1 - y0 + 1) / 2, .5)
    for x, y in pts:
        if kind == "flat":
            step = 1
        else:
            nx = (x + .5 - cx) / rx
            ny = (y + .5 - cy) / ry if kind == "sphere" else 0.0
            r2 = nx * nx + ny * ny
            nz = math.sqrt(1 - r2) if r2 <= 1 else 0.0
            if r2 > 1:
                nx, ny = nx / math.sqrt(r2), ny / math.sqrt(r2)
            i = LIGHT[0] * nx + LIGHT[1] * ny + LIGHT[2] * nz
            step = 0 if i > .8 else 1 if i > .3 else 2 if i > -.05 else 3
        lay.set(x, y, sp.c(ramp, min(step, max_step)))


def outline_parts(sp, context, parts):
    """파츠 레이어에 외곽선을 두릅니다. 바깥(투명)에 닿으면 외곽선 색, 몸이나 다른 파츠 위면 그 파츠
    재질의 가장 어두운 단계(셀아웃). context는 이미 완성된 아래 그림(몸체)입니다."""
    for p in parts:
        p.add_outline()
    comp = pixkit.composite({"ctx": context, **{p.name: p for p in parts}}, ["ctx"] + [p.name for p in parts])
    for p in parts:
        for y in range(sp.height):
            for x in range(sp.width):
                if not p.outline[y][x]:
                    continue
                outside = any(not (0 <= x + dx < sp.width and 0 <= y + dy < sp.height)
                              or comp[y + dy][x + dx] == 0 for dx, dy in pixkit.NEIGH4)
                if outside:
                    continue
                own = next((p.px[y + dy][x + dx] for dx, dy in pixkit.NEIGH4
                            if p.inside(x + dx, y + dy) and p.px[y + dy][x + dx] > 1
                            and not p.outline[y + dy][x + dx]), None)
                r = sp.ramp_of(own) if own else None
                if r:
                    p.px[y][x] = sp.darkest(r[0])


def flatten(sp, layers):
    out = layer(sp, "flat")
    for lay in layers:
        for y in range(sp.height):
            for x in range(sp.width):
                if lay.px[y][x]:
                    out.px[y][x] = lay.px[y][x]
    return out


def save(sp, lay, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = Image.new("RGBA", (sp.width, sp.height), (0, 0, 0, 0))
    for y in range(sp.height):
        for x in range(sp.width):
            v = lay.px[y][x]
            if v:
                img.putpixel((x, y), tuple(sp.palette[v][:3]) + (255,))
    img.save(path)


def shift(sp, lay, dx, dy):
    out = layer(sp, lay.name)
    for y in range(sp.height):
        for x in range(sp.width):
            if lay.px[y][x]:
                out.set(x + dx, y + dy, lay.px[y][x])
    return out
