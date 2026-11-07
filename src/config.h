#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// Pin map (must match wiring exactly)
static const uint8_t PIN_ULTRASONIC_TRIG = 2;
static const uint8_t PIN_ULTRASONIC_ECHO = 3;
static const uint8_t PIN_LED = 4;
static const uint8_t PIN_BUZZER = 5;
static const uint8_t PIN_SERVO = 6;

// Behavior
static const float ALERT_DISTANCE_CM = 30.0f;

// Servo sweep
static const uint8_t SERVO_MIN_DEG = 15;
static const uint8_t SERVO_MAX_DEG = 165;
static const uint8_t SERVO_STEP_DEG = 1;

// Scan timing (also respects HC-SR04 >= 60 ms requirement)
static const unsigned long SCAN_STEP_INTERVAL_MS = 70;
static const unsigned long ECHO_TIMEOUT_US = 30000UL;

// Alert pattern timing
static const unsigned long ALERT_TOGGLE_INTERVAL_MS = 120;

// Buzzer tone (passive piezo)
static const unsigned int BUZZER_FREQUENCY_HZ = 2200;

#endif
