with open(d, 'w') as sp:
    with open((a), 'rt') as f:
        c = csv.reader(f)
        for i, row in enumerate(c):
            if (i < 4):
                pass
            else:
                ada = str(row[1])
                if (ada.startswith('IO')):
                    it = 'OPTIDX'
                elif (ada.startswith('IF')):
                    it = 'FUTIDX'
                elif (ada.startswith('EO')):
                    it = 'OPTSTK'
                else:
                    it = 'FUTSTK'
                b = ada.split(' ', 5)
                if (it == 'OPTIDX' or it == 'OPTSTK'):
                    sym = b[2]
                    exp = datetime.datetime.strptime(b[3], '%d%b%y').strftime('%Y%m%d')
                    spr = format(float(b[4]), '.2f')
                    ot = b[1]
                else:
                    sym = b[1]
                    exp = datetime.datetime.strptime(b[2], '%d%b%y').strftime('%Y%m%d')
                    spr = ''
                    ot = ''
                # print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %((fn,row[0], it, sym, exp, spr, ot, ada, row[2], row[3], row[5], row[6], row[7])))
                sp.write("%s,,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ((
                    row[0], it, sym, exp, spr, ot, ada, row[2], row[3], row[4], row[5], row[6], row[7],
                    row[8])))

