import time
import network
import gc


gc.collect()

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("G2_8802", "portland")
sta_if.ifconfig((('192.168.43.153', '255.255.255.0', '192.168.43.1', '192.168.43.1')))

while not sta_if.isconnected():
    time.sleep(0.5)

print('network config:', sta_if.ifconfig())
