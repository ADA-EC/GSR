#include <WiFiClient.h>
#include <ESP8266WiFi.h>
#include <MQTT.h>
#include <PubSubClient.h>

//----SERIAL CONFIG ----
#define SERIAL_SPEED        115200

//----WIFI CONFIG ----
#define WIFI_SSID           "Forfs"    //your Wifi SSID
#define WIFI_PASSWD         "toiao123" //your wifi password
#define MAX_WIFI_INIT_RETRY 10
#define WIFI_RETRY_DELAY    500

//----MQTT CONFIG ----
#define MQTT_CLIENT_ID      "ADA-GSR"
#define MQTT_SERVER         "m11.cloudmqtt.com" //MQTT broker sever. I use https://www.cloudmqtt.com/
#define MQTT_UNAME          "zwrbsgco"     //MQTT broker user name - I use this broker https://www.cloudmqtt.com/
#define MQTT_PASSW          "Gu19Jq6j-ruy" //MQTT broker password
#define MQTT_BROKER_PORT    18002          //MQTT BROKER listening port
#define MQTT_TOPIC_INFO     "esp32/pacient_info"
#define MQTT_TOPIC_RESPONSE "esp32/pacient_response"

#define ESP_NAME            "cavalo_de_troia"

#define outPin 14
#define inPin 15
#define ResistorShunt 27

WiFiClient wifi_client;
PubSubClient mqtt_client(wifi_client, MQTT_SERVER, MQTT_BROKER_PORT);
bool mqtt_status;
bool got_id = false;
bool work = true;

double val = 0 ; 
int freq = 1000;
double t = 0;
const double pi = 3.1415;
const double fs = 1000;
int ledChannel = 0;
int resolution = 8;
double shuntTensao;
//double current;
//double ResistPele;
double skinTensao;

//Wifi Initialization function
int WiFi_init(const char* wifi_ssid, const char* wifi_passwd){

        int retries = 0;

        Serial.print("Connecting to WiFi ");
        Serial.print(wifi_ssid);
        Serial.println("..........");

        //set wifi station mode => ESP will attempt to connect to the registered wifis 
        WiFi.mode(WIFI_STA);

        //start connecting to WiFi AP
        WiFi.begin(wifi_ssid, wifi_passwd);
        
        //check the status of WiFi connection to be WL_CONNECTED
        while ((WiFi.status() != WL_CONNECTED) && (retries < MAX_WIFI_INIT_RETRY)) {
               retries++;
               delay(WIFI_RETRY_DELAY);
               Serial.println("#");
        }

        //return the WiFi connection status
        return WiFi.status();
}

//MQTT callback function invoked for every MQTT received message on a subscribed topic
void mqtt_callback(const MQTT::Publish& pub){
        if(got_id == false){
               Serial.println("From topic " + pub.topic() + ", received message from pacient " + pub.payload_string() + "...\n");
               mqtt_client.publish(MQTT_TOPIC_RESPONSE, "1");
               got_id = true;
        }
        else{
               if(pub.payload_string() == "stop"){
                      work = false;
               }
               else if(pub.payload_string() == "work"){
                      work = true;
               }
               else{
                      mqtt_client.publish(MQTT_TOPIC_RESPONSE, "1");
               }
        }
}

int MQTT_init(){
        Serial.println("Initializing MQTT communication.........");

        //set callback on received messages => when a message arrives at the topic where the ESP is subscribed,
        //a function called "callback" is called
        mqtt_client.set_callback(mqtt_callback);
        //max retries to connect to the broker
        mqtt_client.set_max_retries(255);
        
        //here we connect to MQTT broker and we increase the keepalive for more reliability
        //keepalive = time in seconds of the connection
        //auth = username and password of the broker
        if (mqtt_client.connect(MQTT::Connect(MQTT_CLIENT_ID).set_keepalive(20000).set_auth(String(MQTT_UNAME), String(MQTT_PASSW)))) {
                Serial.println("Connection to MQTT broker SUCCESS..........");

                //tries to subscribe on the patient's info topic
                if (mqtt_client.subscribe(MQTT_TOPIC_INFO)) {
                        Serial.println("Subscription to MQTT topic [" + String(MQTT_TOPIC_INFO) + "] SUCCESS.........");
                }                
                else {
                        Serial.println("MQTT unable to subscribe to [" + String(MQTT_TOPIC_INFO) + "] ERROR.........");
                        mqtt_client.disconnect();
                        return false;
                }
        } 
        else {
                Serial.println("Connection to MQTT broker ERROR..........");
        }
        
        return mqtt_client.connected();
}

void connection_start(){
  //mqtt_status variable is pre-defined to be false
  mqtt_status = false;
  
  //Tries to connect on a wifi
  while(WiFi.status() != WL_CONNECTED){
    Serial.println("New attempt to connect to WiFi:");
    delay(500);
    if (WiFi_init(WIFI_SSID, WIFI_PASSWD) != WL_CONNECTED) {
      Serial.println("WiFi connection ERROR....");
    }
    else {
      //if connected, will show the IP of the connection
      Serial.print("WiFi connection OK with IP ");
      Serial.print(String(WiFi.localIP()[0]) + "." + String(WiFi.localIP()[1]) + "." + String(WiFi.localIP()[2]) + "." + String(WiFi.localIP()[3]));
      Serial.println("....");
    
      while(WiFi.status() == WL_CONNECTED && mqtt_status == false){
        //Initialization of the connection to the MQTT's broker
        Serial.println("New attempt to connect to MQTT's broker:");
        mqtt_status = MQTT_init();
      
        //"mqtt_status = true" means success
        if (!mqtt_status)
                Serial.println("MQTT connection ERROR....");
        else
                Serial.println("MQTT connection OK....");
      }
    }

    delay(2000);
  }
}

//example
void get_and_send_data(double shuntTensao, double skinTensao){
  mqtt_client.publish(MQTT_TOPIC_RESPONSE, "2" + String(skinTensao));
  mqtt_client.publish(MQTT_TOPIC_RESPONSE, "3" + String(shuntTensao));  
}

void setup() { 
  Serial.begin(SERIAL_SPEED);
  delay(100);
  Serial.println("Starting pins...");
  pinMode(outPin, OUTPUT);
  pinMode(inPin, INPUT);
  ledcSetup(ledChannel, 30000, resolution);
  
  Serial.println();
  Serial.println("MQTT connection starting....");
  
  connection_start();

  //example
}

void loop() {
     t = millis();
     val = 127+127*sin(2*pi*(freq/fs)*t);
     ledcWrite(outPin, val);
     shuntTensao = analogRead(inPin)*3.3/4096;
     //current = shuntTensao/ResistorShunt;
     skinTensao = val-shuntTensao;
     //ResistPele = skinTensao/current;
     //Serial.println(ResistPele);  
     delay(500);
     
     if(work == true){
         if(WiFi.status() != WL_CONNECTED){
             Serial.println("Connection to WiFi lost. Restarting connection...");
             delay(500);
             connection_start();
         }
         
         if (mqtt_status) {
             //we start with got_id = false, because we need a first handshake to make sure that the ESP32
             //is operation normally before sending data. After the handshake, we have got_id = true
             if(got_id == true){
                //below an example of sending data
                //mqtt_client.publish(MQTT_TOPIC_RESPONSE, "Hello I am ESP-" + String(ESP_NAME));
                get_and_send_data(shuntTensao, skinTensao);
                Serial.println("MQTT message sent....");
                delay(500);
             }
    
             //keeping the ESP in a loop on the connection
             mqtt_client.loop();
             delay(500);
         }
     }
}
