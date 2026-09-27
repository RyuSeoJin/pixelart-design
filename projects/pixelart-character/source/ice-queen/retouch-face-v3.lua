-- CHANGELOG v1.0 · 2026-09-27 — 320 정지 그림의 눈 폭·높이·시선 균형을 1px로 보정
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local base=Image{fromFile=root..'export/ice-queen/ice-queen-still-320x320-v1.png'}
local result=Image{fromFile=root..'export/ice-queen/ice-queen-still-320x320-v2.png'}
local overlay=Image{fromFile=root..'source/ice-queen/face-retouch-320-v2.png'}
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
-- 먼 눈의 폭을 넓히고 두 눈의 윗선·아랫선을 맞춥니다.
for y=70,75 do area(y,146,151); area(y,157,165) end
for y=68,69 do area(y,160,165) end
for y=76,77 do area(y,148,149) end
for y=68,69 do for x=160,165 do set(x,y,'F6D2BC') end end
for y=76,77 do for x=148,149 do set(x,y,'F6D2BC') end end
local colors={S='F6D2BC',D='383C55',W='FFF1E4',P='2A4F80',B='3E8FB8',H='7FD0E0',L='E2A895'}
local function eye(x0,rows)
 for row,line in ipairs(rows) do
  for i=1,#line do set(x0+i-1,69+row,colors[line:sub(i,i)]) end
 end
end
eye(146,{'DDDDDD','WHPBWS','WBPBWS','SBHBWS','SLLLSS','SSSSSS'})
eye(157,{'DDDDDDDD','WHPBBWWD','WBPBBWWW','SBHHBWWL','SLLLLLSS','SSSSSSSS'})
set(165,70,'F6D2BC'); set(165,71,'F6D2BC')
result:saveAs(root..'export/ice-queen/ice-queen-still-320x320-v3.png')
overlay:saveAs(root..'source/ice-queen/face-retouch-320-v3.png')
mask:saveAs(root..'source/ice-queen/face-mask-320-v3.png')
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
sprite:saveAs(root..'sprites/ice-queen-still-v3.aseprite')
print('얼굴 보정 v3 저장 완료')
