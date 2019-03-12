void setup()
{
  pinMode(16, OUTPUT);//Definimos o pino 2 (LED) como saída.
  pinMode( 4, INPUT);
  ledcAttachPin(16, 0);//Atribuimos o pino 2 ao canal 0.
  ledcSetup(0, 1000, 10);//Atribuimos ao canal 0 a frequencia de 1000Hz com resolucao de 10bits.
  Serial.begin(115200); 
}
 
void loop()
{
  for (int i = 0; i < 1024; i++)
  {
    ledcWrite(0, i);//Escrevemos no canal 0, o duty cycle "i".
    delay(2);
    Serial.println(analogRead(4));
  }
 
  for (int i = 1023; i > 0; i--)
  {
    ledcWrite(0, i);
    delay(2);
    Serial.println(analogRead(4));
  }
  
}
