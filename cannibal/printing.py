# -*- coding: utf-8; -*-
"""
Copyright (c) 2020 Felix Huber

printing.py: helper functions to send a PDF document to a (CUPS) printer

printing.py is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with printing.py. If not, see <http://www.gnu.org/licenses/>.

"""


import platform
import os
import tempfile

from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from pdfTools import PdfDoc

if platform.system() == 'Windows':
    realOS = False
else:
    realOS = True
    
def printPDF(printer, pdf, title):
    """
    print the pdf file using the lpr command
    """
    #print("prntr %s" % printer.printerName())
    #print("range %s" % printer.printRange())
    #print("from  %s" % printer.fromPage())
    #print("to    %s" % printer.toPage())
    #print("order %s" % printer.pageOrder())
    print("size  %s" % printer.paperSize())

    return

    if printer.printRange() == 2:
        # user selected page range
        startPage = printer.fromPage() - 1
        endPage = printer.toPage() - 1
    else:
        startPage = 0
        endPage = pdf.getPageCount() - 1

    if (printer.pageOrder() == 1):
        # backwards
        temp = startPage
        startPage = endPage
        endPage = temp
        step = -1
    else:
        step = +1
    
    tmpPdf = PdfDoc()
    tmpPdf.openPdf()
    # copy all pages in the right order
    for i in range(startPage, endPage+step, step):
        tmpPdf.insertDocument(pdf.getDoc(), fromPage=i, toPage=i)

    # create a temp file with the requested pages
    fd, tempName = tempfile.mkstemp(suffix=".pdf", prefix="cnb_")
    os.close(fd) # we don't need fd, is this dangerous?

    tmpPdf.savePdf(tempName)
    tmpPdf.closePdf()
    
    if realOS is True:
        printLpr(printer.printerName(), title, tempName)
    else:
        printWin(printer.printerName(), title, tempName)
    
    os.remove(tempName)

def printLpr(printer, title, fileName):
    """
    send a file to a printer using lpr
    """
    if realOS is True:
        printCmd = "lpr -P {} -J {} {}".format(
            printer, title, fileName) 
        os.system(printCmd)

def printWin(printer, title, fileName):
    """
    Try to send a file to a printer by manually
    copying chunks of data
    This is windows specific and really a unsupported
    dirty hack
    """
    if realOS is False:
        try:
            import win32print
            p = win32print.OpenPrinter(printer, {'DesiredAccess':win32print.PRINTER_ALL_ACCESS})
            #devmode = win32print.GetPrinter(p, 2)["pDevMode"]
            #devmode.PaperSize = 20
            ## 1 = portrait, 2 = landscape
            #devmode.Orientation = 1
            #win32print.SetPrinter(p, 2, devmode, 0)
            
            job = win32print.StartDocPrinter(p, 1, (title, None, "RAW"))
            win32print.StartPagePrinter(p)
            f = open(fileName, 'rb')
            while True:
                data = f.read(1024)  
                if not data:
                    break
                win32print.WritePrinter(p, data)
            f.close()
            win32print.EndPagePrinter(p)
            win32print.EndDocPrinter(p)
            win32print.ClosePrinter(p)
        except:
            # if anything fails just give up
            print("Error printing file")
            pass
