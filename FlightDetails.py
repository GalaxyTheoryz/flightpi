"""
FlightDetails.py
Manage the database of known ICAO24 decodes, fetch from external APIs as needed
Thanks to 'joshuadouch' for the API - https://radarspotting.com/forum/index.php?topic=6117.0
Matt Dyson
08/06/18
Part of FlightPi - http://github.com/mattdy/flightpi
Updated API URL's as per update to forum post listed above. With help from https://github.com/GalaxyTheoryz/flightpi/blob/33f0e4729ee9cc15891b992310b0c9cecbbb68ac/FlightDetails.py
"""

import logging
import sys
import sqlite3
import time
import urllib.request

log = logging.getLogger('root')
TIMEOUT=60 # Number of minutes to keep a cache of our API hits

class FlightDetails:
    def __init__(self,filename="/home/pi/flightpi/details.sql"):
        log.debug("Starting FlightDetails database at %s" % (filename))
        self.apiCache = { }

        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self.c = self.conn.cursor()

        self.c.execute("CREATE TABLE IF NOT EXISTS `airframe` (icao text, type text, registration text)")

        log.debug("Loaded FlightDetails")

    def getRow(self, icao):
        self.c.execute('SELECT * FROM `airframe` WHERE `icao`=?', [icao])
        row = self.c.fetchone()
        if row is None:
            if icao in self.apiCache:
                if self.apiCache[icao] > time.time() - (TIMEOUT * 60 * 60):
                    return None
            try:
                log.debug("Attempting to fetch details from external API")
                with urllib.request.urlopen("https://api.joshdouch.me/hex-type.php?hex=%s" % (icao)) as response:
                    type = response.read()
                with urllib.request.urlopen("https://api.joshdouch.me/hex-reg.php?hex=%s" % (icao)) as response:
                    reg = response.read()


                if type=="n/a" or type=="0": type=None
                if reg=="n/a" or reg=="0": reg=None

                self.apiCache[icao] = time.time()

                if type is not None and reg is not None:
                    log.info("Successful fetch for %s, now inserting into database" % (icao))
                    self.c.execute("INSERT INTO `airframe` (icao, type, registration) VALUES (?, ? ,?)", [str(icao), str(type), str(reg)])
                    self.conn.commit()
                    row = (icao, type, reg)

            except Exception as e:
                log.error("Error fetching from external API {0}".format(e))

        return row

    def getType(self, icao):
        row = self.getRow(icao)
        if row is not None:
            return self.getRow(icao)[1]
        else:
            return None

    def getRegistration(self, icao):
        row = self.getRow(icao)
        if row is not None:
            return self.getRow(icao)[2]
        else:
            return None
