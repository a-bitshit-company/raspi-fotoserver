import paho.mqtt.client as mqtt

counter = 0
def on_message(client, userdata, message):
    if(message.topic == 'notify'):
        counter+1
        print("new picture taken")

client = mqtt.Client('countClient')
client.connect('127.0.0.1') #ip von mosquitto broker
client.subscribe("notify")
client.on_message = on_message
client.loop_forever
