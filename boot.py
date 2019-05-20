# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import uos  # noqa: F401
import machine  # noqa: F401
# uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
if sta_if.active():
    ifconfig = sta_if.ifconfig()
    print("Connected! IP:", ifconfig[0])
else:
    print("Failed to connect :(")

webrepl.start()

gc.collect()
