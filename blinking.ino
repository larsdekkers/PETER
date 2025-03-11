int motor1 = 9; 
int motor1L = 8; 
int motor1R = 7; 
int motor2 = 11;
int motor2L = 12;
int motor2R = 13;
int sensOut = 5;
int sensIn = 6;

int error = 0;
int rotateTimeL = 600; // time in ms to rotate left
int rotateTimeR = 710; // time in ms to rotate right

int moveTime = 260; // time in ms
int moveTimeStart = 260;
int moveTimeStop = 260;

int motorSpeed = 120; //from 0 to 255
int sensStopDistance = 70; // in cm
int startTime = 100; // time in ms
int motorAdjustment = 97; // in % of total

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
void loop() {

}
void ControlMotors(int motorNumber, int speed) { //running the motors
  if (motorNumber == 1) { // left motor
    if (speed == 0) { // stop the motor
      analogWrite(motor1, 0);
    }
    else if (speed > 0) { // run the motor forward
      digitalWrite(motor1R, LOW);
      digitalWrite(motor1L, HIGH);
      int motorspeed = speed*(motorAdjustment/100.0);
      analogWrite(motor1, motorspeed); //run it at set speed
    }
    else if (speed < 0) { // run the motor backward
      digitalWrite(motor1R, HIGH);
      digitalWrite(motor1L, LOW);
      int motorspeed = abs(speed)*(motorAdjustment/100.0);
      analogWrite(motor1, motorspeed); // use the positive value of speed
    }
  }
  else if (motorNumber == 2) { // right motor
    if (speed == 0) { // stop the motor
      analogWrite(motor2, 0);
    }
    else if (speed > 0) { // run the motor forward
      digitalWrite(motor2L, LOW);
      digitalWrite(motor2R, HIGH);
      analogWrite(motor2, speed);
    }
    else if (speed < 0) { // run the motor backward
      digitalWrite(motor2L, HIGH);
      digitalWrite(motor2R, LOW);
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
      else if (data == "forward") { // moving forward
        Forward(moveTime);
        Serial.println("done");
      }
      else if (data == "right") { // rotating right
        Rotate(-90);
        Stop();
        delay(500);
        Serial.println("done");
      }
      else if (data == "left") { // rotating left
        Rotate(90);
        Stop();
        delay(500);
        Serial.println("done");
      }
      else if (data == "backward") { // rotating backward
        Rotate(90);
        Stop();
        delay(500);
        Rotate(90);
        Stop();
        delay(500);
        Serial.println("done");
      }
      else if (data == "forwardStart") { // initial high power for starting
        Start(3, 1, 1);
        Forward(moveTimeStart);
        Serial.println("done");
      }
      else if (data == "forwardStop") {
        Forward(moveTimeStop);
        Stop(); 
        delay(500);
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
      else if (data[0] == 'f') { // changing moveTime
        if (data[1] == 't') {
        moveTimeStart = atoi(data.substring(2).c_str());
        }
        else if (data[1] == 'p') {
         moveTimeStop = atoi(data.substring(2).c_str());
        }
        else {
        moveTime = atoi(data.substring(2).c_str()); // convert the rest of the string to an int
        }
      }
      else if (data[0] == 'r') { // changing rotateTime
        if (data[1] == 'l') { // left time
          rotateTimeL = atoi(data.substring(2).c_str());
        }
        else { // right time
          rotateTimeR = atoi(data.substring(2).c_str()); // convert the rest of the string to an int
        }
      }
      else if (data[0] == 'a') { // changing startTime
        startTime = atoi(data.substring(1).c_str()); // convert the rest of the string to an int
      }
      else if (data[0] == 'm') { // changing motorAdjustment
        motorAdjustment = atoi(data.substring(1).c_str()); // convert the rest of the string to an int
      }
      else if (data[0] == 'd') { // sensStopDistance
        sensStopDistance = atoi(data.substring(1).c_str()); // convert the rest of the string to an int
      }
  }
}
void Start(int motorNumber, int direction, int direction2) { // small high voltage to start motors
  if (motorNumber == 3) {
    ControlMotors(1, 255*direction);
    ControlMotors(2, 255*direction2);
  }
  else {
    ControlMotors(motorNumber, 255*direction);
  }
  delay(startTime);
}
void Rotate(int degrees) { //rotating peter using both weels
  int rotateTimes = (abs(degrees)/90); //calculate the time needed to rotate
  if (degrees > 0) { // rotating left
    Start(3, 1, -1);
    ControlMotors(1, motorSpeed);
    ControlMotors(2, -motorSpeed);
    delay(rotateTimeL*rotateTimes); // wait until rotation is complete
  }
  if (degrees < 0) { // rotating right
    Start(3, -1, 1);
    ControlMotors(1, -motorSpeed);
    ControlMotors(2, motorSpeed);
    delay(rotateTimeR*rotateTimes); // wait until rotation is complete
  }
}
void Forward(int time) { // moving both motors forward
  ControlMotors(1, motorSpeed);
  ControlMotors(2, motorSpeed);
  int times = time/40;
  int timeForEach = time/times;
  for (int i = 0; i < times; i++) {
    delay(timeForEach);
    ReadSensor();
  }
  Stop();
}
void Stop() { //stopping both motors
  ControlMotors(1, 0);
  ControlMotors(2, 0);
}
void ReadSensor() { // checking if something is nearby
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
    digitalWrite(LED_BUILTIN, HIGH);
    error = 1; 
  }
 }
}


