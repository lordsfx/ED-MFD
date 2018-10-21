import json

class Ship:
    def __init__(self):
        self.event_memory = {}
        self.at_system = None
        self.at_station = None

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

    def get_at_system(self):
        return self.at_system

    def set_at_station(self, station):
        self.at_station = station

    def get_at_station(self):
        return self.at_station

class System:
    def __init__(self, _id, _name):
        self.id = _id
        self.name = _name

    @staticmethod
    def load_systems(fn):
        print("Loading Systems...")
        systemObj = []
        systemJSON = json.load(open(fn))
        for s in systemJSON:
            systemObj.append( System(s["id"], s["name"]) )
        print("Loading completed.")
        return systemObj

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

    def outpost_pad_info(self):
        img = []
        if self.type_id == 1:
            img.append("schema_civillian.png")
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
            print("Station " + self.name + " at " + self.system_name + ", " + self.type + ", layout: " + str(self.docking_pad_layout()))
        else:
            print("Station " + self.name)

    @staticmethod
    def load_stations(fn):
        print("Loading Stations...")
        stationObj = []
        stationJSON = json.load(open(fn))
        for s in stationJSON:
            stationObj.append( Station(s["id"], s["name"], s["system_id"], s["type"], s["type_id"], s["is_planetary"]) )
        print("Loading completed.")
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

