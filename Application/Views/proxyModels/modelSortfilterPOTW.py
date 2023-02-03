from PyQt5.QtCore import *

class ProxyModel (QSortFilterProxyModel): #Custom Proxy Model
    def __init__(self):
        super(ProxyModel,self).__init__()
        self.cllientCode =''
        self.symbol=''
        self.token=''

    # def filterAcceptsRow(self, row, parent):
    #     # print('filter')
    #     if(self.cllientCode=='' and self.symbol==''):
    #         return True
    #
    #     elif(self.symbol==''):
    #         if (self.sourceModel().index(row, 0, parent).data() == self.cllientCode):
    #             return True
    #         else:
    #             return False
    #     elif (self.cllientCode == ''):
    #         if (self.symbol in self.sourceModel().index(row, 4, parent).data()):
    #             return True
    #         else:
    #             return False
    #
    #     else:
    #         if(self.sourceModel().index(row, 0, parent).data() == self.cllientCode and self.symbol in self.sourceModel().index(row, 4, parent).data()):
    #             # print(self.cllientCode,self.symbol)
    #             return True
    #         else:
    #             return False
    def filterAcceptsRow1(self, row, parent):
        # print('filter')


        if(self.cllientCode=='' and self.symbol=='' and self.token==''):
            return True


        elif (self.cllientCode == '' and self.symbol==''):
            if (self.sourceModel().index(row, 2, parent).data() == self.token):
                return True
            else:
                return False
        elif(self.cllientCode == '' and self.token==''):
            if (self.symbol in self.sourceModel().index(row, 4, parent).data()):
                return True
            else:
                return False

            # else:
            #     if (self.sourceModel().index(row, 2, parent).data() == self.token and self.symbol in self.sourceModel().index(row, 4, parent).data()):
            #         return True
            #     else:
            #         return False


        elif (self.symbol == ''):
            if (self.cllientCode == ''):
                if (self.sourceModel().index(row, 2, parent).data() == self.token):
                    return True
                else:
                    return False
            elif (self.token == ''):
                if (self.sourceModel().index(row, 0, parent).data() == self.cllientCode):
                    return True
                else:
                    return False
            else:
                if (self.sourceModel().index(row, 2, parent).data() == self.token and self.sourceModel().index(row, 0, parent).data() == self.cllientCode):
                    return True
                else:
                    return False

        elif (self.token == ''):
            if (self.cllientCode == ''):
                if (self.symbol in self.sourceModel().index(row, 4, parent).data()):
                    return True
                else:
                    return False
            elif (self.symbol == ''):
                if (self.sourceModel().index(row, 0, parent).data() == self.cllientCode):
                    return True
                else:
                    return False
            else:
                if (self.sourceModel().index(row, 0, parent).data() == self.cllientCode and self.symbol in self.sourceModel().index(row, 4, parent).data()):
                    return True
                else:
                    return False

        else:
            if(self.sourceModel().index(row, 0, parent).data() == self.cllientCode and self.symbol in self.sourceModel().index(row, 4, parent).data() and self.sourceModel().index(row, 2, parent).data() == self.token):
                # print(self.cllientCode,self.symbol)
                return True
            else:
                return False
    def filterAcceptsRow(self, row, parent):
        client = self.sourceModel().index(row, 0, parent).data()
        symbol = self.sourceModel().index(row, 4, parent).data()
        token = self.sourceModel().index(row, 2, parent).data()
        # print(type(client),type(symbol),type(token))
        if(self.token != ''):

            # print(self.token,token,type(self.token),type(token))

            if(int(self.token)==token):
                return True
            else:
                return False
        else:
            if(self.cllientCode=='' and self.symbol == ''):
                return True
            elif(self.symbol == '' and self.cllientCode==client):
                return True
            elif(self.symbol.lower() in symbol.lower() and self.cllientCode==''):
                return True
            elif(self.symbol.lower() in symbol.lower() and self.cllientCode==client):
                return True
            else:
                return False


    def setClientCode(self,code):
        self.cllientCode =code

    def setSymbol(self,symbol):
        self.symbol = symbol

    def setToken(self,token):
        self.token=token