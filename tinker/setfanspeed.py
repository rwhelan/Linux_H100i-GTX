

import usb.core
import usb.util
import struct

def setfanspeed(percent):
    b = struct.pack('b', percent)
    dev.write(2, "\x12"+b)
#    print repr("\x12"+b)
    dev[0][(0,0)][1].read(32)

dev = usb.core.find(idVendor=0x1b1c, idProduct=0x0c03)
dev.reset()
dev.ctrl_transfer(0x40, 0x02, wValue=0x0002)
dev.write(2, "\x14\x00\x00\x00")

setfanspeed(0)
