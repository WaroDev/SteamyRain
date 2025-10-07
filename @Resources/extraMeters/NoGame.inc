[NoGameStyle]
SolidColor=#TextBG#
FontColor=#TextColor#
MouseActionCursor=0
Padding=49,2,49,0
FontSize=9
StringCase=Upper
StringAlign=Center
Container=NoGameContainer
DynamicVariables=1
Group=NoGame
Hidden=1
FontSize=10
AntiAlias=1

[NoGameContainer]
Meter=Shape
Shape=Rectangle 0,20,#TilePixels#,[TilePixelsY] | Fill Color #Dark2# | StrokeWidth 0
DynamicVariables=1
Group=NoGame

[LogoNoGame]
Meter=Image
PreserveAspectRatio=1
ImageName=#@#img\SteamyRain
ImageAlpha=50
DynamicVariables=1
Container=NoGameContainer
Group=NoGame
X=-10
Y=([NoGamePos]-20)
W=([NoGamePos]+90)

[NoGameText]
Meter=String
Text="No games found"
FontColor=#TextColor#
SolidColor=#SettingsHover#
Padding=47,2,48,0
FontSize=12
StringCase=Upper
StringAlign=Center
DynamicVariables=1
Container=NoGameContainer
Group=NoGame
AntiAlias=1
Hidden=1
Y=[NoGamePos]
X=(#TilePixels#/2)

[ScanText]
Meter=String
Text="Scan for Games"
LeftMouseUpAction=[!WriteKeyValue Variables SkinPosX "#CURRENTCONFIGX#" "#@#SkinInfo.inc"][!WriteKeyValue Variables SkinPosY "#CURRENTCONFIGY#" "#@#SkinInfo.inc"]["#@#UpdateGames.pyw"]
MouseOverAction=[!SetOption ScanText SolidColor #Dark1#][!UpdateMeter ScanText][!ReDraw]
MouseLeaveAction=[!SetOption ScanText SolidColor #TextBG#][!UpdateMeter ScanText][!ReDraw]
MeterStyle=NoGameStyle
X=(#TilePixels#/2)
Y=25r

[HiddenText]
Meter=String
Text="Hidden Games"
LeftMouseUpAction=[!WriteKeyValue Variables SkinPosX "#CURRENTCONFIGX#" "#@#SkinInfo.inc"][!WriteKeyValue Variables SkinPosY "#CURRENTCONFIGY#" "#@#SkinInfo.inc"][!WriteKeyValue Variables hiddenWindow "(1-#hiddenWindow#)" "#@#SkinInfo.inc"][!SetVariable hiddenWindow "(1-#hiddenWindow#)" #CURRENTCONFIG#][!ToggleConfig "SteamyRain\Hidden" "Hidden.ini"]
MouseOverAction=[!SetOption HiddenText SolidColor #Dark1#][!UpdateMeter HiddenText][!ReDraw]
MouseLeaveAction=[!SetOption HiddenText SolidColor #TextBG#][!UpdateMeter HiddenText][!ReDraw]
MeterStyle=NoGameStyle
X=(#TilePixels#/2)
Y=19r