-- v1.0: 정면 시안 출력
local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'work/front-generated_v004.png')
app.activeSprite=s
app.command.SpriteSize{ui=false,width=1024,height=1024,method='bilinear'}
s:saveAs(root..'image-undecided/1024/view/front_v003.png')
s:close()
