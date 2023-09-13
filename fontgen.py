from symbol_button import *
import os 

class HeaderFile:
    def __init__(self, name, x, y):
        self.filename = name
        self.filedata = []
        self.x = x
        self.y = y
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
        self.filedata.append("#include <fontgen_common.h>")
        self.filedata.append("")
        self.filedata.append("extern {} {};".format("FontCommon", self.filename + "_" + str(self.x) + "x" + str(self.y)))
        self.filedata.append("")
        self.filedata.append("#endif")      
    
class SourceFile:
    def __init__(self, name, x, y, symbols:SymbolButton):
        self.symbols = symbols
        self.filename = name
        self.filedata = []
        self.x = x
        self.y = y
        self.generateData()
    
    def saveFile(self):
        if not os.path.exists(self.filename):
            os.mkdir(self.filename)
        file = open("{}/{}.c".format(self.filename, self.filename), "w")
        for line in self.filedata:
           file.write(line + '\n')
        file.close() 
    
    def generateData(self):
        self.filedata.append("#include '{}.h'".format(self.filename))
        self.filedata.append("static const uint8_t {} [] = ".format(self.filename + str(self.x) + "x" + str(self.y)))
        self.filedata[-1] += "{"
        cnt = 8
        value = 0
        rc = 0
        self.filedata.append("   ")
        for i, s in enumerate(self.symbols):
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
        self.filedata[-1] += "};"
        
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
        self.filedata.append("} FontCommon;")      
        self.filedata.append("")
        self.filedata.append("#endif")
            
class GeneratedFont:
    def __init__(self, name, x, y, symbols:SymbolButton):
        self.sourceFile = SourceFile(name, x, y, symbols)
        self.headerFile = HeaderFile(name, x, y)
        self.commonFile = FontgenCommonFile(name)
        self.sourceFile.saveFile()
        self.headerFile.saveFile()
        self.commonFile.saveFile()
   
    
    
        
        