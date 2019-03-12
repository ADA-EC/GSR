import paho.mqtt.client as mqtt
import time
import datetime
import threading as thr

"""
resistor shunt (resistência mtmtmt pequena) em série com a pele => conversor AD calcula a tensão no resistor e assim temos a corrente
a tensão na pele é a tensão de saída menos a queda de tensão no shunt
Vpele/Ipele = Zpele
mandar dados do ESP para o pc e calcular aqui ou calcular no ESP?

tensão de saida
tensão de entrada
tensão do AD (resistor shunt -> calcular corrente)

"""
# Function executing in a thread to try to connect to the broker

MAX_RETRIES = 5
MAX_TIME_OF_DISCONNECTION = 30
RECEIVE = False
SHUNT_RESISTOR = 1 #ohm

def count_time_for_disconnection():
	global RECEIVE
	initialdate = datetime.datetime.now()
	actualdate = initialdate
	while((actualdate-initialdate).total_seconds() < MAX_TIME_OF_DISCONNECTION):
		#print((actualdate-initialdate).total_seconds())
		if(RECEIVE == False):
			actualdate = datetime.datetime.now()
			#print("RECEIVE false")

		else:
			#print("RECEIVE true")
			initialdate = datetime.datetime.now()
			actualdate = initialdate
			RECEIVE = False

		time.sleep(2)

def try_handshake():
	print("Waiting for ESP32 receive the solicitation of pacient " + idPacient + "...")
	client.publish("esp32/pacient_info", payload=idPacient, qos=1)
	print("Solicitation sent! Waiting for response.")
	client.subscribe("esp32/pacient_response")
	time.sleep(5)
	retries = 0
	while transfer == False and retries < MAX_RETRIES:
		print("Resending the solicitation...")
		if transfer == False:
			client.publish("esp32/pacient_info", payload=idPacient, qos=1)
		time.sleep(5)
		retries += 1

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	global connected
	connected = True

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global transfer
	global RECEIVE
	global skinTensao
	global shuntTensao
	#global tipoInfo
	if msg.topic == "esp32/pacient_response" and str(msg.payload)[2] == '1':
		print("Got response! Starting receiving data...")
		transfer = True
	else:
		if msg.topic == "esp32/pacient_info" and str(msg.payload)[2] == '2':
			skinTensao = str(msg.payload)[2:]
			skinTensao = skinTensao[:-1]
			#tipoInfo = 1
		elif msg.topic == "esp32/pacient_info" and str(msg.payload)[2] == '3':
			shuntTensao = str(msg.payload)[2:]
			shuntTensao = shuntTensao[:-1]
			#tipoInfo = 0
		print(msg.topic+" "+str(msg.payload))

	RECEIVE = True

# Callback for subscribing
def on_subscribe(client, userdata, mid, granted_qos):
	#print("Success subscribing.")
	pass

# Callback from publishing
def on_publish(client, userdata, mid):
	#print("Success publishing.")
	pass

# Callback from disconnecting
def on_disconnect(client, userdata, rc):
	global connected
	if rc != 0:
		print("Unexpected disconnection.")
		connected = False


idPacient = input("Enter here the pacient's id: ")
client = mqtt.Client(client_id="rootpc")
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

transfer = False
connected = False

client.loop_start()
while connected == False:
	time.sleep(3)

try_handshake()
if transfer == False:
	print("Could not connect to the ESP32. Please check the status of your board.")
	quit()

t = thr.Thread(target=count_time_for_disconnection)
t.start()

skinTensao = 0
shuntTensao = 1
skinCurrent = 0
skinImpedance = 0
#tipoInfo = 0

while True:
	if t.isAlive():
		if skinCurrent == 0:
			print("Waiting new information (current = 0).")
			time.sleep(1)
			if(shuntTensao != 0):
				skinCurrent = shuntTensao/SHUNT_RESISTOR
			pass
		else:
			print("skinTensao = " + str(skinTensao))
			print("shuntTensao = " + str(shuntTensao))
			skinCurrent = shuntTensao/SHUNT_RESISTOR
			skinImpedance = skinTensao/skinCurrent

			print("skinCurrent = " + str(skinCurrent))
			print("skinImpedance = " + str(skinImpedance))

			time.sleep(5)

	else:
		print("The ESP32 has been disconnected. Restart the program and your board.")
		quit()
	
	#client.publish("esp8266/sensori", payload="primeiro payload", qos=1)
	#time.sleep(5)
	#client.publish("esp8266/sensori", payload="segundo payload", qos=1)
	#time.sleep(5)