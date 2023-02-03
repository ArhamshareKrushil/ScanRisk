from  Application.Services.UDP.Parse_NSEFO.F7220 import process




def getOutput(self,Decoded_Packet):
    Start_Pointof_Record = 48
    output =process.process(self, Decoded_Packet, Start_Pointof_Record)
    self.sender.sendData(output)
    print(output)