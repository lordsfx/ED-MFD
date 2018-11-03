import sys, pygame
import json
from mfd_functions import *
from mfd_interface import *
from ed_object import *
from ed_journal import *
from watchdog.observers import Observer

pygame.init()

# param
scale = 1
if len(sys.argv) > 1:
    scale = float(sys.argv[1])

# set stage
pygame.display.set_caption(MFD.title)
img_MFD = pygame.image.load(MFD.image_wallpaper)
APP_WIDTH, APP_HEIGHT = img_MFD.get_rect().size
APP_SIZE = APP_WIDTH, APP_HEIGHT
mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF|NOFRAME)
img_MFD = img_MFD.convert()
MFD.set_font("fonts/Eurostile.ttf")
MFD.set_scale(scale)

blur_MFD = pygame.Surface(APP_SIZE)
blur_MFD.fill(COLOR_GREY)
blur_MFD.set_alpha(20, RLEACCEL)
layer_BTN = pygame.image.load(MFD.image_buttons).convert_alpha()

img_MFD.blit(blur_MFD, (0, 0))
img_MFD.blit(layer_BTN, (0, 0))

TIMER_LOOP = Button.TIMER_STEP * 10

# display panels

MFD_RP_SIZE = MFD.sd(MFD_RP_WIDTH), MFD.sd(MFD_RP_HEIGHT)
MFD_RP_XY = MFD.sd(MFD_RP_X), MFD.sd(MFD_RP_Y)

MFD_MP_SIZE = MFD.sd(MFD_MP_WIDTH), MFD.sd(MFD_MP_HEIGHT)
MFD_MP_XY = MFD.sd(MFD_MP_X), MFD.sd(MFD_MP_Y)

# init buttons

bm1_MFD = [ None,	# 0
    Button("SYS Full"    , MFD.sd(MFD_XC1), MFD.sd(MFD_YT1), COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 1
    Button("ENG Full"    , MFD.sd(MFD_XC2), MFD.sd(MFD_YT1), COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 2
    Button("WEP Full"    , MFD.sd(MFD_XC3), MFD.sd(MFD_YT1), COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 3
    Button("ENG 4+SYS 2" , MFD.sd(MFD_XC4), MFD.sd(MFD_YT1), COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 4
    Button("WEP 4+SYS 2" , MFD.sd(MFD_XC5), MFD.sd(MFD_YT1), COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 5
    Button("Heat Sink"   , MFD.sd(MFD_XR1), MFD.sd(MFD_YC1), COLOR_GREEN),	# 6
    Button("Silent Run"  , MFD.sd(MFD_XR1), MFD.sd(MFD_YC2), COLOR_GREEN, Button.TYPE_TOGGLE),	# 7
    Button("Chaff"       , MFD.sd(MFD_XR1), MFD.sd(MFD_YC3), COLOR_GREEN),	# 8
    Button("Shield Cell" , MFD.sd(MFD_XR1), MFD.sd(MFD_YC4), COLOR_GREEN),	# 9
    Button("Disco Scan"  , MFD.sd(MFD_XR1), MFD.sd(MFD_YC5), COLOR_ORANGE, Button.TYPE_HOLD),	# 10
    Button("Orbit Lines" , MFD.sd(MFD_XC5), MFD.sd(MFD_YB1), COLOR_GREEN, Button.TYPE_TOGGLE),	# 11
    Button("Ship Lights" , MFD.sd(MFD_XC4), MFD.sd(MFD_YB1), COLOR_GREEN, Button.TYPE_TOGGLE),	# 12
    Button("Landing Gear", MFD.sd(MFD_XC3), MFD.sd(MFD_YB1), COLOR_GREEN, Button.TYPE_TOGGLE),	# 13
    None, None, None, None, 							# 14 - 17
    Button("Docking Req" , MFD.sd(MFD_XL1), MFD.sd(MFD_YC3), COLOR_ORANGE),	# 18
    Button("Cargo Scoop" , MFD.sd(MFD_XL1), MFD.sd(MFD_YC2), COLOR_GREEN, Button.TYPE_TOGGLE),	# 19
    Button("Hard Points" , MFD.sd(MFD_XL1), MFD.sd(MFD_YC1), COLOR_GREEN, Button.TYPE_TOGGLE),	# 20
    None, None, None, None, None, None, None, None ]	# 21 - 28

# init panel - right panel

rpanel = pygame.Surface( (MFD.sd(MFD_RP_WIDTH), MFD.sd(MFD_RP_HEIGHT)) )
rp1_MFD = Panel(MFD.sd(MFD_RP_X), MFD.sd(MFD_RP_Y), MFD.sd(MFD_RP_WIDTH), MFD.sd(MFD_RP_HEIGHT))
#rp1_MFD.add_image("images/EliteDangerous_Logo.png")
#rp1_MFD.add_text(["Hello World, the quick brown fox jumps over the lazy dog."])
rp1_MFD.add_text(["Created by CMDR Lord Shadowfax"])
rp1_MFD.add_text(["Elite:Dangerous MFD v1.1"])
#rp1_MFD.add_text(["Loading universe data ..."])

# init panel - middle panel

mpanel = pygame.Surface( (MFD.sd(MFD_MP_WIDTH), MFD.sd(MFD_MP_HEIGHT)) )
mp1_MFD = Panel(MFD.sd(MFD_MP_X), MFD.sd(MFD_MP_Y), MFD.sd(MFD_MP_WIDTH), MFD.sd(MFD_MP_HEIGHT))
mp1_MFD.add_image("images/EliteDangerous_Logo.png")
mp1_MFD.add_text(["",""])

Coriolis.init()
last_pad = 0
#rp1_MFD.add_coriolis(last_pad)

# set init background
mfd.blit(img_MFD, (0, 0))
noframe = True

# load last states, if any
if load_button_states(bm1_MFD):
    #print("Loaded last states - ")
    #show_button_states(bm1_MFD)
    draw_background(mfd, img_MFD)
    draw_button_states(mfd, bm1_MFD)
    pygame.display.flip()

# journals
journal_evh = JournalEventHandler()
journal_obs = Observer()
journal_obs.schedule(journal_evh, Journal.path, recursive=False)
journal_obs.start()

# ED objects
my_ship = Ship()
milkyway = Universe()

# user event timer
EVENT_APP_LOOP = pygame.USEREVENT
pygame.time.set_timer(EVENT_APP_LOOP, TIMER_LOOP)

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
        if event.key == pygame.K_j:  joy_index = MFD_DISCOSCAN	# Disco Scan
        if event.key == pygame.K_k:  joy_index = MFD_HARDPOINT	# Hard Points
        if event.key == pygame.K_l:  joy_index = MFD_CARGOSCOOP	# Cargo Scoop
        if event.key == pygame.K_m:  joy_index = MFD_LANDING	# Landing Gear
        if event.key == pygame.K_n:  joy_index = MFD_LIGHTS	# Ship Lights
        if event.key == pygame.K_o:  joy_index = MFD_ORBITLINES	# Orbit Lines
        if event.key == pygame.K_q:  joy_index = MFD_DOCKINGREQ	# Docking Req
        if joy_index > 0:
            button_pressed = bm1_MFD[joy_index]

        if event.key == pygame.K_r:         # Ctrl-R : Reset all states
            if mods & pygame.KMOD_CTRL:
                for b in bm1_MFD:
                    if b: b.reset_state()
                rp1_MFD.add_text(["- reset all states"])
        if event.key == pygame.K_p:         # Ctrl-P : Coriolis Pad Test
            if mods & pygame.KMOD_CTRL:
                last_pad += 1
                if last_pad > 45: last_pad = 0
                rp1_MFD.add_coriolis(last_pad)
        if event.key == pygame.K_0:         # Ctrl-0 : Coriolis All Pads
            if mods & pygame.KMOD_CTRL:
                rp1_MFD.add_coriolis(0)
        if event.key == pygame.K_SPACE:
            if noframe:
                mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF|NOFRAME)
                noframe = False
            else:
                mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF)
                noframe = True
        if event.type == QUIT or event.key == pygame.K_ESCAPE:
            save_button_states(bm1_MFD)
            journal_obs.stop()
            break

        if button_pressed:
            if mods & pygame.KMOD_CTRL:
                if button_pressed.type == Button.TYPE_SWITCH_1:
                    switch_group_states(button_pressed, bm1_MFD)
                else:
                    button_pressed.update_state()
                #print("MFD: " + button_pressed.name + ", State: " + str(button_pressed.state))
            if mods & pygame.KMOD_ALT:
                button_pressed.reset_state()

    if event.type == EVENT_APP_LOOP:
        tick_button_states(bm1_MFD)

    journal_updates = journal_evh.get_updates()
    if journal_updates:
        for j in journal_updates:
            #print(j)
            Journal.parser(j, my_ship)
        Journal.display(rp1_MFD, my_ship, milkyway)

    #show_button_states(bm1_MFD)
    draw_background(mfd, img_MFD)
    draw_button_states(mfd, bm1_MFD)
    draw_panel(mfd, rpanel, rp1_MFD, True)
    draw_panel(mfd, mpanel, mp1_MFD)
    pygame.display.flip()

    if not milkyway.loaded:
        milkyway.load_data()


# End While

