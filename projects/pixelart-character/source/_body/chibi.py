# -*- coding: utf-8 -*-
"""공통 몸체 「chibi」 — 필드 사양의 idle · walk 프레임을 그립니다

모든 캐릭터가 함께 쓰는 민무늬 몸(피부 + 흰 속옷)입니다. 기준 방향은 왼쪽 3/4 — 먼 쪽(화면 왼쪽 _L)
팔 · 다리는 몸 뒤, 가까운 쪽(화면 오른쪽 _R)은 몸 앞입니다. 프레임마다 머리 · 몸 · 손이 기본 자세에서
얼마나 움직였는지는 사양 파일 animations.{태그}.offsets와 같아야 합니다 — 이 파일이 그 값을 읽어 씁니다.

    python chibi.py   →  ./{태그}/{00..}.png · ./preview.png
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_lib"))
import fieldkit as fk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SKIN, CLOTH = "SKIN", "CLOTH_B"

# 기본 자세 좌표 (필드 사양 기준선: 눈 25 · 턱 33 · 어깨 35 · 허리 43 · 가랑이 47 · 무릎 53 · 발목 57 · 발바닥 59)
HEAD = (32.5, 23.5, 10.5, 9.5)          # 중심 x, y, 반지름 x, y — 3/4라 얼굴이 살짝 왼쪽
NECK = (30, 33, 33, 34)
TORSO = [(27, 35), (37, 35), (38, 43), (36, 47), (28, 47), (26, 43)]
ARM_L = [(25, 36), (28, 36), (27, 45), (24, 45)]      # 먼 쪽(뒤)
ARM_R = [(36, 36), (39, 36), (40, 45), (37, 45)]      # 가까운 쪽(앞)
HAND_L, HAND_R = (25.5, 46.5), (38.5, 46.5)
LEG_L = [(28, 47), (31, 47), (31, 57), (28, 57)]
LEG_R = [(33, 47), (36, 47), (36, 57), (33, 57)]
FOOT_L, FOOT_R = (27, 57, 31, 59), (32, 57, 37, 59)  # 발: 앞으로 살짝 김


def body(sp, dh=(0, 0), db=(0, 0), hr=(0, 0), hl=(0, 0), legs=None, feet=None):
    """한 프레임. dh · db · hr · hl: 머리 · 몸 · 가까운 손 · 먼 손 이동량. legs · feet: 걷기용 좌표 덮어쓰기."""
    L = fk.layer(sp, "body")
    legs = legs or (LEG_L, LEG_R)
    feet = feet or (FOOT_L, FOOT_R)
    # 뒤 → 앞: 먼 팔, 먼 다리, 몸통, 목, 가까운 다리, 발, 머리, 가까운 팔, 손
    fk.paint(sp, L, lambda t: t.poly([(x + hl[0], y + hl[1]) for x, y in ARM_L], 1), SKIN, "cyl", max_step=3)
    fk.paint(sp, L, lambda t: t.ellipse(HAND_L[0] + hl[0], HAND_L[1] + hl[1], 2.2, 2.1, 1), SKIN, "sphere", 2)
    fk.paint(sp, L, lambda t: t.poly(legs[0], 1), SKIN, "cyl", 3)
    fk.paint(sp, L, lambda t: t.poly([(x + db[0], y + db[1]) for x, y in TORSO], 1), CLOTH, "cyl", 2)
    fk.paint(sp, L, lambda t: fk.rect(t, NECK[0] + db[0], NECK[1] + db[1], NECK[2] + db[0], NECK[3] + db[1], 1), SKIN, "flat")
    L.pixels([(x, NECK[1] + db[1]) for x in range(NECK[0] + db[0], NECK[2] + db[0] + 1)], sp.c(SKIN, 2))
    fk.paint(sp, L, lambda t: t.poly(legs[1], 1), SKIN, "cyl", 2)
    for f in feet:
        fk.paint(sp, L, lambda t, f=f: fk.rect(t, *f, 1), CLOTH, "sphere", 2)
    fk.paint(sp, L, lambda t: t.ellipse(HEAD[0] + dh[0], HEAD[1] + dh[1], HEAD[2], HEAD[3], 1), SKIN, "sphere", 2)
    fk.paint(sp, L, lambda t: t.poly([(x + hr[0], y + hr[1]) for x, y in ARM_R], 1), SKIN, "cyl", 2)
    fk.paint(sp, L, lambda t: t.ellipse(HAND_R[0] + hr[0], HAND_R[1] + hr[1], 2.4, 2.2, 1), SKIN, "sphere", 2)
    # 얼굴 기호 — 눈(세로 3, 하이라이트 1), 볼, 입. 3/4라 왼쪽 눈이 얼굴 가장자리 쪽
    ex, ey = 27 + dh[0], 24 + dh[1]
    for x in (ex, ex + 7):
        L.pixels([(x, ey), (x, ey + 1), (x, ey + 2), (x + 1, ey + 1), (x + 1, ey + 2)], 1)
        L.set(x, ey, sp.c("EYE", 0))
        L.set(x + 1, ey + 1, sp.c("EYE", 1))
    L.pixels([(ex - 1, ey + 3), (ex + 9, ey + 3)], sp.c("ACCENT", 0))
    L.pixels([(ex + 3, ey + 5), (ex + 4, ey + 5)], sp.c(SKIN, 3))
    L.add_outline()
    # 안쪽 선(팔 · 다리가 몸에 겹치는 곳)은 피부 가장 어두운 단계로
    for y in range(sp.height):
        for x in range(sp.width):
            if L.outline[y][x] and all(L.inside(x + dx, y + dy) and L.px[y + dy][x + dx] for dx, dy in pixkit4()):
                L.px[y][x] = sp.c(SKIN, 3)
    return L


def pixkit4():
    return ((1, 0), (-1, 0), (0, 1), (0, -1))


def walk_legs(f):
    """8프레임 걷기 — 가까운 다리와 먼 다리가 반대 위상으로 앞뒤. 발은 땅에 닿는 프레임에서 y=57~59 고정."""
    phase = [0, 1, 2, 1, 0, -1, -2, -1][f]           # 가까운 다리의 앞(+)뒤(-)
    lift = [0, 1, 0, 0, 0, 1, 0, 0][f]                # 뒤로 갈 때 살짝 들림
    def leg(base, d, up):
        return [(x + d * (1 if y >= 52 else 0) + (d // 2 if 47 < y < 52 else 0), y - (up if y >= 55 else 0)) for x, y in base]
    lr = leg(LEG_R, 2 * phase, lift if phase < 0 else 0)
    ll = leg(LEG_L, -2 * phase, lift if phase > 0 else 0)
    fr = (FOOT_R[0] + 2 * phase, FOOT_R[1] - (lift if phase < 0 else 0), FOOT_R[2] + 2 * phase, FOOT_R[3] - (lift if phase < 0 else 0))
    fl = (FOOT_L[0] - 2 * phase, FOOT_L[1] - (lift if phase > 0 else 0), FOOT_L[2] - 2 * phase, FOOT_L[3] - (lift if phase > 0 else 0))
    return (ll, lr), (fl, fr)


def main():
    sp = fk.load_spec()
    frames = []
    for tag, a in sp.animations.items():
        for f in range(a["frames"]):
            dh, db, hr = sp.offset(tag, "head", f), sp.offset(tag, "body", f), sp.offset(tag, "hand_R", f)
            hl = (-hr[0], hr[1]) if tag == "walk" else hr    # 걷기: 먼 손은 반대 위상
            legs = feet = None
            if tag == "walk":
                legs, feet = walk_legs(f)
            L = body(sp, dh, db, hr, hl, legs, feet)
            fk.save(sp, L, os.path.join(HERE, tag, "%02d.png" % f))
            frames.append(L)
    # 미리보기 시트
    from PIL import Image
    K = 4
    sheet = Image.new("RGBA", (sp.width * K * len(frames), sp.height * K), (120, 120, 130, 255))
    for i, L in enumerate(frames):
        tmp = os.path.join(HERE, "_tmp.png")
        fk.save(sp, L, tmp)
        sheet.alpha_composite(Image.open(tmp).convert("RGBA").resize((sp.width * K, sp.height * K), Image.NEAREST), (i * sp.width * K, 0))
        os.remove(tmp)
    sheet.save(os.path.join(HERE, "preview.png"))
    print("공통 몸체 chibi — %d프레임" % len(frames))


if __name__ == "__main__":
    main()
