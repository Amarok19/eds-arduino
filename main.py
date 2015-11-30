#!/usr/bin/python

# Information for EDS:
## DESCRIPTION: 'Interface for reading values stored in a plain file as values of process points.'
## INFORMATION: ' '
## INFORMATION: ' '
## INFORMATION: ' '
## ARGUMENT: 'Full path to the mapper file', fullpath, '~/eds-map'
## ARGUMENT: 'Number of points', point_count, 23

import os
import sys
import fileinput
import time
import PyEds2
import re
import pyxeds2
import time
import serial

# nie dziala bez hardcode - wina po stronie EDS
fullpath = '/home/student/eds-map'
point_count = 26

live = pyxeds2.createLive()

live.setupLogger('debug=7 subsystems=ALL logger=console:7')
err = live.init(pyxeds2.LiveMode.ReadWrite, '0.0.0.0', 0, '127.0.0.1', 43000, 1000, 32768)
if pyxeds2.liveErrCode(err) != pyxeds2.LiveErrCode.NoError:
    print 'init() returned:', pyxeds2.liveErrMessage(err);

for i in range(point_count):
    live.setOutput(i)

arduino = serial.Serial('/dev/ttyACM0', 115200)
f = open(fullpath, 'r')
map = [None] * 999
for i in range(point_count):
    line = f.readline().split(":")
    map[int(line[0])] = int(line[1])  # identyfikator:LID
f.close()

while 1:
    for i in range(point_count):
        line = arduino.readline().split(':')
        live.writeAnalog(map[int(line[0])], float(line[1]), 'G')
    arduino.readline()
    live.synchronizeOutput()
    time.sleep(1)

live.shut()
