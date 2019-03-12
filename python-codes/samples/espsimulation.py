import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

	client.subscribe("esp32/pacient_info")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print("From topic "+msg.topic+", pacient is "+str(msg.payload)[1:])
	client.publish("esp32/pacient_response", payload=1, qos=1)

# Callback for subscribing
def on_subscribe(client, userdata, mid, granted_qos):
	print("Success subscribing.")

# Callback from publishing
def on_publish(client, userdata, mid):
	print("Success publishing.")

# Callback from disconnecting
def on_disconnect(client, userdata, rc):
	if rc != 0:
		print("Unexpected disconnection.")


client = mqtt.Client(client_id="espsim")
client.username_pw_set("zwrbsgco", password="Gu19Jq6j-ruy")
client.reconnect_delay_set(max_delay=60)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect

try:
	client.connect("m11.cloudmqtt.com", 18002, keepalive=300)
except ConnectionError:
	print("Could not connect to the Broker. Please check if you computer is connected and try again.")
	quit()
except Exception:
	print("An error has occurred. Try again.")
	quit()

client.loop_start()
transfer = False

while True:
	if transfer == False:
		pass
	else:
		#continuar
		pass

	#client.publish("esp8266/sensori", payload="primeiro payload", qos=1)
	#time.sleep(5)
	#client.publish("esp8266/sensori", payload="segundo payload", qos=1)
	#time.sleep(5)
