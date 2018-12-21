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

; #1 SYS 3 / Ctrl-T
5Joy1::
   send, {Down}{Left 1}
   controlsend, , {Ctrl Down}t{Ctrl Up}, Elite:Dangerous MFD
   return

; #2 ENG 3 / Ctrl-Y
5Joy2::
   send, {Down}{Up 1}
   controlsend, , {Ctrl Down}y{Ctrl Up}, Elite:Dangerous MFD
   return

; #3 WEP 3 / Ctrl-U
5Joy3::
   send, {Down}{Right 1}
   controlsend, , {Ctrl Down}u{Ctrl Up}, Elite:Dangerous MFD
   return

; #4 ENG/SYS (4/2) / Ctrl-D
5Joy4::
   send, {Down}{Up 2}{Left}{Up}
   controlsend, , {Ctrl Down}d{Ctrl Up}, Elite:Dangerous MFD
   return

; #5 WEP/SYS (4/2) / Ctrl-E
5Joy5::
   send, {Down}{Right 2}{Left}{Right}
   controlsend, , {Ctrl Down}e{Ctrl Up}, Elite:Dangerous MFD
   return

; #6 Heat Sink / Ctrl-H
5Joy6::
   controlsend, , {Ctrl Down}h{Ctrl Up}, Elite:Dangerous MFD
   return

; #7 Silent Run / Ctrl-M
5Joy7::
   controlsend, , {Ctrl Down}m{Ctrl Up}, Elite:Dangerous MFD
   return

; #8 Chaff / Ctrl-F
5Joy8::
   controlsend, , {Ctrl Down}f{Ctrl Up}, Elite:Dangerous MFD
   return

; #9 Shield Cell / Ctrl-I
5Joy9::
   controlsend, , {Ctrl Down}i{Ctrl Up}, Elite:Dangerous MFD
   return

; #10 Orbit Lines / Ctrl-O
5Joy10::
   controlsend, , {Ctrl Down}o{Ctrl Up}, Elite:Dangerous MFD
   return

; #11 Orbit Lines / Ctrl-N
5Joy11::
   controlsend, , {Ctrl Down}n{Ctrl Up}, Elite:Dangerous MFD
   return

; #12 Ship Lights / Ctrl-L
5Joy12::
   controlsend, , {Ctrl Down}l{Ctrl Up}, Elite:Dangerous MFD
   return

; #13 WEP Full / Ctrl-C
5Joy13::
   send, {Down}{Right 4}
   controlsend, , {Ctrl Down}c{Ctrl Up}, Elite:Dangerous MFD
   return

; #14 ENG Full / Ctrl-B
5Joy14::
   send, {Down}{Up 4}
   controlsend, , {Ctrl Down}b{Ctrl Up}, Elite:Dangerous MFD
   return

; #15 SYS Full / Ctrl-A
5Joy15::
   send, {Down}{Left 4}
   controlsend, , {Ctrl Down}a{Ctrl Up}, Elite:Dangerous MFD
   return

; #16 Landing Gear / Ctrl-G
5Joy16::
   controlsend, , {Ctrl Down}g{Ctrl Up}, Elite:Dangerous MFD
   return

; #17 Disco Scan / Ctrl-J
5Joy17::
   send, {] down}
   controlsend, , {Ctrl Down}j{Ctrl Up}, Elite:Dangerous MFD
   sleep 5000
   send, {] up}
   return

; #18 Dock Request / Ctrl-Q
5Joy18::
   controlsend, , {Ctrl Down}q{Ctrl Up}, Elite:Dangerous MFD
   send, 1ee{space}d{Space}qq1
   return

; #19 Cargo Scoop / Ctrl-S
5Joy19::
   controlsend, , {Ctrl Down}s{Ctrl Up}, Elite:Dangerous MFD
   return

; #20 Hard Points / Ctrl-P
5Joy20::
   controlsend, , {Ctrl Down}p{Ctrl Up}, Elite:Dangerous MFD
   return

; --

; #21 Prev Mode / Ctrl-,
5Joy21::
   controlsend, , {Ctrl Down}`,{Ctrl Up}, Elite:Dangerous MFD
   return

; #22 Next Mode / Ctrl-.
5Joy22::
   controlsend, , {Ctrl Down}.{Ctrl Up}, Elite:Dangerous MFD
   return

