
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local work=root..'source/arctic-fox/work/'
local pc=app.pixelColor
local s=Sprite(1440,540,ColorMode.RGB);local dst=s.cels[1].image
for y=0,539 do for x=0,1439 do local v=(math.floor(x/18)+math.floor(y/18))%2==0 and 232 or 245;dst:drawPixel(x,y,pc.rgba(v,v,v,255)) end end
for i,side in ipairs({'left','right'}) do
 local ref=app.open(root..'source/arctic-fox/image-confirmed/1024/view/side_'..side..'_v001.png')
 local raw=Image(ref.spec);raw:drawSprite(ref,1)
 local px=app.open(root..'source/arctic-fox/image-undecided/180/view/side_'..side..'_v002.png')
 local pix=Image(px.spec);pix:drawSprite(px,1)
 for y=0,179 do for x=0,179 do
  local sx=math.floor(520+(x-90)/(142/856));local sy=math.floor(117+(y-29)/(142/856))
  local r=0;if sx>=0 and sx<raw.width and sy>=0 and sy<raw.height then r=raw:getPixel(sx,sy) end
  local a=pix:getPixel(x,y)
  for dy=0,2 do for dx=0,2 do
   -- 비교 칸은 캐릭터 중심을 기준으로 좁히며 배율은 동일합니다.
   local xx=(i-1)*720+(x-30)*3+dx
   if xx>=(i-1)*720 and xx<(i-1)*720+360 and pc.rgbaA(r)>200 then dst:drawPixel(xx,y*3+dy,r) end
   local xx2=(i-1)*720+360+(x-30)*3+dx
   if xx2>=(i-1)*720+360 and xx2<i*720 and pc.rgbaA(a)>0 then dst:drawPixel(xx2,y*3+dy,a) end
  end end
 end end
 ref:close();px:close()
end
app.activeSprite=s;app.command.SaveFileAs{ui=false,filename=work..'side180-approved-reference_v002.png'};s:close()
print('REFERENCE_COMPARISON_SAVED')
