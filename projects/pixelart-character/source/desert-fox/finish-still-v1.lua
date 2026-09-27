-- CHANGELOG v1.0 · 2026-09-28 — 얼굴 내부 보정과 편집 가능한 도트 원본을 저장합니다.
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-character")
local source=root.."/source/desert-fox/"
local out=root.."/export/desert-fox/"
local base=Image{fromFile=out.."desert-fox-base-320x320-v1.png"}
local final=Image(base)
local overlay=Image(320,320,ColorMode.RGB)
local mask=Image(320,320,ColorMode.RGB)
local pc=app.pixelColor
local function color(hex)
 return pc.rgba(tonumber(hex:sub(1,2),16),tonumber(hex:sub(3,4),16),tonumber(hex:sub(5,6),16),255)
end
local function area(y,x0,x1)
 for x=x0,x1 do mask:drawPixel(x,y,color('FFFFFF')) end
end
-- 눈과 입 주변 실제 얼굴 안쪽만 포함하고 머리카락·턱 윤곽을 제외.
for y=73,79 do area(y,144,149) end
for y=71,78 do area(y,158,168) end
for y=79,83 do area(y,150,164) end
for y=84,86 do area(y,151,162) end
local function set(x,y,hex)
 assert(pc.rgbaA(mask:getPixel(x,y))==255,'얼굴 마스크 밖 보정')
 local c=color(hex); final:drawPixel(x,y,c); overlay:drawPixel(x,y,c)
end
-- 모래색으로 섞인 코·입 주변을 피부 램프로 정리하고 작은 미소를 복원.
for y=79,86 do
 for x=150,164 do
  if pc.rgbaA(mask:getPixel(x,y))==255 then set(x,y,'FFB0A0') end
 end
end
set(154,81,'B87574');set(155,81,'F6D2BC')
set(154,84,'B87574');set(155,85,'B87574');set(156,85,'B87574');set(157,85,'B87574');set(158,84,'B87574')
set(156,86,'F6D2BC')
-- 눈의 기존 가로 범위 안에서 청록 홍채와 1px 반짝임만 명료하게.
for y=76,78 do for x=146,148 do set(x,y,'3E8FB8') end end
set(146,76,'FFFFFF');set(148,76,'2A4F80');set(147,78,'7FD0E0')
for y=73,76 do for x=161,164 do set(x,y,'3E8FB8') end end
set(161,73,'FFFFFF');set(162,73,'7FD0E0');set(164,73,'2A4F80');set(164,74,'2A4F80');set(162,76,'7FD0E0');set(163,76,'7FD0E0')
final:saveAs(out..'desert-fox-still-320x320-v1.png')
overlay:saveAs(source..'face-retouch-320-v1.png');mask:saveAs(source..'face-mask-320-v1.png')
local sprite=Sprite(320,320,ColorMode.RGB)
sprite.layers[1].name='base_2x';sprite:newCel(sprite.layers[1],1,base,Point(0,0))
local face=sprite:newLayer();face.name='face_retouch_1px';sprite:newCel(face,1,overlay,Point(0,0))
local scope=sprite:newLayer();scope.name='face_mask';scope.isVisible=false;sprite:newCel(scope,1,mask,Point(0,0))
sprite:saveAs(root..'/sprites/desert-fox-still-v1.aseprite');sprite:close()
