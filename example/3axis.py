# coding: utf-8
## @package 3axis
#  This is a library for the FaBo 3AXIS I2C Brick.
#
#  http://fabo.io/201.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import FaBo3Axis_ADXL345
import time

adxl345 = FaBo3Axis_ADXL345.ADXL345()

while True:
    axes = adxl345.read()
    print "x = " , (axes['x'])
    print "y = " , (axes['y'])
    print "z = " , (axes['z'])
    print
    time.sleep(0.5)
