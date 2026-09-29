-- CHANGELOG v1.0 · 2026-09-29 — 좌향 수정본의 편집 원본과 3배 미리보기를 저장합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
for _,scale in ipairs({1,3}) do
 local s=Sprite(180*scale,180*scale,ColorMode.RGB)
 s.layers[1].name='full_frame'
 for i=0,7 do
  local input=app.open(root..'work/walk-corrected-left/frame-'..string.format('%02d',i)..'_v002.png')
  local im=Image(input.spec);im:drawSprite(input,1);input:close()
  local out=Image(180*scale,180*scale,ColorMode.RGB)
  for y=0,179 do for x=0,179 do local c=im:getPixel(x,y)
   for yy=0,scale-1 do for xx=0,scale-1 do out:drawPixel(x*scale+xx,y*scale+yy,c) end end
  end end
  if i==0 then s.cels[1].image=out else local frame=s:newEmptyFrame();s:newCel(s.layers[1],frame,out,Point(0,0)) end
  s.frames[i+1].duration=0.1
 end
 app.activeSprite=s
 if scale==1 then
  local tag=s:newTag(1,8);tag.name='walk_left'
  s:saveAs(root..'work/walk-left_v002.aseprite')
 else s:saveAs(root..'work/walk-left-preview-3x_v002.gif') end
 s:close()
end
print('WALK_PREVIEW_V002')
