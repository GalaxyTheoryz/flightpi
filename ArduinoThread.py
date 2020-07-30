"""
ArdunioThread
Accepts details of a flight to display, and outputs them to an Arduino for LED display

Matt Dyson
07/06/18

Part of FlightPi - http://github.com/mattdy/flightpi
"""
import threading
import logging
import time
import serial
from FlightColours import FlightColours

log = logging.getLogger('root')

class ArduinoThread(threading.Thread):
    def __init__(self, address="/dev/ttyUSB0"):
        threading.Thread.__init__(self)
        self.stopping = False

        self.display = None

        self.address = address
        self.device = None

    def processFlight(self, flight):
        """ Take the given flight details, translate it into what we want to show on the LCD """
        if(flight is None):
            self.device.write("C\n")
            self.device.flush()
            self.display = None
        else:
            if(self.display is not None and self.display['callsign'] != flight['callsign']):
                # We're getting a new flight, so clear the current display
                self.device.write("C\n")
                self.device.flush()

            self.display = flight

            climb = "L"
            if(flight['verticalRate'] is not None):
                if(int(flight['verticalRate'])>100): climb = "C"
                if(int(flight['verticalRate'])<-100): climb = "D"

            if(flight['track'] is not None):
                self.device.write("D%s\n" % (flight['track']))
    
            if(flight['altitude'] is not None):
                self.device.write("A%s%s\n" % (climb,flight['altitude']))
    
            if flight['callsign'][:3] in FlightColours.col:
                self.device.write("L%s\n" % (FlightColours.col[flight['callsign'][:3]]))
            else:
                # Blank the LEDs if we don't have a specified livery
                self.device.write("LNNN\n")

            self.device.flush()

    def stop(self):
        self.stopping = True

    def run(self):
        log.info("ArduinoThread starting")

        self.device = serial.Serial(self.address, 9600)

        while not self.stopping:
            time.sleep(1)

        self.device.write("C\n")
        self.device.close()

        log.info("ArduinoThread shut down")
