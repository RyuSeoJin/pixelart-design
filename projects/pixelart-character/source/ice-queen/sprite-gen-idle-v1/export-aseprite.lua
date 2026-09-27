-- CHANGELOG v1.0 · 2026-09-28 — 검토용 idle 6프레임 편집 원본
local root=app.fs.joinPath(app.fs.currentPath,"projects/pixelart-character")
local s=Sprite(320,320,ColorMode.RGB)
s.layers[1].name="idle_trial_composite"
for i=0,5 do
 if i>0 then s:newEmptyFrame() end
 local im=Image{fromFile=root.."/export/ice-queen/sprite-gen-idle-v1/frames-320/"..string.format("%02d",i)..".png"}
 s:newCel(s.layers[1],i+1,im,Point(0,0));s.frames[i+1].duration=0.25
end
local tag=s:newTag(1,6);tag.name="idle_trial"
s:saveAs(root.."/sprites/ice-queen-idle-sprite-gen-v1.aseprite");s:close()
