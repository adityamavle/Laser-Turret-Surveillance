#include <ArduinoJson.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX
const int ledPin = 13;           // LED connected to digital pin 13

void setup()
{
    Serial.begin(9600);
    mySerial.begin(9600);
    pinMode(ledPin, OUTPUT); // set the LED pin as an output
}

void loop()
{
    String receivedData = "";

    while (mySerial.available() > 0)
    {
        char c = mySerial.read();
        receivedData += c;
    }

    if (receivedData != "")
    {
        // Decode the received JSON data
        DynamicJsonDocument doc(1024);
        deserializeJson(doc, receivedData);

        // Get the values of angle_x, angle_y, and person from the decoded data
        int angle_x = doc["angle_x"];
        int angle_y = doc["angle_y"];
        int person = doc["person"];

        // Print the received values of angle_x, angle_y, and person
        Serial.print("Received: angle_x=");
        Serial.print(angle_x);
        Serial.print(", angle_y=");
        Serial.print(angle_y);
        Serial.print(", person=");
        Serial.println(person);

        // Toggle the LED at pin 13
        digitalWrite(ledPin, HIGH);
        delay(500);
        digitalWrite(ledPin, LOW);
    }
}
