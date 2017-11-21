import sys, pygame
from pygame.locals import *
pygame.init()

# param
scale = 1
if len(sys.argv) > 1:
    scale = float(sys.argv[1])

def scaled(n):
    return int(n*scale)

# statics
pygame.display.set_caption("Elite:Dangerous MFD")

img_MFD = pygame.image.load('MFD-Display-BG3-wallpaper.png')
APP_WIDTH, APP_HEIGHT = img_MFD.get_rect().size
APP_SIZE = APP_WIDTH, APP_HEIGHT
mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF|NOFRAME)
img_MFD = img_MFD.convert()

img_BTN = pygame.image.load('MFD-Display-BG3-button.png').convert_alpha()
img_MFD.blit(img_BTN, (0, 0))

BTN1_SIZE = BTN1_WIDTH, BTN1_HEIGHT = scaled(110), scaled(50)
TIMER_STEP = 5	# milliseconds
TIMER_LOOP = TIMER_STEP * 10

# color
COLOR_ORANGE = (255, 153, 51)
COLOR_GREEN  = ( 51, 255, 51)

# MFD Layout
#     X L C1 C2 C3 C4 C5 R       Y
# |28|    01 02 03 04 05    |21| T
# |27| 20                06 |22| C1
#      19                07      C2
#      18                08      C3
#      17                09      C4
# |26| 16                10 |23| C5
# |25|    15 14 13 12 11    |24| B

# Positions
MFD_XL1 = 2
MFD_XC3 = 346
MFD_XC4 = 464
MFD_XC5 = 582
MFD_XR1 = 676
MFD_YC1 = 158
MFD_YC2 = 270
MFD_YC3 = 382
MFD_YC4 = 490
MFD_YC5 = 600
MFD_YB1 = 730

# buttons
class Button(object):
    TYPE_PUSH   = 1
    TYPE_TOGGLE = 2
    TYPE_HOLD   = 3
    STATE_RELEASED = STATE_OFF = 0
    STATE_PUSHED   = STATE_ON  = STATE_HOLD = 1
    TIMER_PUSH   = TIMER_STEP * 2
    TIMER_HOLD   = TIMER_STEP * 20
    TIMER_TOGGLE = -1

    def __init__(self, name, pos_x, pos_y, style, _type=TYPE_PUSH, state=STATE_OFF):
        self.name   = name
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.style  = style
        self.type   = _type
        self.state  = state
        self.timer  = 0

    def get_offset(self):
        return (self.pos_x, self.pos_y)

    def get_rect(self):
        return (self.pos_x, self.pos_y, BTN1_WIDTH, BTN1_HEIGHT)

    def update_state(self):
        if self.type == self.TYPE_PUSH:
            self.state = self.STATE_PUSHED
            self.timer = self.TIMER_PUSH
        if self.type == self.TYPE_TOGGLE:
            self.state = (self.state + 1) % 2
            self.timer = self.TIMER_TOGGLE
        if self.type == self.TYPE_HOLD:
            self.state = self.STATE_ON
            self.timer = self.TIMER_HOLD

    def reset_state(self):
        self.state = self.STATE_OFF
        self.timer = 0

    def activated(self):
        if self.state == self.STATE_ON: return True
        else: return False

    def tick(self):
        if self.timer > 0:
            self.timer -= 1
        if self.timer == 0:
            self.state = self.STATE_OFF

def show_button_states(buttons):
    for b in buttons:
       if b:
           print(str(b.state) + " ", end="")
       else:
           print("0 ", end="")
    print(end="\r")

def draw_button_states(surface, buttons):
    surface.blit(img_MFD, (0,0))
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

button_ORANGE = pygame.Surface(BTN1_SIZE)
button_ORANGE.fill(COLOR_ORANGE)
button_ORANGE.set_alpha(90, RLEACCEL)
button_GREEN = pygame.Surface(BTN1_SIZE)
button_GREEN.fill(COLOR_GREEN)
button_GREEN.set_alpha(90, RLEACCEL)

bm1_MFD = [ None,	# 0
    None, None, None, None, None,	# 1 - 5
    Button('Heat Sink'   , scaled(MFD_XR1), scaled(MFD_YC1), button_GREEN),	# 6
    Button('Silent Run'  , scaled(MFD_XR1), scaled(MFD_YC2), button_GREEN, Button.TYPE_TOGGLE),	# 7
    Button('Chaff'       , scaled(MFD_XR1), scaled(MFD_YC3), button_GREEN),	# 8
    Button('Shield Cell' , scaled(MFD_XR1), scaled(MFD_YC4), button_GREEN),	# 9
    Button('Disco Scan'  , scaled(MFD_XR1), scaled(MFD_YC5), button_ORANGE, Button.TYPE_HOLD),	# 10
    Button('Orbit Lines' , scaled(MFD_XC5), scaled(MFD_YB1), button_GREEN, Button.TYPE_TOGGLE),	# 11
    Button('Ship Lights' , scaled(MFD_XC4), scaled(MFD_YB1), button_GREEN, Button.TYPE_TOGGLE),	# 12
    Button('Landing Gear', scaled(MFD_XC3), scaled(MFD_YB1), button_GREEN, Button.TYPE_TOGGLE),	# 13
    None, None, None, None, None,	# 14 - 18
    Button('Cargo Scoop' , scaled(MFD_XL1), scaled(MFD_YC2), button_GREEN, Button.TYPE_TOGGLE),	# 19
    Button('Hard Points' , scaled(MFD_XL1), scaled(MFD_YC1), button_GREEN, Button.TYPE_TOGGLE),	# 20
    None, None, None, None, None, None, None, None ]	# 21 - 28


# set init background
#if scale != 1:
#    img_MFD = pygame.transform.smoothscale(img_MFD, APP_SIZE)
mfd.blit(img_MFD, (0, 0))
noframe = True

# user event timer
pygame.time.set_timer(pygame.USEREVENT, TIMER_LOOP)

# loop
while True:

    event = pygame.event.wait()

    if event.type == QUIT: sys.exit()
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        button_pressed = None
        if event.key == pygame.K_1:         # Heat Sink
            button_pressed = bm1_MFD[6]
        if event.key == pygame.K_2:         # Silent Run
            button_pressed = bm1_MFD[7]
        if event.key == pygame.K_3:         # Chaff
            button_pressed = bm1_MFD[8]
        if event.key == pygame.K_4:         # Shield Cell
            button_pressed = bm1_MFD[9]
        if event.key == pygame.K_5:         # Disco Scan
            button_pressed = bm1_MFD[10]
        if event.key == pygame.K_6:         # Hard Points
            button_pressed = bm1_MFD[20]
        if event.key == pygame.K_7:         # Cargo Scoop
            button_pressed = bm1_MFD[19]
        if event.key == pygame.K_8:         # Landing Gear
            button_pressed = bm1_MFD[13]
        if event.key == pygame.K_9:         # Ship Lights
            button_pressed = bm1_MFD[12]
        if event.key == pygame.K_0:         # Orbit Lines
            button_pressed = bm1_MFD[11]
        if event.key == pygame.K_r:         # Ctrl-R : Reset all states
            if mods & pygame.KMOD_CTRL:
                for b in bm1_MFD:
                    if b: b.reset_state()
                print("Reset all states - ")
        if event.key == pygame.K_SPACE:
            if noframe:
                mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF|NOFRAME)
                noframe = False
            else:
                mfd = pygame.display.set_mode(APP_SIZE, DOUBLEBUF)
                noframe = True
        if event.key == pygame.K_ESCAPE: sys.exit()

        if button_pressed:
            button_pressed.update_state()
            #print("MFD: " + button_pressed.name + ", State: " + str(button_pressed.state))

    if event.type == pygame.USEREVENT:
        tick_button_states(bm1_MFD)

    show_button_states(bm1_MFD)
    draw_button_states(mfd, bm1_MFD)
    pygame.display.flip()
