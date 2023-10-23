#ifndef __FONTGEN_COMMON_H__
#define __FONTGEN_COMMON_H__
#include <stdint.h>

typedef struct {
const uint8_t width;
const uint8_t height;
const uint8_t *data;
const uint8_t compressed;
} FontCommon;

#endif
