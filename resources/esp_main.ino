#include "Arduino.h"
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <Wire.h>
#include <BH1750.h>
const char* ssid     = "Totalplay-10F7";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "1asdasdasdasd";     // The password of the Wi-Fi network
#define HTTP_REST_PORT 8080
ESP8266WebServer server(HTTP_REST_PORT);
// Set your Static IP address
IPAddress local_IP(192, 168, 1, 169);
// Set your Gateway IP address
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);
IPAddress primaryDNS(8, 8, 8, 8); // optional
IPAddress secondaryDNS(8, 8, 4, 4); // optional
BH1750 lightMeter;
int humidity = 0; 
const int relay = D1;

void ping() {
    server.send(200, "text/json", "Service is alive");
}
void get_humidity() {
     //humidity = analogRead(A0);
    humidity = digitalRead(relay);
    // humidity = map(humidity,550,0,0,100);
    Serial.print(humidity);
    if(humidity ==HIGH)
    {
      Serial.println("Encendido");  
      //hacer las acciones necesarias
    }
    String response_txt=String(humidity);
    server.send(200, "text/json", "{\"humidity\":" +response_txt +"}");
}

void get_pump() {
    // Normally Open configuration, send LOW signal to let current flow
    // (if you're usong Normally Closed configuration send HIGH signal)
    digitalWrite(relay, HIGH);
    Serial.println("Current Flowing");
    delay(5000); 
    
    // Normally Open configuration, send HIGH signal stop current flow
    // (if you're usong Normally Closed configuration send LOW signal)
    digitalWrite(relay, LOW);
    Serial.println("Current not Flowing");
    delay(5000);
    server.send(200, "text/json", "{\"Activated pump\"}");
} 
void get_light() {
     //humidity = analogRead(A0);
    float lux = lightMeter.readLightLevel();
    // humidity = map(humidity,550,0,0,100);
    Serial.print(lux);
   
    String response_txt=String(lux);
    server.send(200, "text/json", "{\"lux\":" +response_txt +"}");
}
void restServerRouting() {
    server.on("/", HTTP_GET, []() {
        server.send(200, F("text/html"),
            F("Welcome to the REST Web Server"));
    });
    server.on(F("/get_humidity"), HTTP_GET, get_humidity);
    server.on(F("/get_pump"), HTTP_GET, get_pump);
    server.on(F("/get_light"), HTTP_GET, get_light);
    server.on(F("/ping"), HTTP_GET, ping);
}
// Manage not found URL
void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}
 
void setup(void) {
  Serial.begin(115200);
  //Serial.begin(9600);
  WiFi.mode(WIFI_STA);
  // Configures static IP address
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("STA Failed to configure");
  }
  WiFi.begin(ssid, password);
  Serial.println("");
 
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
 
  // Activate mDNS this is used to be able to connect to the server
  // with local DNS hostmane esp8266.local
  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  //pinMode(sensorPin, INPUT);
  pinMode(relay, OUTPUT);

  Wire.begin();
  if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println(F("BH1750 initialised"));
  }
  else {
    Serial.println(F("Error initialising BH1750"));
  }
  // Set server routing
  restServerRouting();
  // Set not found response
  server.onNotFound(handleNotFound);
  // Start server
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop(void) {
  server.handleClient();
}
