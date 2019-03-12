import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

	client.publish("esp8266/sensori", payload="o noel eh muito lindo", qos=1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

# Callback from publishing
def on_publish(client, userdata, mid):
	print("Success publishing.")

def on_disconnect(client, userdata, rc):
	if rc != 0:
		print("Unexpected disconnection")

client = mqtt.Client(client_id="pubs")
client.username_pw_set("zwrbsgco", password="Gu19Jq6j-ruy")
client.reconnect_delay_set(max_delay=60)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_disconnect = on_disconnect

try:
	client.connect("m11.cloudmqtt.com", 18002, keepalive=300)
except ConnectionError:
	print("Não foi possível conectar ao Broker. Confira se seu computador está conectado.")
	quit()
except Exception:
	print("Houve um erro. Tente novamente.")
	quit()

client.loop_start()

while True:
	client.publish("esp8266/sensori", payload="primeiro payload", qos=1)
	time.sleep(5)
	client.publish("esp8266/sensori", payload="segundo payload", qos=1)
	time.sleep(5)
