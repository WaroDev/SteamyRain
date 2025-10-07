[ModeCheck]
Measure=Calc
IfCondition=#Mode#=1
IfTrueAction=[!SetOption ModeoptionText Text "Switch Vertical"][!SetOption Modeoption Text "[\xea40]"]
IfConditionMode=1
OnUpdateAction=[!UpdateMeterGroup QuickSettings][!UpdateMeterGroup NoGame][!UpdateMeterGroup NoGameFirst][!ReDraw]
DynamicVariables=1

[TextStyle]
SolidColor=#TextBG#
FontColor=#TextColor#
MouseActionCursor=0
DynamicVariables=1
Group=QuickSettings
Padding=10,4,0,2
FontSize=10
AntiAlias=1
Hidden=1
W=150

[BGQuickSettings]
Meter=Shape
Shape=Rectangle (#TilePixels#-166),20,156,72 | Fill Color #Dark1# | StrokeWidth 0
Hidden=1
DynamicVariables=1
Group=QuickSettings

[ModeoptionText]
Meter=String
Text="Switch Horizontal"
LeftMouseUpAction=[!WriteKeyValue Variables Mode "(1-#Mode#)" "#@#SkinInfo.inc"][!ActivateConfig #CURRENTCONFIG#]
MouseOverAction=[!SetOption ModeoptionText SolidColor #Dark1#][!UpdateMeter ModeoptionText][!ReDraw]
MouseLeaveAction=[!SetOption ModeoptionText SolidColor #TextBG#][!UpdateMeter ModeoptionText][!ReDraw]
MeterStyle=TextStyle
Hidden=1
Y=22
X=(#TilePixels#-168)

[Modeoption]
Meter=String
Text="[\xed35]"
StringAlign=Right
MeterStyle=ButtonStyle
Group=QuickSettings
Hidden=1
X=150r
Y=3r

[ScanoptionText]
Meter=String
Text="Scan for Games"
LeftMouseUpAction=[!WriteKeyValue Variables SkinPosX "#CURRENTCONFIGX#" "#@#SkinInfo.inc"][!WriteKeyValue Variables SkinPosY "#CURRENTCONFIGY#" "#@#SkinInfo.inc"]["#@#UpdateGames.pyw"][!HideMeterGroup QuickSettings]
MouseOverAction=[!SetOption ScanoptionText SolidColor #Dark1#][!UpdateMeter ScanoptionText][!ReDraw]
MouseLeaveAction=[!SetOption ScanoptionText SolidColor #TextBG#][!UpdateMeter ScanoptionText][!ReDraw]
MeterStyle=TextStyle
X=-150r
Y=20r

[Scanoption]
Meter=String
Text="[\xec51]"
StringAlign=Right
MeterStyle=ButtonStyle
Group=QuickSettings
Hidden=1
X=150r
Y=3r

[HiddenoptionText]
Meter=String
Text="Hidden Games"
LeftMouseUpAction=[!WriteKeyValue Variables SkinPosX "#CURRENTCONFIGX#" "#@#SkinInfo.inc"][!WriteKeyValue Variables SkinPosY "#CURRENTCONFIGY#" "#@#SkinInfo.inc"][!WriteKeyValue Variables hiddenWindow "(1-#hiddenWindow#)" "#@#SkinInfo.inc"][!SetVariable hiddenWindow "(1-#hiddenWindow#)" #CURRENTCONFIG#][!ToggleConfig "SteamyRain\Hidden" "Hidden.ini"][!HideMeterGroup QuickSettings]
MouseOverAction=[!SetOption HiddenoptionText SolidColor #Dark1#][!UpdateMeter HiddenoptionText][!ReDraw]
MouseLeaveAction=[!SetOption HiddenoptionText SolidColor #TextBG#][!UpdateMeter HiddenoptionText][!ReDraw]
MeterStyle=TextStyle
X=-150r
Y=20r

[Hiddenoption]
Meter=String
Text="[\xed1a]"
StringAlign=Right
MeterStyle=ButtonStyle
Group=QuickSettings
Hidden=1
X=150r
Y=3r

[SettingsoptionText]
Meter=String
Text="Settings"
LeftMouseUpAction=[!WriteKeyValue Variables SkinPosX "#CURRENTCONFIGX#" "#@#SkinInfo.inc"][!WriteKeyValue Variables SkinPosY "#CURRENTCONFIGY#" "#@#SkinInfo.inc"][!WriteKeyValue Variables Settings "1" "#@#SkinInfo.inc"][!SetVariable Settings "1"][!ActivateConfig "SteamyRain\Settings" "Settings.ini"][!HideMeterGroup QuickSettings]
MouseOverAction=[!SetOption SettingsoptionText SolidColor #Dark1#][!UpdateMeter SettingsoptionText][!ReDraw]
MouseLeaveAction=[!SetOption SettingsoptionText SolidColor #TextBG#][!UpdateMeter SettingsoptionText][!ReDraw]
MeterStyle=TextStyle
X=-150r
Y=20r

[Settingsoption]
Meter=String
Text="[\xe713]"
StringAlign=Right
MeterStyle=ButtonStyle
Group=QuickSettings
Hidden=1
X=150r
Y=3r


