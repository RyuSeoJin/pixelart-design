-- CHANGELOG v1.0 · 2026-09-27 — 320 정지 그림의 얼굴 내부만 1px로 보정
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local base=Image{fromFile=root..'export/ice-queen/ice-queen-still-320x320-v1.png'}
local result=Image(base)
local overlay=Image(320,320,ColorMode.RGB)
local mask=Image(320,320,ColorMode.RGB)
local function rgb(hex)
  return app.pixelColor.rgba(tonumber(hex:sub(1,2),16),tonumber(hex:sub(3,4),16),tonumber(hex:sub(5,6),16),255)
end
-- 얼굴 피부와 눈의 실제 내부만 마스크에 포함합니다. 머리카락과 얼굴 윤곽은 제외합니다.
local function area(y,x0,x1)
  for x=x0,x1 do mask:drawPixel(x,y,rgb('FFFFFF')) end
end
for y=70,75 do area(y,146,150) end
for y=70,75 do area(y,157,165) end
for y=76,81 do area(y,150,163) end
for y=82,84 do area(y,151,163) end
area(85,154,159)
local function set(x,y,color)
  assert(app.pixelColor.rgbaA(mask:getPixel(x,y))>0,'얼굴 밖 수정')
  local p=rgb(color)
  result:drawPixel(x,y,p)
  overlay:drawPixel(x,y,p)
end
-- 2×2의 입 점을 피부색으로 정리한 뒤, 1px 입선과 작은 입꼬리로 교체합니다.
for y=82,83 do for x=154,155 do set(x,y,'F6D2BC') end end
set(153,82,'E2A895')
set(154,82,'B87574')
set(155,82,'B87574')
set(156,82,'B87574')
set(157,81,'B87574')
set(155,83,'FFF1E4')
-- 코와 눈은 기존 위치·시선을 유지하고 반짝임·경계만 1px로 정리합니다.
set(153,78,'E2A895')
set(154,78,'FFF1E4')
set(148,72,'7FD0E0')
set(148,73,'3E8FB8')
set(149,75,'7FD0E0')
set(158,72,'7FD0E0')
set(159,72,'3E8FB8')
set(159,73,'2A4F80')
set(160,74,'7FD0E0')
set(161,75,'7FD0E0')
set(162,74,'FFF1E4')
set(163,74,'F6D2BC')
set(163,75,'F6D2BC')
set(157,70,'221A26')
set(158,71,'383C55')
set(165,71,'7A4A58')
result:saveAs(root..'export/ice-queen/ice-queen-still-320x320-v2.png')
overlay:saveAs(root..'source/ice-queen/face-retouch-320-v2.png')
mask:saveAs(root..'source/ice-queen/face-mask-320-v2.png')
local sprite=Sprite(320,320,ColorMode.RGB)
sprite.layers[1].name='base_2x'
sprite:newCel(sprite.layers[1],1,base,Point(0,0))
local face=sprite:newLayer()
face.name='face_retouch_1px'
sprite:newCel(face,1,overlay,Point(0,0))
local scope=sprite:newLayer()
scope.name='face_mask'
sprite:newCel(scope,1,mask,Point(0,0))
scope.isVisible=false
sprite:saveAs(root..'sprites/ice-queen-still-v2.aseprite')
print('얼굴 보정 v2 저장 완료')
