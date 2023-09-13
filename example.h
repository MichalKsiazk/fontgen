#ifndef __EXAMPLE_H__
#define __EXAMPLE_H__

#include <stdint.h>

typedef struct {
  const uint8_t width;
  const uint8_t height;
  const uint16_t *data;
}example;

extern example example_9x9;

#endif
