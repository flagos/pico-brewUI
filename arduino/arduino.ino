#include "OneWire.h"
#include "DallasTemperature.h"
#include "CmdMessenger.h"  // CmdMessenger
#include "TimerOne.h"
#include <avr/wdt.h>
#include "Dimmer.h"
#include "mapping.h"



// Blinking led variables
unsigned long previousToggleLed = 0;   // Last time the led was toggled
bool ledState                   = 0;   // Current state of Led

static int count = 0;

/*
 *   Thermometer
 */

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// Device addresses
DeviceAddress pipeThermometer   = { 0x28, 0xFF, 0xE0, 0xC4, 0x91, 0x15, 0x04, 0x54};
DeviceAddress boilThermometer   = { 0x28, 0xFF, 0x0B, 0xC4, 0x91, 0x15, 0x04, 0xFE};
 
float    pipeTemp,        boilTemp;


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
  kDumpInWater_reached , // Command to send that water has been filled in
  Resistor               // Command to set SSR values

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
  cmdMessenger.attach(Resistor    , OnResistor);
}

// ------------------  C A L L B A C K S -----------------------


void zero_cross_sync_it2(void) {
  count++;
  count %= 100;
  if (count==0)
    toggleLed();
  
  //cmdMessenger.sendCmd(kAcknowledge,"IT");
}


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
  int pin           = (int)                 cmdMessenger.readFloatArg();
  bool value        = (bool)          ((int)cmdMessenger.readFloatArg());

  pinMode(pin, OUTPUT);
  digitalWrite(pin, value?HIGH:LOW);
  cmdMessenger.sendCmd(kAcknowledge,"Set Pin");
}

// Callback function for a set pin bool
void OnPwmPin()
{
  int pin   = (int) cmdMessenger.readFloatArg();
  int value = (int) cmdMessenger.readFloatArg();

  pinMode(pin, OUTPUT);
  analogWrite(pin, value);
  cmdMessenger.sendCmd(kAcknowledge,"Set Pin PWM");
}

void OnDumpIn()
{
  int valve       = (int)      cmdMessenger.readFloatArg();
  int milliliters = (int)      cmdMessenger.readFloatArg();  // 65 liters max each time by design

  cmdMessenger.sendCmd(kAcknowledge,"Set valve dosage");

}

void OnResistor()
{
  int ssr0       = (int)      cmdMessenger.readFloatArg();
  int ssr1       = (int)      cmdMessenger.readFloatArg();
  int ssr2       = (int)      cmdMessenger.readFloatArg();
  int idle       = (int)      cmdMessenger.readFloatArg();

  set_lengths(ssr0, ssr1, ssr2, idle);

  cmdMessenger.sendCmd(kAcknowledge,"Set Resistor");

}






// ------------------ M A I N  ----------------------

// Setup function
void setup()
{
  
  // Listen on serial connection for messages from the pc
  Serial.begin(9600);

  // Adds newline to every command
  cmdMessenger.printLfCr();

  // Attach my application's user-defined callback methods
  attachCommandCallbacks();

  // Start up the library
  //sensors.begin();

  // set the resolution to 12 bit
  sensors.setResolution(pipeThermometer, TEMPERATURE_PRECISION);
  sensors.setResolution(boilThermometer, TEMPERATURE_PRECISION);
  
  sensors.setWaitForConversion(false);
  
  
  // Send the status to the PC that says the Arduino has booted
  cmdMessenger.sendCmd(kAcknowledge,"Arduino has started!");

  // set pin for blink LED
  pinMode(kBlinkLed, OUTPUT);

  Timer1.initialize(1000000);
  Timer1.attachInterrupt(callback_1second);


  // RELAY & ZERO_CROSS
  pinMode(HOT_RESISTOR,  OUTPUT);
  pinMode(MASH_RESISTOR, OUTPUT);
  pinMode(BOIL_RESISTOR, OUTPUT);
  digitalWrite(HOT_RESISTOR , 0);
  digitalWrite(MASH_RESISTOR, 0);
  digitalWrite(BOIL_RESISTOR, 0);
  set_lengths(0, 0, 0, 100);
  
  pinMode(ZERO_CROSS_IT_PIN, INPUT_PULLUP);
  attachInterrupt(ZERO_CROSS_IT, zero_cross_sync_it, RISING);  
  //attachInterrupt(ZERO_CROSS_IT, zero_cross_sync_it2, RISING);  
  
  // enable Watchdog (2 second)
  wdt_enable(WDTO_2S);
}



void interruptTemperature (void) 
{

  pipeTemp = sensors.getTempC(pipeThermometer);  
  boilTemp = sensors.getTempC(boilThermometer);
  
  // call sensors.requestTemperatures() to issue a global temperature 
  // request to all devices on the bus
  sensors.requestTemperatures();
}


void callback_1second(void) {

  //cmdMessenger.sendCmd(kAcknowledge,"Arduino has timer");

  interruptTemperature(); // get temperature data and request measure


  cmdMessenger.sendCmdStart(kReadTemperature);
  cmdMessenger.sendCmdArg<uint16_t>((uint16_t) 100*100); // API is supposed to have 3 thermometers
  cmdMessenger.sendCmdArg<uint16_t>((uint16_t) (pipeTemp*100));
  cmdMessenger.sendCmdArg<uint16_t>((uint16_t) (boilTemp*100));
  cmdMessenger.sendCmdEnd ();
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
    //toggleLed();
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


