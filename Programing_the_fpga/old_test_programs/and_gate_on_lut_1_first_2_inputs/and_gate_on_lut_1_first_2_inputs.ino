int latchPin = 2;  // Latch pin of 74HC595 is connected to Digital pin 5
int clockPin = 3; // Clock pin of 74HC595 is connected to Digital pin 6
int dataPin = 4;  // Data pin of 74HC595 is connected to Digital pin 4

   // Variable to hold the pattern of which LEDs are currently turned on or off
byte ctr_reg = 255;
byte lut2_reg2 = 1;
byte lut2_reg1 = 1;
byte lut1_reg2 = 1;
byte lut1_reg1 = 1;//was 8
/*
 * setup() - this function runs once when you turn your Arduino on
 * We initialize the serial connection with the computer
 */
void setup() 
{
  // Set all the pins of 74HC595 as OUTPUT
  pinMode(latchPin, OUTPUT);
  digitalWrite(latchPin, LOW);
  pinMode(dataPin, OUTPUT);  
  pinMode(clockPin, OUTPUT);

  pinMode(8, OUTPUT);//A
  pinMode(9, OUTPUT);//B
  pinMode(10, OUTPUT);//C
  pinMode(11, OUTPUT);//rst
  pinMode(12, OUTPUT);//D Clock

  pinMode(5, OUTPUT);//A2
  pinMode(6, OUTPUT);//B2
  pinMode(7, OUTPUT);//Cc

  digitalWrite(5,LOW);
  digitalWrite(6,LOW);
  digitalWrite(7,LOW);
  digitalWrite(8,LOW);
  digitalWrite(9,LOW);
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
  digitalWrite(12,LOW);

  delay(200);

  updateShiftRegister();

  

}

/*
 * loop() - this function runs over and over again
 */
void loop() 
{
  //digitalWrite(8,LOW);
  //digitalWrite(9,LOW);
  //delay(500);
  //digitalWrite(8,LOW);
  //digitalWrite(9,HIGH);
  //delay(500);
  //digitalWrite(8,HIGH);
  //digitalWrite(9,LOW);
  //delay(500);
  //digitalWrite(8,HIGH);
  //digitalWrite(9,HIGH);
  delay(500);


 // digitalWrite(12, !digitalRead(12));
}

/*
 * updateShiftRegister() - This function sets the latchPin to low, then calls the Arduino function 'shiftOut' to shift out contents of variable 'leds' in the shift register before putting the 'latchPin' high again.
 */
void updateShiftRegister()
{
digitalWrite(latchPin, LOW);
shiftOut(dataPin, clockPin, MSBFIRST, ctr_reg);
shiftOut(dataPin, clockPin, MSBFIRST, (lut2_reg2));
shiftOut(dataPin, clockPin, MSBFIRST, (lut2_reg1));
shiftOut(dataPin, clockPin, MSBFIRST, (lut1_reg2));
shiftOut(dataPin, clockPin, MSBFIRST, (lut1_reg1));
digitalWrite(latchPin, HIGH);
delay(30);
digitalWrite(latchPin, LOW);
}
