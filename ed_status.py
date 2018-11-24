GUI_NOFOCUS     = 0
GUI_PANEL_INT   = 1	# Right hand side
GUI_PANEL_EXT   = 2	# Left hand side
GUI_PANEL_COMMS = 3
GUI_PANEL_ROLE  = 4
GUI_STATION_SRV = 5
GUI_MAP_GALAXY  = 6
GUI_MAP_SYSTEM  = 7
GUI_ORRERY      = 8
GUI_MODE_FSS    = 9
GUI_MODE_SAA    = 10
GUI_CODEX       = 11

class Status:
    ShipFlags = { "docked"         : 0x1	, "landed"        : 0x2,
                  "gear_down"      : 0x4	, "shield_up"     : 0x8,
                  "supercruise"    : 0x10	, "fa_off"        : 0x20,
                  "hardpoint"      : 0x40	, "in_wing"       : 0x80,
                  "lights"         : 0x100	, "cargo_scoop"   : 0x200,
                  "silent_run"     : 0x400	, "fuel_scooping" : 0x800,
                  "srv_hbrake"     : 0x1000	, "srv_turret"    : 0x2000,
                  "srv_turret_off" : 0x4000	, "srv_drvassist" : 0x8000,
                  "fsd_masslock"   : 0x10000	, "fsd_charging"  : 0x20000,
                  "fsd_cooldown"   : 0x40000	, "low_fuel"      : 0x80000,
                  "over_heat"      : 0x100000	, "has_lat_long"  : 0x200000,
                  "in_danger"      : 0x400000	, "interdicted"   : 0x800000,
                  "in_mainship"    : 0x1000000	, "in_fighter"    : 0x2000000,
                  "in_srv"         : 0x4000000  , "in_analysis"   : 0x8000000,
                  "nightvision"    : 0x10000000 }

    def __init__(self):
        self.flags = 0
        return

    def update_flags(self, _flags):
        self.flags = _flags
        return

    def is_flagged(self, _flag):
        flag = Status.ShipFlags[_flag]
        if self.flags & flag > 0:
            return True
        else:
            return False

    @staticmethod
    def get_ship_flags():
        fl = []
        for f in Status.ShipFlags:
            fl.append(f)
        return fl
