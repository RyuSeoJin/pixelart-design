# -*- coding: utf-8 -*-
"""공통 몸체 「six」 — 6등신 · 키 252px · 320 캔버스(결정 A) 필드 사양의 idle · walk 프레임 초안

코드로 그린 초안입니다. 등신대는 채색 그림을 변환하는 절차가 정석이라, 입력 그림이 오면 이 몸체를 대체합니다.
기준 방향 왼쪽 3/4 — 먼 쪽(화면 왼쪽 _L) 팔 · 다리는 몸 뒤, 가까운 쪽(_R)은 앞. 앵커 이동량은 사양 파일을 읽습니다.
기준선: 머리 52~94 · 눈 76 · 턱 94 · 어깨 106 · 허리 148 · 가랑이 178 · 무릎 236 · 발목 292 · 발바닥 303.

    python body6.py   →  ./{태그}/{00..}.png · ./preview.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import fieldkit as fk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SKIN, CLOTH = "SKIN", "CLOTH_B"
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

HEAD = (158, 73, 22, 22)                                   # 얼굴 x 136~180 · y 51~95
JAW = [(140, 82), (176, 82), (170, 93), (162, 96), (152, 96), (144, 93)]
NECK = [(152, 93), (165, 93), (165, 108), (152, 108)]
TORSO = [(134, 106), (184, 106), (181, 130), (176, 150), (180, 178), (138, 178), (142, 150), (137, 130)]
UPPER_L, FORE_L = [(122, 108), (136, 110), (131, 142), (118, 140)], [(118, 140), (131, 142), (128, 170), (117, 169)]   # 먼 팔(뒤)
UPPER_R, FORE_R = [(181, 108), (195, 110), (198, 142), (185, 140)], [(185, 140), (198, 142), (200, 170), (188, 169)]   # 가까운 팔(앞)
HAND_L, HAND_R = (122.5, 178), (194, 178)
THIGH_L, SHIN_L = [(139, 176), (158, 176), (156, 236), (143, 236)], [(143, 236), (156, 236), (155, 292), (145, 292)]
THIGH_R, SHIN_R = [(160, 176), (180, 176), (177, 236), (164, 236)], [(164, 236), (177, 236), (176, 292), (166, 292)]
FOOT_L, FOOT_R = [(134, 292), (155, 292), (156, 303), (132, 303)], [(156, 292), (177, 292), (179, 303), (154, 303)]


def sh(pts, d):
    return [(x + d[0], y + d[1]) for x, y in pts]


def eye(sp, L, x, y, far):
    """눈 폭 8 · 높이 12 — 속눈썹 2줄 · 흰자 · 홍채 3단계 · 동공 · 하이라이트 2×2. (x, y)는 왼쪽 위."""
    OUT = 1
    for yy in range(y + 2, y + 12):
        for xx in range(x, x + 8):
            L.set(xx, yy, sp.c("EYE", 0))                                       # 흰자
    for yy in range(y + 3, y + 12):                                             # 홍채 폭 6
        for xx in range(x + 1, x + 7):
            L.set(xx, yy, sp.c("EYE", 2 if yy >= y + 7 else 1))
    for yy in range(y + 5, y + 11):                                             # 동공
        for xx in range(x + 3, x + 6):
            L.set(xx, yy, sp.c("EYE", 3))
    L.pixels([(x + 1, y + 4), (x + 2, y + 4), (x + 1, y + 5), (x + 2, y + 5)], sp.c("EYE", 0))   # 하이라이트
    L.pixels([(xx, y) for xx in range(x - 1, x + 9)], OUT)                     # 속눈썹 윗줄
    L.pixels([(xx, y + 1) for xx in range(x, x + 9)], sp.c("EYE", 3))           # 둘째 줄은 홍채 어두운 색 (외곽선 2줄이면 뭉침)
    L.pixels([(x + 9 if not far else x - 2, y + 1), (x + 9 if not far else x - 2, y + 2)], OUT)      # 바깥 끝
    L.pixels([(xx, y + 12) for xx in range(x + 1, x + 8)], sp.c(SKIN, 3))       # 아래 선


def body(sp, dh=(0, 0), db=(0, 0), hr=(0, 0), hl=(0, 0), legs=None, feet=None):
    L = fk.layer(sp, "body")
    legs = legs or ((THIGH_L, SHIN_L), (THIGH_R, SHIN_R))
    feet = feet or (FOOT_L, FOOT_R)
    P = lambda pts, ramp, kind, ms=3: fk.paint(sp, L, lambda t: t.poly(pts, 1), ramp, kind, ms)
    # 뒤 → 앞
    P(sh(UPPER_L, hl), SKIN, "cyl"); P(sh(FORE_L, hl), SKIN, "cyl")
    fk.paint(sp, L, lambda t: t.ellipse(HAND_L[0] + hl[0], HAND_L[1] + hl[1], 8, 9, 1), SKIN, "sphere", 2)
    P(legs[0][0], SKIN, "cyl"); P(legs[0][1], SKIN, "cyl")
    P(sh(NECK, db), SKIN, "flat"); L.pixels([(x, 94 + db[1]) for x in range(152, 166)] + [(x, 95 + db[1]) for x in range(153, 165)], sp.c(SKIN, 2))
    P(sh(TORSO, db), CLOTH, "cyl", 2)
    P(legs[1][0], SKIN, "cyl", 2); P(legs[1][1], SKIN, "cyl", 2)
    for f in feet:
        P(f, CLOTH, "sphere", 2)
    fk.paint(sp, L, lambda t: t.ellipse(HEAD[0] + dh[0], HEAD[1] + dh[1], HEAD[2], HEAD[3], 1), SKIN, "sphere", 2)
    P(sh(JAW, dh), SKIN, "sphere", 2)
    P(sh(UPPER_R, hr), SKIN, "cyl", 2); P(sh(FORE_R, hr), SKIN, "cyl", 2)
    fk.paint(sp, L, lambda t: t.ellipse(HAND_R[0] + hr[0], HAND_R[1] + hr[1], 8.5, 9.5, 1), SKIN, "sphere", 2)
    # 얼굴: 눈 중심 y=76 → 눈 상자 70~82. 3/4라 두 눈이 왼쪽으로 몰림, 사이 9
    eye(sp, L, 141 + dh[0], 70 + dh[1], far=True)
    eye(sp, L, 158 + dh[0], 70 + dh[1], far=False)
    L.pixels([(139 + dh[0] + i, 85 + dh[1]) for i in range(4)] + [(166 + dh[0] + i, 85 + dh[1]) for i in range(4)], sp.c("ACCENT", 0))   # 볼
    L.pixels([(152 + dh[0], 84 + dh[1]), (152 + dh[0], 85 + dh[1])], sp.c(SKIN, 2))          # 코 그림자
    L.pixels([(153 + dh[0] + i, 89 + dh[1]) for i in range(5)], sp.c("ACCENT", 2))            # 입
    L.pixels([(154 + dh[0] + i, 90 + dh[1]) for i in range(3)], sp.c("ACCENT", 1))
    L.add_outline()
    for y in range(sp.height):
        for x in range(sp.width):
            if L.outline[y][x] and all(L.inside(x + dx, y + dy) and L.px[y + dy][x + dx] for dx, dy in N4):
                L.px[y][x] = sp.c(SKIN, 3)
    return L


def walk_legs(f):
    phase = [0, 1, 2, 1, 0, -1, -2, -1][f] * 5
    lift = [0, 3, 0, 0, 0, 3, 0, 0][f]
    def leg(th, sh_, d, up):
        return ([(x + d // 2, y) for x, y in th], [(x + d, y - (up if y >= 280 else 0)) for x, y in sh_])
    lr = leg(THIGH_R, SHIN_R, phase, lift if phase < 0 else 0)
    ll = leg(THIGH_L, SHIN_L, -phase, lift if phase > 0 else 0)
    fr = [(x + phase, y - (lift if phase < 0 else 0)) for x, y in FOOT_R]
    fl = [(x - phase, y - (lift if phase > 0 else 0)) for x, y in FOOT_L]
    return (ll, lr), (fl, fr)


def main():
    sp = fk.load_spec()
    frames = []
    for tag, a in sp.animations.items():
        for f in range(a["frames"]):
            dh, db, hr, hl = (sp.offset(tag, k, f) for k in ("head", "body", "hand_R", "hand_L"))
            legs = feet = None
            if tag == "walk":
                legs, feet = walk_legs(f)
            L = body(sp, dh, db, hr, hl, legs, feet)
            fk.save(sp, L, os.path.join(HERE, tag, "%02d.png" % f))
            frames.append(L)
    from PIL import Image
    sheet = Image.new("RGBA", (sp.width * len(frames), sp.height), (120, 120, 130, 255))
    for i, L in enumerate(frames):
        tmp = os.path.join(HERE, "_tmp.png"); fk.save(sp, L, tmp)
        sheet.alpha_composite(Image.open(tmp).convert("RGBA"), (i * sp.width, 0)); os.remove(tmp)
    sheet.save(os.path.join(HERE, "preview.png"))
    print("공통 몸체 six — %d프레임" % len(frames))


if __name__ == "__main__":
    main()
