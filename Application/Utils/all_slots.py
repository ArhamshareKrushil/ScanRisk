

import traceback
from Application.Utils.supMethods import proceed2login
from Application.Utils.getSpanFile import latest_span,process_span
from Application.Utils.VAR.getVarFile import latest_var,process_var


def createSlots_main(main, tray=None):
    try:
        #BOD  window
        main.login.pblogSignIn.clicked.connect(lambda : proceed2login(main))


        # main.GlobalM.pbApply.clicked.connect(main.setLimit)
    except:
        print(traceback.print_exc())