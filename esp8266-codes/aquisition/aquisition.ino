//Pinos de uso
//Leitura
#define AD8226_OUT 13
#define AMPOP_TIA_OUT 35
//Escrita
#define DAC_IN 25
//Fixos
#define VDD_PIN 34
#define VBIAS_PIN 26

//Valores de tensão em volts
#define VBIAS 1

double tensao_dac_in = 0;
double ad8226_tensao;
double tia_tensao;
double t = 0;

const double pi = 3.1415;
const double fs = 1000;

int freq = 1000;
int ledChannel = 0;
int resolution = 8;

void setup() {
  Serial.begin(115200);

  //Configurando pinos do circuito
  pinMode(DAC_IN, OUTPUT);
  pinMode(AD8226_OUT, INPUT);
  pinMode(AMPOP_TIA_OUT, INPUT);

  //Pinos de tensões fixas
  pinMode(VDD_PIN, OUTPUT);
  digitalWrite(VDD_PIN, HIGH);
  pinMode(VBIAS_PIN, OUTPUT);
  dacWrite(VBIAS_PIN, (255*VBIAS/3.3));

  //Configurando o DAC_IN com PWM
  ledcSetup(ledChannel, 30000, resolution);
  ledcAttachPin(DAC_IN, ledChannel);
}

void loop() {
  //Escrevendo na entrada do circuito (Idac)
  t = millis();
  tensao_dac_in = 127+127*sin(2*pi*(freq/fs)*t);
  dacWrite(DAC_IN, tensao_dac_in);

  //Lendo a tensão da saída do AD8226 e do ampop TIA
  ad8226_tensao = analogRead(AD8226_OUT)*3.3/4096;
  tia_tensao = analogRead(AMPOP_TIA_OUT)*3.3/4096;

  //Serial.println("Tensão saída AD8226: " + String(ad8226_tensao, 4));
  //Serial.println("Tensão saída TIA: " + String(tia_tensao, 4));

  Serial.print(ad8226_tensao);
  Serial.print(",");
  Serial.println(tia_tensao);
  
}
