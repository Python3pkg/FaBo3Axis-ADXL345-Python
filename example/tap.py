# coding: utf-8
## @package tap
#  This is a library for the FaBo 3AXIS I2C Brick.
#
#  http://fabo.io/201.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import faboADXL345
import time

adxl345 =  faboADXL345.ADXL345()
adxl345.enableTap()

while True:
    tap = adxl345.readIntStatus()
    if adxl345.isDoubleTap(tap):
        print "Double Tap"
    if adxl345.isSingleTap(tap):
        print "Single Tap"
    print "*"
    time.sleep(0.5)
