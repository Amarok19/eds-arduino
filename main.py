#!/usr/bin/python

# Information for EDS:
## DESCRIPTION: 'Interface for reading values stored in a plain file as values of process points.'
## INFORMATION: ' '
## INFORMATION: ' '
## INFORMATION: ' '
## ARGUMENT: 'Full path to the communication file', fullpath, '~/commfile'
## ARGUMENT: 'Number of points', point_count, 23

import os
import sys
import fileinput
import time
import PyEds2
import re
import pyxeds2
import time

#usunac hardcode kiedy bedzie odpalane z dba
fullpath = '/home/krzysztof/commfile'
point_count = 23

live = pyxeds2.createLive()

live.setupLogger('debug=7 subsystems=ALL logger=console:7')
err = live.init(pyxeds2.LiveMode.ReadWrite,'0.0.0.0', 0, '127.0.0.1', 43000, 1000, 32768)
if pyxeds2.liveErrCode(err) != pyxeds2.LiveErrCode.NoError:
    print 'init() returned:', pyxeds2.liveErrMessage(err);

for i in range(point_count):
    live.setOutput(i)

while 1:
    readout = []
    f = open (fullpath, 'r')
    for line in f:
        readout.append(float(line))
    f.close()
    for i in range(point_count):
        live.writeAnalog(i, readout[i], 'G')
    live.synchronizeOutput()
    time.sleep(1)

live.shut()