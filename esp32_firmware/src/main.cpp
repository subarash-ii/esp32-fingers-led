#include <Arduino.h>

const int INDEX_LED_PIN = 13;
const int MIDDLE_LED_PIN = 12;
const int RING_LED_PIN = 14;
const int PINKY_LED_PIN = 27;

void setup() {
    Serial.begin(115200);

    pinMode(INDEX_LED_PIN, OUTPUT);
    pinMode(MIDDLE_LED_PIN, OUTPUT);
    pinMode(RING_LED_PIN, OUTPUT);
    pinMode(PINKY_LED_PIN, OUTPUT);
}

void loop() {
    if (Serial.available() > 0) {
        uint8_t data = Serial.read();

        if (data & 0b1000) {
            digitalWrite(INDEX_LED_PIN, HIGH);
        } else {
            digitalWrite(INDEX_LED_PIN, LOW);
        }

        if (data & 0b0100) {
            digitalWrite(MIDDLE_LED_PIN, HIGH);
        } else {
            digitalWrite(MIDDLE_LED_PIN, LOW);
        }

        if (data & 0b010) {
            digitalWrite(RING_LED_PIN, HIGH);
        } else {
            digitalWrite(RING_LED_PIN, LOW);
        }
        
        if (data & 0b0001) {
            digitalWrite(PINKY_LED_PIN, HIGH);
        } else {
            digitalWrite(PINKY_LED_PIN, LOW);
        }
    }
}