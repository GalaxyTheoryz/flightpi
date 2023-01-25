"""
FlightPi.py
Main execution flow. Creates all necessary inputs and outputs, and links them together

Matt Dyson
24/01/18

Part of FlightPi - http://github.com/mattdy/flightpi
"""
import logging
import sys
import os

log = logging.getLogger('root')
log.setLevel(logging.INFO)

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] %(levelname)8s %(module)15s: %(message)s')
stream.setFormatter(formatter)

log.addHandler(stream)

from SbsThread import SbsThread
from LcdThread import LcdThread
#from ArduinoThread import ArduinoThread
import time
#import schedule

class FlightPi:
    def __init__(self):
        self.stopping = False
        self.aircraft = { }
        self.receivers = [ ]
        self.display = None
#        log.info("Starting up VPN in 1 minute")
#        time.sleep(60)
#        os.system("sudo service openvpn restart")

    def stop(self):
        self.stopping = True

    def execute(self):
        log.info("Starting up FlightPi")

        self.lcdThread = LcdThread(0x27,20)
        self.addReceiver(self.lcdThread.processFlight)
        self.lcdThread.start()

#        self.arduinoThread = ArduinoThread("/dev/ttyUSB0")
#        self.addReceiver(self.arduinoThread.processFlight)
#        self.arduinoThread.start()

        self.sbsThread = SbsThread('192.168.1.3',30003) #specify server for SBS messages
        self.sbsThread.addReceiver(self.processMessage)
        self.sbsThread.start()

        log.info("Starting loop")
 #       schedule.every().day.at("22:00").do(self.stop) #stops at 10pm
        try:
            while(self.stopping is False):
                time.sleep(1)
                self.updateAircraft()
#                schedule.run_pending()
        except (KeyboardInterrupt, SystemExit):
            log.warning("Interrupted, shutting down")

#        self.arduinoThread.stop()
        self.sbsThread.stop()
        self.lcdThread.stop()

    def addReceiver(self, callback):
        """ Add a callback function that will be passed updates to the aircraft display """

        log.debug("Added new display receiver - %s" % (callback))
        self.receivers.append(callback)

    def updateAircraft(self):
        ''' Check our list of aircraft for currency, select the one to display '''
        lowest = None

        for i in list(self.aircraft):
            a = self.aircraft[i]
            if(a['lastUpdate'] < time.time() - 30):
                # No update for 30 seconds, so remove
                del self.aircraft[a['icao24']]

            if(a['callsign'] is None):
                # Don't select aircraft that we don't have enough detail on
                continue

            if(lowest is None or a['altitude'] < lowest['altitude']):
                # We have a new favourite
                lowest = a

        if(lowest != self.display):
            if(lowest is not None):
                self.display = dict(lowest) # Take a copy rather than a reference
            else:
                self.display = None

            log.debug("Updating display to: %s" % (self.display))
            for rec in self.receivers:
                try:
                    rec(self.display)
                except Exception as e:
                    log.error("Error processing display through function [%s]" % (rec))
                    log.error(e)

    def processMessage(self,msg):
        ''' Callback function for every message received by our SBS processor '''
#        log.debug("Callback on %s (%s)" % (msg.icao24, msg.callsign))
        if(msg.icao24 is None): return

        if(msg.icao24 in self.aircraft):
            # We know about this aircraft already
            self.aircraft[msg.icao24]['lastUpdate'] = time.time()

            if(msg.aircraftID is not None):
                self.aircraft[msg.icao24]['aircraftID'] = msg.aircraftID

            if(msg.flightID is not None):
                self.aircraft[msg.icao24]['flightID'] = msg.flightID

            if(msg.callsign is not None):
                self.aircraft[msg.icao24]['callsign'] = msg.callsign

            if(msg.altitude is not None):
                self.aircraft[msg.icao24]['altitude'] = msg.altitude

            if(msg.groundSpeed is not None):
                self.aircraft[msg.icao24]['groundSpeed'] = msg.groundSpeed

            if(msg.track is not None):
                self.aircraft[msg.icao24]['track'] = msg.track

            if(msg.verticalRate is not None):
                self.aircraft[msg.icao24]['verticalRate'] = msg.verticalRate

            if(msg.squawk is not None):
                self.aircraft[msg.icao24]['squawk'] = msg.squawk
        else:
            # We don't know about this aircraft, so create it
            self.aircraft[msg.icao24] = {
                'icao24': msg.icao24,
                'aircraftID': msg.aircraftID,
                'flightID': msg.flightID,
                'callsign': msg.callsign,
                'altitude': msg.altitude,
                'groundSpeed': msg.groundSpeed,
                'track': msg.track,
                'verticalRate': msg.verticalRate,
                'squawk': msg.squawk,
                'lastUpdate': time.time()
            }

flightpi = FlightPi()
flightpi.execute()

