-- CHANGELOG v1.0 · 2026-10-08 — 94개 독립 레이어를 편집 원본으로 저장하고 다시 추출합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-background/source/landscape-v015/'
local pkg=root..'unreal-full/';local assets=dofile(root..'assets.lua')
local function save(im,path)local s=Sprite(im.width,im.height,ColorMode.RGB);s.cels[1].image=im;s:saveAs(path);s:close() end
local groups={{'forest',1920,894},{'snow',1920,894},{'forest_ground',120,30},{'snow_ground',120,30},{'celestial_fx',160,64}}
for _,group in ipairs(groups) do
 local s=Sprite(group[2],group[3],ColorMode.RGB);local first=true;local used={}
 for _,a in ipairs(assets) do
  local target=a.region=='shared' and 'celestial_fx' or (a.region..(a.layer=='street_tile' and '_ground' or ''))
  if target==group[1] then
   local im=Image{fromFile=pkg..a.file};local y=0
   if target=='forest' or target=='snow' then y=(a.layer=='sky' or a.layer=='clouds_high' or a.layer:match('stars_')) and 0 or 624 end
   local layer
   if first then layer=s.layers[1];s.cels[1].image=im;s.cels[1].position=Point(0,y);first=false
   else layer=s:newLayer();s:newCel(layer,1,im,Point(0,y)) end
   layer.name=a.name;layer.isVisible=a.phase=='day' or a.name=='T_Sun';used[a.name]={w=im.width,h=im.height,y=y,file=a.file}
  end
 end
 s:saveAs(pkg..'Source/'..group[1]..'.aseprite');s:close()
 local reopened=app.open(pkg..'Source/'..group[1]..'.aseprite')
 for _,layer in ipairs(reopened.layers) do
  local a=used[layer.name];local im=Image(a.w,a.h,ColorMode.RGB);local cel=layer:cel(1)
  im:drawImage(cel.image,Point(cel.position.x,cel.position.y-a.y))
  save(im,pkg..'checks/'..layer.name..'.png')
 end
 reopened:close();collectgarbage('collect')
end
-- 생성 에셋은 8배 최근접 확대판을 함께 보관합니다.
local board=Image(1536,512,ColorMode.RGB)
local positions={Sun={16,16},Moon={432,16},Meteor={16,420},MeteorBig={240,240},MeteorGlow={960,0},MeteorSpark={0,300}}
for _,a in ipairs(assets) do if a.region=='shared' then
 local src=Image{fromFile=pkg..a.file};local pos=positions[a.name:gsub('T_','')];local factor=a.name=='T_MeteorBig' and 4 or (a.name=='T_MeteorGlow' and 4 or 6)
 local im=Image(src.width*factor,src.height*factor,ColorMode.RGB)
 for y=0,im.height-1 do for x=0,im.width-1 do im:drawPixel(x,y,src:getPixel(x//factor,y//factor)) end end
 board:drawImage(im,Point(pos[1],pos[2]))
end end
save(board,pkg..'Preview/celestial_fx_assets.png')
print('Aseprite5개·원본 왕복PNG94개 저장 완료')
