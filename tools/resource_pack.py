# CHANGELOG v1.0 · 2026-09-27 — 승인된 PNG를 불변 버전으로 등록하고 독립 패키지를 검사합니다.
"""최종 그래픽 리소스를 검사하고 resources에 버전별로 등록합니다."""
import argparse
from datetime import datetime
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SLUG = r'[a-z0-9]+(?:-[a-z0-9]+)*'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inside(base, relative):
    # 절대 경로·상위 이동·Windows 별도 드라이브·심볼릭 링크 탈출을 모두 거부합니다.
    require(isinstance(relative, str) and relative and '\\' not in relative and ':' not in relative,
            '경로는 비어 있지 않은 상대 POSIX 경로여야 합니다')
    path = PurePosixPath(relative)
    require(not path.is_absolute() and all(p not in ('.', '..') for p in path.parts), '상위 경로 이동은 금지입니다')
    resolved = (base / relative).resolve()
    require(resolved.is_relative_to(base.resolve()) and resolved != base.resolve(), '등록 범위 밖 경로입니다')
    return resolved


def asset_path(asset_id, version):
    require(isinstance(asset_id, str) and re.fullmatch(r'(characters|icons)(\.'+SLUG+r')+', asset_id), '리소스 식별자 형식 오류')
    require(isinstance(version, str) and re.fullmatch(r'v[1-9][0-9]*', version), '버전은 v1, v2 같은 양의 정수여야 합니다')
    return '/'.join(asset_id.split('.'))+'/'+version


def size_pair(value):
    return isinstance(value, list) and len(value) == 2 and all(type(v) is int and v > 0 for v in value)


def inspect_png(data, size):
    require(size_pair(size), '예상 크기는 양의 정수 두 개여야 합니다')
    with Image.open(io.BytesIO(data)) as image:
        require(image.format == 'PNG' and getattr(image, 'n_frames', 1) == 1, '정지 PNG 또는 PNG 시트만 등록합니다')
        require(list(image.size) == size, '실제 PNG 크기가 승인 크기와 다릅니다')
        rgba = image.convert('RGBA')
        alpha = rgba.getchannel('A')
        require(alpha.getextrema() == (0, 255), '불투명 그림과 실제 투명 영역이 모두 필요합니다')
        require(set(alpha.get_flattened_data()) <= {0, 255}, '픽셀 리소스의 반투명 픽셀은 허용하지 않습니다')
        colors = {p[:3] for p in rgba.get_flattened_data() if p[3]}
        require(all(min(c) >= 10 for c in colors), '가시 RGB 각 채널은 10 이상이어야 합니다')
    return {'size': size, 'alpha': 'binary', 'visible_colors': len(colors), 'sha256': digest(data)}


def verify_animation(animations, files):
    require(isinstance(animations, dict), 'animations는 객체여야 합니다')
    for name, animation in animations.items():
        require(re.fullmatch(SLUG, name), '동작 이름 형식 오류')
        file = animation['file']
        require(file in files and files[file]['role'] == 'sheet', '동작은 등록된 시트 파일을 참조해야 합니다')
        fw, fh = animation['frame_size']
        require(size_pair([fw, fh]), '프레임 크기 오류')
        require(type(animation['loop']) is bool and animation['frames'], '반복 여부와 프레임 목록이 필요합니다')
        w, h = files[file]['size']
        for frame in animation['frames']:
            rect = frame['rect']
            require(isinstance(rect, list) and len(rect) == 4 and all(type(v) is int for v in rect), '프레임 사각형 오류')
            x, y, rw, rh = rect
            require(rw == fw and rh == fh and x >= 0 and y >= 0 and x+rw <= w and y+rh <= h, '시트 밖 프레임입니다')
            require(type(frame['duration_ms']) is int and frame['duration_ms'] > 0, '프레임 시간 오류')


def prepare(root, plan_path):
    plan_path = plan_path.resolve()
    plan = read_json(plan_path)
    require(plan['schema_version'] == 1, '등록서 스키마 버전 오류')
    require(re.fullmatch(SLUG, plan['project']), '프로젝트 이름 형식 오류')
    project = inside(root, 'projects/'+plan['project'])
    require((project/(plan['project']+'-modules.json')).is_file(), '등록된 프로젝트가 아닙니다')
    require(plan_path.is_relative_to((project/'releases').resolve()), '등록서는 소유 프로젝트의 releases에 둡니다')
    path = asset_path(plan['id'], plan['version'])
    require(plan['kind'] in ('character', 'icon'), '종류는 character 또는 icon입니다')
    require(plan['id'].startswith('characters.' if plan['kind']=='character' else 'icons.'), '종류와 식별자가 다릅니다')
    for field, status in [('approval', 'approved'), ('review', 'passed')]:
        record = plan[field]
        require(record['status'] == status and record['by'].strip() and record['evidence'].strip(), field+' 기록이 미완료입니다')
        datetime.fromisoformat(record['at'])
    require({'visual', 'project_spec', 'rights'} <= set(plan['review']['checks']) and
            all(v is True for v in plan['review']['checks'].values()), '외형·프로젝트 사양·권리 검수가 모두 통과해야 합니다')
    files, payloads = {}, {}
    require(plan['files'], '등록할 파일이 없습니다')
    for item in plan['files']:
        name = item['name']
        require(re.fullmatch(SLUG+r'\.png', name), '출력 파일명은 소문자 PNG 이름이어야 합니다')
        require(name not in files, '출력 파일명이 중복됩니다')
        require(item['role'] in ('still', 'icon', 'sheet'), '검토 이미지·미리보기는 등록하지 않습니다')
        source = inside(project, item['source'])
        require(source.is_relative_to((project/'export').resolve()), 'export에서 내보낸 파일만 등록합니다')
        data = source.read_bytes()
        require(digest(data) == item['sha256'], '승인 이후 파일 내용이 바뀌었습니다: '+name)
        files[name] = {'path': name, 'role': item['role'], **inspect_png(data, item['size'])}
        payloads[name] = data
    require(plan['default_file'] in files, '기본 파일을 찾을 수 없습니다')
    verify_animation(plan.get('animations', {}), files)
    asset = {'schema_version': 1, 'id': plan['id'], 'version': plan['version'], 'kind': plan['kind'],
             'default_file': plan['default_file'], 'filter': 'nearest', 'files': files,
             'animations': plan.get('animations', {})}
    if plan['kind'] == 'character':
        require(plan['facing'] in ('left', 'right', 'front'), '캐릭터 방향 오류')
        pivot = plan['pivot']
        w,h = files[plan['default_file']]['size']
        require(isinstance(pivot,list) and len(pivot)==2 and all(type(v) is int for v in pivot) and 0<=pivot[0]<=w and 0<=pivot[1]<=h, '캐릭터 기준점 오류')
        asset.update(facing=plan['facing'], pivot=pivot)
    return path, asset, payloads


def publish(root, plan_path, apply=False):
    path, asset, payloads = prepare(root, plan_path)
    resources = root/'resources'
    destination = inside(resources, path)
    require(not destination.exists(), '기존 버전은 덮어쓸 수 없습니다: '+path)
    if not apply:
        return {'mode': '검사만 수행', 'path': path, 'files': list(payloads)}
    # 단일 작성자 잠금과 manifest의 원자적 교체로, 독자는 완성된 버전만 발견합니다.
    lock = resources/'.publish.lock'
    with lock.open('x', encoding='utf-8') as stream:
        stream.write(str(os.getpid()))
    staging = None
    installed = False
    try:
        catalog = read_json(resources/'manifest.json')
        require(catalog['schema_version'] == 1, '목록 버전 오류')
        require(not any(e['id']==asset['id'] and e['version']==asset['version'] for e in catalog['assets']), '목록에 이미 등록된 버전입니다')
        staging = Path(tempfile.mkdtemp(prefix='.staging-', dir=resources))
        for name, data in payloads.items():
            (staging/name).write_bytes(data)
        write_json(staging/'asset.json', asset)
        destination.parent.mkdir(parents=True, exist_ok=True)
        require(not destination.exists(), '기존 버전은 덮어쓸 수 없습니다')
        staging.rename(destination)
        installed = True
        catalog['assets'].append({'id':asset['id'], 'version':asset['version'], 'kind':asset['kind'], 'path':path+'/asset.json'})
        catalog['assets'].sort(key=lambda a:(a['id'],int(a['version'][1:])))
        temp = resources/'.manifest-next.json'
        write_json(temp, catalog)
        os.replace(temp, resources/'manifest.json')
    except Exception:
        # 이 호출이 만든 경로만 정리합니다. 이미 등록된 버전은 삭제하지 않습니다.
        target = destination if installed else staging
        if target and target.exists():
            require(target.resolve().is_relative_to(resources.resolve()), '정리 대상이 resources 밖입니다')
            shutil.rmtree(target)
        raise
    finally:
        (resources/'.manifest-next.json').unlink(missing_ok=True)
        lock.unlink()
    return {'mode':'등록 완료', 'path':path, 'files':list(payloads)}


def check(resources):
    catalog = read_json(resources/'manifest.json')
    require(catalog['schema_version'] == 1, '목록 버전 오류')
    seen, listed = set(), set()
    for entry in catalog['assets']:
        key = (entry['id'], entry['version'])
        require(key not in seen, '중복 등록입니다')
        seen.add(key)
        require(entry['path']==asset_path(*key)+'/asset.json', '목록 경로 불일치')
        path = inside(resources, entry['path'])
        listed.add(path)
        asset = read_json(path)
        require(asset['schema_version']==1 and asset['id']==key[0] and asset['version']==key[1] and asset['kind']==entry['kind'], '리소스 정보 불일치')
        require(asset['default_file'] in asset['files'] and asset['filter']=='nearest', '기본 파일·표시 방식 오류')
        for name, info in asset['files'].items():
            require(info['path']==name and re.fullmatch(SLUG+r'\.png',name), '파일 경로 오류')
            data = inside(path.parent, name).read_bytes()
            measured = inspect_png(data, info['size'])
            require(all(info[k]==v for k,v in measured.items()), '리소스 변조 또는 정보 불일치: '+name)
        verify_animation(asset['animations'], asset['files'])
        require({p.name for p in path.parent.iterdir()}==set(asset['files'])|{'asset.json'}, '등록되지 않은 파일이 섞였습니다')
    require({p.resolve() for p in resources.glob('**/asset.json')}==listed, '목록에 없는 버전 폴더가 있습니다')
    return {'검사':'통과', '등록_버전':len(seen)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    registration = sub.add_parser('register', help='기본은 검사만 합니다')
    registration.add_argument('plan', type=Path)
    registration.add_argument('--publish', action='store_true', help='승인 기록을 확인한 최종본을 실제 등록합니다')
    validation = sub.add_parser('check', help='복사된 resources 폴더만으로도 검사합니다')
    validation.add_argument('directory', nargs='?', type=Path, default=ROOT/'resources')
    args = parser.parse_args()
    try:
        result = publish(ROOT, args.plan, args.publish) if args.command=='register' else check(args.directory.resolve())
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, '실패: '+str(error)+'\n')


if __name__ == '__main__':
    main()
