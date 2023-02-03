import struct
import time
import lzo
import Application.Services.UDP.Parse_NSEFO.F7202.parse7202 as Fparse7202
import Application.Services.UDP. Parse_NSEFO.F6013.parse6013 as Fparse6013
import Application.Services.UDP. Parse_NSEFO.F6501.parse6501 as Fparse6501
import Application.Services.UDP. Parse_NSEFO.F6511.parse6511 as Fparse6511
import Application.Services.UDP. Parse_NSEFO.F7130.parse7130 as Fparse7130
import Application.Services.UDP. Parse_NSEFO.F7200.parse7200 as Fparse7200
import Application.Services.UDP. Parse_NSEFO.F7201.parse7201 as Fparse7201
import Application.Services.UDP. Parse_NSEFO.F7208.parse7208 as Fparse7208
import Application.Services.UDP. Parse_NSEFO.F7211.parse7211 as Fparse7211
import Application.Services.UDP. Parse_NSEFO.F7220.parse7220 as Fparse7220
import Application.Services.UDP. Parse_NSEFO.F7305.parse7305 as Fparse7305
import Application.Services.UDP. Parse_NSEFO.F7340.parse7340 as Fparse7340


import Application.Services.UDP. Parse_NSECM.CM6501.parse6501 as CMparse6501
import Application.Services.UDP. Parse_NSECM.CM6582.parse6582 as CMparse6582
import Application.Services.UDP. Parse_NSECM.CM7200.parse7200 as CMparse7200
import Application.Services.UDP. Parse_NSECM.CM7202.parse7202 as CMparse7202
import Application.Services.UDP. Parse_NSECM.CM7207.parse7207 as CMparse7207
import Application.Services.UDP. Parse_NSECM.CM7208.parse7208 as CMparse7208
import Application.Services.UDP. Parse_NSECM.CM7214.parse7214 as CMparse7214
import Application.Services.UDP. Parse_NSECM.CM7216.parse7216 as CMparse7216
import Application.Services.UDP. Parse_NSECM.CM7201.parse7201 as CMparse7201
from Application.Utils.configReader import readConfig_All

from Application.Utils.configReader import get_udp_port


def parseFeeds(self, packet, port):
    # print(packet)
    start_Point = 4  # start point of packet
    NoOf_Pckt = struct.unpack('!h', packet[2:4])[0]

    for i in range(NoOf_Pckt):
        Compressed_PcktLen = struct.unpack('!h', packet[start_Point: (start_Point + 2)])[0]
        endPoint = start_Point + 2 + Compressed_PcktLen

        # Uncompressed Packets
        if (Compressed_PcktLen == 0):
            pass



            # Compressed_Packet = packet[start_Point + 2:]
            #
            # Msg_Code = struct.unpack('!h', Compressed_Packet[18:20])
            #
            # if (Msg_Code[0] not in self.listMsgCode):
            #     self.listMsgCode.append(Msg_Code[0])
            #     print(Msg_Code[0], self.listMsgCode)
            #
            # if (port == self.port_fo):

            #     if (Msg_Code[0] == 6501):
            #         Fparse6501.getOutput(self, Compressed_Packet)
            #     elif (Msg_Code[0] == 7340):
            #         Fparse7340.getOutput(self, Compressed_Packet)
            #     elif (Msg_Code[0] == 7305):
            #         Fparse7305.getOutput(self, Compressed_Packet)
            #     if (Msg_Code[0] == 7130):
            #         Fparse7130.getOutput(self, Compressed_Packet)
            #     elif (Msg_Code[0] == 6013):
            #         Fparse6013.getOutput(self, Compressed_Packet)
            #     elif (Msg_Code[0] == 6511):
            #         Fparse6511.getOutput(self, Compressed_Packet)
            #
            #
            # elif (port == self.port_cash):
            #     if (Msg_Code[0] == 7207):
            #         CMparse7207.getOutput(self, Compressed_Packet)
            #     elif (Msg_Code[0] == 7216):
            #         CMparse7216.getOutput(self, Compressed_Packet)
            #     elif (Msg_Code[0] == 6582):
            #         CMparse6582.getOutput(self, Compressed_Packet)
            #     elif (Msg_Code[0] == 6501):
            #         CMparse6501.getOutput(self, Compressed_Packet)


        #Compressed Packets
        else:
            # print(port)


            Compressed_Packet = packet[start_Point + 2: start_Point + Compressed_PcktLen + 2]
            Decoded_Packet = lzo.lzo1z.decompress_safe(Compressed_Packet, 1000)

            Msg_Code = struct.unpack('!h', Decoded_Packet[18:20])

            # if (Msg_Code[0] not in self.listMsgCode):
            #     self.listMsgCode.append(Msg_Code[0])
            #     print(Msg_Code[0], self.listMsgCode)

            if (port == self.port_fo):



                # if (Msg_Code[0] == 7202):
                #
                #     if(self.counter1 <10):
        #         #         print('self.counter1',self.counter1)
        #         #
        #         #         self.counter1 += 1
        #         #         print('self.counter1',self.counter1)
        #         #
        #         #         ####################################
        #         #         st1=time.time()
        #         #         Fparse7202.getOutput(self, Decoded_Packet,'python')
        #         #         et1 = time.time()
        #         #         print('python',st1-et1)
        #         #         ####################################
        #         #
        #         #         ####################################
        #         #         st2=time.time()
        #         #         Fparse7202.getOutput(self, Decoded_Packet,'cython')
        #         #         et2 = time.time()
        #         #         print('cython', st2 - et2)
        #
        #                 ####################################
        #
                if (Msg_Code[0] == 7202):
                  #  print("inside 7202")
                    Fparse7202.getOutput(self, Decoded_Packet,'cython')
                # elif (Msg_Code[0] == 7201):
                #     Fparse7201.getOutput(self, Decoded_Packet)
                elif (Msg_Code[0] == 7208):
                   # print("inside 7202")
                    Fparse7208.getOutput(self, Decoded_Packet)
        #         # elif (Msg_Code[0] == 7200):
        #         #     Fparse7200.getOutput(self, Decoded_Packet)
        #         # elif (Msg_Code[0] == 7211):
        #         #     Fparse7211.getOutput(self, Decoded_Packet)
        #         # elif (Msg_Code[0] == 7220):
        #         #     Fparse7220.getOutput(self, Decoded_Packet)
        #
            elif (port == self.port_cash):
                # print('hello')

                if (Msg_Code[0] == 7202):
                    CMparse7202.getOutput(self, Decoded_Packet)
                # elif (Msg_Code[0] == 7208):
                #     CMparse7208.getOutput(self, Decoded_Packet)
                # elif (Msg_Code[0] == 7200):
                #     CMparse7200.getOutput(self, Decoded_Packet)
                # elif (Msg_Code[0] == 7214):
                #     CMparse7214.getOutput(self, Decoded_Packet)
                # elif (Msg_Code[0] == 7201):
                #     CMparse7201.getOutput(self, Decoded_Packet)
