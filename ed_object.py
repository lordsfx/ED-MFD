import logging
from common import *
import os
import json
import threading
import errno
from config import *
from constants import *
from ed_const import *
from mfd_functions import *
from mfd_interface import Button
from library import *
from eddb import *

class Ship:
    PIP_SYS = 0
    PIP_ENG = 1
    PIP_WEP = 2

    def __init__(self):
        self.status = Status()
        self.event_memory = {}
        self.at_system = None
        self.at_station = None
        self.pips = [0, 0, 0]
        self.pips_set = 0
        self.firegroup = 0
        self.guifocus = 0
        self.fuel = 0
        self.bearings = (0, 0, 0, 0)	# (Latitude, Longitude, Heading, Altitude)
        self.fsd_target = None
        self.cargo_ship_count = 0
        self.cargo_srv_count = 0
        self.cargo_ship_inventory = None
        self.cargo_srv_inventory = None
        self.modules = None
        self.hardpoint_tiny = []
        self.hardpoint_medium = []
        self.hardpoint_large = []
        self.cargo_capacity = 0

    def export_states(self):
        return (self.at_system, self.at_station)

    def import_states(self, _states):
        self.at_system = _states[0]
        self.at_station = _states[1]
        return

    def update_event_memory(self, j_event):
        self.event_memory[j_event["event"]] = ( True, j_event )		# New event = True, Event from Journal

    def get_event_memory(self):
        return self.event_memory

    def event_is_updated(self, event_type):
        return self.event_memory[event_type][0]

    def mark_event_processed(self, event_type):
        temp_mem = self.event_memory[event_type][1]
        self.event_memory[event_type] = ( False, temp_mem )

    def set_at_system(self, system):
        self.at_system = system
        logger.debug("At system: %s" % self.at_system)

    def set_at_station(self, station):
        self.at_station = station
        logger.debug("At station: %s" % self.at_station)

    def set_fsd_target(self, system):
        self.fsd_target = system
        logger.debug("FSD target: %s" % self.fsd_target)

    def update_cargo_count(self, vessel, count):
        if vessel == "Ship":
            self.cargo_ship_count = int(count)
            logger.debug("Ship Cargo count: %d" % self.cargo_ship_count)
        else:
            self.cargo_srv_count = int(count)
            logger.debug("SRV Cargo count: %d" % self.cargo_srv_count)

    def update_cargo_inventory(self, vessel, inventory):
        if vessel == "Ship":
            self.cargo_ship_inventory = inventory
            logger.debug("Ship Cargo inventory: %s" % self.cargo_ship_inventory)
        else:
            self.cargo_srv_inventory = int(inventory)
            logger.debug("SRV Cargo inventory: %s" % self.cargo_srv_inventory)

    def update_modules(self, modules):
        self.modules = modules
        self.hardpoint_tiny = []
        self.hardpoint_medium = []
        self.hardpoint_large = []
        # hardpoints
        for m in self.modules:
            if "Hardpoint" in m["Slot"]:
                logger.debug("Module: %s / %s" % (m["Slot"], m["Item"]))
                if "Tiny" in m["Slot"]:
                    self.hardpoint_tiny.append( (m["Slot"], m["Item"], m["Priority"]) )
                if "Medium" in m["Slot"]:
                    self.hardpoint_medium.append( (m["Slot"], m["Item"], m["Priority"]) )
                if "Large" in m["Slot"]:
                    self.hardpoint_large.append( (m["Slot"], m["Item"], m["Priority"]) )
        self.hardpoint_tiny.sort()
        self.hardpoint_medium.sort()
        self.hardpoint_large.sort()
        # cargos
        self.cargo_capacity = 0
        for m in self.modules:
            if "int_cargorack" in m["Item"]:
                logger.debug("Module: %s / %s" % (m["Slot"], m["Item"]))
                _item_size = m["Item"].split("_")[2]
                self.cargo_capacity += Item_Size.CargoRack[_item_size]

    def update_status_flags(self, _flags, buttons, panel):
        self.status.update_flags(_flags)
        logger.debug("Flags: %s" % _flags)
        for _sf in Status.get_ship_flags():
            if self.status.is_flagged(_sf):
                logger.debug("- Status: %s" % _sf)
        # MFD_SILENTRUN
        if self.status.is_flagged("silent_run"):
            buttons[MFD_SILENTRUN].set_state(Button.STATE_ON)
        else:
            buttons[MFD_SILENTRUN].set_state(Button.STATE_OFF)
        # MFD_HARDPOINT
        if self.status.is_flagged("hardpoint"):
            buttons[MFD_HARDPOINT].set_state(Button.STATE_ON)
        else:
            buttons[MFD_HARDPOINT].set_state(Button.STATE_OFF)
        # MFD_CARGOSCOOP
        if self.status.is_flagged("cargo_scoop"):
            buttons[MFD_CARGOSCOOP].set_state(Button.STATE_ON)
        else:
            buttons[MFD_CARGOSCOOP].set_state(Button.STATE_OFF)
        # MFD_LANDING
        if self.status.is_flagged("gear_down"):
            buttons[MFD_LANDING].set_state(Button.STATE_ON)
        else:
            buttons[MFD_LANDING].set_state(Button.STATE_OFF)
        # MFD_LIGHTS
        if self.status.is_flagged("lights"):
            buttons[MFD_LIGHTS].set_state(Button.STATE_ON)
        else:
            buttons[MFD_LIGHTS].set_state(Button.STATE_OFF)
        # MFD_N_VISION
        if self.status.is_flagged("nightvision"):
            buttons[MFD_N_VISION].set_state(Button.STATE_ON)
        else:
            buttons[MFD_N_VISION].set_state(Button.STATE_OFF)
        # MFD_HUD
        if self.status.is_flagged("in_analysis"):
            panel.add_text([ "  ANALYSIS MODE" ])
            MFD.set_lp_status(STS_ANALYSIS, True)
            MFD.set_lp_status(STS_COMBAT, False)
        else:
            panel.add_text([ "  COMBAT MODE" ])
            MFD.set_lp_status(STS_ANALYSIS, False)
            MFD.set_lp_status(STS_COMBAT, True)
        # FSD Cooldown
        if self.status.is_flagged("fsd_cooldown"):
            MFD.set_lp_status(STS_COOLDOWN, True)
        else:
            MFD.set_lp_status(STS_COOLDOWN, False)
        # FSD Masslock
        if self.status.is_flagged("fsd_masslock"):
            MFD.set_lp_status(STS_MASSLOCK, True)
        else:
            MFD.set_lp_status(STS_MASSLOCK, False)

    def update_status_pips(self, _pips, buttons):
        self.pips = _pips
        logger.debug("SYS:%d ENG:%d WEP:%d" % (self.pips[Ship.PIP_SYS], self.pips[Ship.PIP_ENG], self.pips[Ship.PIP_WEP]))
        if self.pips[Ship.PIP_ENG] == 8 and self.pips[Ship.PIP_SYS] == 4:
            self.pips_set = MFD_ENG4_SYS2
        elif self.pips[Ship.PIP_WEP] == 8 and self.pips[Ship.PIP_SYS] == 4:
            self.pips_set = MFD_WEP4_SYS2
        elif self.pips[Ship.PIP_SYS] == 8:
            self.pips_set = MFD_SYS_FULL
        elif self.pips[Ship.PIP_ENG] == 8:
            self.pips_set = MFD_ENG_FULL
        elif self.pips[Ship.PIP_WEP] == 8:
            self.pips_set = MFD_WEP_FULL
        elif self.pips[Ship.PIP_SYS] == 6:
            self.pips_set = MFD_SYS_3
        elif self.pips[Ship.PIP_ENG] == 6:
            self.pips_set = MFD_ENG_3
        elif self.pips[Ship.PIP_WEP] == 6:
            self.pips_set = MFD_WEP_3
        else:
            if self.pips_set > 0:
                buttons[self.pips_set].set_state(Button.STATE_OFF)
                self.pips_set = 0

        if self.pips_set > 0:
            switch_group_states(buttons[self.pips_set], buttons)
        return

    def update_status_firegroup(self, _firegroup, buttons):
        self.firegroup = _firegroup
        #logger.debug("Fire Group: %s" % self.firegroup)
        return

    def update_status_guifocus(self, _guifocus, buttons, panel):
        self.guifocus = _guifocus
        logger.debug("GUI Focus: %s" % self.guifocus)
        # MFD_FSS
        if self.guifocus == GUI_MODE_FSS:
            panel.add_text([ "  FSS ON" ])
            MFD.set_lp_status(STS_FSS, True)
        else:
            panel.add_text([ " " ])
            MFD.set_lp_status(STS_FSS, False)
        return

    def update_status_fuel(self, _fuel, buttons):
        self.fuel = _fuel
        #logger.debug("Fuel (tons): %s" % self.fuel)
        return

    def update_status_bearings(self, _lat, _long, _head, _alt):
        self.bearings = (float(_lat), float(_long), int(_head), int(_alt))
        #logger.debug("Lat / Long: %f / %f\tHead / Alt: %d / %d" % self.bearings)
        return

    def get_status(self):
        return self.status


class System:
    def __init__(self, _id, _name):
        self.id = _id
        self.name = _name

    @staticmethod
    def load_systems(fn):
        systemObj = []
        try:
            systemJSON = json.load(open(fn))
            _total = len(systemJSON)
            print("Loading Systems [%d] " % _total, end="", flush=True)
            for i, s in enumerate(systemJSON):
                systemObj.append( System(s["id"], s["name"]) )
                if i % 1000 == 0: print(".", end="", flush=True)
            print(" completed")
        except (OSError, IOError) as e:
            if getattr(e, 'errno', 0) == errno.ENOENT:
                logger.error("File %s not found, ignored..." % fn)
        return systemObj


class Universe:
    is_loading = False
    is_loaded = False
    is_refreshing_db = False

    def __init__(self):
        self.system_data = None
        self.station_data = None

    def load_data(self, _info_panel):
        self.system_data  = System.load_systems(os.path.join(EDDB_PATH, EDDB_SYSTEMS_DATA))
        self.station_data = Station.load_stations(os.path.join(EDDB_PATH, EDDB_STATIONS_DATA))
        Universe.is_loaded = True
        Universe.is_loading = False
        _info_panel.add_text(["Data loading completed", ""])

    def thread_load_data(self, _info_panel):
        self.is_loading = True
        tld = threading.Thread(target=self.load_data, args=(_info_panel,))
        tld.start()

    def get_station_data(self, _station, _system):
        station = Station.find_station(self.station_data, self.system_data, _station, _system)
        if station:
            station.print_info()
            return station

    def thread_refresh_eddb(self, _info_panel):
        logger.debug("Loading=[%s], Loaded=[%s], RefreshingDB=[%s]" %
            (Universe.is_loading, Universe.is_loaded, Universe.is_refreshing_db))
        if Universe.is_loading:
            logger.debug("Data loading in progress, request is cancelled.")
            return
        if Universe.is_refreshing_db:
            logger.debug("EDDB refreshing in progress, request is cancelled.")
            return

        _info_panel.add_text(["Refreshing EDDB data ..."])
        Universe.is_refreshing_db = True
        _refreshed = threading.Event()
        tre = threading.Thread(target=eddb.refresh_from_source, args=(_refreshed,))
        nre = threading.Thread(target=self.notify_done, args=(_info_panel,"EDDB data refreshed",_refreshed,))
        tre.start()
        nre.start()

    def notify_done(self, _info_panel, _text, _notify):
        _notify.wait()
        _info_panel.add_text([_text])
        logger.debug(_text)
        Universe.is_refreshing_db = False
        self.thread_load_data(_info_panel)


class Station:
    COR_PAD_CLOCK = [ 0,                                   # direction at N o'clock
        6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 11,    #  1 - 20
        11, 11, 11, 12, 12, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4 ]   # 21 - 40
    COR_PAD_DEPTH = [ 0,                                   # 1: Near, 2: Mid, 3: Far
        1, 1, 3, 3, 1, 1, 2, 3, 1, 3, 1, 1, 2, 3, 3, 1, 1, 3, 3, 1,         #  1 - 20
        1, 2, 3, 1, 3, 1, 1, 2, 3, 3, 1, 1, 3, 3, 1, 1, 2, 3, 1, 3 ]        # 21 - 40
    COR_PAD_SIZE  = [ 0,                                   # 1: small, 2: medium, 3: large
        1, 3, 2, 1, 2, 1, 2, 2, 3, 3, 2, 1, 1, 1, 2, 1, 3, 2, 1, 2,         #  1 - 20
        1, 2, 2, 3, 3, 2, 1, 1, 1, 2, 1, 3, 2, 1, 2, 1, 2, 2, 3, 3 ]        # 21 - 40
    PAD_DEPTH_DESC = [ "undefined", "near", "mid", "far" ]
    PAD_SIZE_DESC  = [ "undefined", "small", "medium", "large" ]
    EDDB_IMG_BASEURL = "https://eddb.io/images/stations/"

    def __init__(self, _id, _name, _system_id, _type, _type_id, _is_planetary):
        self.id = _id
        self.name = _name
        self.system_id = _system_id
        self.type = _type
        self.type_id = _type_id
        self.is_planetary = _is_planetary
        self.system_name = ""

    def set_system_name(self, _system):
        self.system_name = _system

    def docking_pad_layout(self):
        if self.is_planetary:
            return 0
        if self.type_id in [3,7,8,12,20]:	# Starports, Asteroid Base
            return 1
        if self.type_id in [1,2,4,5,6,9]: 	# Outposts w/ image
            return 2
        if self.type_id in [11]: 		# Outposts w/o image
            return 3
        return 0                                # Unknown

    def coriolis_pad_info(self, pad_id):
        return ( self.COR_PAD_CLOCK[pad_id], self.COR_PAD_DEPTH[pad_id], self.COR_PAD_SIZE[pad_id] )

    def outpost_pad_info(self, pad_id):
        img = []
        if self.type_id == 1:
            if pad_id <= 3:
                img.append("schema_civillian.png")
                img.append("schema_civillian_industrial.png")
            else:
                img.append("schema_civillian_industrial.png")
        if self.type_id == 2:
            img.append("schema_commercial.png")
        if self.type_id == 4:
            img.append("schema_civillian_industrial.png")
        if self.type_id == 5:
            img.append("schema_military.png")
        if self.type_id == 6:
            img.append("schema_industrial_mining.png")
        if self.type_id == 9:
            img.append("schema_scientific.png")
        return img

    def print_info(self):
        if self.type:
            logger.info("Station %s at %s, %s, layout: %d" % (self.name, self.system_name, self.type, self.docking_pad_layout()))
        else:
            logger.info("Station %s" % self.name)

    @staticmethod
    def load_stations(fn):
        stationObj = []
        try:
            stationJSON = json.load(open(fn))
            _total = len(stationJSON)
            print("Loading Stations [%d] " % _total, end="", flush=True)
            for i, s in enumerate(stationJSON):
                stationObj.append( Station(s["id"], s["name"], s["system_id"], s["type"], s["type_id"], s["is_planetary"]) )
                if i % 1000 == 0: print(".", end="", flush=True)
            print(" completed")
        except (OSError, IOError) as e:
            if getattr(e, 'errno', 0) == errno.ENOENT:
                logger.error("File %s not found, ignored..." % fn)
        return stationObj

    def find_station(stn_data, sys_data, station, system):
        for stn in stn_data:
            if stn.name == station:
                if stn.system_id:
                    for sys in sys_data:
                        if system:
                            if sys.name == system and sys.id == stn.system_id:
                                stn.set_system_name(system)
                                return stn
                        else:
                            if sys.id == stn.system_id:
                                stn.set_system_name(sys.name)
                                return stn

    def show_landing_pad(station, pad_id):
        pad_layout = station.docking_pad_layout()
        if pad_layout == 1:
            pad_info = station.coriolis_pad_info(pad_id)
            print("Landing pad %d (%s) at %d o'clock %s" %
                (pad_id, Station.PAD_SIZE_DESC[pad_info[2]], pad_info[0], Station.PAD_DEPTH_DESC[pad_info[1]]) )
        if pad_layout == 2:
            pad_info = station.outpost_pad_info()
            for p in pad_info:
                print("Landing pad schema URL: %s%s" % (Station.EDDB_IMG_BASEURL,p))

