-- CHANGELOG v1.0 · 2026-09-27 — 생성 시안의 16px 정리와 최근접 정수배 출력·비교판 생성
-- 실행 위치: 저장소 루트. 픽셀 정리는 Aseprite에서 수행하며 생성 원본은 보존합니다.
local root = app.fs.joinPath(app.fs.currentPath, "projects/pixelart-icon")
local source = app.fs.joinPath(root, "source/representatives-v1")
local ids = {"cmd_settings","sym_close","icon_book","tpl_idea","order_restaurant","act_cook"}
local palettes = {
 cmd_settings={"FFFFFF"}, sym_close={"FFFFFF"},
 icon_book={"172644","244B87","326CC2","69A9F3","FFF0CD","DBC89E","F4C44B","B77B28"},
 tpl_idea={"342747","F3AA27","FFD34C","FFF0AD","B97725","556276","8B9BB0","D0DCE6"},
 order_restaurant={"342747","FFF0CD","D4C5AB","F8CD49","E99B25","B9661C","477735","79A343"},
 act_cook={"342747","384352","546378","8B9BB0","BCCAD3","FFF0CD"}
}
local rgba = app.pixelColor.rgba
local red,green,blue,alpha = app.pixelColor.rgbaR,app.pixelColor.rgbaG,app.pixelColor.rgbaB,app.pixelColor.rgbaA
local function color(h) return rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255) end
local function nearest(c,pal)
 local best,dist=pal[1],math.huge
 for _,v in ipairs(pal) do
  local d=(red(c)-red(v))^2+(green(c)-green(v))^2+(blue(c)-blue(v))^2
  if d<dist then best,dist=v,d end
 end
 return best
end
local function scale(im,n)
 local out=Image(16*n,16*n,ColorMode.RGB)
 for y=0,out.height-1 do for x=0,out.width-1 do out:drawPixel(x,y,im:getPixel(math.floor(x/n),math.floor(y/n))) end end
 return out
end
local function save(im,path)
 local s=Sprite(im.width,im.height,ColorMode.RGB)
 s.cels[1].image=im
 s:saveAs(path)
 s:close()
end
local natives={}
local report={revision="1.0",method="Aseprite에서 알파 범위의 블록별 색상 투표·팔레트 정리 후 16px 원본 생성; 출력은 최근접 정수배",assets={}}
app.fs.makeAllDirectories(app.fs.joinPath(root,"sprites/representatives-v1"))
for _,id in ipairs(ids) do
 local s=app.open(app.fs.joinPath(source,id.."-concept.png"))
 assert(s and s.colorMode==ColorMode.RGB)
 local raw=Image(s.width,s.height,ColorMode.RGB);raw:drawSprite(s,1)
 local minx,miny,maxx,maxy=raw.width,raw.height,-1,-1
 -- 아주 약한 배경 제거 흔적은 내용 경계로 잡지 않습니다.
 for y=0,raw.height-1 do for x=0,raw.width-1 do
  if alpha(raw:getPixel(x,y))>=240 then minx=math.min(minx,x);maxx=math.max(maxx,x);miny=math.min(miny,y);maxy=math.max(maxy,y) end
 end end
 assert(maxx>=minx)
 local w,h=maxx-minx+1,maxy-miny+1
 local dw=math.max(1,math.floor(14*w/math.max(w,h)+0.5));local dh=math.max(1,math.floor(14*h/math.max(w,h)+0.5))
 local ox,oy=math.floor((16-dw)/2),math.floor((16-dh)/2)
 local native=Image(16,16,ColorMode.RGB);local pal={}
 for _,v in ipairs(palettes[id]) do pal[#pal+1]=color(v) end
 for y=0,dh-1 do for x=0,dw-1 do
  local votes,coverage={},0
  for sy=0,6 do for sx=0,6 do
   local rx=math.min(maxx,math.floor(minx+(x+(sx+0.5)/7)*w/dw))
   local ry=math.min(maxy,math.floor(miny+(y+(sy+0.5)/7)*h/dh))
   local c=raw:getPixel(rx,ry)
   if alpha(c)>=128 then coverage=coverage+1;local q=nearest(c,pal);votes[q]=(votes[q] or 0)+1 end
  end end
  if coverage>=25 then
   local best,n=pal[1],-1
   for _,q in ipairs(pal) do if (votes[q] or 0)>n then best,n=q,votes[q] or 0 end end
   native:drawPixel(ox+x,oy+y,best)
  end
 end end
 s:close()
 natives[#natives+1]=native
 local folder=app.fs.joinPath(root,"export/"..id.."/v1");app.fs.makeAllDirectories(folder)
 save(native,app.fs.joinPath(root,"sprites/representatives-v1/"..id..".aseprite"))
 save(native,app.fs.joinPath(source,id.."-native-16.png"))
 for n=1,4 do save(scale(native,n),app.fs.joinPath(folder,"icon-"..(16*n)..".png")) end
 report.assets[#report.assets+1]={id=id,source_size={raw.width,raw.height},source_bounds={minx,miny,w,h},native_content_area={ox,oy,dw,dh},palette=palettes[id]}
end
-- 비교판 위 두 줄은 6배 표시, 아래 네 줄은 16·32·48·64px 실제 크기입니다.
local board=Image(768,512,ColorMode.RGB)
for y=0,511 do for x=0,767 do
 local light=y>=128 and y<256
 local bg=light and rgba(224,225,231,255) or rgba(37,39,52,255)
 board:drawPixel(x,y,bg)
end end
local function put(im,x0,y0,tint)
 for y=0,im.height-1 do for x=0,im.width-1 do local c=im:getPixel(x,y);if alpha(c)>0 then board:drawPixel(x0+x,y0+y,tint or c) end end end
end
for i,im in ipairs(natives) do
 local left=(i-1)*128
 put(scale(im,6),left+16,16,i<=2 and rgba(236,193,100,255) or nil)
 put(scale(im,6),left+16,144,i<=2 and rgba(58,62,76,255) or nil)
 for n=1,4 do put(scale(im,n),left+math.floor((128-16*n)/2),256+(n-1)*64+math.floor((64-16*n)/2),nil) end
end
app.fs.makeAllDirectories(app.fs.joinPath(root,"export/representatives-v1"))
save(board,app.fs.joinPath(root,"export/representatives-v1/comparison.png"))
local f=io.open(app.fs.joinPath(source,"build-report.json"),"w");f:write(json.encode(report));f:close()
print("대표 6종 16px 원본·24개 출력·비교판 생성 완료")
