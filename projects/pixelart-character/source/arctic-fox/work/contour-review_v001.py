# CHANGELOG v1.0 · 2026-09-29 — 출력 픽셀·동작 시간·수정 영역을 검사합니다.
from pathlib import Path
from PIL import Image, ImageSequence
import numpy as np
import hashlib
import json
import shutil

root = Path(__file__).resolve().parents[1]
report = {"상태": "수정본·사용자 검토 전", "프레임": [], "미검수": ["실제 반복 재생 관찰", "엔진 표시"], "별도 작업": "우향 walk 신규 제작"}
for motion, side, count, ms in [("idle", "left", 6, 250), ("idle", "right", 6, 250), ("walk", "left", 8, 100)]:
    folder = root / f"image-undecided/180/anim-{motion}/{side}"
    source = Image.open(root / f"image-confirmed/180/view/side_{side}_v010.png").convert("RGBA")
    palette = set(source.getdata())
    imported = root / f"work/contour-input-{motion}-{side}"
    imported.mkdir(exist_ok=True)
    frames = []
    for i in range(count):
        path = folder / f"frame-{i:02d}_v007.png"
        im = Image.open(path).convert("RGBA")
        a = np.array(im)
        b = np.array(Image.open(folder / f"frame-{i:02d}_v006.png").convert("RGBA"))
        visible = a[:, :, 3] > 0
        colors = {tuple(c) for c in a[visible]}
        changed = np.any(a != b, axis=2)
        # 지정한 수정 영역 밖의 픽셀이 유지되는지 확인합니다.
        allowed = np.zeros((180, 180), dtype=bool)
        allowed[65:85, 73:107] = True
        allowed[140:157, 25:155] = True
        row = {"동작": motion, "방향": side, "프레임": i,
               "크기": list(im.size), "변경 픽셀": int(changed.sum()),
               "범위 밖 변경": int((changed & ~allowed).sum()),
               "추가 색": len(colors - palette), "이진 알파": bool(set(a[:, :, 3].flat) <= {0, 255}),
               "머리 유지": bool(np.array_equal(a[:60], b[:60])),
               "최하단": int(np.where(visible)[0].max()),
               "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        assert row["범위 밖 변경"] == 0 and row["추가 색"] == 0 and row["이진 알파"]
        assert row["머리 유지"] and im.size == (180, 180)
        report["프레임"].append(row)
        frames.append({"file": path.name, "duration_ms": ms, "sha256": row["sha256"]})
        shutil.copy2(path, imported / path.name)
    gif = Image.open(folder / "preview_v007.gif")
    assert gif.n_frames == count
    assert [f.info["duration"] for f in ImageSequence.Iterator(gif)] == [ms] * count
    manifest = {"version": 7, "status": "미확정", "canvas": [180, 180], "loop": True, "frames": frames}
    (folder / "manifest_v007.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
report["점검 내용"] = ["가슴 앞 윤곽의 돌출·움푹한 부분 정리", "꼬리 안쪽의 가시 제거", "walk 8개 자세와 8→1 위치 경로 비교", "원본 팔레트·얼굴·피부·다리·옆트임 유지", "타이밍 유지"]
(root / "work/contour-review_v001.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("프레임 20장: 팔레트·크기·알파·수정 영역·시간 검사 통과")
