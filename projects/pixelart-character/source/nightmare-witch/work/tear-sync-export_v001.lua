local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local items={{'front','v034'},{'side_left','v007'},{'side_right','v005'},{'behind','v006'},{'three-quarter_left','v004'},{'three-quarter_right','v003'}}
for _,q in ipairs(items) do
 local s=app.open(root..'work/'..q[1]..'-tear-generated_'..q[2]..'.png')
 app.activeSprite=s
 app.command.SpriteSize{ui=false,width=992,height=992,method='bilinear'}
 local fg=Image(1024,1024,ColorMode.RGB)
 fg:drawImage(s.cels[1].image,Point(16,16))
 s:close()
 local a=Sprite(1024,1024,ColorMode.RGB)
 a.cels[1].image=fg
 a:saveAs(root..'work/'..q[1]..'-tear_'..q[2]..'.aseprite')
 a:saveAs(root..'image-undecided/1024/view/'..q[1]..'_'..q[2]..'.png')
 a:close()
end
for _,bg in ipairs({{'white',245},{'dark',45}}) do
 local board=Sprite(3072,2048,ColorMode.RGB)
 local im=Image(3072,2048,ColorMode.RGB)
 im:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
 local detail=Sprite(2400,1500,ColorMode.RGB)
 local di=Image(2400,1500,ColorMode.RGB)
 di:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
 for k,q in ipairs(items) do
  local s=app.open(root..'image-undecided/1024/view/'..q[1]..'_'..q[2]..'.png')
  im:drawImage(s.cels[1].image,Point(((k-1)%3)*1024,math.floor((k-1)/3)*1024))
  local crop=Image(650,610,ColorMode.RGB)
  crop:clear(app.pixelColor.rgba(bg[2],bg[2],bg[2],255))
  crop:drawImage(s.cels[1].image,Point(-220,-15))
  di:drawImage(crop,Point(((k-1)%3)*800+75,math.floor((k-1)/3)*750+40))
  s:close()
 end
 board.cels[1].image=im
 board:saveAs(root..'work/tear-sync-six-'..bg[1]..'_v001.png')
 board:close()
 detail.cels[1].image=di
 detail:saveAs(root..'work/tear-sync-detail-'..bg[1]..'_v001.png')
 detail:close()
end
print('6개 전신과 두 배경 비교표 저장 완료')

