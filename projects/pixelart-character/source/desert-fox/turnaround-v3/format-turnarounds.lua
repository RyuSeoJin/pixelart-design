-- CHANGELOG v1.0 · 2026-09-28 — 삼면도 각 시점을 동일 배율의 1024 투명 파일로 저장합니다.
local root=app.fs.joinPath(app.fs.currentPath,'projects/pixelart-character/source/desert-fox/turnaround-v3')
local pc=app.pixelColor
local views={'front','side','back'}
local function formatSet(family, ranges, centers, scale, offsetsY)
  local src=Image{fromFile=root..'/generated-'..family..'.png'}
  assert(src.width==1536 and src.height==1024,'입력 시트 크기 확인 필요')
  local preview=Image(1536,512,ColorMode.RGB)
  preview:clear(pc.rgba(73,80,96,255))
  for i,view in ipairs(views) do
    local dst=Image(1024,1024,ColorMode.RGB)
    -- 동일 배율을 유지하고 정지 삼면도의 접지 행만 맞춥니다. 동작 프레임 보정이 아닙니다.
    for y=0,1023 do
      local sy=math.floor((y-offsetsY[i])/scale)
      if sy>=0 and sy<1024 then
        for x=0,1023 do
          local sx=math.floor((x-512)/scale+centers[i])
          if sx>=ranges[i][1] and sx<ranges[i][2] then
            local c=src:getPixel(sx,sy)
            local a=pc.rgbaA(c)
            if a>0 then
              c=pc.rgba(math.max(10,pc.rgbaR(c)),math.max(10,pc.rgbaG(c)),math.max(10,pc.rgbaB(c)),a)
              dst:drawPixel(x,y,c)
            end
          end
        end
      end
    end
    dst:saveAs(root..'/desert-fox-turnaround-'..family..'-version-'..view..'-1024x1024-v3.png')
    -- 비교판만 배경을 합성합니다. 개별 납품 시안에는 알파를 유지합니다.
    for y=0,511 do for x=0,511 do
      local c=dst:getPixel(x*2,y*2)
      local a=pc.rgbaA(c)/255
      preview:drawPixel((i-1)*512+x,y,pc.rgba(math.floor(pc.rgbaR(c)*a+73*(1-a)),math.floor(pc.rgbaG(c)*a+80*(1-a)),math.floor(pc.rgbaB(c)*a+96*(1-a)),255))
    end end
  end
  preview:saveAs(root..'/desert-fox-turnaround-'..family..'-preview-v3.png')
end
formatSet('front',{{50,570},{580,1030},{1070,1536}},{265,710,1280},0.96,{15,16,15})
formatSet('three-quarter',{{40,530},{560,1030},{1060,1536}},{260,710,1270},0.99,{13,13,13})
