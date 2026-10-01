local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local g=app.open(root..'work/lower-body-generated_v001.png')
app.activeSprite=g
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
local patch=Image(g.cels[1].image)
g:close()
local s=app.open(root..'image-undecided/1024/view/front_v029.png')
app.activeSprite=s
local out=Image(s.cels[1].image)
local pc=app.pixelColor
local function coat(c) return pc.rgbaA(c)>32 and pc.rgbaB(c)>pc.rgbaG(c)*1.18 and pc.rgbaR(c)>pc.rgbaG(c)*1.3 end
for y=475,1023 do
 for x=397,633 do
  local a=out:getPixel(x,y)
  local b=patch:getPixel(x,y)
  if not (coat(a) and coat(b)) then
   if pc.rgbaA(b)<=32 then b=0 end
   if y<489 and pc.rgbaA(a)>32 and pc.rgbaA(b)>32 then
    local t=(y-475)/14
    local function mix(v,w) return math.floor(v*(1-t)+w*t+0.5) end
    b=pc.rgba(mix(pc.rgbaR(a),pc.rgbaR(b)),mix(pc.rgbaG(a),pc.rgbaG(b)),mix(pc.rgbaB(a),pc.rgbaB(b)),pc.rgbaA(a))
   end
   out:drawPixel(x,y,b)
  end
 end
end
s.cels[1].image=out
s:saveAs(root..'work/lower-body_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v030.png')
app.command.CanvasSize{ui=false,left=-390,right=-384,top=-470,bottom=0}
app.command.SpriteSize{ui=false,width=500,height=1108,method='nearest-neighbor'}
s:saveAs(root..'work/lower-body-detail_v001.png')
s:close()
