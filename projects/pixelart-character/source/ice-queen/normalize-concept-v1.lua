-- CHANGELOG v1.0 · 2026-09-27 — 생성 시안을 승인된 1024 캔버스와 색상 하한으로 정리
local spr = app.open('P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/ice-queen-concept-generated-v1.png')
app.command.SpriteSize { ui=false, width=1024, height=1024, method='nearest' }
for _,cel in ipairs(spr.cels) do
  local im=cel.image:clone()
  for it in im:pixels() do
    local p=it()
    local a=app.pixelColor.rgbaA(p)
    if a>0 then
      it(app.pixelColor.rgba(math.max(10,app.pixelColor.rgbaR(p)),math.max(10,app.pixelColor.rgbaG(p)),math.max(10,app.pixelColor.rgbaB(p)),a))
    end
  end
  cel.image=im
end
spr:saveAs('P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/ice-queen-concept-1024x1024-v1.png')
