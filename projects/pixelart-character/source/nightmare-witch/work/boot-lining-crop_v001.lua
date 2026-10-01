local root='P:/github-repository/pixelart-design/projects/pixelart-character/source/nightmare-witch/'
local s=app.open(root..'image-confirmed/1024/view/front.png')
app.activeSprite=s
app.command.CanvasSize{ui=false,left=-400,right=-384,top=-784,bottom=0}
s:saveAs(root..'work/boot-lining-input_v001.png')
s:close()
