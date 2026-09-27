# -*- coding: utf-8 -*-
"""사슴 소녀 · 양 전사 · 요리사의 필드 파츠(기본 자세 한 장)를 CQ-Ref 기준으로 그립니다

파츠는 공통 몸체 chibi의 기본 자세(idle 00) 위에 얹힌다고 보고 그립니다. 캐릭터 상자 x 16~47 · y 28~59 —
머리 · 머리카락은 이 안에만. 머리 x 21~42 · y 28~46, 눈 y 39~43(중심 41), 몸통 y 46~53, 가까운 손 (38.5, 53.5).
머리카락은 fieldkit.hair_render(4단계 · 밝은 뭉치 · 가닥선 · 뾰족 끝)로, 앞머리 밑 이마 그림자는 앞머리 파츠에 넣습니다.

    python parts_gen.py   →  ./{캐릭터}/parts/{파츠}.png + parts.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lib"))
import fieldkit as fk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SKIN = "SKIN"


def base_body(sp):
    from PIL import Image
    import pixkit
    return pixkit.from_image("body", Image.open(os.path.join(HERE, "_body", "idle", "00.png")), sp)


def forehead(sp, body, hair_front):
    """앞머리 바로 아래 피부 1줄을 그림자 단계로 — 앞머리 파츠에 넣어 머리 앵커를 따라가게 합니다."""
    for y in range(1, sp.height):
        for x in range(sp.width):
            if hair_front.px[y - 1][x] and not hair_front.px[y][x] and body.px[y][x] == sp.c(SKIN, 1):
                hair_front.px[y][x] = sp.c(SKIN, 2)


def write(sp, name, order, parts, layers):
    d = os.path.join(HERE, name, "parts")
    os.makedirs(d, exist_ok=True)
    body = base_body(sp)
    if "hair_front" in layers:
        forehead(sp, body, layers["hair_front"])
    fk.outline_parts(sp, body, [layers[n] for n in order if n != "BODY"])
    for n in order:
        if n != "BODY":
            fk.save(sp, layers[n], os.path.join(d, n + ".png"))
    with open(os.path.join(d, "parts.json"), "w", encoding="utf-8") as f:
        json.dump({"order": order, "parts": parts}, f, ensure_ascii=False, indent=1)
    print("파츠 —", name, order)


def deer(sp):
    HAIR, CLOTH, WOOD, ACC = "HAIR", "CLOTH_B", "LEATHER", "ACCENT"
    L = {n: fk.layer(sp, n) for n in ("hair_back", "outfit", "hair_front", "antlers", "staff")}

    def back(t):
        t.ellipse(31, 36, 13.5, 12, 1)
        t.poly([(17, 36), (23, 36), (24, 54), (18, 54), (16, 46)], 1)
        t.poly([(40, 36), (45, 36), (46, 48), (44, 53), (40, 53)], 1)
    fk.hair_render(sp, L["hair_back"], back, HAIR, (0, 0), back=True,
                   strands=[(19, 40, 20, 52), (43, 40, 43, 50)])

    def front(t):
        t.poly([(19, 38), (19, 32), (23, 27), (31, 25), (39, 27), (43, 32), (43, 38),
                (41, 36), (40, 33), (36, 37), (34, 33), (30, 37), (27, 33), (24, 37), (22, 35)], 1)
    fk.hair_render(sp, L["hair_front"], front, HAIR, (27, 30), hi_size=(9, 3),
                   strands=[(31, 26, 27, 34), (31, 26, 34, 34), (31, 26, 23, 33), (31, 26, 39, 33)],
                   tips=[(22, 36), (27, 38), (34, 38), (40, 38)])
    a = L["antlers"]
    for m in (1, -1):
        x0 = 31 + m * 6
        a.line(x0, 29, x0 + m, 22, sp.c(WOOD, 1)); a.line(x0 + m, 22, x0 + m, 18, sp.c(WOOD, 1))
        a.line(x0 + m, 23, x0 + m * 5, 20, sp.c(WOOD, 1)); a.line(x0, 26, x0 - m * 3, 23, sp.c(WOOD, 1))
        a.line(x0 + m * 4, 20, x0 + m * 5, 17, sp.c(WOOD, 1))
        a.pixels([(x0 + m, 18), (x0 + m * 5, 17), (x0 - m * 3, 23)], sp.c(WOOD, 0))
    fk.paint(sp, L["outfit"], lambda t: t.poly([(27, 46), (37, 46), (38, 53), (40, 57), (24, 57), (26, 53)], 1), CLOTH, "cyl", 2)
    L["outfit"].pixels([(x, 51) for x in range(27, 38)], sp.c(ACC, 1))
    L["outfit"].pixels([(31, 47), (32, 47), (33, 47), (32, 48)], sp.c(SKIN, 1))
    L["outfit"].pixels([(29, 49), (35, 49), (32, 50)], sp.c(ACC, 0))
    L["outfit"].pixels([(29, 54), (28, 55), (35, 54), (36, 55)], sp.c(CLOTH, 2))     # 치마 주름
    s = L["staff"]
    s.line(43, 12, 43, 58, sp.c(WOOD, 1)); s.line(44, 12, 44, 58, sp.c(WOOD, 2))
    for p in [(43, 12), (44, 10), (46, 8), (49, 8), (51, 10), (52, 13), (51, 15)]:
        s.set(*p, sp.c(WOOD, 1))
    s.pixels([(45, 9), (46, 9), (47, 9), (48, 9)], sp.c(WOOD, 0))
    s.pixels([(45, 20), (42, 27), (45, 34), (42, 44)], sp.c("CLOTH_A", 1))
    order = ["hair_back", "BODY", "outfit", "staff", "hair_front", "antlers"]
    parts = {"hair_back": {"anchor": "head"}, "outfit": {"anchor": "body"}, "staff": {"anchor": "hand_R"},
             "hair_front": {"anchor": "head"}, "antlers": {"anchor": "head"}}
    write(sp, "deer_girl", order, parts, L)


def goat(sp):
    WOOL, HORN, CLOTH, METAL, LEATHER = "CLOTH_B", "LEATHER", "CLOTH_A", "METAL", "LEATHER"
    L = {n: fk.layer(sp, n) for n in ("hair_back", "outfit", "hair_front", "horns", "hammer")}
    fk.hair_render(sp, L["hair_back"], lambda t: t.ellipse(30.5, 36, 12, 11, 1), WOOL, (0, 0), back=True)

    def wool(t):
        t.ellipse(31, 32, 12, 7, 1)
        for cx, cy, r in ((21, 35, 3.2), (24, 27, 3.4), (31, 24.5, 3.6), (38, 27, 3.4), (39, 34, 3)):
            t.ellipse(cx, cy, r, r, 1)
    # 양털: 가닥선 대신 곱슬(c자) 그림자
    fk.hair_render(sp, L["hair_front"], wool, WOOL, (27, 28), hi_size=(8, 4))
    L["hair_front"].pixels([(25, 30), (24, 31), (33, 27), (34, 28), (38, 31), (39, 32), (29, 34), (28, 35), (35, 35), (36, 36)], sp.c(WOOL, 2))
    for cx in (20.5, 42.5):
        fk.paint(sp, L["horns"], lambda t, cx=cx: t.ellipse(cx, 30, 4.4, 4.4, 1), HORN, "sphere", 3)
        c = int(cx)
        L["horns"].pixels([(c - 2, 28), (c - 1, 27), (c, 27), (c + 1, 28), (c + 2, 29), (c + 2, 30), (c + 1, 31), (c, 32)], sp.c(HORN, 3))
    fk.paint(sp, L["outfit"], lambda t: t.poly([(27, 46), (37, 46), (38, 53), (38, 55), (26, 55), (26, 53)], 1), CLOTH, "cyl", 2)
    fk.paint(sp, L["outfit"], lambda t: fk.rect(t, 29, 47, 35, 51, 1), METAL, "sphere", 2)
    L["outfit"].pixels([(x, 52) for x in range(27, 38)], sp.c(LEATHER, 1))
    L["outfit"].pixels([(31, 52), (32, 52)], sp.c("ACCENT", 1))
    fk.paint(sp, L["outfit"], lambda t: t.ellipse(38.5, 47.5, 3.5, 2.5, 1), METAL, "sphere", 2)
    h = L["hammer"]
    h.line(41, 40, 41, 52, sp.c(LEATHER, 1)); h.line(42, 40, 42, 52, sp.c(LEATHER, 2))
    fk.paint(sp, h, lambda t: fk.rect(t, 38, 52, 52, 59, 1), METAL, "sphere", 2)
    h.pixels([(x, 55) for x in range(39, 52)], sp.c(METAL, 2))
    h.pixels([(40, 53), (41, 53), (50, 58), (51, 58)], sp.c(METAL, 3))
    order = ["hair_back", "BODY", "outfit", "hair_front", "horns", "hammer"]
    parts = {"hair_back": {"anchor": "head"}, "outfit": {"anchor": "body"}, "hair_front": {"anchor": "head"},
             "horns": {"anchor": "head"}, "hammer": {"anchor": "hand_R"}}
    write(sp, "goat_warrior", order, parts, L)


def cook(sp):
    """요리사 「모리」 — spec/design/characters/cook.md. 소품은 모자 하나(임시 허용치 상자 위 8도트)."""
    HAIR, WHITE, RED, PANTS, BTN = "HAIR", "CLOTH_B", "ACCENT", "CLOTH_A", "LEATHER"
    L = {n: fk.layer(sp, n) for n in ("hair_back", "outfit", "hair_front", "hat")}

    def back(t):
        t.ellipse(30.5, 37, 12, 10, 1)
        t.poly([(19, 36), (24, 36), (24, 46), (20, 46), (18, 42)], 1)
        t.poly([(39, 36), (43, 36), (44, 42), (42, 46), (39, 46)], 1)
    fk.hair_render(sp, L["hair_back"], back, HAIR, (0, 0), back=True, strands=[(21, 40, 21, 45), (42, 40, 42, 45)])

    def front(t):
        t.poly([(20, 38), (20, 32), (24, 29), (31, 28), (38, 29), (42, 32), (42, 38),
                (40, 36), (37, 38), (34, 35), (31, 38), (28, 35), (25, 38), (22, 36)], 1)
    fk.hair_render(sp, L["hair_front"], front, HAIR, (27, 31), hi_size=(8, 3),
                   strands=[(31, 29, 27, 35), (31, 29, 35, 35), (31, 29, 23, 34), (31, 29, 39, 34)],
                   tips=[(22, 37), (25, 39), (31, 39), (37, 39), (40, 37)])
    fk.paint(sp, L["outfit"], lambda t: t.poly([(27, 53), (37, 53), (37, 57), (27, 57)], 1), PANTS, "cyl", 3)
    for y in range(sp.height):
        for x in range(sp.width):
            if L["outfit"].px[y][x] == sp.c(PANTS, 1):
                L["outfit"].px[y][x] = sp.c(PANTS, 2)
    fk.paint(sp, L["outfit"], lambda t: t.poly([(27, 46), (37, 46), (38, 53), (38, 55), (26, 55), (26, 53)], 1), WHITE, "cyl", 2)
    L["outfit"].pixels([(34, 50), (34, 52)], sp.c(BTN, 1))
    L["outfit"].pixels([(31, 47), (31, 48), (31, 49), (31, 50), (31, 51)], sp.c(WHITE, 2))
    L["outfit"].pixels([(x, 47) for x in range(29, 36)] + [(x, 48) for x in range(30, 35)], sp.c(RED, 1))
    L["outfit"].pixels([(32, 49), (32, 50)], sp.c(RED, 2))
    L["outfit"].pixels([(37, 52), (26, 52)], sp.c(WHITE, 2))
    fk.paint(sp, L["hat"], lambda t: t.poly([(24, 30), (39, 30), (40, 24), (38, 20), (25, 20), (23, 24)], 1), WHITE, "cyl", 2)
    L["hat"].pixels([(x, 29) for x in range(25, 39)], sp.c(WHITE, 2))
    L["hat"].pixels([(27, 21), (28, 21), (33, 21), (34, 21)], sp.c(WHITE, 0))
    L["hat"].pixels([(29, 23), (30, 24), (35, 23), (36, 24)], sp.c(WHITE, 2))         # 주름
    order = ["hair_back", "BODY", "outfit", "hair_front", "hat"]
    parts = {"hair_back": {"anchor": "head"}, "outfit": {"anchor": "body"}, "hair_front": {"anchor": "head"},
             "hat": {"anchor": "head"}}
    write(sp, "cook", order, parts, L)


if __name__ == "__main__":
    sp = fk.load_spec()
    deer(sp)
    goat(sp)
    cook(sp)
