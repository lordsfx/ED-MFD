#NoEnv
#Persistent
#InstallKeybdHook
#Warn
SetWorkingDir %A_ScriptDir%
SetKeyDelay, 30, 50
SetTitleMatchMode, 2

;; Elite G19s Companion Hotkeys
#IfWinExist, Elite G19s Companion App
{

; Up
2Joy25::
   send, ^+{Up}
   return

; Down
2Joy26::
   send, ^+{Down}
   return

; OK
2Joy16::
   send, ^!{Insert}
   return

; Cancel
2Joy17::
   send, ^!{End}
   return

; Left
2Joy15::
   send, ^+{Left}
   return

; Right
2Joy14::
   send, ^+{Right}
   return

; Menu
2Joy18::
   send, ^!{Home}
   return
}

;#IfWinExist, Untitled - Notepad
#IfWInExist, Elite - Dangerous (CLIENT)
{
WinActivate

;; XBox One controller

F23::ESC
F24::Tab

;; Thrustmaster MFD

; SYS Full
2Joy1::
   send, {Down}{Left 4}
   controlsend, , {Ctrl Down}a{Ctrl Up}, Elite:Dangerous MFD
   return

; ENG Full
2Joy2::
   send, {Down}{Up 4}
   controlsend, , {Ctrl Down}b{Ctrl Up}, Elite:Dangerous MFD
   return

; WEP Full
2Joy3::
   send, {Down}{Right 4}
   controlsend, , {Ctrl Down}c{Ctrl Up}, Elite:Dangerous MFD
   return

; ENG/SYS (4/2)
2Joy4::
   send, {Down}{Up 2}{Left}{Up}
   controlsend, , {Ctrl Down}d{Ctrl Up}, Elite:Dangerous MFD
   return

; WEP/SYS (4/2)
2Joy5::
   send, {Down}{Right 2}{Left}{Right}
   controlsend, , {Ctrl Down}e{Ctrl Up}, Elite:Dangerous MFD
   return

; Scan
2Joy10::
   send, {] down}
   controlsend, , {Ctrl Down}j{Ctrl Up}, Elite:Dangerous MFD
   sleep 5000
   send, {] up}
   return

;; for Elite:Dangerous MFD panel

; Heat Sink
2Joy6::
   controlsend, , {Ctrl Down}f{Ctrl Up}, Elite:Dangerous MFD
   return

; Silent Run
2Joy7::
   controlsend, , {Ctrl Down}g{Ctrl Up}, Elite:Dangerous MFD
   return

; Chaff
2Joy8::
   controlsend, , {Ctrl Down}h{Ctrl Up}, Elite:Dangerous MFD
   return

; Shield Cell
2Joy9::
   controlsend, , {Ctrl Down}i{Ctrl Up}, Elite:Dangerous MFD
   return

; Orbit Lines
2Joy11::
   controlsend, , {Ctrl Down}o{Ctrl Up}, Elite:Dangerous MFD
   return

; Ship Lights
2Joy12::
   controlsend, , {Ctrl Down}n{Ctrl Up}, Elite:Dangerous MFD
   return

; Landing Gear
2Joy13::
   controlsend, , {Ctrl Down}m{Ctrl Up}, Elite:Dangerous MFD
   return

; Cargo Scoop
2Joy19::
   controlsend, , {Ctrl Down}l{Ctrl Up}, Elite:Dangerous MFD
   return

; Hard Points
2Joy20::
   controlsend, , {Ctrl Down}k{Ctrl Up}, Elite:Dangerous MFD
   return

}
