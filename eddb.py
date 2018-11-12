import sys, os
import logging
import json
import requests
import threading
from config import *

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger()

class eddb:

    @staticmethod
    def refresh_from_source(_notify):
        _notify.clear()
        t1 = threading.Thread(target=eddb.download_file, args=(EDDB_SYSTEMS_SOURCE, EDDB_PATH, ))
        t2 = threading.Thread(target=eddb.download_file, args=(EDDB_STATIONS_SOURCE, EDDB_PATH, ))
        t1.start()
        t2.start()
        t2.join()
        eddb.filter_stations(EDDB_PATH)
        _notify.set()

    def download_file(_ins, _dir):
        _outs = os.path.join(_dir, _ins.split('/')[-1])
        try:
            logger.debug("Downloading data from %s" % _ins)
            re = requests.get(_ins, stream=True)
            logger.debug("Writing data to %s" % _outs)
            with open(_outs, "wb") as ofh:
                ofh.write(re.content)
        except:
            logger.error("%s", sys.exc_info()[0])

    def filter_stations(_dir):
        _ifj = os.path.join(_dir, EDDB_STATIONS_PRE)
        _ofj = os.path.join(_dir, EDDB_STATIONS_DATA)
        try:
            logger.debug("Filtering station data %s to %s ..." % (_ifj, _ofj))
            with open(_ifj, "r") as ifh:
                jdata = json.load(ifh)
            for j in jdata: j.pop('selling_modules', None)
            with open(_ofj, "w") as ofh:
                json.dump(jdata, ofh, separators=(',',':'))
        except:
            logger.error("%s", sys.exc_info()[0])
