#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// --- Configuration ---
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://YOUR_LAPTOP_IP:8501/api/data"; // Placeholder endpoint

// Sensors
Adafruit_MPU6050 mpu;

// Simulation variables for missing sensors (Strain/Tilt)
float simStrain = 0.0;
float simTilt = 0.0;

void setup() {
  Serial.begin(115200);
  
  // Power up delay
  delay(1000);
  
  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) { delay(10); }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // WiFi Setup
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  int retry = 0;
  while (WiFi.status() != WL_CONNECTED && retry < 20) {
    delay(500);
    Serial.print(".");
    retry++;
  }
  
  if(WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi Connection Failed - Continuing in Offline Mode");
  }
}

void loop() {
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Simulate other sensors for demo purposes
  simStrain = random(100, 500) + (sin(millis() / 1000.0) * 50); // Fluctuating strain
  simTilt = (a.acceleration.x / 9.8) * 90.0; // Rough tilt calc from accel

  // Create JSON Payload
  String jsonPayload = "{";
  jsonPayload += "\"vibration_x\": " + String(a.acceleration.x) + ",";
  jsonPayload += "\"vibration_y\": " + String(a.acceleration.y) + ",";
  jsonPayload += "\"vibration_z\": " + String(a.acceleration.z) + ",";
  jsonPayload += "\"strain\": " + String(simStrain) + ",";
  jsonPayload += "\"tilt\": " + String(simTilt);
  jsonPayload += "}";

  // Print to Serial (for debugging/demo)
  Serial.println(jsonPayload);

  // Send to Server (if connected)
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    
    int httpResponseCode = http.POST(jsonPayload);
    
    if(httpResponseCode > 0) {
      String response = http.getString();
      // Serial.println(httpResponseCode);
      // Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }

  delay(100); # 10Hz sample rate
}
