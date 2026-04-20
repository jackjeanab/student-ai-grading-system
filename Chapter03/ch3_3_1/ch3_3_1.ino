//Generated Date: Thu, 04 Jul 2024 07:51:39 GMT



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

void Alarm_sound() {
  playBuzzer(14, "523", "800", 0);
  playBuzzer(14, "698", "800", 0);
}

void setup()
{

}

void loop()
{
  Alarm_sound();
  delay(1000);
  Alarm_sound();
  delay(500);
  Alarm_sound();
  delay(2000);
}
