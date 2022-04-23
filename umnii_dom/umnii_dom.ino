#define AMOUNT 1  // кол-во серво
#include "ServoDriverSmooth.h"
#include <ServoSmooth.h>
ServoSmooth servos[AMOUNT];
#include "TM1637.h"
#include <Wire.h>
#include <dht11.h>  // Подключение библиотеки
dht11 DHT;          // Создаем объект
#define DHT11_PIN 10  // Определяем pin к которому подключен датчик
#include <iarduino_RTC.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
int8_t DispMSG[4] {1, 2, 3, 4};
#define CLK 3
#define DIO 2
TM1637 tm1637(CLK, DIO);
iarduino_RTC watch(RTC_DS3231);
#include <NewPing.h>

#define TRIGGER_PIN  13
#define ECHO_PIN     12
#define MAX_DISTANCE 400
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

int sw = 1 ;
int tl, i;
int tm, adb;
int x, xv, xmp;
int hour1;
int hour2;
int hour3 = 22;
int minute1;
int minute2;
int minute3 = 55;
int butTime = 7;
int plus = 6;
int minus = 5;
int date = 4;
int temp, hum, chk;
int timess;
int axy, guy, distguy, svetok;
int svett;

byte bukva_ZH[8]  = {B10101, B10101, B10101, B11111, B10101, B10101, B10101, B00000,}; // Буква "Ж"
byte bukva_N[8]   = {B10001, B10001, B10001, B11111, B10001, B10001, B10001, B00000,}; // Буква "Н"
byte bukva_L[8]   = {B00011, B00111, B00101, B00101, B01101, B01001, B11001, B00000,}; // Буква "Л"
byte bukva_P[8]   = {B11111, B10001, B10001, B10001, B10001, B10001, B10001, B00000,}; // Буква "П"
byte bukva_Mz[8]  = {B10000, B10000, B10000, B11110, B10001, B10001, B11110, B00000,}; // Буква "Ь"
byte bukva_t[8]   = {B00000, B00000, B11111, B10101, B00100, B00100, B00100, B00000,}; // Буква "т"

#define PIN_LED 7

void setup() {
  
  pinMode(A0, INPUT);
  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, HIGH);
  delay(300);
  tm1637.init();
  tm1637.set(BRIGHTEST);
  Serial.begin(9600);
  watch.begin();
  tl = millis();
  tm = millis();
  lcd.init();// Инициализация дисплея
  lcd.backlight();// Включаем подсветку дисплея
  lcd.createChar(1, bukva_P);// Создаем символ под номером 1
  lcd.createChar(2, bukva_L);// Создаем символ под номером 1
  lcd.createChar(3, bukva_ZH);// Создаем символ под номером 8
  lcd.createChar(4, bukva_N);// Создаем символ под номером 4
  lcd.createChar(6, bukva_t);
  lcd.createChar(7, bukva_Mz);// Создаем символ под номером 2
  servos[0].attach(4, 40);
  servos[0].setAccel(0);
  servos[0].setSpeed(800);
  watch.settime(50 , 59, 13, 21, 8, 2021, 5);
  
}

void loop() 
{
  switch (sw)
  {
    case 1:
      temp = DHT.temperature;  // Читаем температуру
      hum = DHT.humidity;
      tm1637.point(true);
      hour1 = watch.Hours;
      hour2 = watch.Hours;
      minute1 = watch.minutes;
      minute2 = watch.minutes;
      hour1 = hour1 / 10;
      hour2 = hour2 % 10;
      minute1 = minute1 / 10;
      minute2 = minute2 % 10;
      DispMSG[0] = hour1;
      DispMSG[1] = hour2;
      DispMSG[2] = minute1;
      DispMSG[3] = minute2;
      tm1637.display(DispMSG);
      butTime =  digitalRead(7);
      if (butTime == 0) {
        sw = 2;
      }
      if (hour1 == 2)
        digitalWrite(12, HIGH);
      if (hour1 == 0 and hour2 > 6)
        digitalWrite(11, HIGH);
      break;
    case 2:
      plus = digitalRead(6);
      minus = digitalRead(5);
      if (plus == 1) {
        x++;
        DispMSG[0] =  x;
      } if (minus == 1) {
        x--;
        DispMSG[0] = x;
      }
      if (x >= 3 || x <= -1) {
        x = 0;
        DispMSG[0] = x;
      }
      tm1637.display(DispMSG);
      butTime =  digitalRead(7);
      if (butTime == 0) {
        watch.settime(0, minute3, hour3);
        sw = 3;
      }
      break;
    case 3:
      plus = digitalRead(6);
      minus = digitalRead(5);
      if (plus == 1) {
        x++;
        DispMSG[1] =  x;
      } if (minus == 1) {
        x--;
        DispMSG[1] = x;
      }
      if (x >= 10 || x <= -1) {
        x = 0;
        DispMSG[1] = x;
      }
      tm1637.display(DispMSG);
      butTime =  digitalRead(7);
      if (butTime == 0) {
        watch.settime(0, minute3, hour3);
        sw = 4;
      }
      break;
    case 4:
      plus = digitalRead(6);
      minus = digitalRead(5);
      if (plus == 1) {
        x++;
        DispMSG[2] =  x;
      } if (minus == 1) {
        x--;
        DispMSG[2] = x;
      }
      if (x >= 6 || x <= -1) {
        x = 0;
        DispMSG[2] = x;
      }
      tm1637.display(DispMSG);
      butTime =  digitalRead(7);
      if (butTime == 0) {
        watch.settime(0, minute3, hour3);
        sw = 5;
      }
      break;
    case 5:
      plus = digitalRead(6);
      minus = digitalRead(5);
      if (plus == 1) {
        x++;
        DispMSG[3] =  x;
      } if (minus == 1) {
        x--;
        DispMSG[3] = x;
      }
      if (x >= 10 || x <= -1) {
        x = 0;
        DispMSG[3] = x;
      }
      tm1637.display(DispMSG);
      butTime =  digitalRead(7);
      if (butTime == 0) {
        hour3 =   DispMSG[0] * 10 + DispMSG[1];
        minute3 =   DispMSG[2] * 10 + DispMSG[3];
        watch.settime(0, minute3, hour3);
        sw = 1;
      }
      break;
  }
  switch (xv)
  {
    case 0:
      chk = DHT.read(DHT11_PIN);
      temp = DHT.temperature;  // Читаем температуру
      hum = DHT.humidity;      // Читаем влажность воздуха
      tl = millis();
      axy = Serial.read();
      lcd.setCursor(0, 0);             // Установка курсора в начало второй строки
      lcd.print("Tem\1epa\6. =");
      lcd.print(temp);
      lcd.setCursor(0, 1);             // Установка курсора в начало второй строки
      lcd.print("B\2a\3\4oc\6\7 =");
      lcd.print(hum);
      if (axy == 49) {
        Serial.print(temp);
        Serial.print("-");
        Serial.print(hum);
        Serial.println("-");
        
      }
      if (axy == 50) {

        timess = millis();
        guy = 1;
      }
      break;
  }
  switch (guy)
  {
    case  0:
      servos[0].tick();
      servos[0].setTargetDeg(179);
      break;
    case 1:
      servos[0].tick();
      servos[0].setTargetDeg(80);
      distguy = sonar.ping_cm();
      if (distguy > 50) {
        if ((millis() - timess) > 5000) {
          guy = 0;
        }
      } else timess = millis();
      break;
  }
  switch (svetok)
  {
    case  0:
      analogWrite(PIN_LED, LOW);
      svett = analogRead(A0);
      if (svett < 100) {
        svetok = 1;
      }
      break;
    case  1:
      svett = analogRead(A0);
        digitalWrite(PIN_LED, HIGH);
      if (svett > 100)
      {
        svetok = 0;
      }
      break;
  }
}
