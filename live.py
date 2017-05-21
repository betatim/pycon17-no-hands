#
# Live coding examples
#

# First demo

print("Hello world!")
2 + 3
print("2 + 3 = {}".format((2+3)))
# maths as well
5/3
2**100
2**1000

import math
math.<tab>
math.sqrt(2**10)

# end
##########################################################################
# LED blinking demo

import machine

led = machine.Pin(2, machine.Pin.OUT)
led.high()  # off
led.low()

import time
for n in range(10):
    led.low()
    time.sleep(0.5)
    led.high()
    time.sleep(0.5)

# end
##########################################################################
# button pressing BROKEN

p = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
N = 0

def pressed(p):
    if p.value() == 0:
        global N
        N += 1
        print('button pressed %i times' % N)

irq = p.irq(trigger=machine.Pin.IRQ_FALLING, handler=pressed)

# end
##########################################################################
# allocate some memory for the traceback

import micropython
micropython.alloc_emergency_exception_buf(100)

# end
##########################################################################
# button pressing WORKS

p = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
N = 0

def pressed(p):
    if p.value() == 0:
        global N
        N += 1
        print('button pressed', N, 'times')

irq = p.irq(trigger=machine.Pin.IRQ_FALLING, handler=pressed)

# end
##########################################################################
# turn on wifi

import network

ap_if = network.WLAN(network.AP_IF)
ap_if.active()

print('network config:', sta_if.ifconfig())

# end
##########################################################################
# web server demo

import socket

html = ("""<!DOCTYPE html><html><head><meta http-equiv="refresh" """
        """content="1"></head><body><h1>Buttons!</h1>%s</body></html>""")

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

while True:
    cl, addr = s.accept()

    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break

    msg = 'Button has been pressed %i times.' % N
    cl.send(html % msg)
    cl.close()

# end
