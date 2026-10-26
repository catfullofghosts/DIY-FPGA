/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  This example code is in the public domain.
 */

// Pin 13 has an LED connected on most Arduino boards.
// Pin 11 has the LED on Teensy 2.0
// Pin 6  has the LED on Teensy++ 2.0
// Pin 13 has the LED on Teensy 3.0
// give it a name:
int data = 22;
int strobe = 23;
int rst = 2;
int ax0 = 27;
int ax1 = 28;
int ax2 = 29;
int ax3 = 30;
int ay0 = 31;
int ay1 = 32;
int ay2 = 33;

int DCLK = 3;
int MOSIp = 4;
int SCKp = 5;
int LOAD = 6;
int MISOp = 7;


// the setup routine runs once when you press reset:
void setup() {
  // initialize the digital pin as an output.
  pinMode(data, OUTPUT);
  pinMode(strobe, OUTPUT);
  pinMode(rst, OUTPUT);
  pinMode(ax0, OUTPUT);
  pinMode(ax1, OUTPUT);
  pinMode(ax2, OUTPUT);
  pinMode(ax3, OUTPUT);
  pinMode(ay0, OUTPUT);
  pinMode(ay1, OUTPUT);
  pinMode(ay2, OUTPUT);
  pinMode(DCLK, OUTPUT);
  pinMode(MOSIp, OUTPUT);
  pinMode(SCKp, OUTPUT);
  pinMode(LOAD, OUTPUT);
  pinMode(MISOp, OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  //set everything low... make an init function
  digitalWrite(data, LOW);   
  digitalWrite(strobe, LOW);  
  digitalWrite(rst, HIGH);  
  digitalWrite(ax0, LOW); //1 
  digitalWrite(ax1, LOW); //2 
  digitalWrite(ax2, LOW); //4 
  digitalWrite(ax3, LOW); //8 
  digitalWrite(ay0, LOW);  
  digitalWrite(ay1, LOW);  
  digitalWrite(ay2, LOW);  
  digitalWrite(DCLK, LOW);  
  digitalWrite(MOSIp, LOW);  
  digitalWrite(SCKp, LOW);  
  digitalWrite(LOAD, LOW);  
  digitalWrite(MISOp, LOW); 
  delay(100);   
  digitalWrite(rst, LOW);
  delay(100);    
  
 set_xy_crospoint(12,0,1);
  set_xy_crospoint(12,4,1);

  set_xy_crospoint(12,5,1);
  
  set_xy_crospoint(12,6,1);
  set_xy_crospoint(12,7,1);
    while(1){
    delay(100); 
    
  }

 //prog      inputs, global in 1,2,3 go to a,b,c,a2,b2,c2
 set_xy_crospoint(0,0,1);
 set_xy_crospoint(3,0,1);
 set_xy_crospoint(1,1,1);
 set_xy_crospoint(4,1,1);
 set_xy_crospoint(2,2,1);
 set_xy_crospoint(5,2,1);




  //prog      output all 4 lut outs go to global outs
// set_xy_crospoint(8,4,1); //x6// 6 and 7 x address are null need to add 2
// set_xy_crospoint(9,5,1); //x7
// set_xy_crospoint(10,6,1); //x8
// set_xy_crospoint(11,7,1);//x9


  while(1){
    delay(100); 
    
  }
}

void strobe_pin(){
  delay(50); 
  digitalWrite(strobe, HIGH);    
  delay(50); 
  digitalWrite(strobe, LOW); 
}

void set_xy_crospoint(int x_val,int y_val,int data_bit){

digitalWrite(ax3, x_val & B00001000);
digitalWrite(ax2, x_val & B00000100);
digitalWrite(ax1, x_val & B00000010);
digitalWrite(ax0, x_val & B00000001);

digitalWrite(ay2, y_val & B00000100);
digitalWrite(ay1, y_val & B00000010);
digitalWrite(ay0, y_val & B00000001);

digitalWrite(data, data_bit); 
strobe_pin();
}
