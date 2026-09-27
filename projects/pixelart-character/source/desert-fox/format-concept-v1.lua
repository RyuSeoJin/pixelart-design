-- CHANGELOG v1.0 · 2026-09-28 — 생성 시안을 1024 규격으로 저장합니다.
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-character/source/desert-fox")
local src=Image{fromFile=root.."/desert-fox-generated-v1.png"}
assert(src.width==src.height,"정사각형 입력 필요")
-- 외형을 다시 그리지 않고 최근접 표본으로 동일 비율의 1024 시안만 생성.
local dst=Image(1024,1024,ColorMode.RGB)
local pc=app.pixelColor
for y=0,1023 do
 for x=0,1023 do
  local p=src:getPixel(math.min(src.width-1,math.floor((x+0.5)*src.width/1024)),math.min(src.height-1,math.floor((y+0.5)*src.height/1024)))
  local a=pc.rgbaA(p)
  -- 알파를 유지하고 투명색 규칙의 가시 RGB 채널 하한만 적용.
  if a>0 then p=pc.rgba(math.max(10,pc.rgbaR(p)),math.max(10,pc.rgbaG(p)),math.max(10,pc.rgbaB(p)),a) end
  dst:drawPixel(x,y,p)
 end
end
dst:saveAs(root.."/desert-fox-concept-1024x1024-v1.png")
