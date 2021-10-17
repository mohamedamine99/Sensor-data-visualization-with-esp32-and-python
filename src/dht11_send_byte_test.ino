#include <dhtnew.h>

DHTNEW mySensor(15);

uint32_t count = 0;
byte H ;
byte L ;
float T;

void setup()
{
  Serial.begin(115200);
  mySensor.setSuppressError(true);
}

void loop()
{
  if (millis() - mySensor.lastRead() > 2000)
  {

    int errcode = mySensor.read();
    T = mySensor.getTemperature();
    H = mySensor.getHumidity();

    Serial.print(uint16_t(T*1000 + H)) ;
    
   /* Serial.println(T) ;
    Serial.println(H) ;*/
   /* Serial.print("\t"); 
    Serial.print(T);
    Serial.print("\t");
    Serial.print("High  = ");
    Serial.print("\t");
    Serial.print(uint8_t(10*T));
    Serial.print("\t");
    Serial.print("Low = ");
    Serial.print("\t");
    Serial.println(uint16_t(10*T));
    Serial.println("********");
    Serial.println(sizeof(uint16_t));
    Serial.println(sizeof(int));*/
  }
}
