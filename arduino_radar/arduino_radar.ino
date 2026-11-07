#include <Arduino.h>
#include <Servo.h>
#include "config.h"

static Servo scanServo;

static unsigned long lastScanStepMs = 0;
static unsigned long lastAlertToggleMs = 0;

static int16_t currentAngleDeg = SERVO_MIN_DEG;
static int8_t sweepDirection = 1; // +1 increasing, -1 decreasing

// Dynamically configurable parameters (defaulted from config.h)
static float alertDistanceCm = ALERT_DISTANCE_CM;
static uint8_t servoStepDeg = SERVO_STEP_DEG;
static unsigned long scanStepIntervalMs = SCAN_STEP_INTERVAL_MS;

static bool alertActive = false;
static bool alertOutputState = false;

static float readDistanceCm(bool &valid) {
  digitalWrite(PIN_ULTRASONIC_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_ULTRASONIC_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_ULTRASONIC_TRIG, LOW);

  const unsigned long durationUs = pulseIn(PIN_ULTRASONIC_ECHO, HIGH, ECHO_TIMEOUT_US);
  if (durationUs == 0) {
    valid = false;
    return -1.0f;
  }

  const float distance = (durationUs * 0.0343f) * 0.5f;
  if (distance < 2.0f || distance > 400.0f) {
    valid = false;
    return -1.0f;
  }

  valid = true;
  return distance;
}

static void setAlertOutputs(bool on) {
  digitalWrite(PIN_LED, on ? HIGH : LOW);
  if (on) {
    tone(PIN_BUZZER, BUZZER_FREQUENCY_HZ);
  } else {
    noTone(PIN_BUZZER);
  }
}

static void advanceSweepAngle() {
  currentAngleDeg += (sweepDirection * servoStepDeg);

  if (currentAngleDeg >= SERVO_MAX_DEG) {
    currentAngleDeg = SERVO_MAX_DEG;
    sweepDirection = -1;
  } else if (currentAngleDeg <= SERVO_MIN_DEG) {
    currentAngleDeg = SERVO_MIN_DEG;
    sweepDirection = 1;
  }
}

static void processIncomingSerial() {
  if (!Serial.available()) return;

  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  if (cmd.length() == 0) return;

  if (cmd.startsWith("ALERT:")) {
    float val = cmd.substring(6).toFloat();
    if (val >= 5.0f && val <= 200.0f) {
      alertDistanceCm = val;
      Serial.print(F("[CMD] ALERT_SET: "));
      Serial.println(alertDistanceCm, 1);
    }
  } else if (cmd.startsWith("STEP:")) {
    int val = cmd.substring(5).toInt();
    if (val >= 1 && val <= 5) {
      servoStepDeg = (uint8_t)val;
      Serial.print(F("[CMD] STEP_SET: "));
      Serial.println(servoStepDeg);
    }
  } else if (cmd.startsWith("SPEED:")) {
    long val = cmd.substring(6).toInt();
    if (val >= 30 && val <= 300) {
      scanStepIntervalMs = (unsigned long)val;
      Serial.print(F("[CMD] SPEED_MS_SET: "));
      Serial.println(scanStepIntervalMs);
    }
  } else if (cmd.equalsIgnoreCase("TEST")) {
    setAlertOutputs(true);
    delay(150);
    setAlertOutputs(false);
    Serial.println(F("[CMD] TEST_COMPLETE"));
  } else if (cmd.equalsIgnoreCase("STATUS")) {
    Serial.print(F("[STATUS] alert_cm: "));
    Serial.print(alertDistanceCm, 1);
    Serial.print(F(", step_deg: "));
    Serial.print(servoStepDeg);
    Serial.print(F(", speed_ms: "));
    Serial.println(scanStepIntervalMs);
  }
}

void setup() {
  pinMode(PIN_ULTRASONIC_TRIG, OUTPUT);
  pinMode(PIN_ULTRASONIC_ECHO, INPUT);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);

  digitalWrite(PIN_ULTRASONIC_TRIG, LOW);
  digitalWrite(PIN_LED, LOW);
  digitalWrite(PIN_BUZZER, LOW);

  scanServo.attach(PIN_SERVO);
  scanServo.write(currentAngleDeg);

  Serial.begin(115200);
}

void loop() {
  const unsigned long now = millis();

  // Listen for interactive serial commands from HUD visualizer
  processIncomingSerial();

  if (now - lastScanStepMs >= scanStepIntervalMs) {
    lastScanStepMs = now;

    // Command servo to current scan angle
    scanServo.write(currentAngleDeg);

    // Sample distance at this angle
    bool valid = false;
    const float distanceCm = readDistanceCm(valid);

    alertActive = (valid && (distanceCm < alertDistanceCm));

    // Telemetry output (compatible with existing parsers while adding alert status)
    Serial.print(F("angle_deg: "));
    Serial.print(currentAngleDeg);
    Serial.print(F(", distance_cm: "));
    if (valid) {
      Serial.print(distanceCm, 1);
    } else {
      Serial.print(F("out_of_range"));
    }
    Serial.print(F(", alert: "));
    Serial.println(alertActive ? 1 : 0);

    if (!alertActive) {
      alertOutputState = false;
      setAlertOutputs(false);
    }

    advanceSweepAngle();
  }

  if (alertActive && (now - lastAlertToggleMs >= ALERT_TOGGLE_INTERVAL_MS)) {
    lastAlertToggleMs = now;
    alertOutputState = !alertOutputState;
    setAlertOutputs(alertOutputState);
  }
}

