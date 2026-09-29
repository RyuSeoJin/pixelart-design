-- CHANGELOG v1.0 · 2026-09-28 — 승인 원본과 도트 결과의 검수용 비교본입니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/arctic-fox/'
local pc=app.pixelColor
local function read(path) local s=app.open(root..path);local im=Image(s.spec);im:drawSprite(s,1);s:close();return im end
local function canvas(w,h) local s=Sprite(w,h,ColorMode.RGB);local im=s.cels[1].image;for y=0,h-1 do for x=0,w-1 do im:drawPixel(x,y,pc.rgba(220,224,231,255)) end end;return s,im end
local function stamp(dst,src,sx,sy,sw,sh,dx,dy,dw,dh)
 for y=0,dh-1 do for x=0,dw-1 do
 local c=src:getPixel(sx+math.floor(x*sw/dw),sy+math.floor(y*sh/dh))
 if pc.rgbaA(c)>127 then dst:drawPixel(dx+x,dy+y,pc.rgba(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),255)) end
 end end
end
local refs,old,new={},{},{}
for i,side in ipairs({'left','right'}) do refs[i]=read('image-confirmed/1024/view/side_'..side..'_v001.png');old[i]=read('work/side-eye-reference_v001.png');new[i]=read('image-undecided/180/view/side_'..side..'_v001.png') end
local s,dst=canvas(720,520)
for i=1,2 do local y=15+(i-1)*255
 stamp(dst,refs[i],i==1 and 430 or 529,160,65,80,20,y,195,240)
 stamp(dst,old[i],520,220,100,120,260,y,195,234)
 stamp(dst,new[i],i==1 and 78 or 86,31,15,18,500,y,195,234)
end
app.command.SaveFileAs{ui=false,filename=root..'work/side180-face-reference_v001.png'};s:close()
s,dst=canvas(1440,720)
for i=1,2 do local dx=(i-1)*720
 stamp(dst,refs[i],i==1 and 405 or 270,49,420,930,dx+10,20,290,640)
 stamp(dst,new[i],i==1 and 72 or 36,11,74,160,dx+350,20,296,640)
end
app.command.SaveFileAs{ui=false,filename=root..'work/side180-full-reference_v001.png'};s:close()
s,dst=canvas(1160,340)
for i=1,2 do local dx=(i-1)*580
 stamp(dst,refs[i],i==1 and 405 or 430,305,240,290,dx+5,10,240,290)
 stamp(dst,new[i],i==1 and 71 or 77,58,48,48,dx+290,10,288,288)
end
app.command.SaveFileAs{ui=false,filename=root..'work/side180-pattern-reference_v001.png'}
print('COMPARISONS_OK')
