#include <Arduino.h>
#include "board.h"

/**
 *  
 */
void setup() {  
  Serial.begin(230400);  

  initBoard();
}

/**
 * 
 */
void loop() {
  scanBoard();

  //liftDropAnalisys();

  plotSquare();
  
  //delay(1000);
  //Serial.println("Nuova lettura");   
} 
