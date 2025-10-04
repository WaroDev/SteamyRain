# SteamyRain
 Rainmeter skin SteamyRain

Thanks to [Nookz](https://forum.rainmeter.net/memberlist.php?mode=viewprofile&u=71269) from Rainmeter Forum who delevoped the skin in the first place.
You can read all about it here in his post and the comments: https://forum.rainmeter.net/viewtopic.php?t=43334

Thanks to:

[macqueen0987](https://forum.rainmeter.net/memberlist.php?mode=viewprofile&u=74947) - who shared his changes for multiple gamedir folders and locale fixes https://forum.rainmeter.net/viewtopic.php?t=43334#p230808
---

## Requirements
You must have python installed!
It is using a python script to fetch the required information and images from your steam folder and build meters dynamically.

---

## Setup
1. Make sure that both paths inside @Resources\SkinInfo.inc are correct. You only need to modify this if your steam installation folder or your Rainmeter installation folder are not in their respective default location.
2. **Optional** Add your non-Steam games. *see section below for more information*
3. Open one of the SteamyRain.ini from the main folder and Click on 'Scan for Games'
4. Wait till it's done and you're good to go.
5. Adjust the settings to your liking.

## Add Non-Steam Games
This part of the process has to be done manually and will only take effect after using 'Scan for Games'

1. Open the @Resrouces\NonSteamGames.inc
2. Add each game using this format:  
```
Egame#="TheNameOfMyGame"
Egame#Path="ThePathToLaunchMyGame"
Egame#Vis=0
```
It does not have to be a game really. It could be any app or url. eg:  
```
Egame1="Photoshop"
Egame1Path="C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Adobe Photoshop 2024.lnk"
Egame1Vis=0
Egame2="RainmeterForums"
Egame2Path="https://forum.rainmeter.net/index.php"
Egame2Vis=0
```
3. Modify the ExtraGamesCount and ExtraGamesCountPLUS variables at the top to reflect the amount of games you added.
In our example above we would set both of these to 2.
4. Inside @Resrouces\img\ELogo and @Resrouces\img\EIcon, add an icon and a logo for each of the games you added.
name them 00#.jpg. '#' reprensent the game number it is associated with.
I would recomend 32x32 for the icon and 460x215 for the logo
5. Run UpdateGames.pyw if you already followed the Setup steps until the end and already clicked on "Scan for Games". Everytime you add new entries to your NonSteamGames.inc file you have to run the python script again or put necessary infos in the *Meters.inc files manually.
6. Done!

---

## Shortcuts and Keybinds
Header Icon:  
RightClick = Open Steam  
MiddleClick = Open Skin settings  
DoubleClick = Minimise into Icon  
  
Icon Mode:  
DoubleClick = Return to full view  
  
Tiles Section:  
RightClick = Hide/Unhide Header  
MiddleClick = Switch from vertical tiling to horizontal tiling and vice versa  
ScrollUp/Down = Scroll games  
  
Settings Menu:  
RightClick = Reset default value  

## Search Function
It's a fairly simple search function. You can search by Name or by ID  
It will return partial matches for names and only identical matches for IDs.  
It will not account for spelling errors..  