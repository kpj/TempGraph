const int sensorPin = A0;

float getTemperature() {
  int sensorVal = analogRead(sensorPin);
  float voltage = (sensorVal / 1024.0) * 5.0;

  float temp = (voltage - .5) * 100;
  return temp;
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  int max_num = 10;
  float sum = 0;
  for(int i = 0; i < max_num; ++i) {
    sum += getTemperature();
    delay(1);
  }
  float avg_temp = sum / max_num;

  Serial.println(avg_temp);
  delay(1000);
}
