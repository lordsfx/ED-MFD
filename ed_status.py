class Status:
    ShipFlags = { "docked"         : 0x1	, "landed"        : 0x2,
                  "gear_down"      : 0x4	, "shield_up"     : 0x8,
                  "supercruise"    : 0x10	, "fa_off"        : 0x20,
                  "hardpoint"      : 0x40	, "in_wing"       : 0x80,
                  "lights"         : 0x100	, "cargo_scoop"   : 0x200,
                  "slient_run"     : 0x400	, "fuel_scooping" : 0x800,
                  "srv_hbrake"     : 0x1000	, "srv_turret"    : 0x2000,
                  "srv_turret_off" : 0x4000	, "srv_drvassist" : 0x8000,
                  "fsd_masslock"   : 0x10000	, "fsd_charging"  : 0x20000,
                  "fsd_cooldown"   : 0x40000	, "low_fuel"      : 0x80000,
                  "over_heat"      : 0x100000	, "has_lat_long"  : 0x200000,
                  "in_danger"      : 0x400000	, "interdicted"   : 0x800000,
                  "in_mainship"    : 0x1000000	, "in_fighter"    : 0x2000000,
                  "in_srv"         : 0x4000000 }

    def __init__(self):
        self.flags = 0
        self.pips = []
        self.firegroup = 0
        self.guifocus = 0
        return

    def update_flags(self, _flags):
        self.flags = _flags
        return

    def update_pips(self, _pips):
        self.pips = _pips
        return

    def update_firegroup(self, _firegroup):
        self.firegroup = _firegroup
        return

    def update_guifocus(self, _guifocus):
        self.guifocus = _guifocus
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
