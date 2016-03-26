// *** SendandReceiveArguments ***

// This example expands the previous SendandReceive example. The Arduino will now receive multiple 
// and sent multiple float values. 
// It adds a demonstration of how to:
// - Return multiple types status; It can return an Acknowlegde and Error command
// - Receive multiple parameters,
// - Send multiple parameters
// - Call a function periodically

#include "CmdMessenger.h"  // CmdMessenger
#include "TimerOne.h"
#include <avr/wdt.h>

// Blinking led variables 
unsigned long previousToggleLed = 0;   // Last time the led was toggled
bool ledState                   = 0;   // Current state of Led
const int kBlinkLed             = 13;  // Pin of internal Led

// Attach a new CmdMessenger object to the default Serial port
CmdMessenger cmdMessenger = CmdMessenger(Serial);

// This is the list of recognized commands. These can be commands that can either be sent or received. 
// In order to receive, attach a callback function to these events
enum
{
  // Commands
  kAcknowledge         , // Command to acknowledge that cmd was received
  kError               , // Command to report errors
  kPing                , // Command ardiono still alive 
  kSetPin              , // Command to request set pin ON/OFF
  kPwmPin              , // Command to request set pin PWM
  kReadTemperature     , // Command to send temperatures from ds18b20
  kDumpInWater         , // Command to dose in water
  kDumpInWater_reached  // Command to send that water has been filled in
  
};

// Commands we send from the PC and want to receive on the Arduino.
// We must define a callback function in our Arduino program for each entry in the list below.

void attachCommandCallbacks()
{
  // Attach callback methods
  cmdMessenger.attach(OnUnknownCommand);
  cmdMessenger.attach(kAcknowledge, OnAcknowledge);
  cmdMessenger.attach(kPing       , OnPing);
  cmdMessenger.attach(kSetPin     , OnSetPin);
  cmdMessenger.attach(kPwmPin     , OnPwmPin);
  cmdMessenger.attach(kDumpInWater, OnDumpIn);
}

// ------------------  C A L L B A C K S -----------------------

// Called when a received command has no attached function
void OnUnknownCommand()
{
  cmdMessenger.sendCmd(kError,"Command without attached callback");
}

// Callback function that responds on ack
void OnAcknowledge()
{
  cmdMessenger.sendCmd(kAcknowledge,"Arduino ACK");
}

// Callback function that responds that Arduino is ready (has booted up)
void OnArduinoReady()
{
  cmdMessenger.sendCmd(kAcknowledge,"Arduino ready");
}

// Callback function send a pong
void OnPing()
{
  cmdMessenger.sendCmd(kAcknowledge,"Arduino Pong");
}

// Callback function for a set pin bool
void OnSetPin()
{
  unsigned char pin = (unsigned char) cmdMessenger.readCharArg();
  bool value        =                 cmdMessenger.readBoolArg();
  
  digitalWrite(pin, value?HIGH:LOW);
  cmdMessenger.sendCmd(kAcknowledge,"Set Pin");
}

// Callback function for a set pin bool
void OnPwmPin()
{
  unsigned char pin   = (unsigned char) cmdMessenger.readCharArg();
  unsigned char value = (unsigned char) cmdMessenger.readCharArg();
  
  analogWrite(pin, value);
  cmdMessenger.sendCmd(kAcknowledge,"Set Pin PWM");
}

void OnDumpIn()
{
  unsigned char valve       = (unsigned char) cmdMessenger.readCharArg();
  unsigned      milliliters = (unsigned)      cmdMessenger.readInt16Arg();  // 65 liters each time by design
  
  
  
  cmdMessenger.sendCmd(kAcknowledge,"Set valve dosage");
  
}





// ------------------ M A I N  ----------------------

// Setup function
void setup() 
{
  // Listen on serial connection for messages from the pc
  Serial.begin(9600); 

  //while(!Serial);

  // Adds newline to every command
  cmdMessenger.printLfCr();   

  // Attach my application's user-defined callback methods
  attachCommandCallbacks();

  // Send the status to the PC that says the Arduino has booted
  cmdMessenger.sendCmd(kAcknowledge,"Arduino has started!");

  // set pin for blink LED
  pinMode(kBlinkLed, OUTPUT);
  
  //Timer1.initialize(1000000);
  //Timer1.attachInterrupt(callback_1second); 
  
  
  // enable Watchdog (2 second)
  wdt_enable(WDTO_2S);
}

void callback_1second(void) {

  //cmdMessenger.sendCmd(kAcknowledge,"Arduino has timer");
  
//  cmdMessenger.sendCmdStart(kReadTemperature);
//  cmdMessenger.sendCmdArg<uint16_t>((uint16_t) 100);
//  cmdMessenger.sendCmdArg<uint16_t>((uint16_t)98);
//  cmdMessenger.sendCmdArg<uint16_t>((uint16_t)96);
//  cmdMessenger.sendCmdEnd ();
}

// Returns if it has been more than interval (in ms) ago. Used for periodic actions
bool hasExpired(unsigned long &prevTime, unsigned long interval) {
  if (  millis() - prevTime > interval ) {
    prevTime = millis();
    return true;
  } else     
    return false;
}

// Loop function
void loop() 
{
  
  // Process incoming serial data, and perform callbacks
  //if(Serial.available()) 
    cmdMessenger.feedinSerialData();

  // Toggle LED periodically. If the LED does not toggle every 2000 ms, 
  // this means that cmdMessenger are taking a longer time than this  
  if (hasExpired(previousToggleLed,2000)) // Toggle every 2 secs
  {
    toggleLed();  
  } 
  
  // reset watchdog
  wdt_reset();

}

// Toggle led state 
void toggleLed()
{  
  ledState = !ledState;
  digitalWrite(kBlinkLed, ledState?HIGH:LOW);
}  
