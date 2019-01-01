import sys, pygame
import json
from mfd_interface import *
from pygame.locals import *

# draw MFD

def draw_background(surface, img_MFD):
    surface.blit(img_MFD, (0,0))

def draw_panel(mfd, surface, panel, add_shade=False, img_lib=None):
    panelbox = pygame.Surface(panel.get_size())
    if add_shade:
        panelbox.fill(COLOR_SHADE)
    panelbox.set_alpha(120, RLEACCEL)
    mfd.blit(panelbox, panel.get_offset())
    panel.render_panel(mfd)
    if img_lib:
        if MFD.show_stkbtn and panel.mfd_mode == MFD_MODE_NORMAL and not MFD.temp_hide_stkbtn:
            mfd.blit(img_lib.STKBTN, panel.get_offset())
        if panel.mfd_mode == MFD_MODE_COMBAT:
            mfd.blit(img_lib.STKBTN, panel.get_offset())
        if panel.mfd_mode == MFD_MODE_EXPLORE:
            mfd.blit(img_lib.FSS, panel.get_offset())
    #print("+", end="", flush=True)

def draw_logo(panel):
    panel.clear_all()
    panel.add_image(IMAGE_ED_LOGO)
    #panel.add_text([""])

def draw_mode_status(mfd, mfd_mode, img_lib):
    # mode
    for m in range(0, len(MFD.MFD_MODE)):
        if (m + 1) == MFD.mode:
            mfd.blit(img_lib.MODE, mfd_mode.ind_xy[m], mfd_mode.ind_area[m])
    # status
    for s in range(0, len(MFD.LP_STATUS)):
        if MFD.get_lp_status(s):
            mfd.blit(img_lib.MODE, mfd_mode.sts_xy[s], mfd_mode.sts_area[s])

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
    if ship.cargo_capacity > 0:
        _all_text.append( ("  In ship : %dt / %dt" % (ship.cargo_ship_count, ship.cargo_capacity), COLOR_ORANGE) )
    else:
        _all_text.append( ("  In ship : %dt" % ship.cargo_ship_count, COLOR_ORANGE) )
    if ship.cargo_srv_count > 0:
        _all_text.append( ("  In SRV : %dt" % ship.cargo_srv_count, COLOR_ORANGE) )
    if ship.cargo_ship_inventory:
        _all_text.append( (" ", COLOR_GREEN) )
        _all_text.append( ("Ship Inventory", COLOR_GREEN) )
        for _inv in ship.cargo_ship_inventory:
            _name = _inv["Name"]
            if "Name_Localised" in _inv: _name = _inv["Name_Localised"]
            if "Stolen" in _inv:
                _stolen = int(_inv["Stolen"])
                if _stolen > 0: str_stolen = " (%dt stolen)" % _stolen
                else: str_stolen = ""
            _all_text.append( ("  %s : %dt%s" % (_name.capitalize(), _inv["Count"], str_stolen), COLOR_ORANGE) )

    panel.clear_all()
    for _text in reversed(_all_text):
        panel.add_text( [ _text[0] ], _text[1] )

def show_details_hardpoint(panel, ship, ref_data):
    _all_text = []
    if ship.hardpoint_large:
        _all_text.append( ("Large Hardpoints", COLOR_GREEN) )
        for _hp in ship.hardpoint_large:
            _item_name = _hp[1]
            _full_name = ref_data.get_item_full_name(_item_name)
            _priority = int(_hp[2]) + 1
            if _full_name: _item_name = _full_name
            _all_text.append( ("  %s  < %d >" % (_item_name, _priority), COLOR_ORANGE) )
    if ship.hardpoint_medium:
        _all_text.append( ("Medium Hardpoints", COLOR_GREEN) )
        for _hp in ship.hardpoint_medium:
            _item_name = _hp[1]
            _full_name = ref_data.get_item_full_name(_item_name)
            _priority = int(_hp[2]) + 1
            if _full_name: _item_name = _full_name
            _all_text.append( ("  %s  < %d >" % (_item_name, _priority), COLOR_ORANGE) )
    if ship.hardpoint_tiny:
        _all_text.append( (" ", COLOR_GREEN) )
        _all_text.append( ("Utility Mounts", COLOR_GREEN) )
        for _hp in ship.hardpoint_tiny:
            _item_name = _hp[1]
            _full_name = ref_data.get_item_full_name(_item_name)
            _priority = int(_hp[2]) + 1
            if _full_name: _item_name = _full_name
            _all_text.append( ("  %s  < %d >" % (_item_name, _priority), COLOR_ORANGE) )

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

def load_mfd_states(MFD):
    buttons = MFD.bmp
    try:
        with open(MFD.state_file) as ifn:
            js = json.load(ifn)
            logger.debug("buttons = %s" % js["buttons"])
            bi = 0
            for b in js["buttons"]:
                if buttons[bi]:
                    buttons[bi].set_state(b)
                bi += 1
            logger.debug("stkbtn = %s" % js["stkbtn"])
            if js["stkbtn"]:
                MFD.set_show_stick_buttons(True)
            else:
                MFD.set_show_stick_buttons(False)
        return True
    except EnvironmentError:
        return False

def save_mfd_states(MFD):
    buttons = MFD.bmp
    try:
        _b_states = []
        for b in buttons:
            if b:
                _b_states.append(b.state)
            else:
                _b_states.append(0)
        states = { 'buttons': _b_states, 'stkbtn': MFD.show_stkbtn }
        with open(MFD.state_file, 'w') as ofn:
            json.dump(states, ofn)
        return True
    except EnvironmentError:
        return False
