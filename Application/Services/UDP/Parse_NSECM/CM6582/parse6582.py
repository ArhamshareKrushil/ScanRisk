from Application.Services.UDP.Parse_NSECM.CM6582 import process


def getOutput(self,Compressed_Packet):
    Start_Pointof_Record = 48
    output = process.process(self, Compressed_Packet, Start_Pointof_Record)
    print(output)
