
#include <Wire.h>

const int request_from = 0x68;
const int request_from_int = 14;

int16_t accel_x, accel_y, accel_z;

void setup(){
  Wire.begin();
  Wire.beginTransmission(request_from);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  Serial.begin(9600);
}

void loop(){
  Wire.beginTransmission(request_from);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(request_from, request_from_int, true);
  accel_x = Wire.read() << 8 | Wire.read();
  accel_y = Wire.read() << 8 | Wire.read();
  accel_z = Wire.read() << 8 | Wire.read();
  // Comma separation for print.
  Serial.print("AccX = ");
  Serial.print(accel_x);
  Serial.print(", AccY = ");
  Serial.print(accel_y);
  Serial.print(", AccZ = ");
  Serial.print(accel_z);
  Serial.print('\n');
  delay(60);
}


