
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local work=root..'source/arctic-fox/work/'
local out=root..'source/arctic-fox/image-undecided/180/view/'
local pc=app.pixelColor;local images={}
for i,side in ipairs({'left','right'}) do
 local s=app.open(out..'side_'..side..'_v002.png');local im=Image(s.spec);im:drawSprite(s,1);images[i]=im;s:close()
end
local function bg(w,h)
 local s=Sprite(w,h,ColorMode.RGB);local im=s.cels[1].image
 for y=0,h-1 do for x=0,w-1 do local v=(math.floor(x/16)+math.floor(y/16))%2==0 and 232 or 245;im:drawPixel(x,y,pc.rgba(v,v,v,255)) end end
 return s,im
end
local function blit(im,src,ox,oy,k)
 for y=0,src.height-1 do for x=0,src.width-1 do local c=src:getPixel(x,y)
 if pc.rgbaA(c)>0 then for dy=0,k-1 do for dx=0,k-1 do im:drawPixel(ox+x*k+dx,oy+y*k+dy,c) end end end
 end end
end
local s,im=bg(1080,540)
blit(im,images[1],0,0,3);blit(im,images[2],540,0,3)
app.command.SaveFileAs{ui=false,filename=work..'side180-comparison_v002.png'};s:close()
local s,im=bg(720,720)
for y=0,179 do for x=0,179 do
 local a=pc.rgbaA(images[1]:getPixel(x,y))>0;local b=pc.rgbaA(images[2]:getPixel(179-x,y))>0
 if a or b then local c=a and b and pc.rgba(70,87,108,255) or a and pc.rgba(230,90,70,255) or pc.rgba(40,160,210,255)
 for dy=0,3 do for dx=0,3 do im:drawPixel(x*4+dx,y*4+dy,c) end end end
end end
app.command.SaveFileAs{ui=false,filename=work..'side180-overlay_v002.png'};s:close()
local s,im=bg(1080,540)
blit(im,images[1],0,0,3);blit(im,images[2],540,0,3)
for _,y in ipairs({29,43,53,60,83,100,133,164,170}) do
 for x=0,1079 do if x%6<3 then im:drawPixel(x,y*3,pc.rgba(190,100,90,255)) end end
end
for _,x in ipairs({270,810}) do for y=0,539 do if y%6<3 then im:drawPixel(x,y,pc.rgba(90,160,200,255)) end end end
app.command.SaveFileAs{ui=false,filename=work..'side180-guides_v002.png'};s:close()
local s=Sprite(180,180,ColorMode.RGB);s.cels[1].image=images[1];s.frames[1].duration=0.6
s:newFrame();s.cels[#s.cels].image=images[2];s.frames[2].duration=0.6
app.command.SaveFileAs{ui=false,filename=work..'side180-direction-toggle_v002.gif'};s:close()
-- 선택 눈빛과 양쪽 결과를 같은 논리 격자의 최근접 확대에서 비교합니다.
local s,im=bg(720,320)
for i,sp in ipairs(images) do
 local crop=Image(40,40,ColorMode.RGB)
 for y=0,39 do for x=0,39 do crop:drawPixel(x,y,sp:getPixel(70+x,20+y)) end end
 blit(im,crop,(i-1)*360,0,8)
end
app.command.SaveFileAs{ui=false,filename=work..'side180-face_v002.png'};s:close()
print('COMPARISONS_SAVED')
