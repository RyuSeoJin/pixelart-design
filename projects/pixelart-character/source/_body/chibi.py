# -*- coding: utf-8 -*-
"""공통 몸체 「chibi」 — CQ-Ref 기준(짜리몽땅 약 1.7등신 · 몸 키 32도트)의 idle · walk 프레임을 그립니다

모든 캐릭터가 함께 쓰는 민무늬 몸(피부 + 흰 속옷)입니다. 기준 방향은 왼쪽 3/4 — 먼 쪽(화면 왼쪽 _L)
팔 · 다리는 몸 뒤, 가까운 쪽(화면 오른쪽 _R)은 몸 앞입니다. 프레임마다 머리 · 몸 · 손이 기본 자세에서
얼마나 움직였는지는 사양 파일 animations.{태그}.offsets와 같아야 합니다 — 이 파일이 그 값을 읽어 씁니다.

기준선(사양): 머리 28~46 · 눈 40 · 어깨 47 · 허리 51 · 가랑이 53 · 무릎 55 · 발목 57 · 발바닥 59.

    python chibi.py   →  ./{태그}/{00..}.png · ./preview.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import fieldkit as fk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SKIN, CLOTH = "SKIN", "CLOTH_B"
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

# 기본 자세 — 목 없이 머리가 몸통 위에 바로 얹힙니다. 3/4라 머리 중심이 살짝 왼쪽.
HEAD = (31.5, 37.0, 11.0, 9.5)                 # 중심 x, y · 반지름 x, y → x 20~42 · y 28~46
TORSO = [(26, 46), (38, 46), (39, 53), (25, 53)]
ARM_L = [(23, 47), (26, 47), (26, 52), (23, 52)]      # 먼 쪽(뒤)
ARM_R = [(38, 47), (41, 47), (41, 52), (38, 52)]      # 가까운 쪽(앞)
HAND_L, HAND_R = (24.5, 53.5), (39.5, 53.5)
LEG_L = [(27, 53), (31, 53), (31, 57), (27, 57)]
LEG_R = [(33, 53), (37, 53), (37, 57), (33, 57)]
FOOT_L, FOOT_R = (26, 57, 31, 59), (32, 57, 38, 59)   # 발: 앞(오른쪽)이 살짝 김


def body(sp, dh=(0, 0), db=(0, 0), hr=(0, 0), hl=(0, 0), legs=None, feet=None):
    L = fk.layer(sp, "body")
    legs = legs or (LEG_L, LEG_R)
    feet = feet or (FOOT_L, FOOT_R)
    sh = lambda pts, d: [(x + d[0], y + d[1]) for x, y in pts]
    # 뒤 → 앞: 먼 팔 · 손, 먼 다리, 몸통, 가까운 다리, 발, 머리, 가까운 팔 · 손
    fk.paint(sp, L, lambda t: t.poly(sh(ARM_L, hl), 1), SKIN, "cyl", 3)
    fk.paint(sp, L, lambda t: t.ellipse(HAND_L[0] + hl[0], HAND_L[1] + hl[1], 2.0, 1.8, 1), SKIN, "sphere", 2)
    fk.paint(sp, L, lambda t: t.poly(legs[0], 1), SKIN, "cyl", 3)
    fk.paint(sp, L, lambda t: t.poly(sh(TORSO, db), 1), CLOTH, "cyl", 2)
    fk.paint(sp, L, lambda t: t.poly(legs[1], 1), SKIN, "cyl", 2)
    for f in feet:
        fk.paint(sp, L, lambda t, f=f: fk.rect(t, *f, 1), CLOTH, "sphere", 2)
    fk.paint(sp, L, lambda t: t.ellipse(HEAD[0] + dh[0], HEAD[1] + dh[1], HEAD[2], HEAD[3], 1), SKIN, "sphere", 2)
    fk.paint(sp, L, lambda t: t.poly(sh(ARM_R, hr), 1), SKIN, "cyl", 2)
    fk.paint(sp, L, lambda t: t.ellipse(HAND_R[0] + hr[0], HAND_R[1] + hr[1], 2.2, 2.0, 1), SKIN, "sphere", 2)
    # 얼굴 기호 — CQ-Ref: 눈은 머리 아래쪽(y 40), 세로 4 · 가로 2, 하이라이트 1. 3/4라 두 눈이 왼쪽으로 몰림
    ex, ey = 25 + dh[0], 39 + dh[1]
    for x in (ex, ex + 8):
        L.pixels([(x, ey), (x, ey + 1), (x, ey + 2), (x, ey + 3), (x + 1, ey), (x + 1, ey + 1), (x + 1, ey + 2), (x + 1, ey + 3)], 1)
        L.pixels([(x, ey + 1), (x, ey + 2), (x + 1, ey + 1), (x + 1, ey + 2)], sp.c("EYE", 2))
        L.set(x, ey + 1, sp.c("EYE", 0))
    L.pixels([(ex - 1, ey + 4), (ex + 10, ey + 4)], sp.c("ACCENT", 0))          # 볼
    L.pixels([(ex + 4, ey + 5), (ex + 5, ey + 5)], sp.c(SKIN, 3))                # 입
    L.add_outline()
    for y in range(sp.height):
        for x in range(sp.width):
            if L.outline[y][x] and all(L.inside(x + dx, y + dy) and L.px[y + dy][x + dx] for dx, dy in N4):
                L.px[y][x] = sp.c(SKIN, 3)
    return L


def walk_legs(f):
    """8프레임 걷기 — 짧은 다리라 앞뒤 1~2도트, 뒤로 간 발은 1도트 들림."""
    phase = [0, 1, 2, 1, 0, -1, -2, -1][f]
    lift = [0, 1, 0, 0, 0, 1, 0, 0][f]
    def leg(base, d):
        return [(x + (d if y >= 55 else d // 2), y) for x, y in base]
    lr, ll = leg(LEG_R, phase), leg(LEG_L, -phase)
    up_r, up_l = (lift if phase < 0 else 0), (lift if phase > 0 else 0)
    fr = (FOOT_R[0] + phase, FOOT_R[1] - up_r, FOOT_R[2] + phase, FOOT_R[3] - up_r)
    fl = (FOOT_L[0] - phase, FOOT_L[1] - up_l, FOOT_L[2] - phase, FOOT_L[3] - up_l)
    return (ll, lr), (fl, fr)


def main():
    sp = fk.load_spec()
    frames = []
    for tag, a in sp.animations.items():
        for f in range(a["frames"]):
            dh, db, hr = sp.offset(tag, "head", f), sp.offset(tag, "body", f), sp.offset(tag, "hand_R", f)
            hl = (-hr[0], hr[1]) if tag == "walk" else hr
            legs = feet = None
            if tag == "walk":
                legs, feet = walk_legs(f)
            L = body(sp, dh, db, hr, hl, legs, feet)
            fk.save(sp, L, os.path.join(HERE, tag, "%02d.png" % f))
            frames.append(L)
    from PIL import Image
    K = 4
    sheet = Image.new("RGBA", (sp.width * K * len(frames), sp.height * K), (120, 120, 130, 255))
    for i, L in enumerate(frames):
        tmp = os.path.join(HERE, "_tmp.png")
        fk.save(sp, L, tmp)
        sheet.alpha_composite(Image.open(tmp).convert("RGBA").resize((sp.width * K, sp.height * K), Image.NEAREST), (i * sp.width * K, 0))
        os.remove(tmp)
    sheet.save(os.path.join(HERE, "preview.png"))
    print("공통 몸체 chibi (CQ-Ref) — %d프레임" % len(frames))


if __name__ == "__main__":
    main()
