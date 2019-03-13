#define outPin 9
#define inPin 33
#define ResistorShunt 1

double val = 0 ; 
int freq = 1000;
double t = 0;
const double pi = 3.1415;
const double fs = 1000;
int ledChannel = 0;
int resolution = 8;
double measure;
double current;
double ResistPele;
double VPele;

void setup() {
  Serial.begin(115200);
  pinMode(outPin, OUTPUT);
  pinMode(inPin, INPUT);
  ledcSetup(ledChannel, 30000, resolution);
}

void loop() {
  t = millis();
  val = 127+127*sin(2*pi*(freq/fs)*t);
  dacWrite(outPin, val);
  measure = analogRead(inPin)* 3.3/4096;
  current = measure/ResistorShunt;
  VPele = val-measure;
  ResistPele = VPele/current;
  Serial.print("measure: ");
  Serial.println(measure);
  Serial.print("Rpele: ");
  Serial.println(ResistPele);  
}
