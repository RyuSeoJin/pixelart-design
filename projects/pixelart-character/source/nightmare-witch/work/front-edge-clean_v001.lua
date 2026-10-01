-- v1.0: 확정 원본의 저알파 색 잔여만 정리합니다.
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'image-confirmed/1024/view/front.png')
app.activeSprite=s
local im=s.cels[1].image
local n=0
for it in im:pixels() do
 local c=it()
 if app.pixelColor.rgbaA(c)<=32 and c~=0 then it(0); n=n+1 end
end
s:saveAs(root..'work/front-edge-clean_v001.aseprite')
s:saveAs(root..'image-undecided/1024/view/front_v010.png')
print('정리 픽셀: '..n)
s:close()
