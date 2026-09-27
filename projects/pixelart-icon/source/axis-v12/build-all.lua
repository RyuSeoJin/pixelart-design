-- CHANGELOG v1.0 · 2026-09-27 — 공통 UI v4 실제 크기와 현재 전체 비교판
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
local folder=app.fs.joinPath(root,"export/collection-v12")
local function load(a,size)
 local s=assert(app.open(app.fs.joinPath(root,a.output_directory.."/icon-"..size..".png")))
 local im=Image(size,size,ColorMode.RGB);im:drawSprite(s,1);s:close();return im
end
local function put(board,im,x0,y0)
 for y=0,im.height-1 do for x=0,im.width-1 do local c=im:getPixel(x,y);if alpha(c)>0 then board:drawPixel(x0+x,y0+y,c) end end end
end
for _,light in ipairs({false,true}) do
 local bg=light and rgba(224,225,231,255) or rgba(37,39,52,255)
 local fg=light and rgba(58,62,76,255) or rgba(220,222,231,255)
 local all=Image(960,936,ColorMode.RGB);all:clear(bg)
 for i,a in ipairs(catalog.items) do
  local x=((i-1)%8)*120;local y=math.floor((i-1)/8)*104
  put(all,load(a,64),x+28,y+8)
  text(all,a.id,x+math.floor((120-#a.id*4)/2),y+92,fg)
 end
 save(all,app.fs.joinPath(folder,light and "all-64-light.png" or "all-64-dark.png"))
end
