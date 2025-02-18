
String data;
int motor1 = 9; 
int motor1L = 8; 
int motor1R = 7; 
int motor2 = 11;
int motor2L = 12;
int motor2R = 13;
int sensOut = 5;
int sensIn = 6;
int error = 0;

int rotateTime = 1000;
int moveTime = 1000;
float duration, distance;
void setup() {
  // put your setup code here, to run once:
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
 	digitalWrite(sensOut, LOW);  
	delayMicroseconds(2);  
	digitalWrite(sensOut, HIGH);  
	delayMicroseconds(20);  
	digitalWrite(sensOut, LOW);  
 
 duration = pulseIn(sensIn, HIGH);
 distance = (duration*0.0343)/2; //speed of sound in cm/microSec
 if (distance < 1000) {
  if (distance < 30) {
    Stop();
    error = 1;
  }
 }
 delay(100);
}

void ControlMotors(int motorNumber, int speed) {
  if (motorNumber == 1) {
    if (speed == 0) {
      analogWrite(motor1, 0);
    }
    else if (speed > 0) {
      digitalWrite(motor1R, HIGH);
      digitalWrite(motor1L, LOW);
      analogWrite(motor1, abs(speed));
    }
    else if (speed < 0) {
      digitalWrite(motor1R, LOW);
      digitalWrite(motor1L, HIGH);
      analogWrite(motor1, abs(speed));
    }
  }
  else if (motorNumber == 2) {
    if (speed == 0) {
      analogWrite(motor2, 0);
    }
    else if (speed > 0) {
      digitalWrite(motor2L, HIGH);
      digitalWrite(motor2R, LOW);
      analogWrite(motor2, abs(speed));
    }
    else if (speed < 0) {
      digitalWrite(motor2L, LOW);
      digitalWrite(motor2R, HIGH);
      analogWrite(motor2, abs(speed));
    }
  }
  
}
void serialEvent() {
  if (Serial.available()) {
      data = Serial.readStringUntil('\n');
      if (data == "0") {
        digitalWrite(LED_BUILTIN, LOW);
        Stop();
        Serial.println("done");
      }
      else if (data == "1") {
        Serial.println(error);
      }
      else if (data == "right") {
        Rotate(90);
        Forward();
        delay(moveTime);
        Serial.println("done");
      }
      else if (data == "left") {
        Rotate(-90);
        Forward();
        delay(moveTime);
        Serial.println("done");
      }
      else if (data == "forward") {
        Forward();
        delay(moveTime);
        Serial.println("done");
      }
      else if (data == "backward") {
        Rotate(180);
        Forward();
        delay(moveTime);
        Serial.println("done");
      }
      else if (data == "lMotor") {
        ControlMotors(1, 255);
      }
      else if (data == "rMotor") {
        ControlMotors(2, 255);
      }
      else if (data == "bothF") {
        ControlMotors(1, 255);
        ControlMotors(2, 255);
      }
      else if (data == "bothB") {
        ControlMotors(1, -255);
        ControlMotors(2, -255);
      }
      else if (data == "reset") {
        error = 0;
      }
  }
}
void Rotate(int degrees) {
  if (degrees > 0) {
    ControlMotors(1, 255);
    ControlMotors(2, -255);
  }
  if (degrees < 0) {
    ControlMotors(1, -255);
    ControlMotors(2, 255);
  }
  int rotateTimes = (abs(degrees)/90);
  delay(rotateTime*rotateTimes);
}

void Forward() {
  ControlMotors(1, 255);
  ControlMotors(2, 255);
}
void Stop() {
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

