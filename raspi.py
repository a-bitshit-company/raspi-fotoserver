import base64
from picamera import PiCamera
from time import sleep
import paho.mqtt.client as mqtt

PATH = '/home/pi/image.jpg'

def takePic():
    camera = PiCamera()
    camera.rotation = 0
    camera.framerate = 15
    sleep(5)
    camera.capture(PATH)

def encode_base64(fName):
    with open(fName, 'rb') as file:
        binary_file_data = file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        return base64_encoded_data.decode('utf-8')

def on_message(client, userdata, message):
    if(message.topic == 'notify'):
        takePic()
        client.publish("pictures", encode_base64(PATH))

client = mqtt.Client('raspi')
client.connect('127.0.0.1') #ip von mosquitto broker
client.subscribe("pictures")
client.subscribe("notify")
client.on_message = on_message
client.loop_forever



