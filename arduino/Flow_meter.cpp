#include "Flow_meter.h"
#include "mapping.h"
#include "Arduino.h"

static int flow_count = 0;


// The hall-effect flow sensor outputs approximately 4.5 pulses per second per
// litre/minute of flow.
float calibrationFactor = 4.5;
unsigned long oldTime;
volatile byte pulseCount;  

float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;



unsigned long compute_flow_Ml(void) {
  
  if((millis() - oldTime) > 1000)    // Only process counters once per second
    { 
      // Disable the interrupt while calculating flow rate and sending the value to
      // the host
      detachInterrupt(FLOW_METER_IT);
      
      // Because this loop may not complete in exactly 1 second intervals we calculate
      // the number of milliseconds that have passed since the last execution and use
      // that to scale the output. We also apply the calibrationFactor to scale the output
      // based on the number of pulses per second per units of measure (litres/minute in
      // this case) coming from the sensor.
      flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
    
      // Note the time this processing pass was executed. Note that because we've
      // disabled interrupts the millis() function won't actually be incrementing right
      // at this point, but it will still return the value it was set to just before
      // interrupts went away.
      oldTime = millis();
    
      // Divide the flow rate in litres/minute by 60 to determine how many litres have
      // passed through the sensor in this 1 second interval, then multiply by 1000 to
      // convert to millilitres.
      flowMilliLitres = (flowRate / 60) * 1000;
    
      // Add the millilitres passed in this second to the cumulative total
      totalMilliLitres += flowMilliLitres;

      // Reset the pulse counter so we can start incrementing again
      pulseCount = 0;
    
      // Enable the interrupt again now that we've finished sending output
      attachInterrupt(FLOW_METER_IT, flow_meter_it, FALLING);
    }

  return totalMilliLitres;
}

void flow_meter_it(void) {
  pulseCount++;
}

