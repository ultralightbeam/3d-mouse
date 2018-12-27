
#include <Wire.h>

const int MPU6050_addr = 0x68;
int16_t AccX,AccY,AccZ;

void setup(){
  Wire.begin();
  Wire.beginTransmission(MPU6050_addr);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  Serial.begin(9600);
}

void loop(){
  Wire.beginTransmission(MPU6050_addr);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050_addr,14, true);
  AccX = Wire.read() << 8 | Wire.read();
  AccY = Wire.read() << 8 | Wire.read();
  AccZ = Wire.read() << 8 | Wire.read();
  // comma separation for print.
  Serial.print("AccX = ");
  Serial.print(AccX);
  Serial.print(", AccY = ");
  Serial.print(AccY);
  Serial.print(", AccZ = ");
  Serial.print(AccZ);
  Serial.print('\n');
  delay(60);
}


