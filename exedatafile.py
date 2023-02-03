import os
import traceback

lisFinal = []



cwd = os.getcwd()

# cwd= ('D:\scanRisk')

a=os.listdir(cwd)
print(a)


for i in a :
    if(os.path.isdir(os.path.join(cwd,i))):
        newPath  = os.path.join(cwd,i)
        print('newPath',newPath)
        newList = os.listdir(newPath)
        for ij in newList:

            newPath1 = os.path.join(newPath, ij)

            if(ij == '__pycache__'):
                pass
            elif (os.path.isdir(newPath1)):
                newList1 = os.listdir(newPath1)
                for ix in newList1:
                    newPath2 = os.path.join(newPath1, ix)

                    if (ix == '__pycache__'):

                        pass

                    elif (os.path.isdir(newPath2)):
                        newList2 = os.listdir(newPath2)
                        for iz in newList2:
                            newPath3 = os.path.join(newPath2, iz)

                            if (iz == '__pycache__'):

                                pass

                            elif (os.path.isdir(newPath3)):
                                newList3 = os.listdir(newPath3)
                                for iy in newList3:
                                    newPath4 = os.path.join(newPath3, iy)

                                    if (iy == '__pycache__'):

                                        pass

                                    elif (os.path.isdir(newPath4)):
                                        newList4 = os.listdir(newPath4)
                                        for iw in newList4:
                                            newPath5 = os.path.join(newPath4, iw)

                                            if (iw == '__pycache__'):

                                                pass

                                            elif (os.path.isdir(newPath5)):
                                                newList5 = os.listdir(newPath5)
                                                for id in newList5:
                                                    newPath6 = os.path.join(newPath5, id)

                                                    if (id == '__pycache__'):

                                                        pass

                                                    elif (os.path.isdir(newPath6)):
                                                        newList6 = os.listdir(newPath6)
                                                        for ih in newList5:
                                                            print(ih)
                                                    else:

                                                        xx2 = newPath6.replace('D:\scanRisk\\', '').replace(r'\\',
                                                                                                            '/').replace(
                                                            '\\',
                                                            '/')
                                                        xx1 = xx2.replace('/' + id, '')
                                                        po = (xx2, xx1)
                                                        lisFinal.append(po)


                                            else:

                                                xx2 = newPath5.replace('D:\scanRisk\\', '').replace(r'\\', '/').replace(
                                                    '\\',
                                                    '/')
                                                xx1 = xx2.replace('/' + iw, '')
                                                po = (xx2, xx1)
                                                lisFinal.append(po)



                                    else:

                                        xx2 = newPath4.replace('D:\scanRisk\\', '').replace(r'\\', '/').replace('\\',
                                                                                                                '/')
                                        xx1 = xx2.replace('/' + iy, '')
                                        po = (xx2, xx1)
                                        lisFinal.append(po)



                            else:

                                xx2 = newPath3.replace('D:\scanRisk\\', '').replace(r'\\', '/').replace('\\', '/')
                                xx1 = xx2.replace('/' + iz, '')
                                po = (xx2, xx1)
                                lisFinal.append(po)

                    else:

                        xx2 = newPath2.replace('D:\scanRisk\\', '').replace(r'\\','/').replace('\\','/')
                        xx1 = xx2.replace('/'+ix, '')
                        po = (xx2,xx1)
                        lisFinal.append(po)
            else:
                xx2 = newPath1.replace('D:\scanRisk\\', '').replace(r'\\', '/').replace('\\', '/')
                xx1 = xx2.replace('/' + ij, '')
                po = (xx2, xx1)
                lisFinal.append(po)
    else:
        path1= os.path.join(cwd,i)
        xx2 = path1.replace('D:\scanRisk\\', '').replace(r'\\', '/').replace('\\', '/')
        xx1 = xx2.replace('/' + i, '')
        po = (xx2, xx1)
        lisFinal.append(po)

# print(lisFinal)

newls = []
for i in lisFinal:

    print(i[0][-3:])
    if('.py' == i[0][-3:]):
          pass
    else:
        newls.append(i)

print(newls)