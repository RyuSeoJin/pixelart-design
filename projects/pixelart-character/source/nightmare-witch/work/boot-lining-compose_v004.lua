local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local g=app.open(root..'work/boot-lining-selected_v001.png')
app.activeSprite=g
app.command.SpriteSize{ui=false,width=240,height=240,method='bilinear'}
local patch=Image(g.cels[1].image)
g:close()
local s=app.open(root..'image-confirmed/1024/view/front.png')
app.activeSprite=s
local out=Image(s.cels[1].image)
local pc=app.pixelColor
for y=38,76 do
 for x=44,201 do
  if x<=115 or x>=132 then
   local a=out:getPixel(x+400,y+784)
   local b=patch:getPixel(x,y)
   local t=math.min(1,(y-37)/4,(77-y)/5)
   if pc.rgbaA(a)>32 and pc.rgbaA(b)>32 then
    local function mix(v,w) return math.floor(v*(1-t)+w*t+0.5) end
    out:drawPixel(x+400,y+784,pc.rgba(mix(pc.rgbaR(a),pc.rgbaR(b)),mix(pc.rgbaG(a),pc.rgbaG(b)),mix(pc.rgbaB(a),pc.rgbaB(b)),pc.rgbaA(a)))
   end
  end
 end
end
s.cels[1].image=out
s:saveAs(root..'work/boot-lining_v004.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v028.png')
app.command.CanvasSize{ui=false,left=-400,right=-384,top=-784,bottom=0}
app.command.SpriteSize{ui=false,width=720,height=720,method='nearest-neighbor'}
s:saveAs(root..'work/boot-lining-detail_v004.png')
s:close()
