from  Application.Services.UDP.Parse_NSEFO.F7305 import process



def getOutput(self,Compressed_Packet):

    Start_Pointof_Record = 48

    output =process.process(self, Compressed_Packet, Start_Pointof_Record)
    self.sender.sendData(output)
    print(output)
