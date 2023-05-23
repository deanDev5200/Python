#include <Servo.h>


Servo servoEye;
Servo servoEyeUpDown;
Servo servoJaw;
bool isConnect;
bool isTalk;
int buzzer = 13;
unsigned long lastMls;
void setup() { 
  Serial.begin(9600);
  servoEye.attach(9);
  servoEyeUpDown.attach(10);
  servoJaw.attach(11);
  servoJaw.write(90);
  servoEye.write(90);
  servoEyeUpDown.write(135);
}

void loop()
{
  if (Serial.available())
  {
    char c = Serial.read();
    if (isConnect)
    {
      if (c=='#')
      {
        tone(buzzer, 659.26, 50);
        delay(50);
        delay(30);
        tone(buzzer, 1760, 55);
        delay(55);
        delay(25);
        tone(buzzer, 1318.51, 50);
        delay(50);
        delay(10);
        isConnect = false;
      }
      else if (c=='.')
      {
        isTalk = true;
        lastMls = millis()/100;
      }
      else if (c==',')
      {
        isTalk = false;
      }
    }
    else
    {
      if (c=='%')
      {
        tone(buzzer, 659.26, 50);
        delay(50);
        delay(30);
        tone(buzzer, 1318.51, 55);
        delay(55);
        delay(25);
        tone(buzzer, 1760, 60);
        delay(60);
        delay(10);
        isConnect = true;
      }
    }
  }

  if (isConnect)
  {
    if (isTalk)
    {
      Jaw();
    }
    else
    {
      servoJaw.write(90);
      servoEye.write(90);
      servoEyeUpDown.write(135);
    }
  }
}

void Eye()
{
  int rand = random(0, 29)/10;
  if (rand == 0)
  {
    servoEye.write(0);
  }
  else if (rand == 1)
  {
    servoEye.write(90);
  }
  else if (rand == 2)
  {
    servoEye.write(180);
  }
}

void Jaw()
{
  unsigned long mls = millis()/100;
  //Serial.println("millis: " + String(mls) + " last: " + String(lastMls));
  if (mls > lastMls+42)
  {
    servoJaw.write(90);
    lastMls = mls;
  }
  else if (mls > lastMls+39)
  {
    servoJaw.write(135);
  }
  else if (mls > lastMls+36)
  {
    servoJaw.write(90);
  }
  else if (mls > lastMls+33)
  {
    servoJaw.write(135);
  }
  else if (mls > lastMls+30)
  {
    servoJaw.write(90);
  }
  else if (mls > lastMls+27)
  {
    servoJaw.write(135);
  }
  else if (mls > lastMls+24)
  {
    servoJaw.write(90);
    Eye();
  }
  else if (mls > lastMls+21)
  {
    servoJaw.write(135);
  }
  else if (mls > lastMls+18)
  {
    servoJaw.write(90);
  }
  else if (mls > lastMls+15)
  {
    servoJaw.write(135);
  }
  else if (mls > lastMls+12)
  {
    servoJaw.write(90);
  }
  else if (mls > lastMls+9)
  {
    servoJaw.write(135);
  }
  else if (mls > lastMls+6)
  {
    servoJaw.write(90);
  }
  else if (mls > lastMls+3)
  {
    servoJaw.write(135);
    Eye();
  }
}
