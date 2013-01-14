import I2C
import time

class LSM303DLM:
    #I2C addresses for LSM303
    _ACCEL_ADDRESS = 0x18
    _MAG_ADDRESS = 0x1e

    # device types

    _LSM303DLH_DEVICE = 0
    _LSM303DLM_DEVICE = 1
    _LSM303DLHC_DEVICE = 2
    _LSM303_DEVICE_AUTO = 3

    # SA0_A states

    _LSM303_SA0_A_LOW = 0
    _LSM303_SA0_A_HIGH = 1
    _LSM303_SA0_A_AUTO = 2

    # register addresses

    _LSM303_CTRL_REG1_A = 0x20
    _LSM303_CTRL_REG2_A = 0x21
    _LSM303_CTRL_REG3_A = 0x22
    _LSM303_CTRL_REG4_A = 0x23
    _LSM303_CTRL_REG5_A = 0x24
    _LSM303_CTRL_REG6_A = 0x25 # DLHC only
    _LSM303_HP_FILTER_RESET_A = 0x25 # DLH, DLM only
    _LSM303_REFERENCE_A = 0x26
    _LSM303_STATUS_REG_A = 0x27

    _LSM303_OUT_X_L_A = 0x28
    _LSM303_OUT_X_H_A = 0x29
    _LSM303_OUT_Y_L_A = 0x2A
    _LSM303_OUT_Y_H_A = 0x2B
    _LSM303_OUT_Z_L_A = 0x2C
    _LSM303_OUT_Z_H_A = 0x2D

    _LSM303_FIFO_CTRL_REG_A = 0x2E # DLHC only
    _LSM303_FIFO_SRC_REG_A = 0x2F # DLHC only

    _LSM303_INT1_CFG_A = 0x30
    _LSM303_INT1_SRC_A = 0x31
    _LSM303_INT1_THS_A = 0x32
    _LSM303_INT1_DURATION_A = 0x33
    _LSM303_INT2_CFG_A = 0x34
    _LSM303_INT2_SRC_A = 0x35
    _LSM303_INT2_THS_A = 0x36
    _LSM303_INT2_DURATION_A = 0x37

    _LSM303_CLICK_CFG_A = 0x38 # DLHC only
    _LSM303_CLICK_SRC_A = 0x39 # DLHC only
    _LSM303_CLICK_THS_A = 0x3A # DLHC only
    _LSM303_TIME_LIMIT_A = 0x3B # DLHC only
    _LSM303_TIME_LATENCY_A = 0x3C # DLHC only
    _LSM303_TIME_WINDOW_A = 0x3D # DLHC only

    _LSM303_CRA_REG_M = 0x00
    _LSM303_CRB_REG_M = 0x01
    _LSM303_MR_REG_M = 0x02

    _LSM303_OUT_X_H_M = 0x03
    _LSM303_OUT_X_L_M = 0x04
    _LSM303_OUT_Y_H_M = 0x07 # The addresses of the Y and Z magnetometer output registers
    _LSM303_OUT_Y_L_M = 0x08 # are reversed on the DLM and DLHC relative to the DLH.
    _LSM303_OUT_Z_H_M = 0x05 # These four defines have dummy values so the library can
    _LSM303_OUT_Z_L_M = 0x06 # determine the correct address based on the device type.

    _LSM303_SR_REG_M = 0x09
    _LSM303_IRA_REG_M = 0x0A
    _LSM303_IRB_REG_M = 0x0B
    _LSM303_IRC_REG_M = 0x0C

    _LSM303_WHO_AM_I_M = 0x0F # DLM only

    def __init__(self, accel_address = _ACCEL_ADDRESS, mag_address = _MAG_ADDRESS):
        self.accel = I2C.I2C(accel_address)
        self.mag = I2C.I2C(mag_address)

    def enableDefault(self):
        #Enable Accelerometer
        self.accel.writeByte(self._LSM303_CTRL_REG1_A, 0x3F)
        #Enable Magnetometer
        self.mag.writeByte(self._LSM303_MR_REG_M, 0x00) # 0b00000000
        self.mag.writeByte(self._LSM303_CRB_REG_M, 0x70) # 011100000
        self.mag.writeByte(self._LSM303_CRA_REG_M, 0x1C) # 0b00011100

    def readRawAccel(self):
        xla = self.accel.readByte(self._LSM303_OUT_X_L_A)
        xha = self.accel.readByte(self._LSM303_OUT_X_H_A)
        yla = self.accel.readByte(self._LSM303_OUT_Y_L_A)
        yha = self.accel.readByte(self._LSM303_OUT_Y_H_A)
        zla = self.accel.readByte(self._LSM303_OUT_Z_L_A)
        zha = self.accel.readByte(self._LSM303_OUT_Z_H_A)

        data = [(xha<<8|xla)>>4, (yha<<8|yla)>>4,(zha<<8|zla)>>4]
        for i in range(3):
            if(data[i]>2**12/2-1):
                data[i]-=2**12

        return data

    def readRawMag(self):
        xla = self.mag.readByte(self._LSM303_OUT_X_L_M)
        xha = self.mag.readByte(self._LSM303_OUT_X_H_M)
        yla = self.mag.readByte(self._LSM303_OUT_Y_L_M)
        yha = self.mag.readByte(self._LSM303_OUT_Y_H_M)
        zla = self.mag.readByte(self._LSM303_OUT_Z_L_M)
        zha = self.mag.readByte(self._LSM303_OUT_Z_H_M)

        data = [xha<<8|xla, yha<<8|yla,zha<<8|zla]
        for i in range(3):
            if(data[i]>2**16/2-1):
                data[i]-=2**16

        return data


