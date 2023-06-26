from PyQt5.QtCore import *

class ProxyModel (QSortFilterProxyModel): #Custom Proxy Model
    def __init__(self):
        super(ProxyModel,self).__init__()
        self.cllientCode =''
        self.symbol=''
        self.Neg = False

    def filterAcceptsRow(self, row, parent):
        Qty = self.sourceModel().index(row, 15, parent).data()
        # print('filter')


        if(self.cllientCode=='' and self.symbol==''):
            if (self.Neg == True):
                if (int(Qty) < 0):
                    return True
                else:
                    return False

            return True

        elif(self.symbol==''):
            if (self.sourceModel().index(row, 0, parent).data() == self.cllientCode):
                if (self.Neg == True):
                    if (int(Qty) < 0):
                        return True
                    else:
                        return False
                return True
            else:
                return False
        elif (self.cllientCode == ''):
            if (self.symbol.lower() in self.sourceModel().index(row, 4, parent).data().lower()):
                if (self.Neg == True):
                    if (int(Qty) < 0):
                        return True
                    else:
                        return False
                return True
            else:
                return False

        else:
            if(self.sourceModel().index(row, 0, parent).data() == self.cllientCode and self.symbol.lower() in self.sourceModel().index(row, 4, parent).data().lower()):
                # print(self.cllientCode,self.symbol)
                if (self.Neg == True):
                    if (int(Qty) < 0):
                        return True
                    else:
                        return False
                return True
            else:
                return False

    def setClientCode(self,code):
        self.cllientCode =code

    def setSymbol(self,symbol):
        self.symbol = symbol