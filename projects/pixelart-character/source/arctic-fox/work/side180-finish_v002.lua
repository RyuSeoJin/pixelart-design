
local root='P:/github-repository/pixelart-design/projects/pixelart-character/'
local out=root..'source/arctic-fox/image-undecided/180/view/'
local pc=app.pixelColor
local function c(h) return pc.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255) end
for i,side in ipairs({'left','right'}) do
 local s=app.open(root..'sprites/arctic-fox/side_'..side..'_v002.aseprite');local im=s.cels[1].image
 local function dot(x,y,h) if i==2 then x=179-x end;im:drawPixel(x,y,c(h)) end
 -- 눈 중심 행을 공통 사양 43으로 맞춥니다.
 for x=81,84 do dot(x,41,'221A26') end
 dot(81,42,'F6D2BC');dot(84,42,'F4F7FA')
 dot(82,42,'2A4F80');dot(83,42,'3E8FB8')
 dot(82,43,'3E8FB8');dot(83,43,'7FD0E0')
 dot(82,44,'7FD0E0');dot(83,44,'7FD0E0')
 dot(82,45,'F6D2BC');dot(83,45,'F6D2BC')
 if i==2 then
  -- 윤곽 대응 중 꼬리/부츠 색이 바지로 흘러든 부분을 바지 재질로 복원합니다.
  for y=111,143 do for x=82,98 do
   local col=im:getPixel(x,y)
   if col==c('F4F7FA') or col==c('C3CCD8') then im:drawPixel(x,y,c('8C97AD')) end
  end end
 end
 s:saveAs(root..'sprites/arctic-fox/side_'..side..'_v002.aseprite')
 app.command.SaveFileAs{ui=false,filename=out..'side_'..side..'_v002.png'};s:close()
end
print('NATIVE_FIX_DONE')
