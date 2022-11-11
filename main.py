# main.py

from machine import I2C, Pin, SPI
import machine
import time
import epd4in2
import framebuf



time.sleep(3)

w = 400
h = 300
x = 0
y = 0
black = 0
white = 1
buf = bytearray(w * h // 8)

pin = Pin(2, Pin.OUT)
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)

# SPIV on ESP32
sck = Pin(14)
#miso = Pin(12)
mosi = Pin(13)
cs = Pin(15)
dc = Pin(3)
rst = Pin(12)
busy = Pin(2)

spi = SPI(1, baudrate=40000000, polarity=0, phase=0)

e = epd4in2.EPD(spi, cs, dc, rst, busy)
e.init()

fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)

from digital_digits import DigitalDigits
dd = DigitalDigits(
        framebuffer=fb,
        x=0,
        y=0,
        width=w,
        height=h-100,
        space_between_digits=20,
        segment_space=2,
        segment_thickness=20)

print("start")
from SI7021 import SI7021
si7021 = SI7021(i2c)


while(True):
        temperature = round(si7021.temperature(), 1)

        print(temperature)
        dd.set_value(temperature)
        e.display_frame(buf)
        print("done")

        machine.deepsleep(300000)
