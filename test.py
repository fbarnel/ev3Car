#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import struct
import pickle

path="/tmp/dirMotorTraces.bin"
fLogTraces=open(path,"wb")
state="running"
start = time.time()
for i in range(10000):
    byteS2=struct.pack(">IIIIIIIIIs",i,25,100,12000,0,123,8737,98,4,b'running')
    fLogTraces.write(byteS2)
end = time.time()
print("Elapsed time binary=%f" %(end-start))
fLogTraces.close()

dataTrace = {
    'index' : 0,
    'PWM' : 0,
    'Pos' : 0,
    'Speed' : 0,
    'PD' : 0,
    'PP' : 0,
    'PI' : 0,
    'SD' : 0,
    'SP' : 0,
    'SI' : 0,
    'state' : 'hold'
}



start = time.time()
for j in range(10):
    listTrace=[]
    path="/tmp/dirMotorTracesP"+str(j)+".bin"
    with open(path, 'wb+') as fLogTraces:
        for i in range(1000):
            dataTrace = (i, 25, 100, 100, 12000, 0, 123, 8737, 98, 4, 'running')
            listTrace.append(dataTrace)

        pickle.dump(listTrace, fLogTraces, pickle.DEFAULT_PROTOCOL)
    fLogTraces.close()
end = time.time()
print("Elapsed time pickle bin=%f" %(end-start))

start = time.time()
for j in range(10):
    path="/tmp/dirMotorTracesP"+str(j)+".bin"
    with open(path, 'rb') as fLogTraces:
        data = pickle.load(fLogTraces)

        for dataTrace in data: print(dataTrace)
    fLogTraces.close()

end = time.time()
print("Elapsed time pickle bin decode=%f" %(end-start))






path="/tmp/dirMotorTraces.txt"
fLogTraces=open(path,"w")
start = time.time()
for i in range(10000):
    fLogTraces.write("%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%s\n" % (i, 25, 100, 100, 12000, 0, 123, 8737, 98, 4, 'running'))
end = time.time()
print("Elapsed time text=%f" %(end-start))
fLogTraces.close()

start = time.time()
with open('/tmp/dirMotorTraces.bin', 'rb') as fLogTraces:
    cst = memoryview(fLogTraces.read())

for i in range(1000):
    lineIntB=cst[36*i:36*(i+1)]
    lineIntS=struct.unpack(">IIIIIIIII", lineIntB)
    #print(lineIntS)
end = time.time()
print("Elapsed time binary Read=%f" %(end-start))
fLogTraces.close()


