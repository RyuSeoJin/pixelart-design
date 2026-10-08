# CHANGELOG v1.0 · 2026-10-08 — v015 검수본을 전달 폴더로 묶고 현행 기준을 갱신합니다.
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,shutil,zipfile,hashlib
ROOT=Path(__file__).resolve().parent;PKG=ROOT/'unreal-full';PROJECT=ROOT.parent.parent
report=json.loads((PKG/'package-validation.json').read_text(encoding='utf-8'));assert report['passed']
assert not (PROJECT/'final').exists()
m=json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))
ref=json.loads((ROOT/'incoming/to_chatgpt/02_current_v014/manifest.json').read_text(encoding='utf-8'))
record={'version':15,'request':'00_REQUEST.md · 사용자 제공 to_chatgpt (3).zip','source_package':'v014 · 사용자 요청서에 따르면 UE 가져오기 완료','preserved':[{'file':a['file'],'sha256':a['sha256']} for a in ref['assets'] if a['layer']!='stars'],'removed':['Textures/T_Forest_Stars.png','Textures/T_Snow_Stars.png'],'new_color_variants':40,'new_star_layers':6,'new_shared_assets':['T_Sun','T_Moon','T_Meteor','T_MeteorBig','T_MeteorGlow','T_MeteorSpark'],'method':'새벽·저녁은 Aseprite에서 낮판 윤곽을 보존한 색상 변환입니다. 별은 기존 픽셀을 밝기로 분리하고 C에100픽셀을 더했습니다. 천체·효과는 내장 GPT 원화6장을 생성하고 Aseprite로 팔레트·크기·이진 알파를 정리했습니다.','sky_night_modified':False,'source_files':5,'engine_executed':False,'art_approval':'검토 대기','notes':['해·달의 위치는 요청서 궤도 공식을 그대로 적용했습니다. 새벽·저녁의 해 일부는 기존 뒷산 능선에 가려지며 해와 달 모두 보입니다.','천체는 assets의 phase=all이며 body 층의 궤도·가시 시간으로 표시합니다.','미리보기의 별 반짝임 밝기는 최대값입니다. 실제 반짝임과 구름 흐름은 게임이 manifest 값으로 계산합니다.','별똥별 빛무리·반짝임은 미리보기에 포함했으며 실제 게임에서는 요청서대로 meteor·meteor_big 두 종류를 먼저 연결합니다.']}
(PKG/'conversion-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prompts=json.loads((ROOT/'generation-prompts.json').read_text(encoding='utf-8'))
for r in prompts['records']:
 r['raw_input']='input/'+r['name']+'.png';r['sha256']=hashlib.sha256((ROOT/r['raw_input']).read_bytes()).hexdigest();r.pop('path',None)
prompts['raw_input_base']='../source/landscape-v015/';prompts['processing']='finish-art.lua · Aseprite 도트 정리'
(PKG/'generation-prompts.json').write_text(json.dumps(prompts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copytree(PKG,PROJECT/'final',ignore=shutil.ignore_patterns('__pycache__','*.pyc','checks'))
files=[p for p in (PROJECT/'final').rglob('*') if p.is_file()]
with zipfile.ZipFile(PROJECT/'final.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,'final/'+p.relative_to(PROJECT/'final').as_posix())
with zipfile.ZipFile(PROJECT/'final.zip') as z:
 assert z.testzip() is None
 for p in files:assert z.read('final/'+p.relative_to(PROJECT/'final').as_posix())==p.read_bytes()
spec=PROJECT/'spec/design/landscape-v015-request.md';shutil.copy2(ROOT/'incoming/to_chatgpt/00_REQUEST.md',spec)
stamp=datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')
log=PROJECT/'pixelart-background-change-log.md';text=log.read_text(encoding='utf-8')
start=text.index('숲·설원 패럴렉스 최종 전달 폴더는');end=text.index('### 프로젝트 정의',start)
current=f'''숲·설원 배경 최종 전달 폴더는 `final/`이며 제작 기준은 `source/landscape-v015/unreal-full/`입니다. 사용자 제공 `spec/design/landscape-v015-request.md`가 이번 시간대·천체 확장 정본이며, 픽셀 규격은 `rules/landscape-fixed-2026-10-08.md`를 따릅니다. PNG1픽셀=월드4단위, 배경 폭7680과 공통 카메라·지면832를 유지합니다. 캐릭터·플레이어 건물은 변경하지 않습니다.

v014의 별2장을 제외한42장은 해시·배치를 그대로 유지합니다. 새벽·저녁 색상판40장, 별A·B·C6장, 공용 해·달2장을 합쳐 assets90개입니다. 공용 별똥별·큰 별똥별·빛무리·반짝임4개는 별도fx입니다. Textures는94장, render_order는16층, Aseprite 원본은5개입니다. 일반 PNG1920×270, 하늘·별1920×894, 높은 구름1920×624, 바닥120×30, 하단 색면480×270은 동일합니다.

새벽·저녁은 낮판 알파를 보존한 색상 변환입니다. 하늘은 세로 색 변화만 사용합니다. 기존 밤 하늘에 천체가 없어 수정하지 않았습니다. 별은 겹침 없이105·210·485픽셀로 분리했고, 기존700픽셀에 흐린 별100픽셀을 더했습니다. 해·달은48×48이며 요청서의15시간 궤도를 사용합니다. 구름 흐름은 높은 층3·낮은 층6월드단위/실제초입니다. 천체·효과 원화는 내장 GPT로 생성하고 Aseprite에서 정리했습니다.

시간대4개×배율25·100%의 지역별 화면과 궤도 표시판,04:00~다음04:00의1시간 간격 흐름, 효과 미리보기를 전달합니다. 검사{report['checks']}개가 통과했고 원본 왕복94개가 포함됩니다. 가져오기 경로는 `/Game/Art/PixelLandscape_v015`, pixels_per_unreal_unit은0.25입니다. 사용자 요청서에 따르면 v014는 UE 가져오기가 완료됐으며, v015의 실제 엔진 실행은 하지 않았습니다. 미술 승인은 별도입니다. 이전 전달본은 `source/landscape-v014/final-before-v015/`에 보존합니다.

식당 제작 기준과 도시 바닥은 이번 범위에서 변경하지 않았습니다.

'''
text=text[:start]+current+text[end:]
entry=f'### {stamp} — (추가) 새벽·저녁·천체·별똥별 배경 v015\n\n게임의4시간대·천체 효과 확장 요청에 따라 기존42장을 보존하면서 색상판40장과 별3층·공용 천체·효과를 추가했습니다. 94개PNG와5개Aseprite 원본, 시간대·궤도·하루 흐름·효과 미리보기 및 가져오기 설정을 저장했습니다. 검사{report["checks"]}개가 통과했습니다. 새벽·저녁 해의 일부는 요청서 궤도와 기존 산 능선에 따라 가려지며 좌표나 산을 임의 수정하지 않았습니다. 실제 UE 실행은 하지 않았습니다.\n\n'
text=text.replace('## 변경 이력 (최신이 위)\n\n','## 변경 이력 (최신이 위)\n\n'+entry,1)
log.write_text('<!-- CHANGELOG v1.18 · 2026-10-08 — (추가) 4시간대·천체·효과 -->\n'+text,encoding='utf-8')
p=PROJECT/'pixelart-background-remaining-work.md';text=p.read_text(encoding='utf-8');start=text.index('- **패럴렉스 v014');end=text.index('- **도시 바닥**',start)
text=text[:start]+'''- **패럴렉스 v015 미술 검토** — `final/Preview/`의4시간대 비교판·궤도 표시판·하루 흐름·별똥별 화면에서 색온도·가림·효과를 확인합니다.
- **패럴렉스 v015 UE 연결** — `/Game/Art/PixelLandscape_v015`에94개 텍스처와 스프라이트를 가져옵니다. assets90개·fx4개·render_order16층과4시간대, 별 문턱·반짝임·구름 흐름을 연결합니다. 해·달은 phase=all 공용 그림이며 body 궤도로 표시합니다. 게임은 meteor·meteor_big 두fx를 우선 연결하고 빛무리·반짝임은 이후 확장합니다. 1픽셀=월드4단위를 중복 확대하지 않고 낮밤 전환·양방향 이동·실제 엔진 메모리를 확인합니다.
'''+text[end:]
text=text.replace('패럴렉스 v014의 바닥 격자·접합과 고정 규격 미술 승인입니다. 파일·좌표 검수는 완료됐습니다.','패럴렉스 v015의 새벽·저녁 색과 천체·별똥별 미술 승인입니다. 파일·좌표 검수는 완료됐습니다.')
p.write_text('<!-- CHANGELOG v1.13 · 2026-10-08 — (변경) v015 엔진·미술 검수 -->\n'+text,encoding='utf-8')
p=PROJECT/'pixelart-background-structure.json';data=json.loads(p.read_text(encoding='utf-8'))
for r in data['resources']:
 if r['id']=='landscape-source':r.update(path='source/landscape-v015',label='숲·설원 v015 · 4시간대·천체·효과')
 if r['id']=='landscape-final':r['label']='숲·설원 최종 전달 폴더 · v015'
data['resources'].insert(2,dict(id='landscape-v014-history',path='source/landscape-v014',label='2시간대 배경 이전본 · v015로 대체',role='archive',kind='directory'))
data['resources'].insert(2,dict(id='landscape-v015-request',path='spec/design/landscape-v015-request.md',label='사용자 제공4시간대·천체 요청서',role='specification',kind='file'))
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'version':15,'files':len(files),'zip_bytes':(PROJECT/'final.zip').stat().st_size,'zip_sha256':hashlib.sha256((PROJECT/'final.zip').read_bytes()).hexdigest()}))
