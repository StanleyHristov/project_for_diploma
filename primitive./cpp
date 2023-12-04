#include <TimerOne.h>

struct IRSensor {
  int pin;
  int threshold;
};

class MotorController {
public:
  MotorController(int pin1, int pin2) : motorPin1(pin1), motorPin2(pin2) {
    pinMode(motorPin1, OUTPUT);
    pinMode(motorPin2, OUTPUT);
  }

  void moveLeft() {
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, HIGH);
  }

  void moveRight() {
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, LOW);
  }

  void stop() {
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);
  }

private:
  int motorPin1;
  int motorPin2;
};

void setupIRSensor(IRSensor &sensor) {
  pinMode(sensor.pin, INPUT);
}

bool isObstacleDetected(const IRSensor &sensor) {
  return analogRead(sensor.pin) < sensor.threshold;
}

void moveBasedOnIRSensors(const IRSensor &leftSensor, const IRSensor &rightSensor, MotorController &motorController) {
  if (isObstacleDetected(leftSensor)) {
    motorController.moveRight();
  } else if (isObstacleDetected(rightSensor)) {
    motorController.moveLeft();
  } else {
    motorController.stop();
  }
}

const int timerInterval = 100000;
volatile bool timerFlag = false;

void setup() {
  Serial.begin(9600);

  IRSensor leftIRSensor = {A0, 500};
  IRSensor rightIRSensor = {A1, 500};

  MotorController motorController(motor1Pin, motor2Pin);

  setupIRSensor(leftIRSensor);
  setupIRSensor(rightIRSensor);

  Timer1.initialize(timerInterval);
  Timer1.attachInterrupt(timerISR);
}

void loop() {
  if (timerFlag) {
    IRSensor leftIRSensor = {A0, 500};
    IRSensor rightIRSensor = {A1, 500};
    MotorController motorController(motor1Pin, motor2Pin);

    moveBasedOnIRSensors(leftIRSensor, rightIRSensor, motorController);

    timerFlag = false;
  }
}

void timerISR() {
  timerFlag = true;
}
