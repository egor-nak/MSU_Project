// Include library
#include <TMC2208Stepper.h>
#include <Servo.h>
#include <GyverHX711.h>
#include <ArduinoSTL.h>



// Помечаем нужные пины
#define EN_PIN    38  // LOW:Driver enabled. HIGH: Driver disabled
#define STEP_PIN  54  // Step on rising edge
#define DIR_PIN 55
#define X_MIN 2
#define LIGHT_PIN 40

bool button_was_pushed = false;
bool direct = false; // true - наверх, false - вниз


// обозначаем используемые элементы
TMC2208Stepper driver = TMC2208Stepper(&Serial1);
Servo myservo;
GyverHX711 sensor(21, 20, HX_GAIN32_B);
// HX_GAIN128_A - канал А усиление 128
// HX_GAIN32_B - канал B усиление 32
// HX_GAIN64_A - канал А усиление 64

void go_down_until_end();

void setup() {

  // Обозначаем порты вывода
  Serial.begin(250000);
  Serial1.begin(250000);
  
  driver.push();

  // Prepare pins
  pinMode(EN_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(X_MIN, OUTPUT);

  
  // Настройка шаговика
  digitalWrite(EN_PIN, HIGH);   // Disable driver in hardware
  driver.pdn_disable(true);     // Use PDN/UART pin for communication
  driver.I_scale_analog(false); // Use internal voltage reference
  driver.rms_current(500);      // Set driver current 500mA
  driver.toff(2);               // Enable driver in software
  digitalWrite(EN_PIN, LOW);    // Enable driver in hardware
  digitalWrite(DIR_PIN, LOW); // Если HIGH - то едет вниз, а если LOW - то вверх
  direct = true;

  uint32_t data = 0;
  driver.DRV_STATUS(&data);


  // Настройка сервы
  myservo.attach(11);


  // Настройка концевика
  attachInterrupt(0, myEventListener, CHANGE);


  // Настройка АЦП
  sensor.tare();


  // Светодиод
  pinMode(LIGHT_PIN, OUTPUT);
  digitalWrite(LIGHT_PIN, LOW);
}


void loop() {
  digitalWrite(LIGHT_PIN, LOW);
  for (int pos = 0; pos <= 180; pos += 3.6) { //серва куртится по часовой
     myservo.write(pos);
     delay(1000);
     go_up_until_end();
     go_down_until_end();
  }

  for (int pos = 180; pos >= 0; pos -= 3.6) { //серва куртится против часовой
     myservo.write(pos);
     delay(1000);
     digitalWrite(LIGHT_PIN, LOW);
     go_up_until_end();
     go_down_until_end();
  }
    
}

void go_down_until_end() {
  
  digitalWrite(DIR_PIN, HIGH); // он теперь едет вниз
  direct = false;
  while (!button_was_pushed) { // едем вниз пока не нажмем на концевик
    digitalWrite(STEP_PIN, HIGH);
    delay(1);
    digitalWrite(STEP_PIN, LOW);
    delay(1);
  }

  digitalWrite(DIR_PIN, LOW); // он теперь едет вверх
  direct = true;
  button_was_pushed = false;
  for (int i = 0; i < 100; ++i) {
    digitalWrite(STEP_PIN, HIGH);
    delay(1);
    digitalWrite(STEP_PIN, LOW);
    delay(1);
  }

  digitalWrite(DIR_PIN, HIGH); // он теперь едет вниз
  direct = false;
}


void go_up_until_end() {
  digitalWrite(DIR_PIN, LOW); // он теперь едет вверх
  direct = true;
  
  int prev = 0;
  if (sensor.available()) {
      prev = sensor.read();
  }
//  Serial.println(sensor.read());
  while (sensor.read() <= 800000) { // едем вверх пока не изменится давление
    digitalWrite(STEP_PIN, HIGH);
    delay(1);
    digitalWrite(STEP_PIN, LOW);
    delay(1);
    prev = sensor.read();
//    Serial.println(sensor.read());
  }
  digitalWrite(LIGHT_PIN, HIGH);
  Serial.println("HIGH");
  delay(1000);
  digitalWrite(LIGHT_PIN, LOW);
  Serial.println("LOW");
  delay(1000);
}

void myEventListener() {
  button_was_pushed = true;
}
