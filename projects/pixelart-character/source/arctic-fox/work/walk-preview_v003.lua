-- CHANGELOG v1.0 · 2026-09-29 — 16프레임 수정본과 동일 주기의 전후 비교 미리보기를 저장합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
for _,scale in ipairs({1,3}) do
 local s=Sprite(180*scale,180*scale,ColorMode.RGB)
 s.layers[1].name='full_frame'
 for i=0,15 do
  local input=app.open(root..'work/walk-corrected-left/frame-'..string.format('%02d',i)..'_v003.png')
  local im=Image(input.spec);im:drawSprite(input,1);input:close()
  local out=Image(180*scale,180*scale,ColorMode.RGB)
  for y=0,179 do for x=0,179 do local c=im:getPixel(x,y)
   for yy=0,scale-1 do for xx=0,scale-1 do out:drawPixel(x*scale+xx,y*scale+yy,c) end end
  end end
  if i==0 then s.cels[1].image=out else local frame=s:newEmptyFrame();s:newCel(s.layers[1],frame,out,Point(0,0)) end
  s.frames[i+1].duration=0.05
 end
 app.activeSprite=s
 if scale==1 then
  local tag=s:newTag(1,16);tag.name='walk_left'
  s:saveAs(root..'work/walk-left_v003.aseprite')
 else s:saveAs(root..'work/walk-left-preview-3x_v003.gif') end
 s:close()
end
print('WALK_PREVIEW_V003')

local comp=Sprite(1080,540,ColorMode.RGB)
for i=0,15 do
 local out=Image(1080,540,ColorMode.RGB)
 for side=0,1 do
  local index=side==0 and math.floor(i/2) or i
  local version=side==0 and '002' or '003'
  local source=app.open(root..'work/walk-corrected-left/frame-'..string.format('%02d',index)..'_v'..version..'.png')
  local im=Image(source.spec);im:drawSprite(source,1);source:close()
  for y=0,179 do for x=0,179 do local c=im:getPixel(x,y)
   for yy=0,2 do for xx=0,2 do out:drawPixel(side*540+x*3+xx,y*3+yy,c) end end
  end end
 end
 if i==0 then comp.cels[1].image=out else local fr=comp:newEmptyFrame();comp:newCel(comp.layers[1],fr,out,Point(0,0)) end
 comp.frames[i+1].duration=0.05
end
app.activeSprite=comp;comp:saveAs(root..'work/walk-before-after_v003.gif');comp:close()
