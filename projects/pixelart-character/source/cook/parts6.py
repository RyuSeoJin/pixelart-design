# -*- coding: utf-8 -*-
"""요리사 「모리」 6등신 파츠 초안 — spec/design/characters/cook.md의 「6등신 사양 적용 메모」대로

공통 몸체 six(source/_body6)의 기본 자세 위에 얹힙니다. 코드로 그린 초안이라 입력 그림이 오면 대체합니다.

    python parts6.py   →  ./parts6/{파츠}.png + parts.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import fieldkit as fk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
HAIR, WHITE, RED, PANTS, BTN, SKIN, SHOE = "HAIR", "CLOTH_B", "ACCENT", "CLOTH_A", "LEATHER", "SKIN", "LEATHER"


def main():
    sp = fk.load_spec()
    from PIL import Image
    import pixkit
    body = pixkit.from_image("body", Image.open(os.path.join(HERE, "..", "_body6", "idle", "00.png")), sp)
    L = {n: fk.layer(sp, n) for n in ("hair_back", "outfit", "hair_front", "hat")}

    # 뒷머리: 단발 폭 60(128~188), 턱 아래 y 130까지. 3/4라 왼쪽이 넓음
    def back(t):
        t.ellipse(157, 76, 31, 31, 1)
        t.poly([(126, 76), (140, 76), (142, 130), (130, 132), (124, 110)], 1)
        t.poly([(176, 76), (188, 76), (190, 108), (186, 128), (176, 128)], 1)
    fk.hair_render(sp, L["hair_back"], back, HAIR, (0, 0), back=True,
                   strands=[(132, 90, 134, 126), (138, 84, 139, 126), (181, 84, 182, 124)])
    # 앞머리: 눈(70) 위 y 68에서 끝, 뾰족 5개, 밝은 뭉치 22×10, 가닥선 8줄
    def front(t):
        t.poly([(128, 68), (128, 58), (136, 48), (150, 44), (166, 44), (180, 48), (188, 58), (188, 68),
                (184, 62), (178, 68), (172, 60), (164, 67), (156, 58), (148, 67), (141, 60), (134, 68)], 1)
    fk.hair_render(sp, L["hair_front"], front, HAIR, (146, 54), hi_size=(22, 10),
                   strands=[(157, 46, 141, 66), (157, 46, 148, 68), (157, 46, 156, 60), (157, 46, 164, 68),
                            (157, 46, 172, 64), (157, 46, 178, 68), (157, 46, 134, 66), (157, 46, 184, 62)],
                   tips=[(133, 69), (147, 68), (163, 68), (177, 69), (185, 63)])
    # 이마 그림자 2줄 (앞머리 파츠에)
    for y in range(1, sp.height):
        for x in range(sp.width):
            if L["hair_front"].px[y - 1][x] and not L["hair_front"].px[y][x] and body.px[y][x] == sp.c(SKIN, 1):
                L["hair_front"].px[y][x] = sp.c(SKIN, 2)
                if body.px[y + 1][x] == sp.c(SKIN, 1):
                    L["hair_front"].px[y + 1][x] = sp.c(SKIN, 2)
    # 바지 178~292 · 신발 292~303
    o = L["outfit"]
    for leg in ([(139, 178), (158, 178), (155, 292), (145, 292)], [(160, 178), (180, 178), (176, 292), (166, 292)]):
        fk.paint(sp, o, lambda t, p=leg: t.poly(p, 1), PANTS, "cyl", 3)
    for y in range(sp.height):
        for x in range(sp.width):
            if o.px[y][x] == sp.c(PANTS, 1):
                o.px[y][x] = sp.c(PANTS, 2)
    for foot in ([(134, 292), (155, 292), (156, 303), (132, 303)], [(156, 292), (177, 292), (179, 303), (154, 303)]):
        fk.paint(sp, o, lambda t, p=foot: t.poly(p, 1), SHOE, "sphere", 3)
    # 재킷 106~156 + 앞치마 156~210
    fk.paint(sp, o, lambda t: t.poly([(133, 106), (185, 106), (182, 130), (178, 156), (142, 156), (136, 130)], 1), WHITE, "cyl", 2)
    fk.paint(sp, o, lambda t: t.poly([(142, 156), (178, 156), (181, 212), (139, 212)], 1), WHITE, "cyl", 2)
    o.pixels([(141, y) for y in range(160, 210)] + [(179, y) for y in range(160, 210)], sp.c(WHITE, 2))   # 앞치마 옆선
    o.pixels([(x, 156) for x in range(143, 178)], sp.c(WHITE, 2))                                    # 앞치마 허리선
    for yy in (118, 130, 142):                                                                        # 단추 2열 × 3
        for xx in (152, 164):
            o.pixels([(xx, yy), (xx + 1, yy), (xx + 2, yy), (xx, yy + 1), (xx + 1, yy + 1), (xx + 2, yy + 1)], sp.c(BTN, 1))
    o.pixels([(158, y) for y in range(110, 156)], sp.c(WHITE, 2))                                    # 여밈 선
    # 목수건 폭 20 · 높이 6 + 매듭 8
    fk.paint(sp, o, lambda t: t.poly([(148, 104), (170, 104), (168, 110), (150, 110)], 1), RED, "cyl", 2)
    fk.paint(sp, o, lambda t: t.poly([(156, 110), (162, 110), (161, 118), (157, 118)], 1), RED, "cyl", 2)
    # 소매: 팔 위 흰 소매 106~150 (가까운 팔 · 먼 팔)
    fk.paint(sp, o, lambda t: t.poly([(181, 108), (195, 110), (198, 148), (185, 146)], 1), WHITE, "cyl", 2)
    fk.paint(sp, o, lambda t: t.poly([(122, 108), (136, 110), (131, 146), (118, 144)], 1), WHITE, "cyl", 3)
    o.pixels([(x, 146) for x in range(185, 199)] + [(x, 144) for x in range(118, 132)], sp.c(WHITE, 2))
    # 모자: 상자 위 32도트(20~56), 폭 48, 위가 부푼 원통
    fk.paint(sp, L["hat"], lambda t: t.poly([(134, 56), (182, 56), (186, 40), (182, 24), (170, 18), (146, 18), (134, 24), (130, 40)], 1), WHITE, "cyl", 2)
    L["hat"].pixels([(x, 54) for x in range(135, 182)] + [(x, 55) for x in range(135, 182)], sp.c(WHITE, 2))   # 띠
    for x0 in (142, 156, 170):
        L["hat"].pixels([(x0, 22), (x0 + 1, 22), (x0, 23), (x0 + 1, 23)], sp.c(WHITE, 0))
        L["hat"].pixels([(x0 + 6, y) for y in range(26, 50)], sp.c(WHITE, 2))                            # 주름
    order = ["hair_back", "BODY", "outfit", "hair_front", "hat"]
    parts = {"hair_back": {"anchor": "head"}, "outfit": {"anchor": "body"}, "hair_front": {"anchor": "head"}, "hat": {"anchor": "head"}}
    fk.outline_parts(sp, body, [L[n] for n in order if n != "BODY"])
    d = os.path.join(HERE, "parts6")
    os.makedirs(d, exist_ok=True)
    for n in order:
        if n != "BODY":
            fk.save(sp, L[n], os.path.join(d, n + ".png"))
    with open(os.path.join(d, "parts.json"), "w", encoding="utf-8") as f:
        json.dump({"order": order, "parts": parts}, f, ensure_ascii=False, indent=1)
    print("파츠6 — cook", order)


if __name__ == "__main__":
    main()
