-- CHANGELOG v1.0 · 2026-09-29 — 원본·하체 프레임을 정수배로 비교합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
local out=Image(1280,640,ColorMode.RGB)
for i=0,8 do
 local path=i==8 and 'image-confirmed/180/view/side_left_v010.png' or ('work/walk-corrected-left/frame-'..string.format('%02d',i)..'_v001.png')
 local s=app.open(root..path);local im=Image(s.spec);im:drawSprite(s,1);s:close()
 local ox=(i%5)*256;local oy=math.floor(i/5)*320
 for y=95,174 do for x=45,108 do local c=im:getPixel(x,y)
  for yy=0,3 do for xx=0,3 do out:drawPixel(ox+(x-45)*4+xx,oy+(y-95)*4+yy,c) end end
 end end
end
local s=Sprite(out.width,out.height,ColorMode.RGB);s.cels[1].image=out;app.activeSprite=s;s:saveAs(root..'work/walk-detail_v001.png');s:close()
