//Generated Date: Sun, 07 Jul 2024 07:55:47 GMT



void playBuzzer(int pin, String frequency, String delaytime, int channel) {
  int freq = 2000;
  int resolution = 8;
  ledcSetup(channel, freq, resolution);
  ledcAttachPin(pin, channel);
  String f="",d="",split=",";
  int s1=0;
  frequency+=",";
  delaytime+=",";
  for (int i=0;i<frequency.length();i++) {
    if (frequency[i]==split[0]) {
  	   f=frequency.substring(s1,i);
  	   s1=i+1;
  	   for (int j=0;j<delaytime.length();j++) {
  	      if (delaytime[j]==split[0]) {
  		    d=delaytime.substring(0,j);
  		    ledcWriteTone(channel, f.toInt());
  		    delay(d.toInt());
  		    delaytime=delaytime.substring(j+1);
  		    break;
  	      }
  	    }
    }
  }
  ledcWriteTone(channel, 0);
}

void mySong1() {
  playBuzzer(14, "784", "500", 0);
  playBuzzer(14, "659", "500", 0);
  playBuzzer(14, "659", "500", 0);
  delay(500);
}

void mySong2() {
  playBuzzer(14, "698", "500", 0);
  playBuzzer(14, "587", "500", 0);
  playBuzzer(14, "587", "500", 0);
  delay(500);
}

void setup()
{

}

void loop()
{
  mySong1();
  mySong2();
}
