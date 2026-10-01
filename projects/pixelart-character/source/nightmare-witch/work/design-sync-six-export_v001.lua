local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local items={{'front','v033'},{'side_left','v006'},{'side_right','v004'},{'behind','v005'},{'three-quarter_left','v003'},{'three-quarter_right','v002'}}
for _,q in ipairs(items) do
 local s=app.open(root..'work/'..q[1]..'-design-sync-generated_'..q[2]..'.png')
 app.activeSprite=s
 app.command.SpriteSize{ui=false,width=992,height=992,method='bilinear'}
 local fg=Image(1024,1024,ColorMode.RGB)
 fg:drawImage(s.cels[1].image,Point(16,16))
 s:close()
 local a=Sprite(1024,1024,ColorMode.RGB)
 a.cels[1].image=fg
 a:saveAs(root..'work/'..q[1]..'_'..q[2]..'.aseprite')
 a:saveAs(root..'image-undecided/1024/view/'..q[1]..'_'..q[2]..'.png')
 a:close()
end
for _,bg in ipairs({{'white',245},{'dark',45}}) do
 local board=Sprite(3072,2048,ColorMode.RGB)
 local im=Image(3072,2048,ColorMode.RGB)
 im:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
 for k,q in ipairs(items) do
  local s=app.open(root..'image-undecided/1024/view/'..q[1]..'_'..q[2]..'.png')
  im:drawImage(s.cels[1].image,Point(((k-1)%3)*1024,math.floor((k-1)/3)*1024))
  local single=Image(1024,1024,ColorMode.RGB)
  single:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
  single:drawImage(s.cels[1].image,Point(0,0))
  for _,c in ipairs({{'head',250,0,550,340},{'hands',260,420,530,330},{'boots',290,760,450,264}}) do
   local d=Sprite(c[4]*2,c[5]*2,ColorMode.RGB)
   local crop=Image(c[4],c[5],ColorMode.RGB)
   crop:drawImage(single,Point(-c[2],-c[3]))
   d:close()
   d=Sprite(c[4],c[5],ColorMode.RGB)
   d.cels[1].image=crop
   app.activeSprite=d
   app.command.SpriteSize{ui=false,width=c[4]*2,height=c[5]*2,method='nearest'}
   d:saveAs(root..'work/'..q[1]..'-sync-'..c[1]..'-'..bg[1]..'_'..q[2]..'.png')
   d:close()
  end
  s:close()
 end
 board.cels[1].image=im
 board:saveAs(root..'work/design-sync-six-'..bg[1]..'_v001.png')
 board:close()
end

