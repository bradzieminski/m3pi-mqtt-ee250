
#include <math.h>

// These constants won't change. They're used to give names to the pins used:
// Analog input pin that the potentiometer is attached to
int pins[] = { A0, A1, A2, A3, };

#define S1 0
#define S2 1
#define S3 2
#define S4 3

#define wSize 15
#define maxD 99

int windows[4][wSize] = { {}, {}, {}, {} };
int avg[wSize] = { };
int index = 0;

void setup() 
{  
  Serial.begin(19200);
}

void loop() 
{
  if (index == wSize)
  {
    index = 0;
  }
  for (int s = 0; s < 4; s++)
  {
    windows[s][index] = fmin(maxD, analogRead(pins[s]));
    avg[s] = 0;
    for (int n = 0; n < wSize; n++)
    {
      avg[s] += windows[s][n];
    }
    avg[s] /= wSize;
    avg[s] /= 2;
    avg[s] *= 2;
  }
  index++;
  
  Serial.println(avg[S1]); 
  /*Serial.print("   ");
  Serial.print(avg[S2]); 
  Serial.print("   ");
  Serial.print(avg[S3]); 
  Serial.print("   ");
  Serial.println(avg[S4]);*/
}
