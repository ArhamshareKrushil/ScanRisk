from Application.Services.UDP.Parse_NSEFO.F6501 import process

def getOutput(self,Compressed_Packet):
    Start_Pointof_Record = 48

    output = process.process(self, Compressed_Packet, Start_Pointof_Record)
    print(output)
    self.sender.sendData(output)

