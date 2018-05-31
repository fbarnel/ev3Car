#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import struct

path="/tmp/dirMotorTraces.bin"
fLogTraces=open(path,"wb")
state="running"
start = time.time()
for i in range(100):
    byteS2=struct.pack(">IIIIIIIII",i,25,100,12000,0,123,8737,98,4)
    fLogTraces.write(byteS2)
end = time.time()
print("Elapsed time binary=%f" %(end-start))
fLogTraces.close()

path="/tmp/dirMotorTraces.txt"
fLogTraces=open(path,"w")
start = time.time()
for i in range(100):
    fLogTraces.write("%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n" % (i, 25, 100, 100, 12000, 0, 123, 8737, 98, 4))
end = time.time()
print("Elapsed time text=%f" %(end-start))
fLogTraces.close()

start = time.time()
with open('/tmp/dirMotorTraces.bin', 'rb') as fLogTraces:
    cst = memoryview(fLogTraces.read())

for i in range(100):
    lineIntB=cst[36*i:36*(i+1)]
    lineIntS=struct.unpack(">IIIIIIIII", lineIntB)
    print(lineIntS)
end = time.time()
print("Elapsed time binary Read=%f" %(end-start))
fLogTraces.close()


