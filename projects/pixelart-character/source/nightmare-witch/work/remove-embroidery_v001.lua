local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local g=app.open(root..'work/remove-embroidery-generated_v001.png')
app.activeSprite=g
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
local patch=Image(g.cels[1].image)
g:close()
local s=app.open(root..'image-undecided/1024/view/front_v028.png')
app.activeSprite=s
local out=Image(s.cels[1].image)
local pc=app.pixelColor
for _,r in ipairs({{389,312,425,342},{615,583,665,623}}) do
 for y=r[2],r[4] do
  for x=r[1],r[3] do
   local a=out:getPixel(x,y)
   local b=patch:getPixel(x,y)
   local t=math.min(1,(x-r[1])/4,(r[3]-x)/4,(y-r[2])/4,(r[4]-y)/4)
   local function mix(v,w) return math.floor(v*(1-t)+w*t+0.5) end
   out:drawPixel(x,y,pc.rgba(mix(pc.rgbaR(a),pc.rgbaR(b)),mix(pc.rgbaG(a),pc.rgbaG(b)),mix(pc.rgbaB(a),pc.rgbaB(b)),pc.rgbaA(a)))
  end
 end
end
s.cels[1].image=out
s:saveAs(root..'work/remove-embroidery_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v029.png')
s:close()

