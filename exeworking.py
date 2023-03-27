import os
import traceback

lisFinal = []



cwd = os.getcwd()

cwd= ('D:\scanRiskDesktop-Branch-V1.0.0')
a=os.listdir(cwd)

# print(a)

for i in a :
    if (i == '.git' or i == '.idea' or i == '.pytest_cache' or i == '.gitignore'):
        pass

    elif(os.path.isdir(i)):

        newPath = os.path.join(cwd, i)
        print('newPath', newPath)
        newList = os.listdir(newPath)

        for ij in newList:
            newPath1 = os.path.join(newPath, ij)

            if (ij == '__pycache__'):
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
                                        for id in newList4:
                                            newPath5 = os.path.join(newPath4, id)
                                            if (id == '__pycache__'):
                                                pass
                                            elif (os.path.isdir(newPath5)):
                                                newList5 = os.listdir(newPath5)
                                                for im in newList5:
                                                    newPath6 = os.path.join(newPath5, im)
                                                    if (im == '__pycache__'):
                                                        pass
                                                    elif (os.path.isdir(newPath6)):

                                                        newList6 = os.listdir(newPath6)
                                                        for iw in newList5:
                                                            newPath7 = os.path.join(newPath6, iw)
                                                            if (iw == '__pycache__'):
                                                                pass
                                                            elif (os.path.isdir(newPath7)):
                                                                pass
                                                            else:
                                                                xx2 = newPath7.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', '')
                                                                if (xx2[-3:] == '.py'):
                                                                    lisFinal.append(
                                                                        newPath7.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', ''))


                                                    else:
                                                        xx2 = newPath6.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', '')
                                                        if (xx2[-3:] == '.py'):
                                                            lisFinal.append(newPath6.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', ''))


                                            else:
                                                xx2 = newPath5.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', '')
                                                if (xx2[-3:] == '.py'):
                                                    lisFinal.append(newPath5.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', ''))


                                    else:
                                        xx2 = newPath4.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', '')
                                        if (xx2[-3:] == '.py'):
                                            lisFinal.append(newPath4.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', ''))
                            else:
                                xx2 = newPath3.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', '')
                                if (xx2[-3:] == '.py'):
                                    lisFinal.append(newPath3.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', ''))

                    else:
                        xx1 = newPath2.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', '')
                        if (xx1[-3:] == '.py'):
                            lisFinal.append(newPath2.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', ''))

            else:
                print('else 2', newPath1)
                xx = newPath1.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', '')
                # print(xx[-3:])
                if (xx[-3:] == '.py'):
                    lisFinal.append(newPath1.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', ''))


    else:
        xx = i.replace('D:\scanRiskDesktop-Branch-V1.0.0\\', '')
        # print(xx[-3:])
        if (xx[-3:] == '.py'):
            # print('tej',xx)
            lisFinal.append(xx)


print(len(lisFinal))
print(lisFinal)