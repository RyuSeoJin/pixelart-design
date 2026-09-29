-- CHANGELOG v1.0 · 2026-09-28 — 좌우 부위 확대 대조
local base='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
local p=app.pixelColor
local out=Image(900,700,ColorMode.RGB)
out:clear(p.rgba(220,222,228,255))
local rects={{74,36,39,23},{74,82,39,30},{75,111,30,35}}
for n,side in ipairs({'left','right'}) do
 local s=app.open(base..'image-undecided/180/view/side_'..side..'_v008.png')
 local im=Image(s.spec); im:drawSprite(s,1); s:close()
 for row,r in ipairs(rects) do
  for y=0,r[4]-1 do for x=0,r[3]-1 do
   local sx=r[1]+x;if n==2 then sx=179-sx end
   local c=im:getPixel(sx,r[2]+y)
   if p.rgbaA(c)>0 then for dy=0,5 do for dx=0,5 do out:drawPixel((n-1)*450+20+x*6+dx,(row-1)*230+y*6+dy,c) end end end
  end end
 end
end
local s=Sprite(out.width,out.height,ColorMode.RGB);s.cels[1].image=out;app.activeSprite=s
s:saveAs(base..'work/detail-inspection_v004.png');s:close()

