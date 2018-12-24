import sys, pygame
import json
from mfd_interface import *
from pygame.locals import *

# draw MFD

def draw_background(surface, img_MFD):
    surface.blit(img_MFD, (0,0))

def draw_panel(mfd, surface, panel, add_shade=False, img_stkbtn=None):
    panelbox = pygame.Surface(panel.get_size())
    if add_shade:
        panelbox.fill(COLOR_SHADE)
    panelbox.set_alpha(120, RLEACCEL)
    mfd.blit(panelbox, panel.get_offset())
    panel.render_panel(mfd)
    if panel.mfd_mode == MFD_MODE_NORMAL:
        mfd.blit(img_stkbtn, panel.get_offset())
    #print("+", end="", flush=True)

def draw_logo(panel):
    panel.clear_all()
    panel.add_image(IMAGE_ED_LOGO)
    #panel.add_text([""])

def draw_mode(mfd, mfd_mode, img_mode):
    for m in range(0, len(MFD.MFD_MODE)):
        if (m + 1) == MFD.mode:
            mfd.blit(img_mode, mfd_mode.ind_xy[m], mfd_mode.ind_area[m])

def show_details_explore(panel, ship, star_class=None):
    _all_text = []
    _all_text.append( ("Current Location", COLOR_GREEN) )
    _loc = "  "
    if ship.at_station: _loc += "%s / " % ship.at_station
    if ship.at_system:
        _loc += ship.at_system
        _all_text.append( (_loc, COLOR_ORANGE) )
    if ship.fsd_target:
        _all_text.append( (" ", COLOR_GREEN) )
        _all_text.append( ("Next Jump", COLOR_GREEN) )
        _all_text.append( ("  %s" % ship.fsd_target, COLOR_ORANGE) )
        if star_class:
            _all_text.append( ("  Class %s" % star_class, COLOR_ORANGE) )

    panel.clear_all()
    for _text in reversed(_all_text):
        panel.add_text( [ _text[0] ], _text[1] )

def show_details_cargo(panel, ship):
    _all_text = []
    _all_text.append( ("Cargo", COLOR_GREEN) )
    _all_text.append( ("  In ship: %d" % ship.cargo_ship_count, COLOR_ORANGE) )
    if ship.cargo_srv_count > 0:
        _all_text.append( ("  In SRV: %d" % ship.cargo_srv_count, COLOR_ORANGE) )

    panel.clear_all()
    for _text in reversed(_all_text):
        panel.add_text( [ _text[0] ], _text[1] )

# button actions

def show_button_states(buttons):
    for (i, b) in enumerate(buttons):
       if i > 0:
          if b:
             print("%d:%s " % (i, str(b.state)), end="")
          else:
             print("0 ", end="")
          if i % 5 == 0:
             print(" ", end="")
    print(end="\r")

def switch_group_states(this_button, buttons):
    for b in buttons:
       if b and b.type == this_button.type:
          if b == this_button:
             #this_button.update_state()
             this_button.set_state(Button.STATE_ON)
          else:
             b.reset_state()

def draw_button_states(surface, buttons):
    for b in buttons:
        if b and b.activated():
            if b.type == Button.TYPE_HOLD:
                _width = int(b.width * (Button.TIMER_HOLD - b.timer) / (Button.TIMER_HOLD * 0.7))
                if _width > b.width: _width = b.width
                _style = b.style.subsurface( (0, 0), (_width, b.height) )
                surface.blit(_style, b.get_offset())
            else:
                surface.blit(b.style, b.get_offset())

def tick_button_states(buttons):
    tbc = False
    for b in buttons:
        if b and (b.type == Button.TYPE_HOLD or b.type == Button.TYPE_PUSH):
            if b.activated(): tbc = True
            b.tick()
    return tbc

def load_button_states(buttons):
    try:
        with open(MFD.state_file) as ifn:
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
        with open(MFD.state_file, 'w') as ofn:
            json.dump(states, ofn)
        return True
    except EnvironmentError:
        return False
