#!/usr/bin/env python3
# -*- coding: utf-8; -*-
"""
 script to convert .ui file to .py for pyqt
"""

import os
import subprocess


# taken from Dive into Python
def listDirectory(directory, fileExtList):                                         
    """get list of file info objects for files of particular extensions"""
    fileList = [os.path.normcase(f)
                for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]  
    fileList = [os.path.join(directory, f) 
               for f in fileList
                if os.path.splitext(f)[1] in fileExtList]                          
    return fileList  

def convertUi(root=os.curdir):
    """Convert all .ui files to .py"""
    fileList = listDirectory(root, [".ui"])
    for f in fileList:
        print(f)
        (name, extension) = os.path.splitext(f)
        subprocess.call(["pyuic5", f, "-o", "../cannibal/"+name+".py"])

convertUi(os.curdir)
os.chdir("../cannibal/i18n")
subprocess.call(["pylupdate5", "cannibal.pro"])
subprocess.call(["linguist-qt5", "cannibal_de.ts"])
