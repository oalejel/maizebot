const int stepPin1 = 3; 
const int dirPin1 = 4; 
const int stepPin2 = 5; 
const int dirPin2 = 6; 
  int incoming[4];
 
 
void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin1,OUTPUT); 
  pinMode(dirPin1,OUTPUT);
  pinMode(stepPin2,OUTPUT); 
  pinMode(dirPin2,OUTPUT);
  Serial.begin(9600); // set the baud rate
  Serial.println("Ready"); // print "Ready" once
}
void loop() {

  if(Serial.available() >= 4){
    // fill array
    for (int i = 0; i < 4; i++){
      incoming[i] = Serial.read();
    }
    // use the values
    moveMotor(0, incoming[1], incoming[0]);
    moveMotor(1, incoming[3], incoming[2]);
  }
}

void moveMotor(int motor, int dist, int dir){
  if(motor == 0){
    if(dir){
      digitalWrite(dirPin1,HIGH);
    }
    else{
      digitalWrite(dirPin1,LOW);
    }
    for(int x = 0; x < dist; x++) {
      digitalWrite(stepPin1,HIGH); 
      delayMicroseconds(700); 
      digitalWrite(stepPin1,LOW); 
      delayMicroseconds(700); 
    }
  }
  if(motor == 1){
    if(dir){
      digitalWrite(dirPin2,HIGH);
    }
    else{
      digitalWrite(dirPin2,LOW);
    }
    for(int x = 0; x < dist; x++) {
      digitalWrite(stepPin2,HIGH); 
      delayMicroseconds(700); 
      digitalWrite(stepPin2,LOW); 
      delayMicroseconds(700); 
    }
  }
}
