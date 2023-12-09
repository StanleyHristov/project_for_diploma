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

  bool isMoving() {
    return (digitalRead(motorPin1) == HIGH || digitalRead(motorPin2) == HIGH);
  }

private:
  int motorPin1;
  int motorPin2;
};

void setupIRSensor(IRSensor &sensor) {
  pinMode(sensor.pin, INPUT);
}

bool isWhiteLineDetected(const IRSensor &sensor) {
  return analogRead(sensor.pin) > sensor.threshold;
}

void moveBasedOnIRWhiteLines(const IRSensor &leftSensor, const IRSensor &rightSensor, MotorController &motorController) {
  bool leftLineDetected = isWhiteLineDetected(leftSensor);
  bool rightLineDetected = isWhiteLineDetected(rightSensor);

  if (leftLineDetected || rightLineDetected) {
    if (leftLineDetected && !rightLineDetected) {
      motorController.moveRight();
    } else if (!leftLineDetected && rightLineDetected) {
      motorController.moveLeft();
    } else {
      motorController.stop();
    }
  } else {
    motorController.stop();
  }
}

const int timerInterval = 100000;
volatile bool timerFlag = false;
unsigned long previousMillis = 0;
const long motorTimeout = 2000;

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
  unsigned long currentMillis = millis();

  if (timerFlag) {
    IRSensor leftIRSensor = {A0, 500};
    IRSensor rightIRSensor = {A1, 500};
    MotorController motorController(motor1Pin, motor2Pin);

    moveBasedOnIRWhiteLines(leftIRSensor, rightIRSensor, motorController);

    if (motorController.isMoving() && (currentMillis - previousMillis >= motorTimeout)) {
      motorController.stop();
      previousMillis = currentMillis;
    }

    timerFlag = false;
  }
}

void timerISR() {
  timerFlag = true;
}
