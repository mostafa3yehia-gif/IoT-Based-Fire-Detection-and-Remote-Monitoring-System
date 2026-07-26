import time
import machine
import dht
import network
from umqtt.simple import MQTTClient


sensor = dht.DHT22(machine.Pin(15))
led = machine.Pin(2, machine.Pin.OUT)
buzzer = machine.Pin(4, machine.Pin.OUT)

# WiFi
ssid = "Wokwi-GUEST"
password = ""

# MQTT
MQTT_BROKER = "broker.hivemq.com"
CLIENT_ID = "esp32_fire_sender"
TOPIC = b"MY"

# Connect WiFi
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)

    while not wifi.isconnected():
        pass

    print("WiFi Connected")

connect_wifi()

# Connect MQTT
client = MQTTClient(CLIENT_ID, MQTT_BROKER)
client.connect()
print("MQTT Connected")

while True:
    try:
        sensor.measure()

        temp = sensor.temperature()

        print("----------------------")
        print("Temperature:", temp, "C")

        if temp >= 48:
            led.on()
            buzzer.on()
            message = str(temp) + ",FIRE"

        else:
            led.off()
            buzzer.off()
            message = str(temp) + ",SAFE"

        # Publish الرسالة
        client.publish(TOPIC, message)
        print("Published:", message)

    except OSError:
        print("Sensor Error!")

    time.sleep(2)
