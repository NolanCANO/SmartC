#include "LiquidCrystal.h"
#include "DHT.h"

#define DHTPIN 2

#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);

  dht.begin();
}

void loop() {
  delay(2000);
  lcd.clear();

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  } else {
    Serial.println(F("Reading from DHT sensor"));
  }

  lcd.setCursor(0,0);

  String displayTemp = "T: " + String(t) + " C ";

  lcd.print(displayTemp);

  lcd.setCursor(0,1);

  String displayHumi = "H: " + String(h) + " % ";

  lcd.print(displayHumi);
}
