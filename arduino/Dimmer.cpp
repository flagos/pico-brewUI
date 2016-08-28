#include "Dimmer.h"
#include "mapping.h"
#include "Arduino.h"


static int count = 0, current_idx = 0, idx = 0;
static int lengths[4];


int get_index(int index) {
  for (int i=0; i<sizeof(lengths)/sizeof(lengths[0]); i++)
    if (index < lengths[i])
      return i;
  return sizeof(lengths)/sizeof(lengths[0]); // should not be here
}

void zero_cross_sync_it(void) {

  int state_idx = get_index(idx);
  
  if( current_idx == 0) {
    digitalWrite( MASH_RESISTOR, 0 );      
    digitalWrite( BOIL_RESISTOR, 0 );      
    digitalWrite( HOT_RESISTOR,  1 );
  }
  if( current_idx == 1) {
    digitalWrite( HOT_RESISTOR,  0 );
    digitalWrite( BOIL_RESISTOR, 0 );      
    digitalWrite( MASH_RESISTOR, 1 );      
  }
  if( current_idx == 2) {
    digitalWrite( HOT_RESISTOR,  0 );      
    digitalWrite( MASH_RESISTOR, 0 );
    digitalWrite( BOIL_RESISTOR, 1 );           
  }
  if( current_idx == 3) {
    digitalWrite( HOT_RESISTOR,  0 );      
    digitalWrite( MASH_RESISTOR, 0 );
    digitalWrite( BOIL_RESISTOR, 0 );           
  }
  
  idx++;
  idx %= lengths[3];
}


void set_lengths(int SSR0, int SSR1, int SSR2, int IDLE) {
  lengths[0] = SSR0;
  lengths[1] = SSR0 + SSR1;
  lengths[2] = SSR0 + SSR1 + SSR2;
  lengths[3] = SSR0 + SSR1 + SSR2 + IDLE;
}
