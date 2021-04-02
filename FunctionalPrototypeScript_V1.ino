#include <Event.h>//include event libraries
#include <Timer.h>//include timer libraries

#include <dht.h>//include dht libraries

#define dht_apin A0 // Analog Pin sensor is connected to
 
dht DHT;//create dht variable for pin 

int light = 0; // store the current light value

Timer t;//create timer t
int pin = 13;//set variable 'pin' to PIN 13 on the arduino 


void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600); //configure serial to talk to computer
    
    delay(500);//Delay to let system boot
    Serial.println("DHT11 Humidity & temperature Sensor\n\n"); //Print this text to the computer
    delay(1000);//Wait before accessing Sensor
 
    pinMode(13, OUTPUT); // configure digital pin 13 as an output for LED relay 

    pinMode(pin, OUTPUT); //Initially set the LEDs to be on 
    t.oscillate(pin, 28800000, HIGH);//Toggle the LED relay on/off every 8hrs
    t.every(2000, Action, 150);//Every 2000s, perform 'Action' (Measure temp, humidity & light)
}

void loop() {
  // put your main code here, to run repeatedly:
 
     t.update();//runs the timer
      
    //delay(2000);//Wait 5 seconds before accessing sensor again.
 
    //Fastest should be once every two seconds.

}

void Action()
{
    DHT.read11(dht_apin);\\read data from the DHT11
    
    Serial.print("Current humidity = ");\\print text
    Serial.print(DHT.humidity);\\print humidity
    Serial.print("%  ");\\print text
    Serial.print("temperature = ");\\print text
    Serial.print(DHT.temperature);\\print temp
    Serial.println("C  ");\\print text

    if (DHT.temperature >= 22) {  
    digitalWrite(12, HIGH); // The "3" is for the power input of both fans (1 relay for both)
    //     digitalWrite(5, HIGH); // The "5" is the same as above
    }
   
        if (DHT.temperature < 22) {  
    digitalWrite(12, 0);  // The "3" is for the power input of both fans (1 relay for both)
    //    digitalWrite(5, 0);  // The "5" is the same as above
    }

    light = analogRead(A1); // read and save value from Photoresistor
    
    Serial.println(light); // print current light value
 
    if(light > 450) { // If it is bright...
        Serial.println("LEDs On!"); //print text
        //digitalWrite(13,LOW); //turn left LED off
    }
    else if(light > 200 && light < 451) { // If it is average light...
        Serial.println("It is average light!");//print text
        //digitalWrite(13, LOW); // turn left LED on
    }
    else { // If it's dark...
        Serial.println("LEDs Off!");//print text
        //digitalWrite(13,HIGH); // Turn left LED on
    }
    
}
