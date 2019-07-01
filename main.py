import machine
import usocket
from machine import Pin

button = Pin(4, Pin.IN)
led_r = Pin(15, Pin.OUT)
led_g = Pin(12, Pin.OUT)
led_b = Pin(13, Pin.OUT)

led_r.on()
led_g.off()
led_b.off()

state = False

# TODO: The doorbell goes high but this button goes low
EXPECTED_STATE = 1
IRQ_EDGE = Pin.IRQ_RISING
# DOORBELL_TIME = 1000000 # 1s
DOORBELL_TIME = 60000  # 60ms
DOORBELL_TIMEOUT = 10000000  # 10s

IRCCAT_HOST = "10.143.0.12"
IRCCAT_PORT = 12345
# IRCCAT_HOST = "192.168.88.251"
# IRCCAT_PORT = 8080

IRCCAT_ADDR = usocket.getaddrinfo(IRCCAT_HOST, IRCCAT_PORT)[0][-1]

DOORBELL_MESSAGE = "BING BONG! Somebody's at the door!"
STARTUP_MESSAGE = "The doorbell has entered the building"
STARTUP_TIME_MS = 1000  # 1s
# STARTUP_TIME_MS = 10000  # 10s


in_startup = True


def startupify(_):
    global in_startup
    in_startup = False
    print("Started up")


startup_timer = machine.Timer(1)
startup_timer.init(
    mode=machine.Timer.ONE_SHOT, period=STARTUP_TIME_MS, callback=startupify
)


def bing_bong(message):
    sock = usocket.socket()
    sock.connect(IRCCAT_ADDR)
    sock.send(bytes(message, "utf8"))
    sock.send(bytes("\n", "utf8"))
    sock.close()


def on_press(pin):
    if pin.value() == EXPECTED_STATE:
        pulse_len = machine.time_pulse_us(pin, EXPECTED_STATE, DOORBELL_TIMEOUT)
        if pulse_len > DOORBELL_TIME:
            if in_startup:
                bing_bong(STARTUP_MESSAGE)
            else:
                bing_bong(DOORBELL_MESSAGE)


button.irq(on_press)

print("woop")
