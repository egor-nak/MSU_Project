#include <GyverHX711.h>
#include <TMC2208Stepper.h>

#define PIN_FIRST_SCALES 21
#define PIN_SECOND_SCALES 20

#define EN_PIN_STEPPER_ROUND 38  // LOW: Driver enabled. HIGH: Driver disabled
#define STEP_PIN_STEPPER_ROUND 54  // Step on rising edge
#define DIR_PIN_STEPPER_ROUND 55

#define MOVE_UP_DIR_STEPPER_UP_CLOCKWISE HIGH
#define MOVE_UP_DIR_STEPPER_UP_NON_CLOCKWISE LOW

#define FiveV_pin 16



#define STEP_PIN_UP_DOWN 60
#define DIR_PIN_UP_DOWN 61
#define ENABLE_PIN_UP_DOWN 56

#define MOVE_DOWN_DIR_STEPPER_UP_DOWN LOW
#define MOVE_UP_DIR_STEPPER_UP_DOWN HIGH

#define DIGITAL_IN_OPTICAL_SENSOR_FOR_COUNT 32 // digital inputconst
#define DIGITAL_IN_OPTICAL_SENSOR_FOR_GO_HOME 57

#define END_STOP_PIN 32


TMC2208Stepper stepper_round = TMC2208Stepper(&Serial1);
TMC2208Stepper stepper_up_down = TMC2208Stepper(&Serial1);

GyverHX711 scales(PIN_FIRST_SCALES, PIN_SECOND_SCALES, HX_GAIN64_A); // объявление весов



const double max_pressure_value = 100.0;
bool flag_setting_scales = true; // Флаг выставление нужно ли выставить ноль на весах
double zero_scales_value = 0.0; // Значение нуля весов

int pin_now = 1; // на каком пине сейчас находится барабан
int pin_in_total = 25;



// ------------------------ END STOP -------------------------------------------

int end_stop_check_push() { // возвращает  значение зачал ли концевик (1 - не нажат, 0 - нажат)
  return digitalRead(END_STOP_PIN);
}


// ------------------------ Оптический датчик для возвращения в нулевую позицию -----------------------


void init_optical_sensor_for_go_home() {
  pinMode (DIGITAL_IN_OPTICAL_SENSOR_FOR_GO_HOME, INPUT);
}

bool get_value_from_optical_sensor_for_home() {
  bool value_D0 = digitalRead(DIGITAL_IN_OPTICAL_SENSOR_FOR_GO_HOME);
  return !value_D0;
}


// ------------------------- Весы -----------------------------

void set_up_zero_value_for_scales() { // функция выставления значения нуля весов
    long  tmp;
    uint32_t ms = millis();
    while ((millis() - ms) <= 3000) {
      tmp = scales.read();
    }
    zero_scales_value =(16477 - (tmp / 1000)) / 0.53;
    flag_setting_scales = false;
}

double get_scales_value() { // Функцяи получения силы давления в данный момент
  long  value = scales.read();
  double ans = (16477 - (value / 1000)) / 0.53 - zero_scales_value;
  return ans;
}


// ---------------------- Stepper для барабана (ROUND) -------------

void init_stepper_round() { // инициализация шаговика
  stepper_round.push();
  pinMode(EN_PIN_STEPPER_ROUND, OUTPUT);
  pinMode(STEP_PIN_STEPPER_ROUND, OUTPUT);
  pinMode(DIR_PIN_STEPPER_ROUND, OUTPUT);
  digitalWrite(EN_PIN_STEPPER_ROUND, HIGH);   // Disable driver in hardware

  stepper_round.pdn_disable(true);     // Use PDN/UART pin for communication
  stepper_round.I_scale_analog(false); // Use internal voltage reference
  stepper_round.rms_current(1000);      // Set driver current 500mA
  stepper_round.toff(2);               // Enable driver in software

  digitalWrite(EN_PIN_STEPPER_ROUND, LOW);    // Enable driver in hardware
  digitalWrite(DIR_PIN_STEPPER_ROUND, MOVE_UP_DIR_STEPPER_UP_NON_CLOCKWISE); 
}

void stepper_round_move_once() { // одно движение шаговика
  digitalWrite(STEP_PIN_STEPPER_ROUND, !digitalRead(STEP_PIN_STEPPER_ROUND));
  delayMicroseconds(500);
}

void stepper_round_change_pin(int pins_count) { // сдвинуться на n - количество пинов
  int count_interrapts = 0;
  int count_moves = 0;
  int count_pins_skiped = 0;
  while (count_pins_skiped != pins_count) {
    stepper_round_move_once();
    count_moves++;
    if (count_moves % 662 == 0) { // именно 662, я просто поситал, сколько ему нужно шагов, чтобы сместиться на один пин
      count_moves = 0;
      count_pins_skiped++;
    }
  }
//  Serial.println("st");
}

void go_to_the_pin_n(int pin_num) { // передаётся номер пина, индексация идёт с 1
  if (pin_num > pin_in_total || pin_num == pin_now) return ;
  if (pin_now < pin_num) {
    stepper_round_change_pin(pin_num - pin_now);
  } else {
    while (true) { // снова ноходим home
    bool ans_from_optical_sensor = get_value_from_optical_sensor_for_home();
    if (ans_from_optical_sensor) {
      break;
    }
    stepper_round_move_once();
   }
   stepper_round_change_pin(pin_num - 1);
  }
  pin_now = pin_num;
}

 


void go_to_the_home_position() {
  long tmp;
  uint32_t ms = millis();
  bool ans_from_optical_sensor;
  while ((millis() - ms) <= 3000) { // убераем весь шум с оптического датчика (на всякий случай)
    ans_from_optical_sensor = get_value_from_optical_sensor_for_home();
    tmp = scales.read();
  }
  while (true) { // нужно вначале соскочить с Home, чтобы потом не было неправильнйо постановки нуля
  ans_from_optical_sensor = get_value_from_optical_sensor_for_home();
  if (!ans_from_optical_sensor) {
    break;
  }
  stepper_round_move_once();
  }
  while (true) { // снова ноходим home
    ans_from_optical_sensor = get_value_from_optical_sensor_for_home();
    if (ans_from_optical_sensor) {
      break;
    }
    stepper_round_move_once();
  }

  for (int i = 0; i < 7; ++i) { // это просто костыль, чтобы он выставил ноль абсолютно точно
    stepper_round_move_once();
  }
}

// --------------------------- Stepper UP_DOWN -----------------------------

void init_stepper_up_down() {
  stepper_up_down.push();

  pinMode(ENABLE_PIN_UP_DOWN, OUTPUT);
  pinMode(STEP_PIN_UP_DOWN, OUTPUT);
  pinMode(DIR_PIN_UP_DOWN, OUTPUT);
  digitalWrite(ENABLE_PIN_UP_DOWN, HIGH);   // Disable driver in hardware

  stepper_up_down.pdn_disable(true);     // Use PDN/UART pin for communication
  stepper_up_down.I_scale_analog(false); // Use internal voltage reference
  stepper_up_down.rms_current(100);      // Set driver current 500mA
  stepper_up_down.toff(2);               // Enable driver in software

  digitalWrite(ENABLE_PIN_UP_DOWN, LOW);    // Enable driver in hardware
  digitalWrite(DIR_PIN_UP_DOWN, MOVE_UP_DIR_STEPPER_UP_DOWN); // Если HIGH - то едет вверх, а если LOW - то вниз
}

void stepper_up_down_move_once() { // одно движение шаговика
  digitalWrite(STEP_PIN_UP_DOWN, !digitalRead(STEP_PIN_UP_DOWN));
  delayMicroseconds(100);
}

void move_up_while_max_pressure() { // движение вверх до достижения порога давления
  double ans = get_scales_value();
  delay(500);                       // это кастыль, чтобы ацп не брало знаение из самого себя, его не удалять!!!!!!!!!!!!!!!!!!!!
  ans = get_scales_value();
  digitalWrite(DIR_PIN_UP_DOWN, MOVE_UP_DIR_STEPPER_UP_DOWN);
  while (ans <= max_pressure_value) {
    stepper_up_down_move_once();
    ans = get_scales_value();
  }
  digitalWrite(FiveV_pin, !digitalRead(FiveV_pin));
  delayMicroseconds(500);
}

void move_down_maximal() { // движение шаговика максимально вниз, пока он не нажмёт на концевик
  delay(500);
  digitalWrite(DIR_PIN_UP_DOWN, MOVE_DOWN_DIR_STEPPER_UP_DOWN);
  int ans_check = end_stop_check_push();
  while (ans_check != 0) {
    stepper_up_down_move_once();
    ans_check = end_stop_check_push();
  }

  digitalWrite(DIR_PIN_UP_DOWN, MOVE_UP_DIR_STEPPER_UP_DOWN);
  
  delayMicroseconds(500);
}

void stepper_up_down_press() { // функция выталкиевает пин с заданым давлением и потом возвращается в домашнее значение
  move_up_while_max_pressure();
  move_down_maximal();
}


// -------------------------------------------------------------------------

void press_pin_number(int n) { // передаётся номер пина, индексация идёт с 1
  go_to_the_pin_n(n);
  stepper_up_down_press();
}

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  
  // --------------------- Весы --------------------------
  delay(500); // это время на то чтобы датчик весов очнулся
  scales.tare(); // калибровка нуля весов
 // ------------------------------------------------------

 pinMode(FiveV_pin, OUTPUT); // делайем, пин для пяти вольтового разряда
 init_stepper_round();
 init_optical_sensor_for_go_home();
 init_stepper_up_down();
// set_up_zero_value_for_scales();
// move_down_maximal(); // возвращяем макимально вниз шаговик для up_down движений
// go_to_the_home_position(); // идём на начальную позицию с пином номер 1
}


void loop() {
  if (flag_setting_scales) { // выставление значения нуля весам
     set_up_zero_value_for_scales();
     move_down_maximal(); // возвращяем макимально вниз шаговик для up_down движений
     go_to_the_home_position(); // идём на начальную позицию с пином номер 1
   }
  while (!Serial.available());
  int x = Serial.readString().toInt();
  press_pin_number(x);
}
