#include 'bby.h'
static const uint8_t bby5x5 [] = {
    0xfc, 0x63, 0x1f, 0x98, 0x42, 0x10, 0xbe, 0x1f,
    0xc3, 0xff, 0xf, 0xc3, 0xf8, 0xc7, 0xe1, 0xf, 0xe1,
    0xf0, 0xff, 0xf0, 0xfc, 0x7f, 0xf0, 0x84, 0x21, 0xfc,
    0x7f, 0x1f, 0xfe, 0x3f, 0xf, 0xff, 0x1f, 0xc6, 0x3e,
    0x97, 0xe3,
0xf0
};

FontCommon bby_5x5 = {5, 5, bby5x5,1};
uint8_t bby_Interface(const char* str)
{
    uint8_t retval = 0;
    if(str > 47)
    {
        retval -= 48
    }
    if(str > 64)
    {
        retval -= 7
    }
    if(str > 255)
    {
        retval -= 189
    }
}
