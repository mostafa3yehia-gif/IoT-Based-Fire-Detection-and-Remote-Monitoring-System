import network
from umqtt.simple import MQTTClient
import time
from machine import Pin, SoftI2C
from i2c_lcd import I2cLcd

led = Pin(2, Pin.OUT)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
lcd = I2cLcd(i2c, 0x27, 2, 16)

# WiFi 
ssid = "Wokwi-GUEST"
password = ""

# MQTT
MQTT_BROKER = "broker.hivemq.com"
CLIENT_ID = "receiver"
TOPIC = b"MY"

# Callback 
def callback_function(topic, msg):

    msg = msg.decode()
    print(msg)

    temp, status = msg.split(",")

    lcd.clear()

    lcd.move_to(0, 0)
    lcd.putstr("Temp:{} C".format(temp))

    lcd.move_to(0, 1)

    if status == "FIRE":
        led.on()
        lcd.putstr("!!! FIRE !!!")

    else:
        led.off()
        lcd.putstr("Status: SAFE")

# WiFi 
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    pass

lcd.clear()
lcd.putstr("WiFi Connected")
time.sleep(2)

client = MQTTClient(CLIENT_ID, MQTT_BROKER)
client.set_callback(callback_function)
client.connect()

lcd.clear()
lcd.putstr("MQTT Connected")
time.sleep(2)

client.subscribe(TOPIC)

lcd.clear()
lcd.putstr("Waiting...")
time.sleep(1)

while True:
    client.check_msg()
    time.sleep(2)
