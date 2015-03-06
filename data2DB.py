import os
import numpy as np
import matplotlib.pylab as plt
import Tkinter, Tkconstants, tkFileDialog
# import dataReader as dr
import dataOps as dO


    

def openDirectory():
    
    tkObj=Tkinter.Tk()
    tkObj.file_opt = options = {}
    filesPath=tkFileDialog.askdirectory()
    allFiles=[]
    if filesPath:
        for root, dirs, files in os.walk(filesPath):
            for file in files:
                if file.endswith(".dat"):
                     allFiles.append(os.path.join(root, file))
                     temp=dO.alphaNumExtract(file)
                     print(temp,root)
                     
                     #Now here add the part where I take the file and
                     #input it to the database maybe I can have this database on the repository
                     #itself
    
    
    
if __name__=='__main__':
    openDirectory()
    