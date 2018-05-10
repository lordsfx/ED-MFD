import os, sys
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Journal:
    events_monitor = [ "SupercruiseExit", "Location", "DockingGranted" ]
    path = "./journals"
    pattern = "Journal.*.log"
    last_system = ""
    last_station = ""

    @staticmethod
    def parser(journal, panel):
        if journal["event"] == "SupercruiseExit" and journal["BodyType"] == "Station":
            Journal.last_system = journal["StarSystem"]
            Journal.last_station = journal["Body"]
        if journal["event"] == "DockingGranted":
            if Journal.last_system and Journal.last_station:
                panel.add_text([ "%s, %s" % (Journal.last_station, Journal.last_system) ])

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
            print("%s modified" % event.src_path)

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
                print(journal['event'])
                sys.stdout.flush()
            jj = self.jfh.readline()

    def get_updates(self):
        if not self.have_update:
            return None
        self.have_update = False
        return self.captured_events

