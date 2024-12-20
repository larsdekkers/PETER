
String data ;
void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  
}

void serialEvent() {
  if (Serial.available()) {
      data = Serial.readStringUntil('\n');
      if (data == "on") {
        digitalWrite(LED_BUILTIN, HIGH);
        Serial.println("hello");
      }
      else if (data == "off") {
        digitalWrite(LED_BUILTIN, LOW);
      }

      else if (data == "0") {
        Errorcode("1101");
      }
  }
}
void Errorcode(char code[]) {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  for (int i = 0; i < strlen(code); i++) {
    int number = code[i];
    Serial.println(number);
    if (number == 48) { // 48 is de standaard code voor 0
      digitalWrite(LED_BUILTIN, LOW);
    }
    else if (number == 49) { // 49 is de standaard code voor 1
      digitalWrite(LED_BUILTIN, HIGH);
    }
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
  }
}

