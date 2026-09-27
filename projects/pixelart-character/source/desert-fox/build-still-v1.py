# CHANGELOG v1.0 · 2026-09-28 — 승인 시안을 160 격자·320 출력·512 배포 검토본으로 변환합니다.
"""사막여우 도트 초안과 재현 가능한 검사 자료를 만듭니다."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

SOURCE = Path(__file__).resolve().parent
PROJECT = SOURCE.parents[1]
OUT = PROJECT / 'export/desert-fox'
OUT.mkdir(parents=True, exist_ok=True)
spec = json.loads((PROJECT / 'spec/design/pixel-spec-field.json').read_text(encoding='utf-8'))
colors = list(dict.fromkeys([spec['palette']['outline']] + [c for ramp in spec['palette']['ramps'].values() for c in ramp]))
palette = np.array([tuple(bytes.fromhex(c[1:])) for c in colors], dtype=np.int32)
im = Image.open(SOURCE / 'desert-fox-concept-1024x1024-v1.png').convert('RGBA')
# 귀를 키 측정에서 제외하고 몸 중심을 고정합니다. 꼬리 포함 바운딩박스로 재중앙 배치하지 않습니다.
small = im.resize((151, 151), Image.Resampling.BOX)
a = np.array(small)
rgb = a[:, :, :3].astype(np.int32)
nearest = ((rgb[:, :, None, :] - palette[None, None, :, :]) ** 2).sum(axis=3).argmin(axis=2)
a[:, :, :3] = palette[nearest]
a[:, :, 3] = np.where(a[:, :, 3] >= 128, 255, 0)
a[a[:, :, 3] == 0] = 0
native = Image.new('RGBA', (160, 160))
native.paste(Image.fromarray(a), (8, 3))
native.save(SOURCE / 'desert-fox-working-160x160-draft-v1.png')
base = native.resize((320, 320), Image.Resampling.NEAREST)
base.save(OUT / 'desert-fox-base-320x320-v1.png')
# 손질은 별도 파일에서 수행하며 초안에 최종 통과 판정을 붙이지 않습니다.
print(json.dumps({'native_bbox': native.getbbox(), 'palette_colors': len({c for c in native.get_flattened_data() if c[3]})}))
