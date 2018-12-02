import logging
import sys, pygame
import json
from config import *
from mfd_functions import *
from mfd_interface import *
from ed_object import *
from ed_journal import *
from watchdog.observers import Observer

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

# param
scale = 1
if len(sys.argv) > 1:
    scale = float(sys.argv[1])

# set stage
pygame.init()
pygame.display.set_caption(MFD.title)
img_MFD = pygame.image.load(IMAGE_WALLPAPER)
APP_WIDTH, APP_HEIGHT = img_MFD.get_rect().size
APP_SIZE = APP_WIDTH, APP_HEIGHT
mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF|NOFRAME)
img_MFD = img_MFD.convert()
MFD.set_font(DEFAULT_FONT)
MFD.set_scale(scale)

blur_MFD = pygame.Surface(APP_SIZE)
blur_MFD.fill(COLOR_GREY)
blur_MFD.set_alpha(20, RLEACCEL)
layer_BTN = pygame.image.load(IMAGE_BUTTON).convert_alpha()

img_MFD.blit(blur_MFD, (0, 0))
img_MFD.blit(layer_BTN, (0, 0))

TIMER_LOOP = Button.TIMER_STEP * 10

# ED objects
my_ship = Ship()
milkyway = Universe()

# init buttons

bm1_MFD = [ None,	# 0
    Button("SYS Full"    ,  1, MFD_XC1, MFD_YT1, COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 1
    Button("ENG Full"    ,  2, MFD_XC2, MFD_YT1, COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 2
    Button("WEP Full"    ,  3, MFD_XC3, MFD_YT1, COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 3
    Button("ENG 4+SYS 2" ,  4, MFD_XC4, MFD_YT1, COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 4
    Button("WEP 4+SYS 2" ,  5, MFD_XC5, MFD_YT1, COLOR_ORANGE, Button.TYPE_SWITCH_1),	# 5
    Button("Heat Sink"   ,  6, MFD_XR1, MFD_YC1, COLOR_GREEN),	# 6
    Button("Silent Run"  ,  7, MFD_XR1, MFD_YC2, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 7
    Button("Chaff"       ,  8, MFD_XR1, MFD_YC3, COLOR_GREEN),	# 8
    Button("Shield Cell" ,  9, MFD_XR1, MFD_YC4, COLOR_GREEN),	# 9
    Button("Disco Scan"  , 10, MFD_XR1, MFD_YC5, COLOR_ORANGE, Button.TYPE_HOLD),	# 10
    Button("Orbit Lines" , 11, MFD_XC5, MFD_YB1, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 11
    Button("Ship Lights" , 12, MFD_XC4, MFD_YB1, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 12
    Button("Landing Gear", 13, MFD_XC3, MFD_YB1, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 13
    None, None, None, None, 							# 14 - 17
    Button("Docking Req" , 18, MFD_XL1, MFD_YC3, COLOR_ORANGE),	# 18
    Button("Cargo Scoop" , 19, MFD_XL1, MFD_YC2, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 19
    Button("Hard Points" , 20, MFD_XL1, MFD_YC1, COLOR_GREEN,  Button.TYPE_TOGGLE),	# 20
    None, None, None, None, None, None, None, None ]	# 21 - 28

# init panels

# right panel
MFD_RP_SIZE = MFD.sd(MFD_RP_WIDTH), MFD.sd(MFD_RP_HEIGHT)
MFD_RP_XY = MFD.sd(MFD_RP_X), MFD.sd(MFD_RP_Y)

rpanel = pygame.Surface( (MFD.sd(MFD_RP_WIDTH), MFD.sd(MFD_RP_HEIGHT)) )
rp1_MFD = Panel(MFD.sd(MFD_RP_X), MFD.sd(MFD_RP_Y), MFD.sd(MFD_RP_WIDTH), MFD.sd(MFD_RP_HEIGHT), MFD_RP_ROWS)
#rp1_MFD.add_image("images/EliteDangerous_Logo.png")
#rp1_MFD.add_text(["Hello World, the quick brown fox jumps over the lazy dog."])
rp1_MFD.add_text(["Created by CMDR Lord Shadowfax"], COLOR_GREEN)
rp1_MFD.add_text(["Elite:Dangerous MFD v" + MFD_VER], COLOR_GREEN)
rp1_MFD.add_text(["", "Loading universe data ..."])

# mid panel
MFD_MP_SIZE = MFD.sd(MFD_MP_WIDTH), MFD.sd(MFD_MP_HEIGHT)
MFD_MP_XY = MFD.sd(MFD_MP_X), MFD.sd(MFD_MP_Y)

mpanel = pygame.Surface( (MFD.sd(MFD_MP_WIDTH), MFD.sd(MFD_MP_HEIGHT)) )
mp1_MFD = Panel(MFD.sd(MFD_MP_X), MFD.sd(MFD_MP_Y), MFD.sd(MFD_MP_WIDTH), MFD.sd(MFD_MP_HEIGHT), MFD_MP_ROWS)
draw_logo(mp1_MFD)

# upper panel
MFD_UP_SIZE = MFD.sd(MFD_UP_WIDTH), MFD.sd(MFD_UP_HEIGHT)
MFD_UP_XY = MFD.sd(MFD_UP_X), MFD.sd(MFD_UP_Y)

upanel = pygame.Surface( (MFD.sd(MFD_UP_WIDTH), MFD.sd(MFD_UP_HEIGHT)) )
up1_MFD = Panel(MFD.sd(MFD_UP_X), MFD.sd(MFD_UP_Y), MFD.sd(MFD_UP_WIDTH), MFD.sd(MFD_UP_HEIGHT), MFD_UP_ROWS, MFD_UP_FONT_SIZE)
up1_MFD.add_text([" MODE : NORMAL"], COLOR_GREEN)

# misc init
last_pad = 0
redraw_display = True

# set init background
mfd.blit(img_MFD, (0, 0))
noframe = True

# load last states, if any
if load_button_states(bm1_MFD):
    #logger.debug("Loaded last states - ")
    #show_button_states(bm1_MFD)
    draw_background(mfd, img_MFD)
    draw_button_states(mfd, bm1_MFD)
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
milkyway.thread_load_data(rp1_MFD)

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
            redraw_display = True

        if event.key == pygame.K_x:         # Ctrl-X : Reset all states
            if mods & pygame.KMOD_CTRL:
                for b in bm1_MFD:
                    if b: b.reset_state()
                rp1_MFD.add_text(["- reset all states"])
                redraw_display = True
        if event.key == pygame.K_p:         # Ctrl-P : Coriolis Pad Test
            if mods & pygame.KMOD_CTRL:
                last_pad += 1
                if last_pad > 45: last_pad = 0
                rp1_MFD.add_coriolis(last_pad, Coriolis(MFD_RP_WIDTH))
                redraw_display = True
        if event.key == pygame.K_0:         # Ctrl-0 : Coriolis All Pads
            if mods & pygame.KMOD_CTRL:
                mp1_MFD.clear_all()
                mp1_MFD.add_coriolis(0, Coriolis(MFD_MP_WIDTH))
                mp1_MFD.add_text([""])
                redraw_display = True
        if event.key == pygame.K_r:         # Ctrl-R : Refresh EDDB data
            milkyway.thread_refresh_eddb(rp1_MFD)
            redraw_display = True
        if event.key == pygame.K_SPACE:
            if noframe:
                mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF|NOFRAME)
                noframe = False
            else:
                mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF)
                noframe = True
            redraw_display = True
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
                #logger.debug("MFD: " + button_pressed.name + ", State: " + str(button_pressed.state))
            if mods & pygame.KMOD_ALT:
                button_pressed.reset_state()
            redraw_display = True

    if event.type == EVENT_APP_LOOP:
        if tick_button_states(bm1_MFD):
            redraw_display = True

    journal_updates = journal_evh.get_updates()
    if journal_updates:
        for j in journal_updates:
            #logger.debug(j)
            Journal.parser(j, my_ship)
        Journal.display([rp1_MFD, mp1_MFD], my_ship, milkyway, bm1_MFD)
        redraw_display = True

    #show_button_states(bm1_MFD)
    if redraw_display:
        draw_background(mfd, img_MFD)
        draw_panel(mfd, rpanel, rp1_MFD, True)
        draw_panel(mfd, mpanel, mp1_MFD)
        draw_panel(mfd, upanel, up1_MFD)
        draw_button_states(mfd, bm1_MFD)
        pygame.display.flip()
        redraw_display = False


# End While

