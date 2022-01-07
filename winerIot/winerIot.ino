#include <LiquidCrystal.h>
#define WINERYID 1
#define NUMSENSORS 4
enum reader {
  /*
  S0: inizio nuova lettura seriale con 0xdd
  S1: ricevuto winery_id
  S2: ricevuto numero di sensori con anomalia 
  S4: anomalie su tutti i sensori
  S5: fine lettura con 0xde
  S6: allarme passato
  S7: fine lettura di fine allarme
  */
  S0, S1, S2, S3, S4, S5, S6, S7
};
uint8_t prec_state = 255, state= 255, next_state =255;

#include "SR04.h"
#define TRIG_PIN 4
#define ECHO_PIN 3
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);

#define LIGHTPIN 0
#define ALLARMPIN 13

#include "DHT.h"
static const int DHT_SENSOR_PIN = 2;
#define DHT_SENSOR_TYPE DHT11
DHT dht( DHT_SENSOR_PIN, DHT_SENSOR_TYPE );

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
static unsigned long measurement_timestamp_lcd = 0;

const char* sensor_type[4] =  {"Temperature", "Humidity", "Distance", "Brightness"};
const char* type[5] =  {"" ,"T", "H", "D", "B"};
const char* sensor_msr[4] = {"C", "%", "cm", ""};
reader allarm_read;
uint8_t allarm_to_read, allarm_readed, allarm_on_lcd;
uint8_t sensor_with_anomaly[NUMSENSORS];

void setup() {
  lcd.begin(16, 2);
  dht.begin();
  pinMode(ALLARMPIN, OUTPUT); 
  lcd.print("Init...");
  Serial.begin(9600);
  allarm_to_read = 0;
  allarm_readed = 0;
}

uint8_t check_allarm(){
    if (Serial.available()>0){
      uint8_t received = Serial.read();
      if (received == 10) return (uint8_t)0;
      
      if (received == 0xdd){ 
        allarm_read = S0;
      } 
      if (allarm_read==S0 && received == WINERYID){
        allarm_read = S1;
      }
      if (allarm_read==S1 && received == 0xdc){
        allarm_read = S4;
      }
      if (allarm_read==S1 && received == 0xdb){
        allarm_read = S6;
      }
      if (allarm_read==S1 && received >0 && received < NUMSENSORS){
        allarm_read = S2;
        allarm_to_read = received;
        allarm_readed = 0;
      }
      if ((allarm_read == S2 && allarm_readed == 0) || (allarm_read == S3 && allarm_readed <= allarm_to_read)){
        allarm_read = S3;
        sensor_with_anomaly [allarm_readed] = received;
        allarm_readed = allarm_readed + 1;
      }
      if ((allarm_read == S3 || allarm_read == S4) && received == 0xde){
        allarm_read = S5;
      }
      if (allarm_read == S6 && received == 0xde){
        allarm_read = S7;
      }
    
    if (allarm_read == S5) return (uint8_t)1;
    if (allarm_read == S7) return (uint8_t)2;
  }
  return (uint8_t)0;
}

void print_anomaly_lcd(){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print((char *) "Anomalia sensori");
  lcd.setCursor(0, 1);
  for (uint8_t i = 1; i<=allarm_to_read; i++){
    lcd.print(sensor_with_anomaly[i]);
    lcd.print(" ");
  }
}

void print_lcd(int sensor_id, float measure){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print((char *)sensor_type[sensor_id]);
  lcd.setCursor(0, 1);
  lcd.print(measure);
  lcd.print(" ");
  lcd.print(sensor_msr[sensor_id]);
}

void print_seriale(uint8_t  sensor_id, uint8_t sensor_value){
    Serial.write(0xff);
    Serial.write((char)(WINERYID));
    Serial.write((char)(sensor_id));
    Serial.write((char*)type[sensor_id]);
    Serial.write((char)(sensor_value));
    Serial.write(0xfe); 
}

void print_(uint8_t state, uint8_t m){
  if (allarm_on_lcd != 1){
      print_lcd(state, m);
    }
    print_seriale(state+1, (uint8_t)m);
}

void loop() {
  uint8_t m;
  int l;
  float f;
  long d;

  uint8_t check_status;
  
  if(millis()- measurement_timestamp_lcd > 2000 && ((state == 3 && next_state == 0 )||(state == 255 && next_state == 255))){
    f = dht.readTemperature(true);
    m = (f-32)/1.8;
    
    state = 0;
    next_state = 1;  
    print_(state, m);

    measurement_timestamp_lcd = millis();    
  }
   
  if(millis()- measurement_timestamp_lcd > 2000 && state == 0 && next_state == 1){
    m = dht.readHumidity();

    state = 1;
    next_state = 2;
    print_(state, m);
    
    measurement_timestamp_lcd = millis();
  }

  if(millis()- measurement_timestamp_lcd > 2000 && state == 1 && next_state == 2){
    m = sr04.Distance();

    state = 2;
    next_state = 3;
    print_(state, m);
    
    measurement_timestamp_lcd = millis();
  }
  
  if(millis()- measurement_timestamp_lcd > 2000 && state == 2 && next_state == 3){
    l = analogRead(LIGHTPIN);
    m = (uint8_t)l;

    state = 3;
    next_state = 0;
    print_(state, m);
   
    measurement_timestamp_lcd = millis(); 
  }
  
  check_status = check_allarm();
  if (check_status == 1) {
    digitalWrite(ALLARMPIN, HIGH);  
    print_anomaly_lcd();
    allarm_on_lcd = 1;
  }
  if (check_status == 2){
    digitalWrite(ALLARMPIN, LOW);
    allarm_on_lcd = 0;
    lcd.clear();
  }
}
