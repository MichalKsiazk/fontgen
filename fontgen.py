from symbol_button import *
import os 

class HeaderFile:
    def __init__(self, name, x, y, compressed:bool):
        self.filename = name
        self.filedata = []
        self.x = x
        self.y = y
        self.compressed = compressed
        self.generateData()
    
    def saveFile(self):
        if not os.path.exists(self.filename):
            os.mkdir(self.filename)
        file = open("{}/{}.h".format(self.filename, self.filename), "w")
        for line in self.filedata:
           file.write(line + '\n')
        file.close() 
    
    def generateData(self):
        self.filedata.append("#ifndef __{}_H__".format(self.filename.upper().replace(".H", "")))
        self.filedata.append("#define __{}_H__".format(self.filename.upper().replace(".H", "")))
        self.filedata.append("")
        self.filedata.append("#include <stdint.h>")
        self.filedata.append('#include "fontgen_common.h"')
        self.filedata.append("")
        self.filedata.append("extern {} {};".format("FontCommon", self.filename + "_" + str(self.x) + "x" + str(self.y)))
        self.filedata.append("")
        if self.compressed:
            self.generateCompressedFontInterface()
        self.filedata.append("#endif")   

    def generateCompressedFontInterface(self):
        self.filedata.append("uint8_t {}_Interface(const char* str);".format(self.filename))
        self.filedata.append("")
        pass

    
class SourceFile:
    def __init__(self, name, x, y, symbols:SymbolButton, compressed:bool):
        self.symbols = symbols
        self.filename = name
        self.filedata = []
        self.x = x
        self.y = y
        self.compressed = compressed
        self.compressedDataScheme = []
        self.generateData()
    
    def saveFile(self):
        if not os.path.exists(self.filename):
            os.mkdir(self.filename)
        file = open("{}/{}.c".format(self.filename, self.filename), "w")
        for line in self.filedata:
           file.write(line + '\n')
        file.close() 
    
    def generateData(self):
        self.filedata.append('#include "{}.h"'.format(self.filename))
        self.filedata.append("static const uint8_t {} [] = ".format(self.filename + str(self.x) + "x" + str(self.y)))
        self.filedata[-1] += "{"
        cnt = 8
        value = 0
        rc = 0
        self.filedata.append("   ")
        prevEmpty:bool = False
        for i, s in enumerate(self.symbols):
            if self.compressed:
                if s.isEmpty():
                    print("empty char found", i)
                    if not prevEmpty:
                        self.compressedDataScheme.append([i, 1])
                    else:
                        self.compressedDataScheme[-1][0] = i
                        self.compressedDataScheme[-1][1] += 1
                    prevEmpty = True
                    continue
                else:
                    print("filled char found", i)

            prevEmpty = False
            for y in s.bitMap:
                for x in y:
                    value += (x & 0x1) << (cnt - 1)                
                    cnt -= 1
                    if cnt == 0:
                        cnt = 8
                        if rc >= 8:
                            rc = 0
                            self.filedata.append("   " + " " + hex(value) + ",")
                        else:
                            self.filedata[-1] += " " + hex(value) + ","
                            rc += 1
                        value = 0
        if cnt != 0:  
            cnt = 0
            self.filedata.append(hex(value))
            value = 0
        else:   
            self.filedata[-1].replace(",", "")
        self.filedata.append("};")    
        self.filedata.append("")  
        self.filedata.append("FontCommon {}_{}x{} = ".format(self.filename, self.x, self.y))
        self.filedata[-1] += "{"
        self.filedata[-1] += "{}, {}, {}{}x{}".format(self.x, self.y, self.filename, self.x, self.y)
        self.filedata[-1] += ",{}".format("1" if self.compressed else "0")
        self.filedata[-1] += "};"
        if self.compressed:
            self.generateCompressedFontInterface()
        print(self.compressedDataScheme)

    def generateCompressedFontInterface(self):
        self.filedata.append("uint8_t {}_Interface(const char* str)".format(self.filename))
        self.filedata.append("{")
        self.filedata.append("    uint8_t retval = 0;")
        for x in self.compressedDataScheme:
            self.filedata.append("    if(str > {})".format(str(x[0])))
            self.filedata.append("    {")
            self.filedata.append("        retval -= {};".format(str(x[1])))
            self.filedata.append("    }")
        self.filedata.append("return retval;")
        self.filedata.append("}")
        pass


        
class FontgenCommonFile:
    def __init__(self, destination):
        self.filedata = []
        self.destination = destination
        self.generateData(destination)
    
    def saveFile(self):
        if not os.path.exists(self.destination):
            os.mkdir(self.destination)
        file = open("{}/{}.h".format(self.destination, "fontgen_common"), "w")
        for line in self.filedata:
           file.write(line + '\n')
        file.close() 
    
    def generateData(self, destination):
        self.filedata.append("#ifndef __FONTGEN_COMMON_H__")
        self.filedata.append("#define __FONTGEN_COMMON_H__")
        self.filedata.append("#include <stdint.h>")
        self.filedata.append("")
        self.filedata.append("typedef struct {")
        self.filedata.append("const uint8_t width;")
        self.filedata.append("const uint8_t height;")
        self.filedata.append("const uint8_t *data;")
        self.filedata.append("const uint8_t compressed;")
        self.filedata.append("} FontCommon;")      
        self.filedata.append("")
        self.filedata.append("#endif")
            
class GeneratedFont:
    def __init__(self, name, x, y, symbols:SymbolButton, compressed:bool):
        self.sourceFile = SourceFile(name, x, y, symbols, compressed)
        self.headerFile = HeaderFile(name, x, y, compressed)
        self.commonFile = FontgenCommonFile(name)
        self.sourceFile.saveFile()
        self.headerFile.saveFile()
        self.commonFile.saveFile()
   
    
    
        
        