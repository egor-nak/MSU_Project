#define EN_PIN    38  // LOW: Driver enabled. HIGH: Driver disabled
#define STEP_PIN  54  // Step on rising edge
#define DIR_PIN 55


#include <TMC2208Stepper.h> // Include library
#include <Servo.h>
TMC2208Stepper driver = TMC2208Stepper(&Serial1);  // Create driver and use
                                                 // HardwareSerial0 for communication
Servo myservo;

uint32_t last_time = 0;
bool dir = true;
double pos = 0;


void setup() {
  Serial.begin(9600);
  Serial.println("Start...");
  Serial1.begin(115200);        // Start hardware serial 1
  driver.push();                // Reset registers

  // Prepare pins
  pinMode(EN_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  digitalWrite(EN_PIN, HIGH);   // Disable driver in hardware

  driver.pdn_disable(true);     // Use PDN/UART pin for communication
  driver.I_scale_analog(false); // Use internal voltage reference
  driver.rms_current(500);      // Set driver current 500mA
  driver.toff(2);               // Enable driver in software

  digitalWrite(EN_PIN, LOW);    // Enable driver in hardware
  digitalWrite(DIR_PIN, LOW); // Если HIGH - то едет вниз, а если LOW - то вверх

  uint32_t data = 0;
  Serial.print("DRV_STATUS = 0x");
  driver.DRV_STATUS(&data);
  Serial.println(data, HEX);
  myservo.attach(11);
}

void loop() {
  for (pos = 0; pos <= 180.0; pos += 3.6) {
    myservo.write(pos);
    delay(1000);
    for (int i = 0; i < 2; ++i) {
      uint32_t ms = millis(); // выдаёт время в милисекундах с момента начала работы программы
      while ((millis() - ms) <= 14000) { // пока не пройдет четырнадцать секунд
        digitalWrite(STEP_PIN, HIGH);
        delay(1);                     // Мотор работает только когда мы включаем и выключаем пины
        digitalWrite(STEP_PIN, LOW);
        delay(1);
      }
      if (dir) {    // Меняем направление движения
        digitalWrite(DIR_PIN, HIGH);
        dir = false;
      } else {
        digitalWrite(DIR_PIN, LOW);
        dir = true;
      }
    }
  }
  for (pos = 180; pos >= 0.0; pos -= 3.6) {
    myservo.write(pos);
    delay(1000);
    for (int i = 0; i < 2; ++i) {
      uint32_t ms = millis();
      while ((millis() - ms) <= 14000) {
        digitalWrite(STEP_PIN, HIGH);
        delay(1);
        digitalWrite(STEP_PIN, LOW);
        delay(1);
      }
      if (dir) {
        digitalWrite(DIR_PIN, HIGH);
        dir = false;
      } else {
        digitalWrite(DIR_PIN, LOW);
        dir = true;
      }
    }
  }
}
