import os, sys
import time
import json
import glob, io
from ed_object import *
from ed_status import *
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

J_PATH = "./journals"
J_LOG  = J_PATH+"/Journal.*.log"
J_STAT = J_PATH+"/Status.json"

class Journal:
    events_monitor = [ "SupercruiseExit", "Location", "DockingGranted", "Status" ]
    show_coriolis_types = [ "Coriolis", "Orbis" ]
    path = J_PATH
    patterns = [ J_LOG, J_STAT ]

    @staticmethod
    def openfile(_filename, _seek=None):
        try:
            print("Open journal: %s" % _filename)
            fh = open(_filename)
            if _seek:
                fh.seek(0, _seek)
        except (OSError, IOError) as e:
            print("Error opening: %s, %s" % (_filename, e))
        return fh

    def parser(journal, ship):
        if journal["event"] in Journal.events_monitor:
            ship.update_event_memory(journal)

    def display(panel, ship, universe, buttons):
        event_memory = ship.get_event_memory()
        for em in event_memory:
            if ship.event_is_updated(em):				# event is updated
                print("%s has an update" % em)
                emj = event_memory[em][1]				# retrieve journal content
                # SupercruiseExit
                if em == "SupercruiseExit":
                    panel.add_text([ "Arrived at %s, %s" % (emj["Body"], emj["StarSystem"]) ])
                    ship.set_at_system(emj["StarSystem"])
                    ship.set_at_station(emj["Body"])
                    ship.mark_event_processed(em)
                # Location
                if em == "Location":
                    ship.set_at_system(emj["StarSystem"])
                    ship.set_at_station(emj["StationName"])
                    ship.mark_event_processed(em)
                # DockingGranted
                if em == "DockingGranted":
                    if emj["StationType"] in Journal.show_coriolis_types:
                        panel.add_coriolis(emj["LandingPad"])
                    else:
                        station = universe.get_station_data(ship.get_at_station(), ship.get_at_system())
                        pad_layout = station.docking_pad_layout()
                        if pad_layout == 2:
                            pad_info = station.outpost_pad_info()
                            for p in pad_info:
                                panel.add_image("images/" + p)
                    panel.add_text([ "Docking granted at %s pad %s" % (emj["StationName"], emj["LandingPad"]) ])
                    ship.mark_event_processed(em)
                # Status
                if em == "Status":
                    if emj["Flags"]:
                        ship.update_status_flags(emj["Flags"], buttons)
                        #for status_flag in Status.get_ship_flags():
                        #    if ship.get_status().is_flagged(status_flag):
                        #        panel.add_text([ "Status: %s" % status_flag ])
                    if emj["Pips"]:
                        ship.update_status_pips(emj["Pips"], buttons)
                    if emj["FireGroup"]:
                        ship.update_status_firegroup(emj["FireGroup"], buttons)
                    if emj["GuiFocus"]:
                        ship.update_status_guifocus(emj["GuiFocus"], buttons)
                    ship.mark_event_processed(em)

class JournalEventHandler(PatternMatchingEventHandler):

    def __init__(self):
        PatternMatchingEventHandler.__init__(self, patterns=Journal.patterns)
        self.captured_events = []
        # Journal log
        list_journals = glob.glob(J_LOG)
        self.journal_latest = max(list_journals, key=os.path.getctime)
        self.journal_fh = Journal.openfile(self.journal_latest, io.SEEK_END)
        # Status json
        self.status_json = J_STAT
        self.status_fh = Journal.openfile(self.status_json)

    def on_any_event(self, event):
        if event.is_directory:
            return None
 
        elif event.event_type == "modified":
            if "Status" in event.src_path:
                print("Status updated: %s" % event.src_path)
                self.status_process()
            else:
                print("Journal updated: %s" % event.src_path)
                self.journal_filter()

        elif event.event_type == "created":
            if "Status" in event.src_path:
                print("Status created: %s" % event.src_path)
                if self.status_fh: self.status_fh.close()
                self.status_json = event.src_path
                self.status_fh = Journal.openfile(self.status_json)
                self.status_process()
            else:
                print("Journal created: %s" % event.src_path)
                if self.journal_fh: self.journal_fh.close()
                self.journal_latest = event.src_path
                self.journal_fh = Journal.openfile(self.journal_latest)
                self.journal_filter()

        elif event.event_type == "deleted":
            #print("%s deleted" % event.src_path)
            pass
        else:
            print("other event: %s: %s" % (event.event_type, event.src_path))

    def status_process(self):
        self.status_fh.seek(0, io.SEEK_SET)
        status = json.loads(self.status_fh.readline())
        self.captured_events.append(status)

    def journal_filter(self):
        jj = self.journal_fh.readline()
        while jj:
            journal = json.loads(jj)
            if journal['event'] in Journal.events_monitor:
                self.captured_events.append(journal)
                #print("%s is logged" % journal['event'])
                #sys.stdout.flush()
            jj = self.journal_fh.readline()

    def get_updates(self):
        return_events = self.captured_events
        self.captured_events = []
        return return_events

