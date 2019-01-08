#include <Wire.h>
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
ESP8266WiFiMulti WiFiMulti;

//setIP
//String ipAddress = "192.168.1.2:5000";
String ipAddress = "172.20.10.3:5000";

//Button and pin
const int Bpin = 16;
const int Upin = 2;
const int Dpin = 12;
const int Lpin = 13;
const int Rpin = 15;

// MPU6050 Slave Device Address
const uint8_t MPU6050SlaveAddress = 0x68;

// Select SDA and SCL pins for I2C communication 
const uint8_t scl = D1;
const uint8_t sda = D2;
const int sig = 14; //D5

// sensitivity scale factor respective to full scale setting provided in datasheet 
const uint16_t AccelScaleFactor = 16384;
const uint16_t GyroScaleFactor = 131;

// MPU6050 few configuration register addresses
const uint8_t MPU6050_REGISTER_SMPLRT_DIV   =  0x19;
const uint8_t MPU6050_REGISTER_USER_CTRL    =  0x6A;
const uint8_t MPU6050_REGISTER_PWR_MGMT_1   =  0x6B;
const uint8_t MPU6050_REGISTER_PWR_MGMT_2   =  0x6C;
const uint8_t MPU6050_REGISTER_CONFIG       =  0x1A;
const uint8_t MPU6050_REGISTER_GYRO_CONFIG  =  0x1B;
const uint8_t MPU6050_REGISTER_ACCEL_CONFIG =  0x1C;
const uint8_t MPU6050_REGISTER_FIFO_EN      =  0x23;
const uint8_t MPU6050_REGISTER_INT_ENABLE   =  0x38;
const uint8_t MPU6050_REGISTER_ACCEL_XOUT_H =  0x3B;
const uint8_t MPU6050_REGISTER_SIGNAL_PATH_RESET  = 0x68;

int16_t AccelX, AccelY, AccelZ, Temperature, GyroX, GyroY, GyroZ;

void setup() {
  
  Serial.begin(115200);
  //button setup
  pinMode(sig,INPUT);
  pinMode(Bpin,INPUT);
  pinMode(Upin,INPUT);
  pinMode(Dpin,INPUT);
  pinMode(Lpin,INPUT);
  pinMode(Rpin,INPUT);
  
  //Gyro setup
  Wire.begin(sda, scl);
  MPU6050_Init();
  
  // WIFI setup:
  Serial.println();
  Serial.println();
  Serial.println();
  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }
  WiFi.mode(WIFI_STA);
  //WiFiMulti.addAP("skynet2.4", "chlp7720");
  //WiFiMulti.addAP("Genisys", "kokokrunch");
  WiFiMulti.addAP("I7F", "qwertyuiopq");
}

void loop() {
  double Ax, Ay, Az, Gx, Gy, Gz;
  
  Read_RawValue(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_XOUT_H);
  
  //divide each with their sensitivity scale factor
  Ax = (double)AccelX/AccelScaleFactor;
  Ay = (double)AccelY/AccelScaleFactor;
  Az = (double)AccelZ/AccelScaleFactor;
  Gx = (double)GyroX/GyroScaleFactor;
  Gy = (double)GyroY/GyroScaleFactor;
  Gz = (double)GyroZ/GyroScaleFactor;
  
  //http://172.20.10.3:5000/?Ax=1&Ay=1&Az=1&Gx=1&Gy=1&Gz=1&Touch=1&B1=1
  if ((WiFiMulti.run() == WL_CONNECTED)) {
    HTTPClient http;
    
    http.begin("http://" + ipAddress + "/?Ax="
      +String(Ax)+"&Ay="+String(Ay)+"&Az="+String(Az)
      +"&Gx="+String(Gx)+"&Gy="+String(Gy)+"&Gz="+String(Gz)
      +"&Touch="+String(digitalRead(sig))+"&B1="+String(digitalRead(Bpin))
      +"&up="+String(digitalRead(Upin))+"&down="+String(digitalRead(Dpin))
      +"&left="+String(digitalRead(Lpin))+"&right="+String(digitalRead(Rpin)));
//    Serial.println("http://" + ipAddress + "/?Ax="
//      +String(Ax)+"&Ay="+String(Ay)+"&Az="+String(Ay)
//      +"&Gx="+String(Gx)+"&Gy="+String(Gy)+"&Gz="+String(Gy)
//      +"&Touch="+String(digitalRead(sig))+"&B1="+String(digitalRead(Bpin))
//      +"&up="+String(digitalRead(Upin))+"&down="+String(digitalRead(Dpin))
//      +"&left="+String(digitalRead(Lpin))+"&right="+String(digitalRead(Rpin)));
    http.GET();
    http.end();
    delay(50);
  }
  
}


void I2C_Write(uint8_t deviceAddress, uint8_t regAddress, uint8_t data){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.write(data);
  Wire.endTransmission();
}

// read all 14 register
void Read_RawValue(uint8_t deviceAddress, uint8_t regAddress){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.endTransmission();
  Wire.requestFrom(deviceAddress, (uint8_t)14);
  AccelX = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelY = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelZ = (((int16_t)Wire.read()<<8) | Wire.read());
  Temperature = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroX = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroY = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroZ = (((int16_t)Wire.read()<<8) | Wire.read());
}

//configure MPU6050
void MPU6050_Init(){
  delay(150);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SMPLRT_DIV, 0x07);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_1, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_2, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_CONFIG, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_GYRO_CONFIG, 0x00);//set +/-250 degree/second full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_CONFIG, 0x00);// set +/- 2g full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_FIFO_EN, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_INT_ENABLE, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SIGNAL_PATH_RESET, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_USER_CTRL, 0x00);
}
