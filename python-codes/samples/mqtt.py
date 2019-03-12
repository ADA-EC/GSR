import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

'''
-   Implementar, numa situação de primeiro momento, o computador sendo
    publisher (colocando as informações do paciente no broker) e o ESP
    sendo subscriber (recebendo essas informações)

-   Implementar situação posterior ao recebimento dos dados do paciente (ESP 
    publisher preparado para receber os dados do circuito e o computador subscriber)

-   Verificar que forma os dados serão recebidos no ESP

-   Determinar uma estrutura para o dado que será enviado ao computador

-   Implementar envio dos dados pelo MQTT ao computador

-   Determinar um modo de interpretação dos dados (tradução de tensão para impedância)
    no código rodando no computador

-   Implementar construção de gráficos com os dados recebidos
'''

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    
    #msg = subscribe.simple("esp8266/sensori", hostname="m11.cloudmqtt.com",
	#port=18002, auth={'username':"zwrbsgco", 'password':"Gu19Jq6j-ruy"})
    #print("%s %s" % (msg.topic, msg.payload))
    
    #publish.single("esp8266/sensori", "potato vc eh potato", hostname="m11.cloudmqtt.com",
    #	port=18002, auth={'username':"zwrbsgco", 'password':"Gu19Jq6j-ruy"})

    client.subscribe("esp8266/sensori")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

#def on_subscribe(client, userdata, mid, granted_qos):
#-    print(userdata)

#def on_publish(cient, userdata, mid):
#    print("A mensagem foi enviada! mid = " + str(mid))
#    unsubscribe("esp8266/sensori")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.on_publish = on_publish

client.connect("m11.cloudmqtt.com", 18002, 300)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.publish("esp8266/sensori", "eu sou potato")
print("antes do while true")
while(True):
    pass