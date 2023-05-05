#include <Servo.h>

Servo myservo;

void myFunction()
{
  Serial.println("My function is running!");
}

void setup()
{
  Serial.begin(9600);
  myservo.attach(9);
  // attach servo to pin 9
  while (!Serial)
  {
    // wait for serial port to connect
  }
}

void loop()
{
  if (Serial.available())
  {
    String angle_x = Serial.readString();
    myservo.write(angle_x.toInt());
    Serial.println(angle_x);
    //if(isInt(angle_x)==True)
    //{
    if(angle_x.toInt() > 45)
    {
      digitalWrite (LED_BUILTIN, HIGH);
    }
    else{
      digitalWrite(LED_BUILTIN,LOW);
    }
    myFunction(); // Call the custom function
  }
}
