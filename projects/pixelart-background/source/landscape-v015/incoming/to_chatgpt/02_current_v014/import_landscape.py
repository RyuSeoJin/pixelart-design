# CHANGELOG v1.1 · 2026-10-08 — PNG 1픽셀=월드4단위로 가져옵니다.
# CHANGELOG v1.0 · 2026-10-08 — v014 확장 하늘을 포함한44개 자산입니다.
"""RecordTales 에디터에서 숲·겨울 배경 전체 텍스처와 Paper2D 스프라이트를 생성합니다."""
from pathlib import Path
import json
import unreal

ROOT = Path(__file__).resolve().parent
DEST = "/Game/Art/PixelLandscape_v014"


def main():
    # 기존 프로젝트의 전체 사각형 스프라이트 생성 함수를 사용합니다.
    if not hasattr(unreal, "RTArtImportLibrary"):
        raise RuntimeError("RecordTales 모듈이 로드된 에디터에서 실행해주세요.")
    config = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    specs = {item["name"]: item for item in config["assets"]}
    files = [ROOT / item["file"] for item in config["assets"]]
    if len(files) != 44 or len(specs) != 44 or not all(f.is_file() for f in files):
        raise RuntimeError("배경 PNG44개와 manifest.json을 확인해주세요.")
    # 재실행 시 기존 에셋을 덮어쓰지 않고 명확히 중단합니다.
    for file in files:
        for name in (file.stem, file.stem + "_Sprite"):
            if unreal.EditorAssetLibrary.does_asset_exist(DEST + "/" + name):
                raise RuntimeError("이미 존재하는 에셋입니다: " + DEST + "/" + name)
    result = []
    for file in files:
        task = unreal.AssetImportTask()
        for key, value in {
            "filename": str(file), "destination_path": DEST,
            "destination_name": file.stem, "replace_existing": False,
            "automated": True, "save": False,
        }.items():
            task.set_editor_property(key, value)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        texture = unreal.load_asset(DEST + "/" + file.stem)
        if not isinstance(texture, unreal.Texture2D):
            raise RuntimeError("텍스처 가져오기 실패: " + file.name)
        # 비정방형 원본과 알파, 선명한 도트를 보존합니다.
        for key, value in {
            "compression_settings": unreal.TextureCompressionSettings.TC_EDITOR_ICON,
            "mip_gen_settings": unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS,
            "filter": unreal.TextureFilter.TF_NEAREST,
            "lod_group": unreal.TextureGroup.TEXTUREGROUP_PIXELS2D,
            "srgb": True,
        }.items():
            texture.set_editor_property(key, value)
        sprite = unreal.RTArtImportLibrary.make_sprite(texture, DEST, file.stem + "_Sprite")
        if sprite is None:
            raise RuntimeError("스프라이트 생성 실패: " + file.name)
        sprite.set_editor_property("pixels_per_unreal_unit", 0.25)
        size = sprite.get_editor_property("source_dimension")
        if (size.x, size.y) != tuple(specs[file.stem]["size"]):
            raise RuntimeError("스프라이트의 전체 캔버스 규격이 다릅니다.")
        for asset in (texture, sprite):
            if not unreal.EditorAssetLibrary.save_loaded_asset(asset, False):
                raise RuntimeError("에셋 저장 실패: " + asset.get_path_name())
        result.append({"texture": texture.get_path_name(), "sprite": sprite.get_path_name()})
    (ROOT / "import-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    unreal.log("숲·겨울 배경 텍스처 44개와 스프라이트 44개를 저장했습니다. 아트 목록 연결은 별도입니다.")


if __name__ == "__main__":
    main()
