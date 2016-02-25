import usb.core
import usb.util
import struct
import time

#https://www.arduino.cc/en/Reference/Map
def mapper(x, mi, mx, mio, mao):
    return (x - mi) * (mao - mio) / (mx - mi) + mio

def setfanspeed(percent):
    b = struct.pack('b', percent)
    dev.write(2, "\x12"+b)
#    print repr("\x12"+b)
    dev[0][(0,0)][1].read(32)


dev = usb.core.find(idVendor=0x1b1c, idProduct=0x0c03)
dev.reset()
dev.ctrl_transfer(0x40, 0x02, wValue=0x0002)
dev.write(2, "\x14\x00\x00\x00")

while True:
   dev.write(2, "\x14\x00\x00\x00")
   data = dev[0][(0,0)][1].read(32)
  # print list(data)[2:4]
   print list(data)

   values = list(data)[2:4]
   print struct.unpack('>h', ''.join([chr(i) for i in values]))[0]
   print
   time.sleep(1.0)
