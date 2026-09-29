-- CHANGELOG v1.0 · 2026-09-29 — 승인 원본을 픽셀 보존 정수배 참고 이미지로 저장
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
for _,side in ipairs({'left','right'}) do
 local src=app.open(root..'image-confirmed/180/view/side_'..side..'_v010.png')
 local im=Image(src.spec);im:drawSprite(src,1);src:close()
 local out=Image(720,720,ColorMode.RGB)
 for y=0,179 do for x=0,179 do
  local c=im:getPixel(x,y)
  for yy=0,3 do for xx=0,3 do out:drawPixel(x*4+xx,y*4+yy,c) end end
 end end
 local s=Sprite(720,720,ColorMode.RGB);s.cels[1].image=out;app.activeSprite=s
 s:saveAs(root..'work/walk-reference-'..side..'_v001.png');s:close()
end
print('REFERENCE_PIXEL_SCALE_COMPLETE')
