#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <MPU6050_light.h>

// WiFi settings
const char* ssid = "HUST";
const char* password = "haideptrai123";

// UDP settings
const char* udpAddress = "255.255.255.255";
const int udpPort = 1234;
const int localPort = 8888;

WiFiUDP udp;
MPU6050 mpu0(Wire);
MPU6050 mpu1(Wire);
MPU6050 mpu2(Wire);

// TCA9548A I2C address
#define TCA9548A_ADDR 0x70

// Function to select the I2C channel on TCA9548A
void tcaSelect(uint8_t channel) {
  if (channel > 7) return;
  Wire.beginTransmission(TCA9548A_ADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

// Variables to store offsets
float offsetX[3], offsetY[3], offsetZ[3];

void calibrateSensor(MPU6050 &mpu, uint8_t index) {
    // Take multiple readings to calculate the average offset
    const int numReadings = 1000;
    float sumX = 0, sumY = 0, sumZ = 0;
    for (int i = 0; i < numReadings; i++) {
        mpu.update();
        sumX += mpu.getAngleX();
        sumY += mpu.getAngleY();
        sumZ += mpu.getAngleZ();
        delay(10);  // Small delay between readings
    }

    offsetX[index] = sumX / numReadings;
    offsetY[index] = sumY / numReadings;
    offsetZ[index] = sumZ / numReadings;
}


void setup() {
    Serial.begin(115200);
    Wire.begin();
    WiFi.begin(ssid, password);

    Serial.println("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }

    Serial.println("Connected to WiFi");

    udp.begin(localPort);

    // Initialize all MPU6050 sensors
    tcaSelect(0);
    mpu0.begin();
    calibrateSensor(mpu0, 0);

    tcaSelect(2);
    mpu1.begin();
    calibrateSensor(mpu1, 1);

    tcaSelect(4);
    mpu2.begin();
    calibrateSensor(mpu2, 2);
}

void loop() {
  float angleX[3], angleY[3], angleZ[3]; // array for angle measurements
  
  // Read data from MPU6050 sensors
    tcaSelect(0);
    mpu0.update();
    angleX[0] = mpu0.getAngleX() - offsetX[0];
    angleY[0] = mpu0.getAngleY() - offsetY[0];
    angleZ[0] = mpu0.getAngleZ() - offsetZ[0];

    tcaSelect(2);
    mpu1.update();
    angleX[1] = mpu1.getAngleX() - offsetX[1];
    angleY[1] = mpu1.getAngleY() - offsetY[1];
    angleZ[1] = mpu1.getAngleZ() - offsetZ[1];

    tcaSelect(4);
    mpu2.update();
    angleX[2] = mpu2.getAngleX() - offsetX[2];
    angleY[2] = mpu2.getAngleY() - offsetY[2];
    angleZ[2] = mpu2.getAngleZ() - offsetZ[2];

  String data = "";
  for (uint8_t i = 0; i < 3; i++) {
        data += String(angleX[i], 2) + ";" + String(angleY[i], 2) + ";" + String(angleZ[i], 2);
        if (i < 2) {
            data += ";"; // Add delimiter between sensor data sets
        }
    }

  udp.beginPacket(udpAddress, udpPort);
  udp.write((uint8_t*)data.c_str(), data.length());
  udp.endPacket();
  Serial.println(data);
  //delay(10);
}
