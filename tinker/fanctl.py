

import usb.core
import usb.util
import struct
import time

class tempavg(object):
    def __init__(self, histsize=10):
        self.histsize = histsize
        self.vals = [0] * histsize
    
    def getavg(self):
        return int(sum(self.vals) / self.histsize)

    def addval(self, val):
        self.vals.pop()
        self.vals.insert(0, val)


#https://www.arduino.cc/en/Reference/Map
def mapper(x, mi, mx, mio, mao):
    return (x - mi) * (mao - mio) / (mx - mi) + mio

def setfanspeed(percent):
    b = struct.pack('b', percent)
    dev.write(2, "\x12"+b)
#    print repr("\x12"+b)
    dev[0][(0,0)][1].read(32)

def gettemp():
    _raw = open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r').read()
    return int(_raw) / 1000

dev = usb.core.find(idVendor=0x1b1c, idProduct=0x0c03)
dev.reset()
dev.ctrl_transfer(0x40, 0x02, wValue=0x0002)
dev.write(2, "\x14\x00\x00\x00")

ta = tempavg()

while True:
    ta.addval(gettemp())
    cpu_avg_temp = ta.getavg()
    target = mapper(cpu_avg_temp, 38, 60, 0, 100)
    target = target if target <= 100 else 100
    target = target if target >= 0 else 0
    print ta.vals
    print "Current avg temp: %s" % cpu_avg_temp
    print "Setting fan to: %s" % target
    print
    setfanspeed(target)

    time.sleep(1.0)
