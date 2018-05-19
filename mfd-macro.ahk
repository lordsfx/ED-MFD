﻿#NoEnv
#Persistent
#SingleInstance force
#InstallKeybdHook
#Warn
SetWorkingDir %A_ScriptDir%
SetKeyDelay, 30, 50
SetTitleMatchMode, 2

;; ;; Elite G19s Companion Hotkeys
;; #IfWinExist, Elite G19s Companion App
;; {
;; 
;; ; Up
;; 2Joy25::
;;    ;send, ^+{Up}
;;    send, ^+i
;;    return
;; 
;; ; Down
;; 2Joy26::
;;    ;send, ^+{Down}
;;    send, ^+k
;;    return
;; 
;; ; OK
;; 2Joy16::
;;    send, ^!{Insert}
;;    return
;; 
;; ; Cancel
;; 2Joy17::
;;    send, ^!{End}
;;    return
;; 
;; ; Left
;; 2Joy15::
;;    ;send, ^+{Left}
;;    send, ^+j
;;    return
;; 
;; ; Right
;; 2Joy14::
;;    ;send, ^+{Right}
;;    send, ^+l
;;    return
;; 
;; ; Menu
;; 2Joy18::
;;    send, ^!{Home}
;;    return
;; }

;#IfWinExist, Untitled - Notepad
#IfWInExist, Elite - Dangerous (CLIENT)
{
WinActivate

;; XBox One controller

F23::ESC
F24::!Tab

; LB
1Joy5::
   send, q
   return

; RB
1Joy6::
   send, e
   return

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

; Dock Request
2Joy18::
   controlsend, , {Ctrl Down}q{Ctrl Up}, Elite:Dangerous MFD
   send, 1ee{Space}s{Space}qq1
   return

; NAV Panel
2Joy17::
   send, 1
   return

; COM Panel
2Joy25::
   send, 2
   return

; RDR Panel
2Joy26::
   send, 3
   return

; SYS Panel
2Joy16::
   send, 4
   return

; Previous Panel
2Joy15::
   send, q
   return

; Next Panel
2Joy14::
   send, e
   return

}
