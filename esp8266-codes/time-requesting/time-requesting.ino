#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

const char* ssid     = "Forfs"; // network name
const char* password = "forfs123"; //password


// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);

// Variables to save date and time
String formattedDate;

struct st_day_hour{
  String dayStamp;
  String timeStamp;
};

struct st_day_hour get_day_hour()
{
  struct st_day_hour day_hour;
  while(!timeClient.update()) {
    timeClient.forceUpdate();
  }
  // The formattedDate comes with the following format:
  // 2018-05-28T16:00:13Z
  // We need to extract date and time
  formattedDate = timeClient.getFormattedDate();
  // Extract date
  int splitT = formattedDate.indexOf("T");
  day_hour.dayStamp = formattedDate.substring(0, splitT);
  day_hour.timeStamp = formattedDate.substring(splitT+1, formattedDate.length()-1);
  return day_hour;
}

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Initialize a NTPClient to get time
  timeClient.begin();
  timeClient.setTimeOffset(-10800);
}

void loop() {
  struct st_day_hour day_hour;
  day_hour = get_day_hour();
  Serial.print("DATE: ");
  Serial.println(day_hour.dayStamp);
  Serial.print("HOUR: ");
  Serial.println(day_hour.timeStamp);

}
