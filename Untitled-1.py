import paho.mqtt.client as mqtt #import the client1
broker_address="192.168.100.106"
#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client("testpc") #create new instance
client.connect(broker_address) #connect to broker
client.publish("dust","OFF")#publish