int latchPin = 4;  // Latch pin of 74HC595 is connected to Digital pin 5
int clockPin = 2; // Clock pin of 74HC595 is connected to Digital pin 6
int dataPin = 3;  // Data pin of 74HC595 is connected to Digital pin 4

byte reg1 = 0;    //lut1 pt 1
byte reg2 = 0;    //lut1 pt 2
byte reg3 = 0;    //control
/*
 * setup() - this function runs once when you turn your Arduino on
 * We initialize the serial connection with the computer
 */
void setup() 
{
  // Set all the pins of 74HC595 as OUTPUT
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);  
  pinMode(clockPin, OUTPUT);

  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);

  digitalWrite(8,LOW);
  digitalWrite(9,LOW);
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
  reg1 = 0;
  reg2 = 0;
  reg3 = 0;
    updateShiftRegister();

  reg1 = 0;
  reg2 = 8;//and gate in a & b
  reg3 = 255; // no adder, no ff
  updateShiftRegister();


}

/*
 * loop() - this function runs over and over again
 */
void loop() 
{

  
    digitalWrite(8,LOW);
  digitalWrite(9,LOW);
  delay(500);
  digitalWrite(8,LOW);
  digitalWrite(9,HIGH);
  delay(500);
  digitalWrite(8,HIGH);
  digitalWrite(9,LOW);
  delay(500);
digitalWrite(8,HIGH);
  digitalWrite(9,HIGH);
  delay(500);
  

}

/*
 * updateShiftRegister() - This function sets the latchPin to low, then calls the Arduino function 'shiftOut' to shift out contents of variable 'leds' in the shift register before putting the 'latchPin' high again.
 */
void updateShiftRegister()
{
   digitalWrite(latchPin, LOW);
   shiftOut(dataPin, clockPin, MSBFIRST, reg3);
   shiftOut(dataPin, clockPin, MSBFIRST, reg2);
   shiftOut(dataPin, clockPin, MSBFIRST, reg1);
   digitalWrite(latchPin, HIGH);
}
