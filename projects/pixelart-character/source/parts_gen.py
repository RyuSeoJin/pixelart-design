# -*- coding: utf-8 -*-
"""사슴 소녀 · 양 전사의 필드 파츠(기본 자세 한 장)를 CQ-Ref 기준으로 그립니다

파츠는 공통 몸체 chibi의 기본 자세(idle 00) 위에 얹힌다고 보고 그립니다. 캐릭터 상자 x 16~47 · y 28~59 —
머리 · 머리카락은 이 안에만. 머리 x 21~42 · y 28~46, 눈 y 40~43, 몸통 y 46~53, 가까운 손 (38.5, 53.5). 소품은 몸보다 커도 되지만 얼굴 · 몸통을 가리지 않는 옆 · 아래 · 위에 둡니다.

    python parts_gen.py   →  ./{캐릭터}/parts/{파츠}.png + parts.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lib"))
import fieldkit as fk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def base_body(sp):
    from PIL import Image
    import pixkit
    return pixkit.from_image("body", Image.open(os.path.join(HERE, "_body", "idle", "00.png")), sp)


def write(sp, name, order, parts, layers):
    d = os.path.join(HERE, name, "parts")
    os.makedirs(d, exist_ok=True)
    fk.outline_parts(sp, base_body(sp), [layers[n] for n in order if n != "BODY"])
    for n in order:
        if n != "BODY":
            fk.save(sp, layers[n], os.path.join(d, n + ".png"))
    with open(os.path.join(d, "parts.json"), "w", encoding="utf-8") as f:
        json.dump({"order": order, "parts": parts}, f, ensure_ascii=False, indent=1)
    print("파츠 —", name, order)


def deer(sp):
    HAIR, CLOTH, WOOD, ACC = "HAIR", "CLOTH_B", "LEATHER", "ACCENT"
    L = {n: fk.layer(sp, n) for n in ("hair_back", "outfit", "hair_front", "antlers", "staff")}
    # 뒷머리: 머리보다 크게, 어깨 아래까지 — 실루엣의 대부분
    fk.paint(sp, L["hair_back"], lambda t: t.ellipse(31, 36, 13.5, 12, 1), HAIR, "sphere", 3)
    fk.paint(sp, L["hair_back"], lambda t: t.poly([(17, 36), (23, 36), (24, 54), (18, 54), (16, 46)], 1), HAIR, "cyl", 3)
    fk.paint(sp, L["hair_back"], lambda t: t.poly([(40, 36), (45, 36), (46, 48), (44, 53), (40, 53)], 1), HAIR, "cyl", 3)
    # 앞머리: 눈(y 39) 바로 위에서 끝나는 큰 앞머리, 가르마 뾰족 4개
    fk.paint(sp, L["hair_front"], lambda t: t.poly([(19, 40), (19, 32), (23, 27), (31, 25), (39, 27), (43, 32), (43, 40),
                                                  (41, 38), (40, 34), (36, 38), (34, 33), (30, 38), (27, 33), (24, 38), (22, 35)], 1), HAIR, "sphere", 2)
    L["hair_front"].pixels([(26, 28), (27, 28), (28, 28), (29, 28), (25, 29)], sp.c(HAIR, 0))
    # 뿔: 머리 위 10도트까지, 가지 셋
    a = L["antlers"]
    for m in (1, -1):
        x0 = 31 + m * 6
        a.line(x0, 29, x0 + m, 22, sp.c(WOOD, 1)); a.line(x0 + m, 22, x0 + m, 18, sp.c(WOOD, 1))
        a.line(x0 + m, 23, x0 + m * 5, 20, sp.c(WOOD, 1)); a.line(x0, 26, x0 - m * 3, 23, sp.c(WOOD, 1))
        a.line(x0 + m * 4, 20, x0 + m * 5, 17, sp.c(WOOD, 1))
        a.pixels([(x0 + m, 18), (x0 + m * 5, 17), (x0 - m * 3, 23)], sp.c(WOOD, 0))
    # 원피스: 몸통 46~53 위에 치마 53~57, 허리끈
    fk.paint(sp, L["outfit"], lambda t: t.poly([(26, 46), (38, 46), (39, 53), (41, 57), (23, 57), (25, 53)], 1), CLOTH, "cyl", 2)
    L["outfit"].pixels([(x, 51) for x in range(26, 39)], sp.c(ACC, 1))
    L["outfit"].pixels([(31, 47), (32, 47), (33, 47), (32, 48)], sp.c("SKIN", 1))   # V넥
    L["outfit"].pixels([(29, 49), (35, 49), (32, 50)], sp.c(ACC, 0))                # 구슬
    # 지팡이: 가까운 손(39.5, 53.5)을 지나 머리 위까지 — 몸보다 길게(y 8~58)
    s = L["staff"]
    s.line(43, 12, 43, 58, sp.c(WOOD, 1)); s.line(44, 12, 44, 58, sp.c(WOOD, 2))
    for p in [(43, 12), (44, 10), (46, 8), (49, 8), (51, 10), (52, 13), (51, 15)]:
        s.set(*p, sp.c(WOOD, 1))
    s.pixels([(45, 9), (46, 9), (47, 9), (48, 9)], sp.c(WOOD, 0))
    s.pixels([(45, 20), (42, 27), (45, 34), (42, 44)], sp.c("CLOTH_A", 1))          # 감은 파란 리본
    order = ["hair_back", "BODY", "outfit", "staff", "hair_front", "antlers"]
    parts = {"hair_back": {"anchor": "head"}, "outfit": {"anchor": "body"}, "staff": {"anchor": "hand_R"},
             "hair_front": {"anchor": "head"}, "antlers": {"anchor": "head"}}
    write(sp, "deer_girl", order, parts, L)


def goat(sp):
    WOOL, HORN, CLOTH, METAL, LEATHER = "CLOTH_B", "LEATHER", "CLOTH_A", "METAL", "LEATHER"
    L = {n: fk.layer(sp, n) for n in ("hair_back", "outfit", "hair_front", "horns", "hammer")}
    fk.paint(sp, L["hair_back"], lambda t: t.ellipse(30.5, 36, 12, 11, 1), WOOL, "sphere", 2)
    # 앞머리: 곱슬 뭉치 한 덩어리 — 눈 위에서 끝나고 머리 위로 5도트
    def wool(t):
        t.ellipse(31, 32, 12, 7, 1)
        for cx, cy, r in ((21, 35, 3.2), (24, 27, 3.4), (31, 24.5, 3.6), (38, 27, 3.4), (40.5, 34, 3)):
            t.ellipse(cx, cy, r, r, 1)
    fk.paint(sp, L["hair_front"], wool, WOOL, "sphere", 2)
    L["hair_front"].pixels([(25, 30), (24, 31), (32, 28), (33, 29), (38, 31), (39, 32)], sp.c(WOOL, 2))
    # 말린 뿔: 머리 양옆 위, 지름 9
    for cx in (20.5, 42.5):
        fk.paint(sp, L["horns"], lambda t, cx=cx: t.ellipse(cx, 30, 4.4, 4.4, 1), HORN, "sphere", 3)
        c = int(cx)
        L["horns"].pixels([(c - 2, 28), (c - 1, 27), (c, 27), (c + 1, 28), (c + 2, 29), (c + 2, 30), (c + 1, 31), (c, 32)], sp.c(HORN, 3))
    # 갑옷: 파란 튜닉 + 가슴 금속판 + 벨트 + 가까운 어깨 갑옷
    fk.paint(sp, L["outfit"], lambda t: t.poly([(26, 46), (38, 46), (39, 53), (39, 55), (25, 55), (25, 53)], 1), CLOTH, "cyl", 2)
    fk.paint(sp, L["outfit"], lambda t: fk.rect(t, 29, 47, 36, 51, 1), METAL, "sphere", 2)
    L["outfit"].pixels([(x, 52) for x in range(26, 39)], sp.c(LEATHER, 1))
    L["outfit"].pixels([(31, 52), (32, 52)], sp.c("ACCENT", 1))
    fk.paint(sp, L["outfit"], lambda t: t.ellipse(39.5, 47.5, 3.5, 2.5, 1), METAL, "sphere", 2)
    # 망치: 가까운 손에서 땅으로, 머리는 몸통만 하게(15×8) 발 오른쪽 땅에
    h = L["hammer"]
    h.line(41, 40, 41, 52, sp.c(LEATHER, 1)); h.line(42, 40, 42, 52, sp.c(LEATHER, 2))
    fk.paint(sp, h, lambda t: fk.rect(t, 38, 52, 52, 59, 1), METAL, "sphere", 2)
    h.pixels([(x, 55) for x in range(39, 52)], sp.c(METAL, 2))
    h.pixels([(40, 53), (41, 53), (50, 58), (51, 58)], sp.c(METAL, 3))
    order = ["hair_back", "BODY", "outfit", "hair_front", "horns", "hammer"]
    parts = {"hair_back": {"anchor": "head"}, "outfit": {"anchor": "body"}, "hair_front": {"anchor": "head"},
             "horns": {"anchor": "head"}, "hammer": {"anchor": "hand_R"}}
    write(sp, "goat_warrior", order, parts, L)


if __name__ == "__main__":
    sp = fk.load_spec()
    deer(sp)
    goat(sp)
