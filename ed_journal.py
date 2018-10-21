import os, sys
import time
import json
from ed_object import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Journal:
    events_monitor = [ "SupercruiseExit", "Location", "DockingGranted" ]
    show_coriolis_types = [ "Coriolis", "Orbis" ]
    path = "./journals"
    pattern = "Journal.*.log"

    @staticmethod
    def parser(journal, ship):
        if journal["event"] in Journal.events_monitor:
            ship.update_event_memory(journal)

    def display(panel, ship):
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
                    panel.add_text([ "Docking granted at %s pad %s" % (emj["StationName"], emj["LandingPad"]) ])
                    ship.mark_event_processed(em)

class JournalEventHandler(FileSystemEventHandler):

    def __init__(self):
        self.latest_journal = ""
        self.jfh = None
        self.have_update = False
        self.captured_events = []

    def on_any_event(self, event):
        if event.is_directory:
            return None
 
        elif event.event_type == "modified":
            #print("%s modified" % event.src_path)

            if not self.jfh:
                self.latest_journal = event.src_path
                self.jfh = open(self.latest_journal)

            self.journal_filter()

        elif event.event_type == "created":
            print("%s created" % event.src_path)

            if self.jfh: self.jfh.close()
            self.latest_journal = event.src_path
            self.jfh = open(self.latest_journal)

            if self.jfh:
                self.journal_filter()

    def journal_filter(self):
        jj = self.jfh.readline()
        while jj:
            journal = json.loads(jj)
            if journal['event'] in Journal.events_monitor:
                if not self.have_update:
                    self.captured_events = []
                    self.have_update = True
                self.captured_events.append(journal)
                print("%s is logged" % journal['event'])
                sys.stdout.flush()
            jj = self.jfh.readline()

    def get_updates(self):
        if not self.have_update:
            return None
        self.have_update = False
        return self.captured_events

