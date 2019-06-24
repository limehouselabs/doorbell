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
if not sta_if.isconnected():
    while True:
        status = sta_if.status()
        if status == network.STAT_IDLE:
            print("ERROR: Not doing anything??")
            machine.deepsleep()
        elif status == network.STAT_GOT_IP:
            print("Connected!")
            break
        elif status == network.STAT_WRONG_PASSWORD:
            print("ERROR: AP Password has changed!")
            machine.deepsleep()
        elif status == network.STAT_NO_AP_FOUND:
            print("WARNING: No AP found...? Sleeping for 1 minute.")
            machine.deepsleep(60000)
        elif status == network.STAT_CONNECT_FAIL:
            print("ERROR: Unable to connect :(")
            machine.deepsleep(300000)
        else:
            print("Connecting...")
            machine.lightsleep(1000)

ifconfig = sta_if.ifconfig()
print("IP:", ifconfig[0])

webrepl.start()

gc.collect()
