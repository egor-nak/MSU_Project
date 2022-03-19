#include <SpeedyStepper.h>



const int LED_PIN = 26;
const int MOTOR_STEP_PIN = 3;
const int MOTOR_DIRECTION_PIN = 2;



SpeedyStepper stepper;

void setup() 
{
  Serial.begin(57600);
  pinMode(LED_PIN, OUTPUT);   
  stepper.connectToPins(MOTOR_STEP_PIN, MOTOR_DIRECTION_PIN);
}



void loop() 
{
  stepper.setSpeedInStepsPerSecond(1800);
  stepper.setAccelerationInStepsPerSecondPerSecond(1800);
  char ans = Serial.read();
  Serial.write(ans);
  if (ans == -1) {
    stepper.setSpeedInStepsPerSecond(18000);
  stepper.setAccelerationInStepsPerSecondPerSecond(18000);
     stepper.moveRelativeInSteps(18000*5);
    delay(100);
  }
  if (ans == '9') {
    stepper.moveRelativeInSteps(-800*5);
    delay(100);
  } else if (ans == '8'){
    stepper.moveRelativeInSteps(800*5);
    delay(100);
  }
}
