#NoEnv
#Persistent
#SingleInstance force
#InstallKeybdHook
#Warn
SetWorkingDir %A_ScriptDir%
SetKeyDelay, 30, 50
SetTitleMatchMode, 2

;#IfWinExist, Untitled - Notepad
#IfWInExist, Elite - Dangerous (CLIENT)

;; Thrustmaster MFD

; SYS Full
5Joy1::
   send, {Down}{Left 4}
   controlsend, , {Ctrl Down}a{Ctrl Up}, Elite:Dangerous MFD
   return

; ENG Full
5Joy2::
   send, {Down}{Up 4}
   controlsend, , {Ctrl Down}b{Ctrl Up}, Elite:Dangerous MFD
   return

; WEP Full
5Joy3::
   send, {Down}{Right 4}
   controlsend, , {Ctrl Down}c{Ctrl Up}, Elite:Dangerous MFD
   return

; ENG/SYS (4/2)
5Joy4::
   send, {Down}{Up 2}{Left}{Up}
   controlsend, , {Ctrl Down}d{Ctrl Up}, Elite:Dangerous MFD
   return

; WEP/SYS (4/2)
5Joy5::
   send, {Down}{Right 2}{Left}{Right}
   controlsend, , {Ctrl Down}e{Ctrl Up}, Elite:Dangerous MFD
   return

; Scan
;5Joy10::
;   send, {] down}
;   controlsend, , {Ctrl Down}j{Ctrl Up}, Elite:Dangerous MFD
;   sleep 5000
;   send, {] up}
;   return

;; for Elite:Dangerous MFD panel

; Heat Sink
5Joy6::
   controlsend, , {Ctrl Down}f{Ctrl Up}, Elite:Dangerous MFD
   return

; Silent Run
5Joy7::
   controlsend, , {Ctrl Down}g{Ctrl Up}, Elite:Dangerous MFD
   return

; Chaff
5Joy8::
   controlsend, , {Ctrl Down}h{Ctrl Up}, Elite:Dangerous MFD
   return

; Shield Cell
5Joy9::
   controlsend, , {Ctrl Down}i{Ctrl Up}, Elite:Dangerous MFD
   return

; Orbit Lines
5Joy11::
   controlsend, , {Ctrl Down}o{Ctrl Up}, Elite:Dangerous MFD
   return

; Ship Lights
5Joy12::
   controlsend, , {Ctrl Down}n{Ctrl Up}, Elite:Dangerous MFD
   return

; Landing Gear
5Joy13::
   controlsend, , {Ctrl Down}m{Ctrl Up}, Elite:Dangerous MFD
   return

; Cargo Scoop
5Joy19::
   controlsend, , {Ctrl Down}l{Ctrl Up}, Elite:Dangerous MFD
   return

; Hard Points
5Joy20::
   controlsend, , {Ctrl Down}k{Ctrl Up}, Elite:Dangerous MFD
   return

; Dock Request
5Joy18::
   controlsend, , {Ctrl Down}q{Ctrl Up}, Elite:Dangerous MFD
   send, 1ee{Space}s{Space}qq1
   return

; NAV Panel
5Joy17::
   send, 1
   return

; COM Panel
5Joy25::
   send, 2
   return

; RDR Panel
5Joy26::
   send, 3
   return

; SYS Panel
5Joy16::
   send, 4
   return

; Previous Panel
5Joy15::
   send, q
   return

; Next Panel
5Joy14::
   send, e
   return

; Prev Mode
5Joy21::
   controlsend, , {Ctrl Down},{Ctrl Up}, Elite:Dangerous MFD
   return

; Next Mode
5Joy22::
   controlsend, , {Ctrl Down}.{Ctrl Up}, Elite:Dangerous MFD
   return

