#ifndef BUTTON_H
#define BUTTON_H

class Button{

  public:
    Button(int pin);
    int read();
    void setup();
    


  private:
    int ppin;

};


#endif