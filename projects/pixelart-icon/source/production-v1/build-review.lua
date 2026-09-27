-- CHANGELOG v1.0 · 2026-09-27 — 전체 66종의 밝은/어두운 배경·실제 출력 크기 비교판
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-icon")
local f=assert(io.open(app.fs.joinPath(root,"spec/design/recordtales-icon-catalog.json"),"r"))
local catalog=json.decode(f:read("*a"));f:close()
local rgba,alpha=app.pixelColor.rgba,app.pixelColor.rgbaA
local font={
 A={"010","101","111","101","101"},B={"110","101","110","101","110"},C={"011","100","100","100","011"},
 D={"110","101","101","101","110"},E={"111","100","110","100","111"},F={"111","100","110","100","100"},
 G={"011","100","101","101","011"},H={"101","101","111","101","101"},I={"111","010","010","010","111"},
 J={"001","001","001","101","010"},K={"101","101","110","101","101"},L={"100","100","100","100","111"},
 M={"101","111","111","101","101"},N={"101","111","111","111","101"},O={"010","101","101","101","010"},
 P={"110","101","110","100","100"},Q={"010","101","101","111","011"},R={"110","101","110","101","101"},
 S={"011","100","010","001","110"},T={"111","010","010","010","010"},U={"101","101","101","101","111"},
 V={"101","101","101","101","010"},W={"101","101","111","111","101"},X={"101","101","010","101","101"},
 Y={"101","101","010","010","010"},Z={"111","001","010","100","111"},["_"]={"000","000","000","000","111"},
 ["0"]={"111","101","101","101","111"},["1"]={"010","110","010","010","111"},["2"]={"110","001","010","100","111"},
 ["3"]={"110","001","010","001","110"},["4"]={"101","101","111","001","001"},["5"]={"111","100","110","001","110"},
 ["6"]={"011","100","110","101","010"},["7"]={"111","001","010","010","010"},["8"]={"010","101","010","101","010"},["9"]={"010","101","011","001","110"}
}
local function text(im,str,x0,y0,c)
 str=str:upper()
 for i=1,#str do local glyph=font[str:sub(i,i)]
  if glyph then for y,row in ipairs(glyph) do for x=1,3 do if row:sub(x,x)=="1" then im:drawPixel(x0+(i-1)*4+x-1,y0+y-1,c) end end end end
 end
end
local function save(im,path) local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(path);s:close() end
local images={}
for _,a in ipairs(catalog.items) do
 local path=app.fs.joinPath(root,"export/"..a.id.."/v1/icon-16.png")
 if app.fs.isFile(path) then local s=app.open(path);local im=Image(16,16,ColorMode.RGB);im:drawSprite(s,1);s:close();images[a.id]=im end
end
local folder=app.fs.joinPath(root,"export/collection-v1");app.fs.makeAllDirectories(folder)
local function board(items,n,light,name)
 local cols=8;local cw=120;local ch=n==4 and 104 or 76
 local out=Image(cols*cw,math.ceil(#items/cols)*ch,ColorMode.RGB)
 local bg=light and rgba(224,225,231,255) or rgba(37,39,52,255)
 local fg=light and rgba(58,62,76,255) or rgba(197,201,217,255)
 out:clear(bg)
 for i,a in ipairs(items) do
  local x0=((i-1)%cols)*cw;local y0=math.floor((i-1)/cols)*ch;local im=images[a.id]
  if im then
   local ox=x0+math.floor((cw-16*n)/2);local oy=y0+8
   for y=0,16*n-1 do for x=0,16*n-1 do local c=im:getPixel(math.floor(x/n),math.floor(y/n))
    if alpha(c)>0 then
     if light and a.color_mode=="white_tint" then c=fg end
     out:drawPixel(ox+x,oy+y,c)
    end
   end end
  end
  text(out,string.format("%02d",i),x0+55,y0+ch-23,fg)
  text(out,a.id,x0+math.floor((cw-(#a.id*4-1))/2),y0+ch-12,fg)
 end
 save(out,app.fs.joinPath(folder,name))
end
board(catalog.items,4,false,"all-64-dark.png")
board(catalog.items,4,true,"all-64-light.png")
board(catalog.items,2,false,"all-32-dark.png")
board(catalog.items,1,false,"all-16-dark.png")
-- 계열별 비교판은 한 행에 실제 16·32·48·64 출력 크기를 나란히 배치합니다.
for _,group in ipairs({"menu","symbol","category","ticket","emotion","order","action"}) do
 local items={};for _,a in ipairs(catalog.items) do if a.group==group then items[#items+1]=a end end
 local out=Image(480,#items*80,ColorMode.RGB);out:clear(rgba(37,39,52,255))
 for i,a in ipairs(items) do
  text(out,a.id,12,(i-1)*80+36,rgba(220,221,230,255))
  local im=images[a.id]
  if im then for n=1,4 do
   local ox=144+(n-1)*80+math.floor((80-16*n)/2);local oy=(i-1)*80+math.floor((80-16*n)/2)
   for y=0,16*n-1 do for x=0,16*n-1 do local c=im:getPixel(math.floor(x/n),math.floor(y/n));if alpha(c)>0 then out:drawPixel(ox+x,oy+y,c) end end end
  end end
 end
 save(out,app.fs.joinPath(folder,group.."-scales.png"))
end
print("전체·계열별 검토 비교판 생성 완료")
