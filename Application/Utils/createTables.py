import traceback

import numpy as np

from PyQt5.QtCore import QSortFilterProxyModel,Qt
from Application.Views.Models import modelPOCW,modelBWM,modelCWM, modelCWSWM,modelGWM,modelTWM,modelTWSWM,modelPOTW,modelSortfilter,modelCMPOCW,modelCMPOTW,modelCMTWM,modelCMCWM,modelBWSWM
from Application.Views.proxyModels import modelSortfilterCWSWM,modelSortfilterPOCW,modelSortfilterTWSWM,modelSortfilterPOTW
from Application.Views.Models import modelTmaster





def tables_details_POTW(POTW):
    try:
        POTW.heads = ['UserID',
                          'Exchange','Token','instrument','symbol','expiry',
                      'strike','c/p','dayQty','dayValue','LTP',
                          'MTM','SerialNO','OpenQty','OpenAmt','netQty',
                          'NetValue','PrevDExpo_Mrg','PrevDSpan_Mrg','Total_Margin','Net_Prem',
                        'FUT_MTM','OPT_MTM','PRM_MRG']

        #############################################################################################################


        POTW.visibleColumns = len(POTW.heads)
        POTW.table = np.zeros((20000, 24), dtype=object)
        POTW.model = modelPOTW.ModelTS(POTW.table, POTW.heads)
        POTW.smodel = modelSortfilterPOTW.ProxyModel()
        POTW.smodel.setSourceModel(POTW.model)
        POTW.tableView.setModel(POTW.smodel)

        POTW.smodel.setDynamicSortFilter(False)
        POTW.smodel.setFilterKeyColumn(0)
        POTW.smodel.setFilterCaseSensitivity(False)
        #############################################
        POTW.tableView.horizontalHeader().setSectionsMovable(True)
        POTW.tableView.verticalHeader().setSectionsMovable(True)
        POTW.tableView.verticalHeader().setFixedWidth(30)
        POTW.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        POTW.tableView.setDragDropMode(POTW.tableView.InternalMove)
        POTW.tableView.setDragDropOverwriteMode(False)

        # POTW.saveDefaultColumnProfile()
        # POTW.lastSavedColumnProfile()
        # POTW.updateDefaultColumnProfile()

        # POTW.tableView.setColumnWidth(0, 0)
        # POTW.tableView.setColumnWidth(1, 0)
        # POTW.tableView.setColumnWidth(2, 0)
        # POTW.tableView.setColumnWidth(4, 85)
        # POTW.tableView.setColumnWidth(5, 75)
        # POTW.tableView.setColumnWidth(6, 40)

        # POTW.tableView.horizontalHeader().moveSection(28, 0)
        # POTW.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # POTW.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # POTW.tableView.horizontalHeader().customContextMenuRequested.connect(POTW.headerRightClickMenu)


    except:
        print(traceback.print_exc())







def tables_details_TWM(TWM):
    try:
        TWM.heads = ['UserID',
                     'EXPO_Margin','SPAN_Margin','Total_Margin','FUT_MTM', 'OPT_MTM','Branch','Name','FNO_MTM','Day_MRG','Sheet','CASH_MTM','PRM_MRG','NET_MRG','PeakMRG']

        #############################################################################################################


        TWM.visibleColumns = len(TWM.heads)
        TWM.table = np.zeros((20000, 15), dtype=object)
        TWM.model = modelTWM.ModelTS(TWM.table, TWM.heads)
        TWM.smodel = QSortFilterProxyModel()
        TWM.smodel.setSourceModel(TWM.model)
        TWM.tableView.setModel(TWM.smodel)

        TWM.smodel.setDynamicSortFilter(False)
        TWM.smodel.setFilterKeyColumn(0)
        TWM.smodel.setFilterCaseSensitivity(False)
        #############################################
        TWM.tableView.horizontalHeader().setSectionsMovable(True)
        TWM.tableView.verticalHeader().setSectionsMovable(True)
        TWM.tableView.verticalHeader().setFixedWidth(30)
        TWM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        TWM.tableView.setDragDropMode(TWM.tableView.InternalMove)
        TWM.tableView.setDragDropOverwriteMode(False)

        # TWM.saveDefaultColumnProfile()
        # TWM.lastSavedColumnProfile()
        # TWM.updateDefaultColumnProfile()

        # TWM.tableView.setColumnWidth(0, 0)
        # TWM.tableView.setColumnWidth(1, 0)
        # TWM.tableView.setColumnWidth(2, 0)
        # TWM.tableView.setColumnWidth(4, 85)
        # TWM.tableView.setColumnWidth(5, 75)
        # TWM.tableView.setColumnWidth(6, 40)

        # TWM.tableView.horizontalHeader().moveSection(28, 0)
        # TWM.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # TWM.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # TWM.tableView.horizontalHeader().customContextMenuRequested.connect(TWM.headerRightClickMenu)


    except:
        print(traceback.print_exc())



def tables_details_TWSWM(TWSWM):
    try:
        TWSWM.heads = ['UserID',
                        'Symbol','EXPO_Margin','SPAN_Margin','Total_Margin','FUT_MTM',
                       'OPT_MTM','FNO_MTM','PRM_MRG','Branch']

        #############################################################################################################


        TWSWM.visibleColumns = len(TWSWM.heads)
        TWSWM.table = np.zeros((10000, 10), dtype=object)
        TWSWM.model = modelTWSWM.ModelTS(TWSWM.table, TWSWM.heads)
        TWSWM.smodel = modelSortfilterTWSWM.ProxyModel()
        TWSWM.smodel.setSourceModel(TWSWM.model)
        TWSWM.tableView.setModel(TWSWM.smodel)

        TWSWM.smodel.setDynamicSortFilter(False)
        TWSWM.smodel.setFilterKeyColumn(0)
        TWSWM.smodel.setFilterCaseSensitivity(False)
        #############################################
        TWSWM.tableView.horizontalHeader().setSectionsMovable(True)
        TWSWM.tableView.verticalHeader().setSectionsMovable(True)
        TWSWM.tableView.verticalHeader().setFixedWidth(30)
        TWSWM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        TWSWM.tableView.setDragDropMode(TWSWM.tableView.InternalMove)
        TWSWM.tableView.setDragDropOverwriteMode(False)

        # TWSWM.saveDefaultColumnProfile()
        # TWSWM.lastSavedColumnProfile()
        # TWSWM.updateDefaultColumnProfile()

        # TWSWM.tableView.setColumnWidth(0, 0)
        # TWSWM.tableView.setColumnWidth(1, 0)
        # TWSWM.tableView.setColumnWidth(2, 0)
        # TWSWM.tableView.setColumnWidth(4, 85)
        # TWSWM.tableView.setColumnWidth(5, 75)
        # TWSWM.tableView.setColumnWidth(6, 40)

        # TWSWM.tableView.horizontalHeader().moveSection(28, 0)
        # TWSWM.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # TWSWM.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # TWSWM.tableView.horizontalHeader().customContextMenuRequested.connect(TWSWM.headerRightClickMenu)

    except:
        print(traceback.print_exc())



def tables_details_BWSWM(BWSWM):
    try:
        BWSWM.heads = ['Branch',
                        'Symbol','EXPO_Margin','SPAN_Margin','Total_Margin','FUT_MTM',
                       'OPT_MTM','FNO_MTM','PRM_MRG','Margin%']

        #############################################################################################################


        BWSWM.visibleColumns = len(BWSWM.heads)
        BWSWM.table = np.zeros((10000, 10), dtype=object)
        BWSWM.model = modelBWSWM.ModelTS(BWSWM.table, BWSWM.heads)
        BWSWM.smodel = QSortFilterProxyModel()
        BWSWM.smodel.setSourceModel(BWSWM.model)
        BWSWM.tableView.setModel(BWSWM.smodel)

        BWSWM.smodel.setDynamicSortFilter(False)
        BWSWM.smodel.setFilterKeyColumn(0)
        BWSWM.smodel.setFilterCaseSensitivity(False)
        #############################################
        BWSWM.tableView.horizontalHeader().setSectionsMovable(True)
        BWSWM.tableView.verticalHeader().setSectionsMovable(True)
        BWSWM.tableView.verticalHeader().setFixedWidth(30)
        BWSWM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        BWSWM.tableView.setDragDropMode(BWSWM.tableView.InternalMove)
        BWSWM.tableView.setDragDropOverwriteMode(False)

        # BWSWM.saveDefaultColumnProfile()
        # BWSWM.lastSavedColumnProfile()
        # BWSWM.updateDefaultColumnProfile()

        # BWSWM.tableView.setColumnWidth(0, 0)
        # BWSWM.tableView.setColumnWidth(1, 0)
        # BWSWM.tableView.setColumnWidth(2, 0)
        # BWSWM.tableView.setColumnWidth(4, 85)
        # BWSWM.tableView.setColumnWidth(5, 75)
        # BWSWM.tableView.setColumnWidth(6, 40)

        # BWSWM.tableView.horizontalHeader().moveSection(28, 0)
        # BWSWM.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # BWSWM.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # BWSWM.tableView.horizontalHeader().customContextMenuRequested.connect(BWSWM.headerRightClickMenu)

    except:
        print(traceback.print_exc())



def tables_details_CWM(CWM):
    try:
        CWM.heads = ['ClientCode',
                     'EXPO_Margin','SPAN_Margin','Total_Margin','FUT_MTM', 'OPT_MTM','FNO_MTM','Day_MRG','PRM_MRG','NET_MRG','PhisicalM']

        #############################################################################################################


        CWM.visibleColumns = len(CWM.heads)
        CWM.table = np.zeros((20000, 11), dtype=object)
        CWM.model = modelCWM.ModelTS(CWM.table, CWM.heads)
        CWM.smodel = QSortFilterProxyModel()
        CWM.smodel.setSourceModel(CWM.model)
        CWM.tableView.setModel(CWM.smodel)

        CWM.smodel.setDynamicSortFilter(False)
        CWM.smodel.setFilterKeyColumn(0)
        CWM.smodel.setFilterCaseSensitivity(False)
        #############################################
        CWM.tableView.horizontalHeader().setSectionsMovable(True)
        CWM.tableView.verticalHeader().setSectionsMovable(True)
        CWM.tableView.verticalHeader().setFixedWidth(30)
        CWM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        CWM.tableView.setDragDropMode(CWM.tableView.InternalMove)
        CWM.tableView.setDragDropOverwriteMode(False)

        # CWM.saveDefaultColumnProfile()
        # CWM.lastSavedColumnProfile()
        # CWM.updateDefaultColumnProfile()

        # CWM.tableView.setColumnWidth(0, 0)
        # CWM.tableView.setColumnWidth(1, 0)
        # CWM.tableView.setColumnWidth(2, 0)
        # CWM.tableView.setColumnWidth(4, 85)
        # CWM.tableView.setColumnWidth(5, 75)
        # CWM.tableView.setColumnWidth(6, 40)

        # CWM.tableView.horizontalHeader().moveSection(28, 0)
        # CWM.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # CWM.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # CWM.tableView.horizontalHeader().customContextMenuRequested.connect(CWM.headerRightClickMenu)


    except:
        print(traceback.print_exc())


def tables_details_CWSWM(CWSWM):
    try:
        CWSWM.heads = ['ClientCode',
                        'Symbol','EXPO_Margin','SPAN_Margin','Total_Margin','FUT_MTM',
                       'OPT_MTM','FNO_MTM','PRM_MRG']

        #############################################################################################################


        CWSWM.visibleColumns = len(CWSWM.heads)
        CWSWM.table = np.zeros((20000, 9), dtype=object)

        CWSWM.table_copy = np.zeros((20000, 7), dtype=object)

        CWSWM.model = modelCWSWM.ModelTS(CWSWM.table, CWSWM.heads)
        CWSWM.smodel = modelSortfilterCWSWM.ProxyModel()
        CWSWM.smodel.setSourceModel(CWSWM.model)

        CWSWM.smodel.setDynamicSortFilter(False)
        CWSWM.smodel.setFilterKeyColumn(0)
        CWSWM.smodel.setFilterCaseSensitivity(False)
        #############################################
        CWSWM.tableView.setModel(CWSWM.smodel)
        CWSWM.tableView.horizontalHeader().setSectionsMovable(True)
        CWSWM.tableView.verticalHeader().setSectionsMovable(True)
        CWSWM.tableView.verticalHeader().setFixedWidth(30)
        CWSWM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        CWSWM.tableView.setDragDropMode(CWSWM.tableView.InternalMove)
        CWSWM.tableView.setDragDropOverwriteMode(False)

        # CWSWM.saveDefaultColumnProfile()
        # CWSWM.lastSavedColumnProfile()
        # CWSWM.updateDefaultColumnProfile()

        # CWSWM.tableView.setColumnWidth(0, 0)
        # CWSWM.tableView.setColumnWidth(1, 0)
        # CWSWM.tableView.setColumnWidth(2, 0)
        # CWSWM.tableView.setColumnWidth(4, 85)
        # CWSWM.tableView.setColumnWidth(5, 75)
        # CWSWM.tableView.setColumnWidth(6, 40)

        # CWSWM.tableView.horizontalHeader().moveSection(28, 0)
        # CWSWM.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # CWSWM.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # CWSWM.tableView.horizontalHeader().customContextMenuRequested.connect(CWSWM.headerRightClickMenu)


    except:
        print(traceback.print_exc())





def tables_details_POCW(POCW):
    try:
        POCW.heads = ['ClientCode',
                          'Exchange','Token','instrument','symbol','expiry',
                      'strike','c/p','dayQty','dayValue','LTP',
                          'MTM','SerialNO','OpenQty','OpenAmt','netQty',
                          'NetValue','FUT_MTM','OPT_MTM','NET_PREM','Prem_Margin']

        #############################################################################################################


        POCW.visibleColumns = len(POCW.heads)
        POCW.table = np.zeros((20000, 21), dtype=object)

        POCW.model = modelPOCW.ModelTS(POCW.table, POCW.heads)
        # POCW.smodel = QSortFilterProxyModel()
        POCW.smodel = modelSortfilterPOCW.ProxyModel()
        POCW.smodel.setSourceModel(POCW.model)
        POCW.tableView.setModel(POCW.smodel)

        POCW.smodel.setDynamicSortFilter(False)
        POCW.smodel.setFilterKeyColumn(0)
        POCW.smodel.setFilterCaseSensitivity(False)
        #############################################
        POCW.tableView.horizontalHeader().setSectionsMovable(True)
        POCW.tableView.verticalHeader().setSectionsMovable(True)
        POCW.tableView.verticalHeader().setFixedWidth(30)
        POCW.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        POCW.tableView.setDragDropMode(POCW.tableView.InternalMove)
        POCW.tableView.setDragDropOverwriteMode(False)

        # POCW.saveDefaultColumnProfile()
        # POCW.lastSavedColumnProfile()
        # POCW.updateDefaultColumnProfile()

        # POCW.tableView.setColumnWidth(0, 0)
        # POCW.tableView.setColumnWidth(1, 0)
        # POCW.tableView.setColumnWidth(2, 0)
        # POCW.tableView.setColumnWidth(4, 85)
        # POCW.tableView.setColumnWidth(5, 75)
        # POCW.tableView.setColumnWidth(6, 40)

        # POCW.tableView.horizontalHeader().moveSection(28, 0)
        # POCW.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # POCW.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # POCW.tableView.horizontalHeader().customContextMenuRequested.connect(POCW.headerRightClickMenu)


    except:
        print(traceback.print_exc())




def tables_details_GlobalM(GlobalM):
    try:
        GlobalM.heads = ['PARTICULARS',
                          'AMOUNT',
                     ]

        #############################################################################################################


        GlobalM.visibleColumns = len(GlobalM.heads)
        GlobalM.table = np.zeros((7, 2), dtype=object)
        GlobalM.model = modelGWM.ModelTS(GlobalM.table, GlobalM.heads)
        GlobalM.smodel = QSortFilterProxyModel()
        GlobalM.smodel.setSourceModel(GlobalM.model)
        GlobalM.tableView.setModel(GlobalM.smodel)

        GlobalM.smodel.setDynamicSortFilter(False)
        GlobalM.smodel.setFilterKeyColumn(0)
        GlobalM.smodel.setFilterCaseSensitivity(False)
        #############################################
        GlobalM.tableView.horizontalHeader().setSectionsMovable(True)
        GlobalM.tableView.verticalHeader().setSectionsMovable(True)
        GlobalM.tableView.verticalHeader().setFixedWidth(30)
        GlobalM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        GlobalM.tableView.setDragDropMode(GlobalM.tableView.InternalMove)
        GlobalM.tableView.setDragDropOverwriteMode(False)

        # GlobalM.saveDefaultColumnProfile()
        # GlobalM.lastSavedColumnProfile()
        # GlobalM.updateDefaultColumnProfile()

        # GlobalM.tableView.setColumnWidth(0, 0)
        # GlobalM.tableView.setColumnWidth(1, 0)
        # GlobalM.tableView.setColumnWidth(2, 0)
        # GlobalM.tableView.setColumnWidth(4, 85)
        # GlobalM.tableView.setColumnWidth(5, 75)
        # GlobalM.tableView.setColumnWidth(6, 40)

        # GlobalM.tableView.horizontalHeader().moveSection(28, 0)
        # GlobalM.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # GlobalM.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # GlobalM.tableView.horizontalHeader().customContextMenuRequested.connect(GlobalM.headerRightClickMenu)


    except:
        print(traceback.print_exc())


def tables_details_BWM(BWM):
    try:
        BWM.heads = ['Branch',
                    'EXPO_Margin','SPAN_Margin','Total_Margin','FUT_MTM', 'OPT_MTM','FNO_MTM','PRM_MRG','Sheet','PeakMRG'
                     ]

        #############################################################################################################


        BWM.visibleColumns = len(BWM.heads)
        BWM.table = np.zeros((10000, 10), dtype=object)
        BWM.model = modelBWM.ModelTS(BWM.table, BWM.heads)
        BWM.smodel = QSortFilterProxyModel()
        BWM.smodel.setSourceModel(BWM.model)
        BWM.tableView.setModel(BWM.smodel)

        BWM.smodel.setDynamicSortFilter(False)
        BWM.smodel.setFilterKeyColumn(0)
        BWM.smodel.setFilterCaseSensitivity(False)
        #############################################
        BWM.tableView.horizontalHeader().setSectionsMovable(True)
        BWM.tableView.verticalHeader().setSectionsMovable(True)
        BWM.tableView.verticalHeader().setFixedWidth(30)
        BWM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        BWM.tableView.setDragDropMode(BWM.tableView.InternalMove)
        BWM.tableView.setDragDropOverwriteMode(False)

        # BWM.saveDefaultColumnProfile()
        # BWM.lastSavedColumnProfile()
        # BWM.updateDefaultColumnProfile()

        # BWM.tableView.setColumnWidth(0, 0)
        # BWM.tableView.setColumnWidth(1, 0)
        # BWM.tableView.setColumnWidth(2, 0)
        # BWM.tableView.setColumnWidth(4, 85)
        # BWM.tableView.setColumnWidth(5, 75)
        # BWM.tableView.setColumnWidth(6, 40)

        # BWM.tableView.horizontalHeader().moveSection(28, 0)
        # BWM.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # BWM.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # BWM.tableView.horizontalHeader().customContextMenuRequested.connect(BWM.headerRightClickMenu)


    except:
        print(traceback.print_exc())


def tables_details_Tmaster(TM):
    try:
        TM.heads = ['TerminalID',
                          'UserID','Name','Branch','GRP','active']

        #############################################################################################################


        TM.visibleColumns = len(TM.heads)
        TM.table = np.zeros((20000, 6), dtype=object)

        TM.model = modelTmaster.ModelTS(TM.table, TM.heads)
        # TM.smodel = QSortFilterProxyModel()
        TM.smodel = QSortFilterProxyModel()
        TM.smodel.setSourceModel(TM.model)
        TM.tableView.setModel(TM.smodel)

        TM.smodel.setDynamicSortFilter(False)
        TM.smodel.setFilterKeyColumn(0)
        TM.smodel.setFilterCaseSensitivity(False)
        #############################################
        TM.tableView.horizontalHeader().setSectionsMovable(True)
        TM.tableView.verticalHeader().setSectionsMovable(True)
        TM.tableView.verticalHeader().setFixedWidth(30)
        TM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        TM.tableView.setDragDropMode(TM.tableView.InternalMove)
        TM.tableView.setDragDropOverwriteMode(False)

        # TM.saveDefaultColumnProfile()
        # TM.lastSavedColumnProfile()
        # TM.updateDefaultColumnProfile()

        # TM.tableView.setColumnWidth(0, 0)
        # TM.tableView.setColumnWidth(1, 0)
        # TM.tableView.setColumnWidth(2, 0)
        # TM.tableView.setColumnWidth(4, 85)
        # TM.tableView.setColumnWidth(5, 75)
        # TM.tableView.setColumnWidth(6, 40)

        # TM.tableView.horizontalHeader().moveSection(28, 0)
        # TM.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # TM.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # TM.tableView.horizontalHeader().customContextMenuRequested.connect(TM.headerRightClickMenu)


    except:
        print(traceback.print_exc())

def tables_details_Cmaster(CM):
    try:
        CM.heads = ['ClientID',
                          'Name','Branch','EPS','ITR','BM',
                            'GRP','Active']

        #############################################################################################################


        CM.visibleColumns = len(CM.heads)
        CM.table = np.zeros((20000, 8), dtype=object)

        CM.model = modelTmaster.ModelTS(CM.table, CM.heads)
        # CM.smodel = QSortFilterProxyModel()
        CM.smodel = QSortFilterProxyModel()
        CM.smodel.setSourceModel(CM.model)
        CM.tableView.setModel(CM.smodel)

        CM.smodel.setDynamicSortFilter(False)
        CM.smodel.setFilterKeyColumn(0)
        CM.smodel.setFilterCaseSensitivity(False)
        #############################################
        CM.tableView.horizontalHeader().setSectionsMovable(True)
        CM.tableView.verticalHeader().setSectionsMovable(True)
        CM.tableView.verticalHeader().setFixedWidth(30)
        CM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        CM.tableView.setDragDropMode(CM.tableView.InternalMove)
        CM.tableView.setDragDropOverwriteMode(False)

        # CM.saveDefaultColumnProfile()
        # CM.lastSavedColumnProfile()
        # CM.updateDefaultColumnProfile()

        # CM.tableView.setColumnWidth(0, 0)
        # CM.tableView.setColumnWidth(1, 0)
        # CM.tableView.setColumnWidth(2, 0)
        # CM.tableView.setColumnWidth(4, 85)
        # CM.tableView.setColumnWidth(5, 75)
        # CM.tableView.setColumnWidth(6, 40)

        # CM.tableView.horizontalHeader().moveSection(28, 0)
        # CM.tableView.horizontalHeader().setContexCMenuPolicy(Qt.CustomContexCMenu)
        # CM.tableView.customContexCMenuRequested.connect(lambda:tableRightClickMenu)
        # CM.tableView.horizontalHeader().customContexCMenuRequested.connect(CM.headerRightClickMenu)


    except:
        print(traceback.print_exc())


def tables_details_CMPOTW(CMPOTW):
    try:
        CMPOTW.heads = ['UserID',
                          'Exchange','Token','Series','symbol','dayQty',
                      'dayValue','LTP','MTM','SerialNO','OpenQty',
                      'OpenAmt','netQty','NetValue','MRG']

        #############################################################################################################


        CMPOTW.visibleColumns = len(CMPOTW.heads)
        CMPOTW.table = np.zeros((20000, 15), dtype=object)
        CMPOTW.model = modelCMPOTW.ModelTS(CMPOTW.table, CMPOTW.heads)
        CMPOTW.smodel = QSortFilterProxyModel()
        CMPOTW.smodel.setSourceModel(CMPOTW.model)
        CMPOTW.tableView.setModel(CMPOTW.smodel)

        CMPOTW.smodel.setDynamicSortFilter(False)
        CMPOTW.smodel.setFilterKeyColumn(0)
        CMPOTW.smodel.setFilterCaseSensitivity(False)
        #############################################
        CMPOTW.tableView.horizontalHeader().setSectionsMovable(True)
        CMPOTW.tableView.verticalHeader().setSectionsMovable(True)
        CMPOTW.tableView.verticalHeader().setFixedWidth(30)
        CMPOTW.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        CMPOTW.tableView.setDragDropMode(CMPOTW.tableView.InternalMove)
        CMPOTW.tableView.setDragDropOverwriteMode(False)

        # CMPOTW.saveDefaultColumnProfile()
        # CMPOTW.lastSavedColumnProfile()
        # CMPOTW.updateDefaultColumnProfile()

        # CMPOTW.tableView.setColumnWidth(0, 0)
        # CMPOTW.tableView.setColumnWidth(1, 0)
        # CMPOTW.tableView.setColumnWidth(2, 0)
        # CMPOTW.tableView.setColumnWidth(4, 85)
        # CMPOTW.tableView.setColumnWidth(5, 75)
        # CMPOTW.tableView.setColumnWidth(6, 40)

        # CMPOTW.tableView.horizontalHeader().moveSection(28, 0)
        # CMPOTW.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # CMPOTW.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # CMPOTW.tableView.horizontalHeader().customContextMenuRequested.connect(CMPOTW.headerRightClickMenu)


    except:
        print(traceback.print_exc())

def tables_details_CMPOCW(CMPOCW):
    try:
        CMPOCW.heads = ['ClientID',
                          'Exchange','Token','Series','symbol','dayQty',
                      'dayValue','LTP','MTM','SerialNO','OpenQty',
                      'OpenAmt','netQty','NetValue','MRG']

        #############################################################################################################


        CMPOCW.visibleColumns = len(CMPOCW.heads)
        CMPOCW.table = np.zeros((20000, 15), dtype=object)
        CMPOCW.model = modelCMPOCW.ModelTS(CMPOCW.table, CMPOCW.heads)
        CMPOCW.smodel = QSortFilterProxyModel()
        CMPOCW.smodel.setSourceModel(CMPOCW.model)
        CMPOCW.tableView.setModel(CMPOCW.smodel)

        CMPOCW.smodel.setDynamicSortFilter(False)
        CMPOCW.smodel.setFilterKeyColumn(0)
        CMPOCW.smodel.setFilterCaseSensitivity(False)
        #############################################
        CMPOCW.tableView.horizontalHeader().setSectionsMovable(True)
        CMPOCW.tableView.verticalHeader().setSectionsMovable(True)
        CMPOCW.tableView.verticalHeader().setFixedWidth(30)
        CMPOCW.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        CMPOCW.tableView.setDragDropMode(CMPOCW.tableView.InternalMove)
        CMPOCW.tableView.setDragDropOverwriteMode(False)

        # CMPOCW.saveDefaultColumnProfile()
        # CMPOCW.lastSavedColumnProfile()
        # CMPOCW.updateDefaultColumnProfile()

        # CMPOCW.tableView.setColumnWidth(0, 0)
        # CMPOCW.tableView.setColumnWidth(1, 0)
        # CMPOCW.tableView.setColumnWidth(2, 0)
        # CMPOCW.tableView.setColumnWidth(4, 85)
        # CMPOCW.tableView.setColumnWidth(5, 75)
        # CMPOCW.tableView.setColumnWidth(6, 40)

        # CMPOCW.tableView.horizontalHeader().moveSection(28, 0)
        # CMPOCW.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # CMPOCW.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # CMPOCW.tableView.horizontalHeader().customContextMenuRequested.connect(CMPOCW.headerRightClickMenu)


    except:
        print(traceback.print_exc())


def tables_details_CMCWM(CMCWM):
    try:
        CMCWM.heads = ['ClientID',
                        'MARGIN','MTM']

        #############################################################################################################


        CMCWM.visibleColumns = len(CMCWM.heads)
        CMCWM.table = np.zeros((20000, 3), dtype=object)
        CMCWM.model = modelCMCWM.ModelTS(CMCWM.table, CMCWM.heads)
        CMCWM.smodel = QSortFilterProxyModel()
        CMCWM.smodel.setSourceModel(CMCWM.model)
        CMCWM.tableView.setModel(CMCWM.smodel)

        CMCWM.smodel.setDynamicSortFilter(False)
        CMCWM.smodel.setFilterKeyColumn(0)
        CMCWM.smodel.setFilterCaseSensitivity(False)
        #############################################
        CMCWM.tableView.horizontalHeader().setSectionsMovable(True)
        CMCWM.tableView.verticalHeader().setSectionsMovable(True)
        CMCWM.tableView.verticalHeader().setFixedWidth(30)
        CMCWM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        CMCWM.tableView.setDragDropMode(CMCWM.tableView.InternalMove)
        CMCWM.tableView.setDragDropOverwriteMode(False)

        # CMCWM.saveDefaultColumnProfile()
        # CMCWM.lastSavedColumnProfile()
        # CMCWM.updateDefaultColumnProfile()

        # CMCWM.tableView.setColumnWidth(0, 0)
        # CMCWM.tableView.setColumnWidth(1, 0)
        # CMCWM.tableView.setColumnWidth(2, 0)
        # CMCWM.tableView.setColumnWidth(4, 85)
        # CMCWM.tableView.setColumnWidth(5, 75)
        # CMCWM.tableView.setColumnWidth(6, 40)

        # CMCWM.tableView.horizontalHeader().moveSection(28, 0)
        # CMCWM.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # CMCWM.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # CMCWM.tableView.horizontalHeader().customContextMenuRequested.connect(CMCWM.headerRightClickMenu)


    except:
        print(traceback.print_exc())

def tables_details_CMTWM(CMTWM):
    try:
        CMTWM.heads = ['UserID',
                     'Branch','Name','MARGIN','MTM','Sheet']

        #############################################################################################################


        CMTWM.visibleColumns = len(CMTWM.heads)
        CMTWM.table = np.zeros((20000, 6), dtype=object)
        CMTWM.model = modelCMTWM.ModelTS(CMTWM.table, CMTWM.heads)
        CMTWM.smodel = QSortFilterProxyModel()
        CMTWM.smodel.setSourceModel(CMTWM.model)
        CMTWM.tableView.setModel(CMTWM.smodel)

        CMTWM.smodel.setDynamicSortFilter(False)
        CMTWM.smodel.setFilterKeyColumn(0)
        CMTWM.smodel.setFilterCaseSensitivity(False)
        #############################################
        CMTWM.tableView.horizontalHeader().setSectionsMovable(True)
        CMTWM.tableView.verticalHeader().setSectionsMovable(True)
        CMTWM.tableView.verticalHeader().setFixedWidth(30)
        CMTWM.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        CMTWM.tableView.setDragDropMode(CMTWM.tableView.InternalMove)
        CMTWM.tableView.setDragDropOverwriteMode(False)

        # CMTWM.saveDefaultColumnProfile()
        # CMTWM.lastSavedColumnProfile()
        # CMTWM.updateDefaultColumnProfile()

        # CMTWM.tableView.setColumnWidth(0, 0)
        # CMTWM.tableView.setColumnWidth(1, 0)
        # CMTWM.tableView.setColumnWidth(2, 0)
        # CMTWM.tableView.setColumnWidth(4, 85)
        # CMTWM.tableView.setColumnWidth(5, 75)
        # CMTWM.tableView.setColumnWidth(6, 40)

        # CMTWM.tableView.horizontalHeader().moveSection(28, 0)
        # CMTWM.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # CMTWM.tableView.customContextMenuRequested.connect(lambda:tableRightClickMenu)
        # CMTWM.tableView.horizontalHeader().customContextMenuRequested.connect(CMTWM.headerRightClickMenu)


    except:
        print(traceback.print_exc())