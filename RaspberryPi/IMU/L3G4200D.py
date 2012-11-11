#!/usr/bin/python

import smbus
import I2C

class L3G4200D:
    _GYRO_ADDRESS = 0x69

    # device types

    _L3G_DEVICE_AUTO = 0
    _L3G4200D_DEVICE = 1
    _L3GD20_DEVICE = 2

    # SA0 states

    _L3G_SA0_LOW = 0
    _L3G_SA0_HIGH = 1
    _L3G_SA0_AUTO = 2

    # register addresses

    _L3G_WHO_AM_I = 0x0F

    _L3G_CTRL_REG1 = 0x20
    _L3G_CTRL_REG2 = 0x21
    _L3G_CTRL_REG3 = 0x22
    _L3G_CTRL_REG4 = 0x23
    _L3G_CTRL_REG5 = 0x24
    _L3G_REFERENCE = 0x25
    _L3G_OUT_TEMP = 0x26
    _L3G_STATUS_REG = 0x27

    _L3G_OUT_X_L = 0x28
    _L3G_OUT_X_H = 0x29
    _L3G_OUT_Y_L = 0x2A
    _L3G_OUT_Y_H = 0x2B
    _L3G_OUT_Z_L = 0x2C
    _L3G_OUT_Z_H = 0x2D

    _L3G_FIFO_CTRL_REG = 0x2E
    _L3G_FIFO_SRC_REG = 0x2F

    _L3G_INT1_CFG = 0x30
    _L3G_INT1_SRC = 0x31
    _L3G_INT1_THS_XH = 0x32
    _L3G_INT1_THS_XL = 0x33
    _L3G_INT1_THS_YH = 0x34
    _L3G_INT1_THS_YL = 0x35
    _L3G_INT1_THS_ZH = 0x36
    _L3G_INT1_THS_ZL = 0x37
    _L3G_INT1_DURATION = 0x38

    def __init__(self, gyro_address = _GYRO_ADDRESS):
        self.gyro = I2C.I2C(gyro_address)

    def enableDefault(self):
        self.gyro.writeByte(self._L3G_CTRL_REG1, 0x0F)

    def readRawGyro(self):
        xlg = self.gyro.readByte(self._L3G_OUT_X_L)
        xhg = self.gyro.readByte(self._L3G_OUT_X_H)
        ylg = self.gyro.readByte(self._L3G_OUT_Y_L)
        yhg = self.gyro.readByte(self._L3G_OUT_Y_H)
        zlg = self.gyro.readByte(self._L3G_OUT_Z_L)
        zhg = self.gyro.readByte(self._L3G_OUT_Z_H)

        data = [(xhg<<8)|xlg, (yhg<<8)|ylg, (zhg<<8)|zlg]

        for i in range(3):
            if(data[i]>2**16/2-1):
                data[i]-=2**16

        return data

