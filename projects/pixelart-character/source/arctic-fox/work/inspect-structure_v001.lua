local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
local paths={'image-confirmed/180/view/side_left_v010.png','image-undecided/180/anim-walk/left/frame-05_v005.png','image-undecided/180/anim-idle/left/frame-02_v005.png'}
local out=Image(1152,576,ColorMode.RGB)
for n,path in ipairs(paths) do
 local s=app.open(root..path);local im=Image(s.spec);im:drawSprite(s,1);s:close()
 for y=0,95 do for x=0,63 do local c=im:getPixel(74+x,78+y)
  for yy=0,5 do for xx=0,5 do out:drawPixel((n-1)*384+x*6+xx,y*6+yy,c) end end
 end end
end
local s=Sprite(1152,576,ColorMode.RGB);s.cels[1].image=out;app.activeSprite=s;s:saveAs(root..'work/inspect-structure_v001.png');s:close()
