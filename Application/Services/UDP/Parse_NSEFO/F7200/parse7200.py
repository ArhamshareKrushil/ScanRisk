from  Application.Services.UDP.Parse_NSEFO.F7200 import process



def getOutput(self,Decoded_Packet):

    Start_Pointof_Record = 48

    output = process.process(self, Decoded_Packet, Start_Pointof_Record)
    print(output)
    self.sender.sendData(output)
