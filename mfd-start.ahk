#Persistent
SetTimer, app_monitor, 5000

; start MFD app
; app window's default size is 1280x800, using a scale factor 0.8 will resize it to 1024x640
Run, py mfd.py 0.8, , Min
WinWait, Elite:Dangerous MFD
; the app is supposed to run off second screen, change the WinMove x,y position accordingly
;WinMove, 0, 0
WinMove, 1940, 3456
#IfWinActive, Elite:Dangerous MFD
LButton::
    WinSet, Bottom

app_monitor:
IfWinNotExist, Elite:Dangerous MFD
   ExitApp
Return
