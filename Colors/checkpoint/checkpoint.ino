const int LED=2;
const int S0=3;
const int S1=4;
const int LectureOUT=5;
const int S2=6;
const int S3=7;

const int led_Rouge=9; 
const int led_Verte=10; 
const int led_Bleu=11; 

enum color {
  red,
  green,
  blue,

  limit,
  powerUp
};

color currentColor = red;
color nextColor = green;


void setup() {

  randomSeed(analogRead(0));  

  pinMode(LED, OUTPUT);
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(LectureOUT, INPUT);  
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(led_Rouge, OUTPUT);
  pinMode(led_Verte, OUTPUT);
  pinMode(led_Bleu, OUTPUT);  
  Serial.begin(9600);
  digitalWrite(LED, 1);
  ledRVBpwm(0,0,0); 
  digitalWrite(S0, 0);
  digitalWrite(S1, 1);
  delay(100);
}

void loop() {
  digitalWrite(S2, 0); 
  digitalWrite(S3, 0);
  int rouge = pulseIn(LectureOUT, 0);
  Serial.print("rouge: ");
  Serial.print(rouge);
  delay(20); 

  digitalWrite(S2, 1); 
  digitalWrite(S3, 1);
  int vert = pulseIn(LectureOUT, 0);
  Serial.print(" | vert: ");
  Serial.print(vert);
  delay(20);
  
  digitalWrite(S2, 0); 
  digitalWrite(S3, 1);
  int bleu = pulseIn(LectureOUT, 0);
  Serial.print(" | bleu: ");
  Serial.print(bleu);
  delay(20); 
  
  digitalWrite(S2, 1); 
  digitalWrite(S3, 0);
  int sansfiltre = pulseIn(LectureOUT, 0);
  Serial.print(" | Sans filtre: ");
  Serial.println(sansfiltre);
  delay(20); 
  
  if (rouge>25 && rouge<45 && vert>40 && vert<60 && bleu>70 && bleu<90){ //orange, checkpoint
    ledRVBpwm(50,50,0);

    if (currentColor == blue){
      currentColor = red;
      nextColor = green;
    }
    else{
      // code nothing (only change when the right checkpoint is reached)
    }
    
  }
  
  else if (rouge>70 && rouge<90 && vert>65 && vert<85 && bleu>100 && bleu<120){ //vert, checkpoint
    ledRVBpwm(0,50,0);
    if (currentColor == red){
      currentColor = green;
      nextColor = blue;
    }
    else{
      // code nothing (only change when the right checkpoint is reached)
    }
  }

  else if (rouge>90 && rouge<120 && vert>70 && vert<90 && bleu>45 && bleu<65){ //bleu, checkpoint
    ledRVBpwm(0,0,100);
    if (currentColor == green){
      currentColor = blue;
      nextColor = red;
    }
    else{
      // code nothing (only change when the right checkpoint is reached)
    }
  }
  
  else if (rouge>30 && rouge<50 && vert>85 && vert<105 && bleu>80 && bleu<105){ //jaune, powerUp
    ledRVBpwm(50,10,0);
    randPowerUp = random(2); // random form 0 to 2 

    switch (randPowerUp) {
      case 0:
        // code freeze 3s
        break;
      case 1:
        // code speed up 5s
        break;
      case 2:
        // code inversion commandes pour l'utilisateur
        break;
      default:
        // ne rien faire
        break;
  }  
     
  }

  else{
    ledRVBpwm(0,0,0);    
  }
  delay(500);

}

void ledRVBpwm(int pwmRouge, int pwmVert, int pwmBleu) { 
 analogWrite(led_Rouge, pwmRouge); 
 analogWrite(led_Verte, pwmVert); 
 analogWrite(led_Bleu, pwmBleu); 
}
