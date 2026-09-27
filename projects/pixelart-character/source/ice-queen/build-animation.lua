-- CHANGELOG v1.0 · 2026-09-27 — 얼음여왕 애니메이션 원본 조립
local s=Sprite(160,160,ColorMode.RGB)
local initial=s.layers[1]
for i=2,12 do s:newEmptyFrame() end
local l=s:newLayer(); l.name="tail"
s:newCel(l,1,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/00-tail.png"},Point(0,0))
s:newCel(l,2,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/01-tail.png"},Point(0,0))
s:newCel(l,3,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/02-tail.png"},Point(0,0))
s:newCel(l,4,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/03-tail.png"},Point(0,0))
s:newCel(l,5,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/04-tail.png"},Point(0,0))
s:newCel(l,6,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/05-tail.png"},Point(0,0))
s:newCel(l,7,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/06-tail.png"},Point(0,0))
s:newCel(l,8,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/07-tail.png"},Point(0,0))
s:newCel(l,9,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/08-tail.png"},Point(0,0))
s:newCel(l,10,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/09-tail.png"},Point(0,0))
s:newCel(l,11,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/10-tail.png"},Point(0,0))
s:newCel(l,12,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/11-tail.png"},Point(0,0))
local l=s:newLayer(); l.name="thigh_L"
s:newCel(l,1,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/00-thigh_L.png"},Point(0,0))
s:newCel(l,2,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/01-thigh_L.png"},Point(0,0))
s:newCel(l,3,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/02-thigh_L.png"},Point(0,0))
s:newCel(l,4,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/03-thigh_L.png"},Point(0,0))
s:newCel(l,5,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/04-thigh_L.png"},Point(0,0))
s:newCel(l,6,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/05-thigh_L.png"},Point(0,0))
s:newCel(l,7,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/06-thigh_L.png"},Point(0,0))
s:newCel(l,8,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/07-thigh_L.png"},Point(0,0))
s:newCel(l,9,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/08-thigh_L.png"},Point(0,0))
s:newCel(l,10,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/09-thigh_L.png"},Point(0,0))
s:newCel(l,11,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/10-thigh_L.png"},Point(0,0))
s:newCel(l,12,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/11-thigh_L.png"},Point(0,0))
local l=s:newLayer(); l.name="thigh_R"
s:newCel(l,1,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/00-thigh_R.png"},Point(0,0))
s:newCel(l,2,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/01-thigh_R.png"},Point(0,0))
s:newCel(l,3,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/02-thigh_R.png"},Point(0,0))
s:newCel(l,4,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/03-thigh_R.png"},Point(0,0))
s:newCel(l,5,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/04-thigh_R.png"},Point(0,0))
s:newCel(l,6,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/05-thigh_R.png"},Point(0,0))
s:newCel(l,7,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/06-thigh_R.png"},Point(0,0))
s:newCel(l,8,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/07-thigh_R.png"},Point(0,0))
s:newCel(l,9,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/08-thigh_R.png"},Point(0,0))
s:newCel(l,10,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/09-thigh_R.png"},Point(0,0))
s:newCel(l,11,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/10-thigh_R.png"},Point(0,0))
s:newCel(l,12,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/11-thigh_R.png"},Point(0,0))
local l=s:newLayer(); l.name="torso"
s:newCel(l,1,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/00-torso.png"},Point(0,0))
s:newCel(l,2,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/01-torso.png"},Point(0,0))
s:newCel(l,3,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/02-torso.png"},Point(0,0))
s:newCel(l,4,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/03-torso.png"},Point(0,0))
s:newCel(l,5,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/04-torso.png"},Point(0,0))
s:newCel(l,6,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/05-torso.png"},Point(0,0))
s:newCel(l,7,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/06-torso.png"},Point(0,0))
s:newCel(l,8,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/07-torso.png"},Point(0,0))
s:newCel(l,9,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/08-torso.png"},Point(0,0))
s:newCel(l,10,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/09-torso.png"},Point(0,0))
s:newCel(l,11,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/10-torso.png"},Point(0,0))
s:newCel(l,12,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/11-torso.png"},Point(0,0))
local l=s:newLayer(); l.name="head"
s:newCel(l,1,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/00-head.png"},Point(0,0))
s:newCel(l,2,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/01-head.png"},Point(0,0))
s:newCel(l,3,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/02-head.png"},Point(0,0))
s:newCel(l,4,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/03-head.png"},Point(0,0))
s:newCel(l,5,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/04-head.png"},Point(0,0))
s:newCel(l,6,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/05-head.png"},Point(0,0))
s:newCel(l,7,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/06-head.png"},Point(0,0))
s:newCel(l,8,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/07-head.png"},Point(0,0))
s:newCel(l,9,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/08-head.png"},Point(0,0))
s:newCel(l,10,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/09-head.png"},Point(0,0))
s:newCel(l,11,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/10-head.png"},Point(0,0))
s:newCel(l,12,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/11-head.png"},Point(0,0))
local l=s:newLayer(); l.name="upperarm_L"
s:newCel(l,1,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/00-upperarm_L.png"},Point(0,0))
s:newCel(l,2,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/01-upperarm_L.png"},Point(0,0))
s:newCel(l,3,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/02-upperarm_L.png"},Point(0,0))
s:newCel(l,4,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/03-upperarm_L.png"},Point(0,0))
s:newCel(l,5,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/04-upperarm_L.png"},Point(0,0))
s:newCel(l,6,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/05-upperarm_L.png"},Point(0,0))
s:newCel(l,7,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/06-upperarm_L.png"},Point(0,0))
s:newCel(l,8,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/07-upperarm_L.png"},Point(0,0))
s:newCel(l,9,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/08-upperarm_L.png"},Point(0,0))
s:newCel(l,10,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/09-upperarm_L.png"},Point(0,0))
s:newCel(l,11,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/10-upperarm_L.png"},Point(0,0))
s:newCel(l,12,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/11-upperarm_L.png"},Point(0,0))
local l=s:newLayer(); l.name="upperarm_R"
s:newCel(l,1,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/00-upperarm_R.png"},Point(0,0))
s:newCel(l,2,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/01-upperarm_R.png"},Point(0,0))
s:newCel(l,3,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/02-upperarm_R.png"},Point(0,0))
s:newCel(l,4,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/03-upperarm_R.png"},Point(0,0))
s:newCel(l,5,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/04-upperarm_R.png"},Point(0,0))
s:newCel(l,6,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/05-upperarm_R.png"},Point(0,0))
s:newCel(l,7,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/06-upperarm_R.png"},Point(0,0))
s:newCel(l,8,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/07-upperarm_R.png"},Point(0,0))
s:newCel(l,9,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/08-upperarm_R.png"},Point(0,0))
s:newCel(l,10,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/09-upperarm_R.png"},Point(0,0))
s:newCel(l,11,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/10-upperarm_R.png"},Point(0,0))
s:newCel(l,12,Image{fromFile="P:/github-repository/pixelart-design/projects/pixelart-character/source/ice-queen/animation-layers/11-upperarm_R.png"},Point(0,0))
s:deleteLayer(initial)
s.frames[1].duration=0.26
s.frames[2].duration=0.2
s.frames[3].duration=0.26
s.frames[4].duration=0.2
s.frames[5].duration=0.1
s.frames[6].duration=0.1
s.frames[7].duration=0.1
s.frames[8].duration=0.1
s.frames[9].duration=0.1
s.frames[10].duration=0.1
s.frames[11].duration=0.1
s.frames[12].duration=0.1
local idle=s:newTag(1,4); idle.name="idle"
local walk=s:newTag(5,12); walk.name="walk"
s:saveAs("P:/github-repository/pixelart-design/projects/pixelart-character/sprites/ice-queen-v1.aseprite")
print("완료: 12프레임, 7레이어")