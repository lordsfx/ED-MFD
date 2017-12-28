import sys, pygame
import json
from mfd_interface import *
from pygame.locals import *
pygame.init()

# param
scale = 1
if len(sys.argv) > 1:
    scale = float(sys.argv[1])
Scale.set(scale)

# state file
FN_MFD_STATE = "mfd.json"

# set stage
pygame.display.set_caption("Elite:Dangerous MFD")
img_MFD = pygame.image.load("images/MFD-Display-BG3-wallpaper.png")
APP_WIDTH, APP_HEIGHT = img_MFD.get_rect().size
APP_SIZE = APP_WIDTH, APP_HEIGHT
mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF|NOFRAME)
img_MFD = img_MFD.convert()
font = pygame.font.Font("fonts/Eurostile.ttf", FONT_SIZE)

blur_MFD = pygame.Surface(APP_SIZE)
blur_MFD.fill(COLOR_GREY)
blur_MFD.set_alpha(20, RLEACCEL)
layer_BTN = pygame.image.load("images/MFD-Display-BG3-button.png").convert_alpha()

img_MFD.blit(blur_MFD, (0, 0))
img_MFD.blit(layer_BTN, (0, 0))

BTN1_SIZE = BTN1_WIDTH, BTN1_HEIGHT = Scale.d(112), Scale.d(50)
TIMER_LOOP = Button.TIMER_STEP * 10

MFD_RP_SIZE = Scale.d(MFD_RP_WIDTH), Scale.d(MFD_RP_HEIGHT)
MFD_RP_XY = Scale.d(MFD_RP_X), Scale.d(MFD_RP_Y)

# common functions

def draw_background(surface):
    surface.blit(img_MFD, (0,0))

# Button actions

def show_button_states(buttons):
    for b in buttons:
       if b:
           print(str(b.state) + " ", end="")
       else:
           print("0 ", end="")
    print(end="\r")

def switch_group_states(this_button, buttons):
    for b in buttons:
       if b and b.type == this_button.type:
          if b == this_button:
             this_button.update_state()
          else:
             b.reset_state()

def draw_button_states(surface, buttons):
    for b in buttons:
        if b and b.activated():
            if b.type == Button.TYPE_HOLD:
                _width = int(BTN1_WIDTH * (Button.TIMER_HOLD - b.timer) / (Button.TIMER_HOLD * 0.7))
                if _width > BTN1_WIDTH: _width = BTN1_WIDTH
                _style = b.style.subsurface( (0, 0), (_width, BTN1_HEIGHT) )
                surface.blit(_style, b.get_offset())
            else:
                surface.blit(b.style, b.get_offset())

def tick_button_states(buttons):
    for b in buttons:
        if b: b.tick()

def load_button_states(buttons):
    try:
        with open(FN_MFD_STATE) as ifn:
            js = json.load(ifn)
            bi = 0
            for state in js:
                if buttons[bi]:
                    buttons[bi].set_state(state)
                bi += 1
        return True
    except EnvironmentError:
        return False

def save_button_states(buttons):
    try:
        states = []
        for b in buttons:
            if b:
                states.append(b.state)
            else:
                states.append(0)
        with open(FN_MFD_STATE, 'w') as ofn:
            json.dump(states, ofn)
        return True
    except EnvironmentError:
        return False

# init buttons

button_ORANGE = pygame.Surface(BTN1_SIZE)
button_ORANGE.fill(COLOR_ORANGE)
button_ORANGE.set_alpha(90, RLEACCEL)
button_GREEN = pygame.Surface(BTN1_SIZE)
button_GREEN.fill(COLOR_GREEN)
button_GREEN.set_alpha(90, RLEACCEL)

bm1_MFD = [ None,	# 0
    Button("SYS Full"    , Scale.d(MFD_XC1), Scale.d(MFD_YT1), button_ORANGE, Button.TYPE_SWITCH_1),	# 1
    Button("ENG Full"    , Scale.d(MFD_XC2), Scale.d(MFD_YT1), button_ORANGE, Button.TYPE_SWITCH_1),	# 2
    Button("WEP Full"    , Scale.d(MFD_XC3), Scale.d(MFD_YT1), button_ORANGE, Button.TYPE_SWITCH_1),	# 3
    Button("ENG 4+SYS 2" , Scale.d(MFD_XC4), Scale.d(MFD_YT1), button_ORANGE, Button.TYPE_SWITCH_1),	# 4
    Button("WEP 4+SYS 2" , Scale.d(MFD_XC5), Scale.d(MFD_YT1), button_ORANGE, Button.TYPE_SWITCH_1),	# 5
    Button("Heat Sink"   , Scale.d(MFD_XR1), Scale.d(MFD_YC1), button_GREEN),	# 6
    Button("Silent Run"  , Scale.d(MFD_XR1), Scale.d(MFD_YC2), button_GREEN, Button.TYPE_TOGGLE),	# 7
    Button("Chaff"       , Scale.d(MFD_XR1), Scale.d(MFD_YC3), button_GREEN),	# 8
    Button("Shield Cell" , Scale.d(MFD_XR1), Scale.d(MFD_YC4), button_GREEN),	# 9
    Button("Disco Scan"  , Scale.d(MFD_XR1), Scale.d(MFD_YC5), button_ORANGE, Button.TYPE_HOLD),	# 10
    Button("Orbit Lines" , Scale.d(MFD_XC5), Scale.d(MFD_YB1), button_GREEN, Button.TYPE_TOGGLE),	# 11
    Button("Ship Lights" , Scale.d(MFD_XC4), Scale.d(MFD_YB1), button_GREEN, Button.TYPE_TOGGLE),	# 12
    Button("Landing Gear", Scale.d(MFD_XC3), Scale.d(MFD_YB1), button_GREEN, Button.TYPE_TOGGLE),	# 13
    None, None, None, None, None,	# 14 - 18
    Button("Cargo Scoop" , Scale.d(MFD_XL1), Scale.d(MFD_YC2), button_GREEN, Button.TYPE_TOGGLE),	# 19
    Button("Hard Points" , Scale.d(MFD_XL1), Scale.d(MFD_YC1), button_GREEN, Button.TYPE_TOGGLE),	# 20
    None, None, None, None, None, None, None, None ]	# 21 - 28

# Panel actions

def draw_panel(surface, panel):
    panelbox = pygame.Surface(MFD_RP_SIZE)
    panelbox.fill((64,64,64))
    panelbox.set_alpha(120, RLEACCEL)
    mfd.blit(panelbox, MFD_RP_XY)
    panel.render_panel(mfd, font)

# init panels

rpanel = pygame.Surface( (Scale.d(MFD_RP_WIDTH), Scale.d(MFD_RP_HEIGHT)) )
rp1_MFD = Panel(Scale.d(MFD_RP_X), Scale.d(MFD_RP_Y), Scale.d(MFD_RP_WIDTH), Scale.d(MFD_RP_HEIGHT))
rp1_MFD.add_image("images/EliteDangerous_Logo.png")
rp1_MFD.add_text(["", "Created by CMDR Lord Shadowfax"])
rp1_MFD.add_text(["Elite:Dangerous MFD"])

Coriolis.init()
last_pad = 0
#rp1_MFD.add_coriolis(last_pad)

# set init background
mfd.blit(img_MFD, (0, 0))
noframe = True

# load last states, if any
if load_button_states(bm1_MFD):
    print("Loaded last states - ")
    #show_button_states(bm1_MFD)
    draw_background(mfd)
    draw_button_states(mfd, bm1_MFD)
    pygame.display.flip()

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
        if event.key == pygame.K_a:  joy_index = 1       # SYS - Full
        if event.key == pygame.K_b:  joy_index = 2       # ENG - Full
        if event.key == pygame.K_c:  joy_index = 3       # WEP - Full
        if event.key == pygame.K_d:  joy_index = 4       # ENG 4 + SYS 2
        if event.key == pygame.K_e:  joy_index = 5       # WEP 4 + SYS 2
        if event.key == pygame.K_f:  joy_index = 6       # Heat Sink
        if event.key == pygame.K_g:  joy_index = 7       # Silent Run
        if event.key == pygame.K_h:  joy_index = 8       # Chaff
        if event.key == pygame.K_i:  joy_index = 9       # Shield Cell
        if event.key == pygame.K_j:  joy_index = 10      # Disco Scan
        if event.key == pygame.K_k:  joy_index = 20      # Hard Points
        if event.key == pygame.K_l:  joy_index = 19      # Cargo Scoop
        if event.key == pygame.K_m:  joy_index = 13      # Landing Gear
        if event.key == pygame.K_n:  joy_index = 12      # Ship Lights
        if event.key == pygame.K_o:  joy_index = 11      # Orbit Lines
        if joy_index > 0:
            button_pressed = bm1_MFD[joy_index]

        if event.key == pygame.K_r:         # Ctrl-R : Reset all states
            if mods & pygame.KMOD_CTRL:
                for b in bm1_MFD:
                    if b: b.reset_state()
                print("Reset all states - ")
        if event.key == pygame.K_p:         # Ctrl-P : Coriolis Pad Test
            if mods & pygame.KMOD_CTRL:
                last_pad += 1
                if last_pad > 45: last_pad = 0
                rp1_MFD.add_coriolis(last_pad)
        if event.key == pygame.K_SPACE:
            if noframe:
                mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF|NOFRAME)
                noframe = False
            else:
                mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF)
                noframe = True
        if event.type == QUIT or event.key == pygame.K_ESCAPE:
            save_button_states(bm1_MFD)
            sys.exit()

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

    #show_button_states(bm1_MFD)
    draw_background(mfd)
    draw_button_states(mfd, bm1_MFD)
    draw_panel(rpanel, rp1_MFD)
    pygame.display.flip()
