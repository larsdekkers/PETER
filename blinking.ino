int motor1 = 9; 
int motor1L = 8; 
int motor1R = 7; 
int motor2 = 11;
int motor2L = 12;
int motor2R = 13;
int sensOut = 5;
int sensIn = 6;

int error = 0;
int rotateTime = 1000; // time in ms
int moveTime = 1000; // time in ms
int motorSpeed = 255; //from 0 to 255
int sensStopDistance = 30; // in cm
String data;
float sensDuration, sensDistance; // in microsec and cm

void setup() { //runs on init
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(motor1, OUTPUT);
  pinMode(motor1L, OUTPUT);
  pinMode(motor1R, OUTPUT);
  pinMode(motor2, OUTPUT);
  pinMode(motor2L, OUTPUT);
  pinMode(motor2R, OUTPUT);
  pinMode(sensOut, OUTPUT);
  pinMode(sensIn, INPUT);
  Serial.begin(9600);
}
void loop() { // runs continualy
 	digitalWrite(sensOut, LOW);  
	delayMicroseconds(2);  
	digitalWrite(sensOut, HIGH);  
	delayMicroseconds(20);  
	digitalWrite(sensOut, LOW);  
 
 sensDuration = pulseIn(sensIn, HIGH); // getting the time that it took for the signal
 if (sensDuration < 58000) { // ignore all items that timed out
  sensDistance = (sensDuration*0.0343)/2; //speed of sound in cm/microSec
  if (sensDistance < sensStopDistance) { // if something is too close
    Stop();
    error = 1; 
  }
 }
 delay(30);
}
void ControlMotors(int motorNumber, int speed) { //running the motors
  if (motorNumber == 1) { // left motor
    if (speed == 0) { // stop the motor
      analogWrite(motor1, 0);
    }
    else if (speed > 0) { // run the motor forward
      digitalWrite(motor1R, HIGH);
      digitalWrite(motor1L, LOW);
      analogWrite(motor1, speed); //run it at set speed
    }
    else if (speed < 0) { // run the motor backward
      digitalWrite(motor1R, LOW);
      digitalWrite(motor1L, HIGH);
      analogWrite(motor1, abs(speed)); // use the positive value of speed
    }
  }
  else if (motorNumber == 2) { // right motor
    if (speed == 0) { // stop the motor
      analogWrite(motor2, 0);
    }
    else if (speed > 0) { // run the motor forward
      digitalWrite(motor2L, HIGH);
      digitalWrite(motor2R, LOW);
      analogWrite(motor2, speed);
    }
    else if (speed < 0) { // run the motor backward
      digitalWrite(motor2L, LOW);
      digitalWrite(motor2R, HIGH);
      analogWrite(motor2, abs(speed));
    }
  } 
}
void serialEvent() { // runs every time that anything happens in the Serial monitor
  if (Serial.available()) { // wait for a serial input
      data = Serial.readStringUntil('\n'); // get the string

      if (data == "0") { // stop all motors
        digitalWrite(LED_BUILTIN, LOW);
        Stop();
        Serial.println("done");
      }
      else if (data == "1") { // use for checking if something is wrong
        Serial.println(error);
      }
      else if (data == "right") { // rotating right and forward
        Rotate(90);
        Forward();
        Serial.println("done");
      }
      else if (data == "left") { // rotating left and forward
        Rotate(-90);
        Forward();
        Serial.println("done");
      }
      else if (data == "forward") { // moving forward
        Forward();
        Serial.println("done");
      }
      else if (data == "backward") { // moving backward
        Rotate(180);
        Forward();
        Serial.println("done");
      }
      else if (data == "lMotor") { // moving left motor forward
        ControlMotors(1, motorSpeed);
      }
      else if (data == "rMotor") { // moving right motor forward
        ControlMotors(2, motorSpeed);
      }
      else if (data == "bothF") { // moving both motors forward
        ControlMotors(1, motorSpeed);
        ControlMotors(2, motorSpeed);
      }
      else if (data == "bothB") { // moving both motors backward
        ControlMotors(1, -motorSpeed);
        ControlMotors(2, -motorSpeed);
      }
      else if (data == "reset") { // reset any errors
        error = 0;
      }
      else if (data[0] == 's') { //changing motorspeed
        motorSpeed = atoi(data.substring(1).c_str()); // convert the rest of the string to an int
      }
      else if (data[0] == 't') { // changing movetime
        moveTime = atoi(data.substring(1).c_str()); // convert the rest of the string to an int
      }
      else if (data[0] == 'r') { // changing rotatetime
        rotateTime = atoi(data.substring(1).c_str()); // convert the rest of the string to an int
      }

  }
}
void Rotate(int degrees) { //rotating peter using both weels
  if (degrees > 0) { // rotating right
    ControlMotors(1, motorSpeed);
    ControlMotors(2, -motorSpeed);
  }
  if (degrees < 0) { // rotating left
    ControlMotors(1, -motorSpeed);
    ControlMotors(2, motorSpeed);
  }
  int rotateTimes = (abs(degrees)/90); //calculate the time needed to rotate
  delay(rotateTime*rotateTimes); // wait until rotation is complete
}
void Forward() { // moving both motors forward
  ControlMotors(1, motorSpeed);
  ControlMotors(2, motorSpeed);
  delay(moveTime);
  Stop();
}
void Stop() { //stopping both motors
  ControlMotors(1, 0);
  ControlMotors(2, 0);
}
void Errorcode(char code[]) {
  for (int i = 0; i < strlen(code); i++) {
    int number = code[i];
    Serial.println(number);
    if (number == 48) { // 48 is de standaard code voor 0
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
    }
    else if (number == 49) { // 49 is de standaard code voor 1
      digitalWrite(LED_BUILTIN, HIGH);
      delay(1000);
    }
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
  }
}

