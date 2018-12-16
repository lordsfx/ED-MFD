import logging
from common import *
import sys, pygame
import json
from config import *
from mfd_functions import *
from mfd_interface import *
from ed_object import *
from ed_journal import *
from watchdog.observers import Observer

# param
scale = 1
if len(sys.argv) > 1:
    scale = float(sys.argv[1])
MFD.set_scale(scale)
APP_SIZE = MFD.sd(DISPLAY_WIDTH), MFD.sd(DISPLAY_HEIGHT)

# set stage
pygame.init()
pygame.display.set_caption(MFD.title)
img_MFD = pygame.image.load(IMAGE_WALLPAPER)
img_MFD = pygame.transform.smoothscale(img_MFD, APP_SIZE)
mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF|NOFRAME)
img_MFD = img_MFD.convert()
MFD.set_font(DEFAULT_FONT)

blur_MFD = pygame.Surface(APP_SIZE)
blur_MFD.fill(COLOR_GREY)
blur_MFD.set_alpha(20, RLEACCEL)
layer_BTN = pygame.image.load((IMAGE_BUTTON % MFD.scale)).convert_alpha()
img_MODE_dark = pygame.image.load((IMAGE_MODE_DARK % MFD.scale)).convert_alpha()
img_MODE = pygame.image.load((IMAGE_MODE % MFD.scale)).convert_alpha()

img_MFD.blit(blur_MFD, (0, 0))
img_MFD.blit(layer_BTN, (0, 0))
img_MFD.blit(img_MODE_dark, (0, 0))

TIMER_LOOP = Button.TIMER_STEP * 10

# ED objects
my_ship = Ship()
milkyway = Universe()

# init buttons

MFD.bmp = [ None,	# 0
    Button("SYS Full"    , MFD_SYS_FULL,   MFD_XC1, MFD_YT1, COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 1
    Button("ENG Full"    , MFD_ENG_FULL,   MFD_XC2, MFD_YT1, COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 2
    Button("WEP Full"    , MFD_WEP_FULL,   MFD_XC3, MFD_YT1, COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 3
    Button("ENG 4+SYS 2" , MFD_ENG4_SYS2,  MFD_XC4, MFD_YT1, COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 4
    Button("WEP 4+SYS 2" , MFD_WEP4_SYS2,  MFD_XC5, MFD_YT1, COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 5
    Button("Heat Sink"   , MFD_HEATSINK,   MFD_XR1, MFD_YC1, COLOR_GREEN),	# 6
    Button("Silent Run"  , MFD_SILENTRUN,  MFD_XR1, MFD_YC2, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 7
    Button("Chaff"       , MFD_CHAFF,      MFD_XR1, MFD_YC3, COLOR_GREEN),	# 8
    Button("Shield Cell" , MFD_SHIELDCELL, MFD_XR1, MFD_YC4, COLOR_GREEN),	# 9
    #Button("Disco Scan"  , MFD_DISCOSCAN,  MFD_XR1, MFD_YC5, COLOR_ORANGE, Button.TYPE_HOLD),	# 10
    Button("FSS"         , MFD_FSS,        MFD_XR1, MFD_YC5, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 10
    Button("Orbit Lines" , MFD_ORBITLINES, MFD_XC5, MFD_YB1, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 11
    Button("Ship Lights" , MFD_LIGHTS,     MFD_XC4, MFD_YB1, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 12
    Button("Landing Gear", MFD_LANDING,    MFD_XC3, MFD_YB1, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 13
    None, None, None, None, 							# 14 - 17
    Button("Docking Req" , MFD_DOCKINGREQ, MFD_XL1, MFD_YC3, COLOR_ORANGE),	# 18
    Button("Cargo Scoop" , MFD_CARGOSCOOP, MFD_XL1, MFD_YC2, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 19
    Button("Hard Points" , MFD_HARDPOINT,  MFD_XL1, MFD_YC1, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 20
    None, None, None, None, None, None, None, None ]	# 21 - 28

# init panels

# right panel
MFD_RP_SIZE = MFD.sd(MFD_RP_WIDTH), MFD.sd(MFD_RP_HEIGHT)
MFD_RP_XY = MFD.sd(MFD_RP_X), MFD.sd(MFD_RP_Y)

rpanel = pygame.Surface( (MFD.sd(MFD_RP_WIDTH), MFD.sd(MFD_RP_HEIGHT)) )
MFD.rpn = Panel(MFD.sd(MFD_RP_X), MFD.sd(MFD_RP_Y), MFD.sd(MFD_RP_WIDTH), MFD.sd(MFD_RP_HEIGHT), MFD_RP_ROWS)
#MFD.rpn.add_text(["12345 67890 12345 67890 12345 67890 12345 67890 12345 67890"], color=COLOR_GREEN)
MFD.rpn.add_text(["Created by CMDR Lord Shadowfax"], color=COLOR_GREEN)
MFD.rpn.add_text(["Elite:Dangerous MFD v" + MFD_VER], color=COLOR_GREEN)
MFD.rpn.add_text(["", "Loading universe data ..."])

# mid panel
MFD_MP_SIZE = MFD.sd(MFD_MP_WIDTH), MFD.sd(MFD_MP_HEIGHT)
MFD_MP_XY = MFD.sd(MFD_MP_X), MFD.sd(MFD_MP_Y)

mpanel = pygame.Surface( (MFD.sd(MFD_MP_WIDTH), MFD.sd(MFD_MP_HEIGHT)) )
for m in MFD.MFD_MODE:
    MFD.mpn[m] = Panel(MFD.sd(MFD_MP_X), MFD.sd(MFD_MP_Y), MFD.sd(MFD_MP_WIDTH), MFD.sd(MFD_MP_HEIGHT), MFD_MP_ROWS)
draw_logo(MFD.mpn[1])

# upper panel
MFD_UP_SIZE = MFD.sd(MFD_UP_WIDTH), MFD.sd(MFD_UP_HEIGHT)
MFD_UP_XY = MFD.sd(MFD_UP_X), MFD.sd(MFD_UP_Y)

upanel = pygame.Surface( (MFD.sd(MFD_UP_WIDTH), MFD.sd(MFD_UP_HEIGHT)) )
MFD.upn = Panel(MFD.sd(MFD_UP_X), MFD.sd(MFD_UP_Y), MFD.sd(MFD_UP_WIDTH), MFD.sd(MFD_UP_HEIGHT), MFD_UP_ROWS, font_size=MFD.sd(MFD_UP_FONT_SIZE), bold=True)
MFD.upn.add_text([" > %s" % MFD.MFD_MODE[MFD.next_mode()]], color=COLOR_GREEN)

# lower panel
MFD_LP_SIZE = MFD.sd(MFD_LP_WIDTH), MFD.sd(MFD_LP_HEIGHT)
MFD_LP_XY = MFD.sd(MFD_LP_X), MFD.sd(MFD_LP_Y)

lpanel = pygame.Surface( (MFD.sd(MFD_LP_WIDTH), MFD.sd(MFD_LP_HEIGHT)) )
MFD.lpn = Panel(MFD.sd(MFD_LP_X), MFD.sd(MFD_LP_Y), MFD.sd(MFD_LP_WIDTH), MFD.sd(MFD_LP_HEIGHT), MFD_LP_ROWS)

# misc init
last_pad = 0
mfd_mode = MFD_Mode()

# set init background
mfd.blit(img_MFD, (0, 0))
noframe = True

# load last states, if any
if load_button_states(MFD.bmp):
    #logger.debug("Loaded last states - ")
    #show_button_states(MFD.bmp)
    draw_background(mfd, img_MFD)
    draw_button_states(mfd, MFD.bmp)
    pygame.display.flip()

# journals
journal_evh = JournalEventHandler()
journal_obs = Observer()
journal_obs.schedule(journal_evh, Journal.path, recursive=False)
journal_obs.start()

# user event timer
EVENT_APP_LOOP = pygame.USEREVENT
pygame.time.set_timer(EVENT_APP_LOOP, TIMER_LOOP)

# load eddb data
milkyway.thread_load_data(MFD.rpn)

# loop
while True:

    event = pygame.event.wait()

    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        button_pressed = None
        joy_index = 0
        if event.key == pygame.K_a:  joy_index = MFD_SYS_FULL	# SYS - Full
        if event.key == pygame.K_b:  joy_index = MFD_ENG_FULL	# ENG - Full
        if event.key == pygame.K_c:  joy_index = MFD_WEP_FULL	# WEP - Full
        if event.key == pygame.K_d:  joy_index = MFD_ENG4_SYS2	# ENG 4 + SYS 2
        if event.key == pygame.K_e:  joy_index = MFD_WEP4_SYS2	# WEP 4 + SYS 2
        if event.key == pygame.K_f:  joy_index = MFD_HEATSINK	# Heat Sink
        if event.key == pygame.K_g:  joy_index = MFD_SILENTRUN	# Silent Run
        if event.key == pygame.K_h:  joy_index = MFD_CHAFF	# Chaff
        if event.key == pygame.K_i:  joy_index = MFD_SHIELDCELL	# Shield Cell
        if event.key == pygame.K_j:  joy_index = MFD_FSS	# FSS
        if event.key == pygame.K_k:  joy_index = MFD_HARDPOINT	# Hard Points
        if event.key == pygame.K_l:  joy_index = MFD_CARGOSCOOP	# Cargo Scoop
        if event.key == pygame.K_m:  joy_index = MFD_LANDING	# Landing Gear
        if event.key == pygame.K_n:  joy_index = MFD_LIGHTS	# Ship Lights
        if event.key == pygame.K_o:  joy_index = MFD_ORBITLINES	# Orbit Lines
        if event.key == pygame.K_q:  joy_index = MFD_DOCKINGREQ	# Docking Req
        if joy_index > 0:
            button_pressed = MFD.bmp[joy_index]
            MFD.set_update()

        if event.key == pygame.K_PERIOD:    # Ctrl-. : Next Mode
            if mods & pygame.KMOD_CTRL:
                MFD.upn.add_text([" > %s" % MFD.MFD_MODE[MFD.next_mode()]], color=COLOR_GREEN)
        if event.key == pygame.K_COMMA:     # Ctrl-, : Prev Mode
            if mods & pygame.KMOD_CTRL:
                MFD.upn.add_text([" > %s" % MFD.MFD_MODE[MFD.prev_mode()]], color=COLOR_GREEN)
        if event.key == pygame.K_x:         # Ctrl-X : Reset all states
            if mods & pygame.KMOD_CTRL:
                for b in MFD.bmp:
                    if b: b.reset_state()
                MFD.rpn.add_text(["- reset all states"])
        if event.key == pygame.K_p:         # Ctrl-P : Coriolis Pad Test
            if mods & pygame.KMOD_CTRL:
                last_pad += 1
                if last_pad > 45: last_pad = 0
                MFD.rpn.add_coriolis(last_pad, Coriolis(MFD_RP_WIDTH))
        if event.key == pygame.K_0:         # Ctrl-0 : Coriolis All Pads
            if mods & pygame.KMOD_CTRL:
                MFD.mpn[1].clear_all()
                MFD.mpn[1].add_coriolis(0, Coriolis(MFD_MP_WIDTH))
        if event.key == pygame.K_r:         # Ctrl-R : Refresh EDDB data
            milkyway.thread_refresh_eddb(MFD.rpn)
            MFD.set_update()
        if event.key == pygame.K_SPACE:
            if noframe:
                mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF|NOFRAME)
                noframe = False
            else:
                mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF)
                noframe = True
            MFD.set_update()
        if event.type == QUIT or event.key == pygame.K_ESCAPE:
            save_button_states(MFD.bmp)
            journal_obs.stop()
            break

        if button_pressed:
            if mods & pygame.KMOD_CTRL:
                if button_pressed.type == Button.TYPE_SWITCH_1:
                    switch_group_states(button_pressed, MFD.bmp)
                else:
                    button_pressed.update_state()
                #logger.debug("MFD: " + button_pressed.name + ", State: " + str(button_pressed.state))
            if mods & pygame.KMOD_ALT:
                button_pressed.reset_state()
            MFD.set_update()

    if event.type == EVENT_APP_LOOP:
        if tick_button_states(MFD.bmp):
            MFD.set_update()

    journal_updates = journal_evh.get_updates()
    if journal_updates:
        for j in journal_updates:
            #logger.debug(j)
            Journal.parser(j, my_ship)
        Journal.display([MFD.rpn, MFD.mpn[1], MFD.lpn], my_ship, milkyway, MFD.bmp)
        MFD.set_update()

    #show_button_states(MFD.bmp)
    if MFD.has_update:
        draw_background(mfd, img_MFD)
        draw_mode(mfd, mfd_mode, img_MODE)
        draw_panel(mfd, rpanel, MFD.rpn, False)
        draw_panel(mfd, mpanel, MFD.mpn[MFD.mode])
        #draw_panel(mfd, upanel, MFD.upn)
        draw_panel(mfd, lpanel, MFD.lpn)
        draw_button_states(mfd, MFD.bmp)
        pygame.display.flip()
        MFD.clear_update()


# End While

