local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local items={
{'front','031',299,18,425,921,519},
{'side_left','005',372,33,345,915,518},
{'side_right','003',351,34,343,925,566},
{'behind','004',305,44,430,920,518},
{'three-quarter_left','002',362,30,400,961,502},
{'three-quarter_right','001',292,26,420,964,588},
}
for _,bg in ipairs({{'white',245},{'dark',45}}) do
 local sheet=Image(2400,2080,ColorMode.RGB)
 sheet:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
 local boots=Image(2400,480,ColorMode.RGB)
 boots:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
 for i,q in ipairs(items) do
  local src=app.open(root..'image-undecided/1024/view/'..q[1]..'_v'..q[2]..'.png')
  local fg=src.cels[1].image
  local crop=Sprite(q[5],q[6],ColorMode.RGB)
  local im=Image(q[5],q[6],ColorMode.RGB)
  im:drawImage(fg,Point(-q[3],-q[4]))
  crop.cels[1].image=im
  app.activeSprite=crop
  app.command.SpriteSize{ui=false,width=math.floor(q[5]*950/q[6]),height=950,method='bilinear'}
  sheet:drawImage(crop.cels[1].image,Point((i-1)%3*800+math.floor((800-crop.width)/2),math.floor((i-1)/3)*1040+40))
  crop:close()
  local b=Sprite(400,240,ColorMode.RGB)
  local bi=Image(400,240,ColorMode.RGB)
  bi:drawImage(fg,Point(-(q[7]-200),-770))
  b.cels[1].image=bi
  boots:drawImage(bi,Point((i-1)*400,120))
  b:close()
  src:close()
 end
 local out=Sprite(2400,2080,ColorMode.RGB)
 out.cels[1].image=sheet
 out:saveAs(root..'work/boots-six-views-'..bg[1]..'_v001.png')
 out:close()
 local z=Sprite(2400,480,ColorMode.RGB)
 z.cels[1].image=boots
 z:saveAs(root..'work/boots-six-details-'..bg[1]..'_v001.png')
 z:close()
end
