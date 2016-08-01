# coding: utf-8
## @package ADXL345
#  This is a FaBo3Axis_ADXL345 library for the FaBo 3AXIS I2C Brick.
#
#  http://fabo.io/201.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

## ADXL345 SLAVE_ADDRESS
SLAVE_ADDRESS   = 0x53
## Who_am_i register
DEVID_REG       = 0x00
## Device id
DEVICE          = 0xe5
## data format register
DATA_FORMAT     = 0x31
## powr control register
POWER_CTL       = 0x2d
## get 3axis register
DATA_XYZ        = 0x32
## Tap Threshold
THRESH_TAP_REG  = 0x1D
## Tap Duration
DUR_REG         = 0x21
## Tap Latency
LATENT_REG      = 0x22
## Tap Window
WINDOW_REG      = 0x23
## interrupt MAP
INT_MAP_REG     = 0x2F
## interrupt Enable
INT_ENABLE_REG  = 0x2E
## Power-saving features control
POWER_CTL_REG   = 0x2D
## Source of Single Tap/Double Tap
TAP_STATUS_REG  = 0x2B
## Axis Control for Single Tap/Double Tap
TAP_AXES_REG    = 0x2A
## Source of Interrupts
INT_SOURCE_REG  = 0x30
## Data Format Control
DATA_FORMAT_REG = 0x31

# Data Format Param
## SELF Test ON   : 0b10000000
SELF_TEST_ON   = 0x80
## SELF Test OFF  : 0b00000000
SELF_TEST_OFF  = 0x00
## SELF SPI ON    : 0b01000000
SPI_ON         = 0x40
## SELF SPI OFF   : 0b00000000
SPI_OFF        = 0x00
## INT_INVERT ON  : 0b00100000
INT_INVERT_ON  = 0x20
## INT_INVERT OFF : 0b00000000
INT_INVERT_OFF = 0x00
## FULL_RES ON    : 0b00001000
FULL_RES_ON    = 0x08
## FULL_RES OFF   : 0b00000000
FULL_RES_OFF   = 0x00
## JUSTIFY ON     : 0b00000100
JUSTIFY_ON     = 0x04
## JUSTIFY OFF    : 0b00000000
JUSTIFY_OFF    = 0x00
## RANGE 16G      : 0b00000011
RANGE_16G      = 0x03
## RANGE 8G       : 0b00000010
RANGE_8G       = 0x02
## RANGE 4G       : 0b00000001
RANGE_4G       = 0x01
## RANGE 2G       : 0b00000000
RANGE_2G       = 0x00

# Data Format Param
## Axis Tap Control Z axis ON : 0b00000001
TAP_AXES_Z_ON  = 0x01
## Axis Tap Control Y axis ON : 0b00000010
TAP_AXES_Y_ON  = 0x02
## Axis Tap Control X axis ON : 0b00000100
TAP_AXES_X_ON  = 0x04
## Axis Interrupt Single Tap  : 0b01000000
INT_SINGLE_TAP = 0x40
## Axis Interrupt Double Tap  : 0b00100000
INT_DOUBLE_TAP = 0x20

# Power Control Param
## AUTO SLEEP ON    : 0b00010000
AUTO_SLEEP_ON  = 0x10
## AUTO SLEEP OFF   : 0b00000000
AUTO_SLEEP_OFF = 0x00
## AUTO MEASURE ON  : 0b00001000
MEASURE_ON     = 0x08
## AUTO MEASURE OFF : 0b00000000
MEASURE_OFF    = 0x00
## SLEEP ON         : 0b00000100
SLEEP_ON       = 0x04
## SLEEP OFF        : 0b00000000
SLEEP_OFF      = 0x00
## WAKEUP 1Hz       : 0b00000011
WAKEUP_1HZ     = 0x03
## WAKEUP 2Hz       : 0b00000010
WAKEUP_2HZ     = 0x02
## WAKEUP 4Hz       : 0b00000001
WAKEUP_4HZ     = 0x01
## WAKEUP 8Hz       : 0b00000000
WAKEUP_8HZ     = 0x00

## SMBus
bus = smbus.SMBus(1)

## ADXL345 I2C Controll class
class ADXL345:

    ## Constructor
    #  @param [in] address ADXL345 i2c slave_address default:0x53
    def __init__(self, address=SLAVE_ADDRESS):
        self.address = address

        self.configuration()
        self.powerOn()

    ## Device check
    #  @param [in] self The object pointer.
    #  @retval true  : found
    #  @retval false : Not found
    def searchDevice(self):
        who_am_i = bus.read_byte_data(self.address, DEVID_REG)

        if(who_am_i == DEVICE):
            return True
        else:
            return False

    ## Set configuration
    #  @param [in] self The object pointer.
    def configuration(self):
        conf = SELF_TEST_OFF | SPI_OFF | INT_INVERT_OFF | FULL_RES_OFF | JUSTIFY_OFF | RANGE_16G
        bus.write_byte_data(self.address, DATA_FORMAT_REG, conf)

    ## ADXL345 Power On
    #  @param [in] self The object pointer.
    def powerOn(self):
        power = AUTO_SLEEP_OFF | MEASURE_ON | SLEEP_OFF | WAKEUP_8HZ
        bus.write_byte_data(self.address, POWER_CTL_REG, power)

    ## Enable Tap
    #  @param [in] self The object pointer.
    #  @param [in] thresh_tap  TAPの強さの閾値       Default:0x32
    #  @param [in] dur         TAP持続時間          Default:0x30
    #  @param [in] latant      識別間隔             Default:0xf8
    #  @param [in] window      識別間隔のインターバル Default:0x10
    def enableTap(self, thresh_tap=0x32, dur=0x30, latant=0xf8, window=0x10):
        bus.write_byte_data(self.address, THRESH_TAP_REG, thresh_tap) # 62.5mg/LBS
        bus.write_byte_data(self.address, DUR_REG, dur)               # 1.25ms/LSB
        bus.write_byte_data(self.address, LATENT_REG, latant)         # 1.25ms/LSB
        bus.write_byte_data(self.address, WINDOW_REG, window)         # 1.25ms/LSB

        int_tap = INT_SINGLE_TAP | INT_DOUBLE_TAP
        bus.write_byte_data(self.address, INT_ENABLE_REG, int_tap)     # Interrupts Tap Enable
        bus.write_byte_data(self.address, TAP_AXES_REG, TAP_AXES_Z_ON) # Tap Enable z axis

    ## Read Tap Status
    # @param [in] self The object pointer.
    # @return byte interrupts Status
    def readIntStatus(self):
        return bus.read_byte_data(self.address, INT_SOURCE_REG)

    ## check SingleTap
    # @param [in] self The object pointer.
    # @param [in] value : interrupts Status
    # @retval true  : Tap
    # @retval false : Not Tap
    def isSingleTap(self, value):
        if((value & INT_SINGLE_TAP) == INT_SINGLE_TAP):
            return True
        else:
            return False

    ## check DoubleTap
    # @param [in] self The object pointer.
    # @param [in] value : interrupts Status
    # @retval true  : Tap
    # @retval false : Not Tap
    def isDoubleTap(self, value):
        if((value & INT_DOUBLE_TAP) == INT_DOUBLE_TAP):
            return True
        else:
            return False

    ## Read 3axis data
    # @param [in] self The object pointer.
    # @retval x : x-axis data
    # @retval y : y-axis data
    # @retval z : z-axis data
    def read(self):
        data = bus.read_i2c_block_data(self.address, DATA_XYZ, 6)

        x = self.dataConv(data[0], data[1])
        y = self.dataConv(data[2], data[3])
        z = self.dataConv(data[4], data[5])

        return {"x":x, "y":y, "z":z}

    ## Data Convert
    # @param [in] self The object pointer.
    # @param [in] data1 LSB
    # @param [in] data2 MSB
    # @retval Value MSB+LSB(int 16bit)
    def dataConv(self, data1, data2):
        value = data1 | (data2 << 8)
        if(value & (1 << 16 - 1)):
            value -= (1<<16)
        return value
