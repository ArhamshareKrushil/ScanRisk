import struct
import time

from Application.Services.UDP.Parse_NSEFO.F7202 import process
import time
# from Application.Services.UDP.Parse_NSEFO.F7202 import process




def getOutput(self,Decoded_Packet,poc):
    # print('7202')
    NoOf_Records = struct.unpack('!h', Decoded_Packet[48:50])
    Start_Pointof_Record = 50
    for ik in range(NoOf_Records[0]):
        End_Pointof_Record = Start_Pointof_Record + 26


        # if(poc == 'python'):
        #     for i in range(100000):
        #         output = process.process(self,Decoded_Packet,Start_Pointof_Record,End_Pointof_Record)
        # else:
        #     for i in range(100000):
        #         output = process1.process(self,Decoded_Packet,Start_Pointof_Record,End_Pointof_Record)




        output = process.process(self, Decoded_Packet, Start_Pointof_Record, End_Pointof_Record)

        if output:
            # print('7202')
            self.sgData7202.emit(output)

        # print('7202')
        Start_Pointof_Record = End_Pointof_Record
