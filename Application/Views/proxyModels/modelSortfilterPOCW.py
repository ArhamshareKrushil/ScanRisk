from PyQt5.QtCore import *

class ProxyModel (QSortFilterProxyModel): #Custom Proxy Model
    def __init__(self):
        super(ProxyModel,self).__init__()
        self.cllientCode =''
        self.symbol=''

    def filterAcceptsRow(self, row, parent):
        # print('filter')
        if(self.cllientCode=='' and self.symbol==''):
            return True

        elif(self.symbol==''):
            if (self.sourceModel().index(row, 0, parent).data() == self.cllientCode):
                return True
            else:
                return False
        elif (self.cllientCode == ''):
            if (self.symbol.lower() in self.sourceModel().index(row, 4, parent).data().lower()):
                return True
            else:
                return False

        else:
            if(self.sourceModel().index(row, 0, parent).data() == self.cllientCode and self.symbol.lower() in self.sourceModel().index(row, 4, parent).data().lower()):
                # print(self.cllientCode,self.symbol)
                return True
            else:
                return False

    def setClientCode(self,code):
        self.cllientCode =code

    def setSymbol(self,symbol):
        self.symbol = symbol