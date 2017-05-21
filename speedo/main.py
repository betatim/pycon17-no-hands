import array
import machine
import micropython
import socket
import time


led = machine.Pin(0, machine.Pin.OUT)
led.high()
time.sleep(0.5)
led.low()
time.sleep(0.5)
led.high()

html = ("""<!DOCTYPE html><html><head><meta http-equiv="refresh" """
        """content="5"></head><body><h1>Speed!</h1>%s</body></html>""")

micropython.alloc_emergency_exception_buf(100)
index = 0
ticks = array.array('i', [0] * 10)
N = 0
p = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)


def cb(p):
    global ticks
    global index
    global N
    if p.value():
        ticks[index] = time.ticks_us()
        index = (index + 1) % 10
        N += 1

irq = p.irq(trigger=machine.Pin.IRQ_RISING, handler=cb)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    irq.trigger(False)

    vals = list(ticks)
    i = index - 1
    then, now = vals[i-1], vals[i]

    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break

    deltaT = (now - then) / 1000000
    circumference = 2.111  # meters

    if deltaT > 0 and time.ticks_us() - now < 5e6:
        speed = circumference / deltaT
        txt = "distance: %s speed: %sm/s" % (N * circumference, speed)
        txt += " speed: %s km/h %s mph" % (speed * 3.6, speed * 3.6 / 1.61)
    else:
        txt = "Start riding!"
        N = 0

    cl.send(html % txt)
    cl.close()
    print(time.ticks_us(), vals)
    irq.trigger(True)
