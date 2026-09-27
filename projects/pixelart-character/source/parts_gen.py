# -*- coding: utf-8 -*-
"""사슴 소녀 · 양 전사의 필드 파츠(기본 자세 한 장)를 그립니다

파츠는 공통 몸체 chibi의 기본 자세(idle 00) 위에 얹힌다고 보고 그립니다. 동작 중 위치는 사양 파일의
앵커 이동량이 옮기므로 여기서는 기본 자세만 그립니다.

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
    body = base_body(sp)
    fk.outline_parts(sp, body, [layers[n] for n in order if n != "BODY"])
    for n in order:
        if n != "BODY":
            fk.save(sp, layers[n], os.path.join(d, n + ".png"))
    with open(os.path.join(d, "parts.json"), "w", encoding="utf-8") as f:
        json.dump({"order": order, "parts": parts}, f, ensure_ascii=False, indent=1)
    print("파츠 —", name, order)


def deer(sp):
    HAIR, CLOTH, WOOD, ACC, LEAF = "HAIR", "CLOTH_B", "LEATHER", "ACCENT", "SKIN"
    L = {n: fk.layer(sp, n) for n in ("hair_back", "outfit", "hair_front", "antlers", "staff")}
    # 뒷머리: 어깨까지 오는 단발 + 3/4라 왼쪽 볼륨
    fk.paint(sp, L["hair_back"], lambda t: t.ellipse(32, 22, 12, 11, 1), HAIR, "sphere", 3)
    fk.paint(sp, L["hair_back"], lambda t: t.poly([(20, 22), (25, 22), (26, 38), (21, 38), (19, 30)], 1), HAIR, "cyl", 3)
    fk.paint(sp, L["hair_back"], lambda t: t.poly([(40, 22), (44, 22), (45, 32), (44, 37), (40, 37)], 1), HAIR, "cyl", 3)
    # 앞머리: 눈(y 24) 바로 위에서 끝나는 가르마 앞머리
    fk.paint(sp, L["hair_front"], lambda t: t.poly([(22, 23), (22, 17), (26, 13), (33, 12), (40, 14), (43, 19), (43, 23),
                                                  (41, 22), (40, 19), (37, 22), (35, 18), (32, 22), (29, 18), (26, 22), (24, 20)], 1), HAIR, "sphere", 2)
    L["hair_front"].pixels([(27, 14), (28, 14), (29, 14), (26, 15)], sp.c(HAIR, 0))
    # 뿔: 1px 가지
    a = L["antlers"]
    for m in (1, -1):
        x0 = 32 + m * 6
        a.line(x0, 14, x0 + m * 1, 8, sp.c(WOOD, 1)); a.line(x0 + m, 8, x0 + m, 5, sp.c(WOOD, 1))
        a.line(x0 + m, 9, x0 + m * 4, 7, sp.c(WOOD, 1)); a.line(x0, 11, x0 - m * 2, 9, sp.c(WOOD, 1))
        a.pixels([(x0 + m, 5), (x0 + m * 4, 7), (x0 - m * 2, 9)], sp.c(WOOD, 0))
    # 옷: 흰 원피스 + 초록 허리끈 (몸통 35~47 위에 47~52까지 치마)
    fk.paint(sp, L["outfit"], lambda t: t.poly([(27, 35), (37, 35), (38, 43), (39, 52), (26, 52), (26, 43)], 1), CLOTH, "cyl", 2)
    L["outfit"].pixels([(x, 43) for x in range(27, 38)], sp.c("ACCENT", 1))
    L["outfit"].pixels([(x, 44) for x in range(27, 38)], sp.c("ACCENT", 2))
    L["outfit"].pixels([(31, 36), (32, 36), (33, 36), (32, 37)], sp.c("SKIN", 1))          # V넥
    L["outfit"].pixels([(30, 38), (34, 38), (32, 39)], sp.c(ACC, 1))                       # 목걸이 구슬
    # 지팡이: 가까운 팔 바깥쪽(x 42~43)을 따라 위로, 손 높이에서 쥔 것처럼 보이게 몸 앞에 둡니다
    s = L["staff"]
    s.line(42, 22, 42, 58, sp.c(WOOD, 1)); s.line(43, 22, 43, 58, sp.c(WOOD, 2))
    for p in [(42, 22), (43, 20), (45, 19), (47, 20), (48, 22)]:
        s.set(*p, sp.c(WOOD, 1))
    s.pixels([(44, 28), (41, 35), (44, 41), (41, 52)], sp.c("ACCENT", 1))
    order = ["hair_back", "BODY", "outfit", "staff", "hair_front", "antlers"]
    parts = {"staff": {"anchor": "hand_R"}, "hair_back": {"anchor": "head"}, "outfit": {"anchor": "body"},
             "hair_front": {"anchor": "head"}, "antlers": {"anchor": "head"}}
    write(sp, "deer_girl", order, parts, L)


def goat(sp):
    WOOL, HORN, CLOTH, METAL, LEATHER = "CLOTH_B", "LEATHER", "CLOTH_A", "METAL", "LEATHER"
    L = {n: fk.layer(sp, n) for n in ("hair_back", "outfit", "hair_front", "horns", "hammer")}
    fk.paint(sp, L["hair_back"], lambda t: t.ellipse(31, 21, 11.5, 11, 1), WOOL, "sphere", 2)
    # 앞머리: 곱슬 뭉치를 한 덩어리로, 눈 위에서 끝남
    def wool(t):
        t.ellipse(32, 17, 11, 6, 1)
        for cx, cy, r in ((23, 20, 3), (26, 14, 3), (32, 12.5, 3.2), (38, 14, 3), (39, 19, 2.2)):
            t.ellipse(cx, cy, r, r, 1)
    fk.paint(sp, L["hair_front"], wool, WOOL, "sphere", 2)
    L["hair_front"].pixels([(27, 15), (26, 16), (33, 14), (34, 15), (38, 17), (39, 18)], sp.c(WOOL, 2))
    # 말린 뿔
    for cx in (21.5, 42.5):
        fk.paint(sp, L["horns"], lambda t, cx=cx: t.ellipse(cx, 15.5, 3.6, 3.6, 1), HORN, "sphere", 3)
        L["horns"].pixels([(int(cx) - 1, 14), (int(cx), 14), (int(cx) + 1, 15), (int(cx) + 1, 16), (int(cx), 17)], sp.c(HORN, 3))
    # 갑옷: 파란 튜닉 + 가슴 금속판 + 벨트
    fk.paint(sp, L["outfit"], lambda t: t.poly([(27, 35), (37, 35), (38, 43), (38, 49), (26, 49), (26, 43)], 1), CLOTH, "cyl", 2)
    fk.paint(sp, L["outfit"], lambda t: fk.rect(t, 29, 36, 35, 41, 1), METAL, "sphere", 2)
    L["outfit"].pixels([(x, 44) for x in range(27, 38)], sp.c(LEATHER, 1))
    L["outfit"].pixels([(31, 44), (32, 44)], sp.c("ACCENT", 1))
    fk.paint(sp, L["outfit"], lambda t: t.ellipse(38.5, 36.5, 3, 2.2, 1), METAL, "sphere", 2)  # 가까운 어깨 갑옷
    # 망치: 가까운 손(38.5, 46.5)에서 땅으로 — 머리가 발 오른쪽 땅에 놓여 얼굴 · 몸을 가리지 않습니다
    h = L["hammer"]
    h.line(40, 34, 40, 53, sp.c(LEATHER, 1)); h.line(41, 34, 41, 53, sp.c(LEATHER, 2))
    fk.paint(sp, h, lambda t: fk.rect(t, 38, 53, 48, 59, 1), METAL, "sphere", 2)
    h.pixels([(x, 56) for x in range(39, 48)], sp.c(METAL, 2))
    order = ["hair_back", "BODY", "outfit", "hair_front", "horns", "hammer"]
    parts = {"hair_back": {"anchor": "head"}, "outfit": {"anchor": "body"}, "hair_front": {"anchor": "head"},
             "horns": {"anchor": "head"}, "hammer": {"anchor": "hand_R"}}
    write(sp, "goat_warrior", order, parts, L)


if __name__ == "__main__":
    sp = fk.load_spec()
    deer(sp)
    goat(sp)
