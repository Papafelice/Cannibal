#!/usr/bin/env python3
# -*- coding: utf-8; -*-
"""
Copyright (c) 2020 Felix Huber

This file is part of the digital signature tool for pdf files.

For the optional creation of QR codes, modules pyqrcode and pypng are needed

cannibal is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with cannibal. If not, see <http://www.gnu.org/licenses/>.

Part of this module was copied from
https://github.com/Rolf-Hempel/PlanetarySystemStacker
"""

__version__ = '0.36.7' 

import os
from sys import exit, argv, path
path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import platform

import fitz
from PyQt5 import QtGui
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, QTranslator, QLocale, qVersion, QSettings
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.QtWidgets import QMessageBox, QDialog, QLineEdit

from main_gui import Ui_MainWindow
from pdfTools import PdfDoc
from addObjects import InsertTextDlg, InsertImageDlg, InsertStampDlg, InsertFileDlg


class Cannibal(QMainWindow):
    """
    This is the main class of the "Cannibal" software. It implements the main GUI
    for the communication with the user. 
    """

    def __init__(self, parent=None, progPath=".", file=None):
        """
        Initialize the Cannibal environment.

        :param parent: None
        """

        # The (generated) QtGui class is contained in module main_gui.py.
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.progPath = progPath

        self.settings = QSettings('FxH', 'cannibal')        
        try:
            self.resize(self.settings.value('WindowSize'))
            self.move(self.settings.value('WindowPos'))
            if self.settings.value('WindowMax') == 'true':
                self.setWindowState(Qt.WindowMaximized)
        except:
            pass
        self.filePath = self.settings.value('LastPath', ".")

        icon = QtGui.QIcon(os.path.join(self.progPath, "icons", "sign.png"))
        self.ui.actionSign.setIcon(icon)
        self.ui.actionQuit.triggered.connect(self.closeEvent)
        self.ui.actionOpen.triggered.connect(self.openPdf)
        self.ui.actionSave.triggered.connect(self.savePdf)
        self.ui.actionSave_as.triggered.connect(self.savePdfAs)
        self.ui.actionClose.triggered.connect(self.closePdf)
        self.ui.actionDocument_Info.triggered.connect(self.documentInfo)
        self.ui.actionSign.triggered.connect(self.sign)
        self.ui.actionInsert_form.triggered.connect(self.insertForm)
        self.ui.actionInsert_text.triggered.connect(self.insertText)
        self.ui.actionInsert_image.triggered.connect(self.insertImage)
        self.ui.actionInsert_stamp.triggered.connect(self.insertStamp)
        self.ui.actionZoom_original.triggered.connect(self.zoomOriginal)
        self.ui.actionZoom_fit_best.triggered.connect(self.zoomFitBest)
        self.ui.actionZoom_in.triggered.connect(self.zoomIn)
        self.ui.actionZoom_out.triggered.connect(self.zoomOut)
        self.ui.actionRotate_left.triggered.connect(self.rotateLeft)
        self.ui.actionRotate_right.triggered.connect(self.rotateRight)
        self.ui.actionFirst_page.triggered.connect(self.firstPage)
        self.ui.actionPrevious_page.triggered.connect(self.prevPage)
        self.ui.actionNext_page.triggered.connect(self.nextPage)
        self.ui.actionLast_page.triggered.connect(self.lastPage)
        self.ui.actionDelete_page.triggered.connect(self.deletePage)
        self.ui.actionInsert_page.triggered.connect(self.insertPage)
        self.ui.actionAppend_page.triggered.connect(self.appendPage)
        self.ui.actionInsert_document.triggered.connect(self.insertDocument)
        self.ui.actionAbout.triggered.connect(self.aboutCannibal)
        
        self.currPage = QLineEdit()
        self.currPage.setMaxLength(4)
        self.currPage.setFixedWidth(60)
        onlyInt = QIntValidator()
        self.currPage.setValidator(onlyInt)
        self.currPage.returnPressed.connect(self.gotoPage)
        self.ui.toolBar.insertWidget(self.ui.actionNext_page, self.currPage)

        self.ui.thumbs.currentItemChanged.connect(self.thumbChange)
        self.ui.thumbs.verticalScrollBar().valueChanged.connect(self.fillPreview)
        self.ui.thumbs.scrollUp.connect(self.prevPage)
        self.ui.thumbs.scrollDown.connect(self.nextPage)
        
        self.guiElements = [self.ui.actionSave, self.ui.actionSave_as,
                            self.ui.actionPrint_setup, self.ui.actionPrint,
                            self.ui.actionClose, self.ui.actionDocument_Info,
                            self.ui.actionSign, self.ui.actionSign_invisibly,
                            self.ui.actionInsert_text, self.ui.actionInsert_image,
                            self.ui.actionInsert_stamp, self.ui.actionInsert_form,
                            self.ui.actionDelete_page, self.ui.actionInsert_page,
                            self.ui.actionAppend_page, self.ui.actionInsert_document,
                            self.ui.actionZoom_original, self.ui.actionZoom_fit_best,
                            self.ui.actionZoom_in, self.ui.actionZoom_out,
                            self.ui.actionRotate_left, self.ui.actionRotate_right,
                            self.ui.actionFirst_page, self.ui.actionPrevious_page,
                            self.currPage,
                            self.ui.actionNext_page, self.ui.actionLast_page,
                            self.ui.actionFind]

        # Deactivate all GUI elements that need an open file
        self.activateGuiElements(self.guiElements, False)
        
        self.showWidget(self.ui.tabs, show=False, pos=0)
        self.showWidget(self.ui.pdfView, show=False, pos=0)

        # pdf doc instance
        self.pdf = PdfDoc()

        # mouse handlers
        self.ui.pdfView.leftMouseRectReleased.connect(self.handleLeftRectRelease)
        self.ui.pdfView.leftMouseButtonReleased.connect(self.handleLeftButtonRelease)

        # Initialize variables
        self.mode = None
        self.fileName = None
        self.isOpen = False
        self.isDirty = False
        self.pageNum = 0
        self.pageCount = 0
        self.page = None
        
        if file is not None:
            self.openPdf(file)
        
    def activateGuiElements(self, elements, enable):
        """
        Enable / Disable selected GUI elements.

        :param elements: List of GUI elements.
        :param enable: If "True", enable the elements; otherwise disable them.
        :return: -
        """
        for element in elements:
            element.setEnabled(enable)

    def showWidget(self, widget, show=True, pos=0):
        """
        show or hide a widget in the central splitter location

        :param widget: widget object to be shown/hidden
        :param show: If "True", show, otherwise hide
        :param pos: position index (left to right)
        :return: -
        """

        if show:
            if self.ui.splitter.indexOf(widget) == -1:
                # new widget: insert it
                self.ui.splitter.insertWidget(pos, widget)
            self.ui.splitter.setSizes([int(self.ui.splitter.size().width() * 0.2),
                                     int(self.ui.splitter.size().width() * 0.8)])
            widget.show()
        else:
            widget.hide()

    def showMsgbox(self, content, title):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(content)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def getConfirmation(self, content, title):
        return QMessageBox.question(self, title, content,
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
    
    def setDirty(self, dirty):
        self.isDirty = dirty
        title = "Cannibal"
        if self.isOpen:
            title = " - " + title
            if self.isDirty:
                title = " *" + title
            title = self.fileName + title
            self.resetPreview()
                
        self.setWindowTitle(title)

    def getOpenFileName(self):
        # Open the file dialog
        fileName, dummy = QFileDialog.getOpenFileName(None, self.tr("Open File"),
                          self.filePath, self.tr("PDF Files (*.pdf);; All files ()"))
        return fileName

    def openPdf(self, file=None):
        """
        This method is invoked by selecting "Open" from the "file" menu.

        :return: -
        """
        
        # check for file in memory
        if not self.closePdf():
            return
        if file is False:
            fileName = self.getOpenFileName()
        else:
            fileName = file

        if fileName and os.path.isfile(fileName):
            self.filePath, self.fileName = os.path.split(fileName) 
            
            ret = self.pdf.openPdf(fileName)
            if ret != 0:
                                    
                # Show the signature tree
                self.showWidget(self.ui.tabs, pos=0)
    
                # Show the page view
                self.showWidget(self.ui.pdfView, pos=1)

                # Activate GUI elements
                self.activateGuiElements(self.guiElements, True)
            
                self.pageCount = self.pdf.getPageCount()
                self.ui.pdfView.clear()
                self.resetPreview()
                self.firstPage()
                self.isOpen = True
                if ret == 2:
                    self.fileName = self.tr("NoName")
                    self.setDirty(True)
                else:
                    self.setDirty(False)
                self.pdf.printSignatures()
            
    def savePdf(self):
        """
        save the current pdf at its original location

        :return: True if saved
        """
        if self.isOpen:
            if self.pdf.isNewPdf():  # a new file or converted format
                return self.savePdfAs()
            else:
                self.pdf.savePdf()
                self.setDirty(False)
                return True
        return False
            
    def savePdfAs(self):
        """
        save the current pdf at a location selected by the user.

        :return: True is saved
        """

        options = QFileDialog.Options()
        filename, extension = QFileDialog.getSaveFileName(self,
            self.tr("Save document as"), self.filePath,
            self.tr("PDF Files (*.pdf)"), options=options)

        if filename and extension:
            self.pdf.savePdf(filename)
            # close and reopen to sync pyMuPdf memory image
            self.setDirty(False)
            self.closePdf()
            self.openPdf(filename)
            return True
        return False

    def closePdf(self):
        """
        close the current pdf

        :return: True if pdf is saved or willingly abandoned
        """
        saved = True
        if self.isOpen and self.isDirty:
            reply = self.getConfirmation(self.tr("Save changes before closing?"), self.tr("Close"))

            if reply == QMessageBox.Yes:
                saved = self.savePdf()
            elif reply == QMessageBox.No:
                saved = True
            else:
                saved = False
            
            if saved is True:
                self.ui.pdfView.clear()
                self.page = None
                self.ui.pdfView.clearPage()
                self.pdf.closePdf()
            
                # Deactivate GUI elements
                self.activateGuiElements(self.guiElements, False)

                # Hide the tab area
                self.showWidget(self.ui.tabs, show=False)
    
                # Hide the page view
                self.showWidget(self.ui.pdfView, show=False)
            
                self.isOpen = False
                self.fileName = None
                self.setDirty(False)
        return saved
            
    def showPage(self):
        """
        render and show the current page
        update the number and preview selection
        """
        self.page = self.pdf.getPage(self.pageNum)
        self.ui.pdfView.showPage(self.page)
        self.currPage.setText(str(self.pageNum+1))
        
    def setPage(self, pNum):
        """
        select the current page in the preview
        thereby triggering the update of the main view
        """
        if pNum >= self.pageCount:
            pNum = self.pageCount-1
        elif pNum < 0:
            pNum = 0

        self.currPage.setText(str(pNum+1))
        self.ui.thumbs.setCurrentRow(pNum)

    def thumbChange(self, current, previous):
        """
        render the page that was selected in preview
        """            
        row = self.ui.thumbs.currentRow()
        if row >= 0:
            self.pageNum = row
            self.showPage()

    def fillPreview(self):
        row1, row2 = self.ui.thumbs.getVisibleRows()
        # check if list is only partially filled
        if row1 == -1:
            row1 = 0
        if row2 == -1:
            row2 = self.pageCount-1
        for i in range(row1, row2+1):
            page = self.pdf.getPage(i)            
            self.ui.thumbs.setThumbImage(i, page)

    def resetPreview(self):
        """
        fill the preview list with thumbnails of pages
        """
        self.ui.thumbs.resetPreview(self.pageCount, self.pageNum)
        self.fillPreview()

    def zoomOriginal(self):
        self.ui.pdfView.zoomOriginal()
        
    def zoomFitBest(self):
        self.ui.pdfView.zoomFitBest()
        
    def zoomIn(self):
        self.ui.pdfView.zoomIn()

    def zoomOut(self):
        self.ui.pdfView.zoomOut()

    def firstPage(self):
        self.setPage(0)
        
    def prevPage(self):
        self.setPage(self.pageNum-1)
        
    def nextPage(self):
        self.setPage(self.pageNum+1)
        
    def lastPage(self):
        self.setPage(self.pageCount-1)

    def gotoPage(self):
        try:
            p = int(self.currPage.text())
            self.setPage(p-1)
        except:
            pass
        
    def deletePage(self):
        self.pdf.deletePage(self.pageNum)
        self.pageCount = self.pdf.getPageCount()
        self.setDirty(True)

    def insertPage(self):
        self._insertPage(self.pageNum)
        self.setDirty(True)
        
    def appendPage(self):
        self._insertPage(-1)
        
    def _insertPage(self, pageNum):
        self.pdf.insertPage(pageNum)
        self.pageCount = self.pdf.getPageCount()
        self.setDirty(True)

    def insertDocument(self):
        dlg = InsertFileDlg(self.settings)
        
        if dlg.exec() == QDialog.Accepted:
            doc = dlg.getDoc()
            if doc is not None:
                self.pdf.insertDocument(doc, pageNum=-1 if dlg.getAppend() is True else self.pageNum)
                dlg.closeDoc()
                self.pageCount = self.pdf.getPageCount()
                self.setDirty(True)

    def rotateLeft(self):
        self.page.setRotation((self.page.rotation - 90) % 360)
        self.ui.pdfView.updateView()
        self.setDirty(True)

    def rotateRight(self):
        self.page.setRotation((self.page.rotation + 90) % 360)
        self.ui.pdfView.updateView()
        self.setDirty(True)

    def changeMode(self, mode):
        """
        change the working mode from pan to mouse rectangle selection
        release of mouse calls dispatcher function

        :return: -
        """
        if self.mode is None:
            self.ui.pdfView.setPan(False)
            self.mode = mode
            QApplication.setOverrideCursor(Qt.CrossCursor)

    def handleLeftRectRelease(self, x0, y0, x1, y1):
        """
        Dispatch mouse rect to initiating function
        """
        self.ui.pdfView.setPan(True)
        QApplication.restoreOverrideCursor()
        # x,y are scaled mouse coordinates
        # dispatch to worker 
        if self.mode is not None:
            insertFunction = getattr(self, "doInsert_%s" % self.mode)
            insertFunction(x0, y0, x1, y1)
            self.mode = None

    def handleLeftButtonRelease(self, x, y):
        # print("mouse x,y %s %s" % (x, y))
        pass
                        
    def sign(self):
        self.changeMode("Sign")

    def doInsert_Sign(self, x0, y0, x1, y1):
        # Todo: get signature data dialog
        self.pdf.addSignature(self.page, x0, y0, x1, y1)
        self.setDirty(True)
        self.pdf.savePdf("testsig.pdf")
        
    def insertForm(self):
        self.changeMode("Form")

    def doInsert_Form(self, x0, y0, x1, y1):
        """
        insert text form into rectangle area
        called after rectangle was selected

        :return: -
        """
        self.pdf.addTextForm(self.page, x0, y0, x1, y1, self.page.rotation)
        self.setDirty(True)
        
    def insertText(self):
        self.changeMode("Text")

    def doInsert_Text(self, x0, y0, x1, y1):
        """
        insert text into rectangle area
        called after rectangle was selected

        :return: -
        """
        dlg = InsertTextDlg(self.settings)
        dlg.enableConvertQR(self.pdf.canQR())
        
        if dlg.exec() == QDialog.Accepted:
            ret = self.pdf.addText(self.page, x0, y0, x1, y1,
                                    dlg.getText(), dlg.getFontSize(),
                                    dlg.getFontName(), dlg.getAllPages(),
                                    dlg.getConvertQR(), self.page.rotation)
            if ret < 0:
                QMessageBox.question(self, self.tr("Error"), self.tr("Text too long/large"),
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.setDirty(True)

    def insertImage(self):
        self.changeMode("Image")

    def doInsert_Image(self, x0, y0, x1, y1):
        """
        insert image into rectangle area
        called after rectangle was selected

        :return: -
        """
        dlg = InsertImageDlg(self.settings)
        if dlg.exec() == QDialog.Accepted:
            try:
                self.pdf.addImage(self.page, x0, y0, x1, y1, dlg.getFileName(),
                                dlg.getAllPages(), 0, self.page.rotation)
                self.setDirty(True)
            except:
                QMessageBox.question(self, self.tr("Error"), self.tr("Couldn't insert image (unknown format?)"),
                                     QMessageBox.Ok, QMessageBox.Ok)

    def insertStamp(self):
        self.changeMode("Stamp")

    def doInsert_Stamp(self, x0, y0, x1, y1):
        """
        insert predefined stamp image into rectangle area
        called after rectangle was selected

        :return: -
        """
        dlg = InsertStampDlg(self.settings, self.progPath)
        if dlg.exec() == QDialog.Accepted:
            self.pdf.addImage(self.page, x0, y0, x1, y1, dlg.getFileName(),
                              dlg.getAllPages(), int(dlg.getStampAngle()),
                              self.page.rotation)
            self.setDirty(True)

    def documentInfo(self):
        if self.pdf:
            info = self.pdf.metadata()
            if info is not None:
                content = "\n".join(["%s:  %s" % (k, v) for k, v in info.items()])
            else:
                content = "---"
            self.showMsgbox(content, "Info")

    def aboutCannibal(self):
        OS = '{0} {1} {2}'.format(platform.system(), platform.release(), platform.architecture()[0])
        PYTHON_VERSION = platform.python_version()
        QT_VERSION = qVersion()
        PYMUPDF_VERSION = fitz.VersionBind

        aboutText = self.tr('''<br>
        Annotate and sign PDF documents.<br>
        Version: {0}<br>
        <br>
        OS: {1}<br>
        <br>
        Software versions used:<br>
        Python: {2}<br>
        pyMuPdf: {3}<br>
        Qt: {4}''')
        self.showMsgbox(aboutText.format(__version__, OS, PYTHON_VERSION, PYMUPDF_VERSION, QT_VERSION),
                        self.tr("About Cannibal"))

    def closeEvent(self, event=None):
        """
        This event is triggered when the user closes the main window by clicking on the cross in
        the window corner, or selects 'Quit' in the file menu.

        :param event: event object
        :return: -
        """

        # Check for unsaved changes
        if self.closePdf() is True:
            if event:
                event.accept()

            # Store window size and position
            self.settings.setValue('WindowSize', self.size())
            self.settings.setValue('WindowPos', self.pos())
            self.settings.setValue('WindowMax', (self.windowState() == Qt.WindowMaximized))
            self.settings.setValue('LastPath', self.filePath)
            self.settings.sync()
            exit(0)
        else:
            # No confirmation by the user: Don't stop program execution.
            if event:
                event.ignore()

def main():
    filePath = os.path.dirname(os.path.realpath(__file__))

    app = QApplication(argv)    
    app.setWindowIcon(QtGui.QIcon(os.path.join(filePath, "icons/Logo.png")))

    # Internationalization support
    translator = QTranslator()
    tPath = os.path.join(filePath, 'i18n')
    if translator.load(QLocale(), 'cannibal', '_', tPath, ".qm"):
        app.installTranslator(translator)

    if len(argv) > 1:
        file = argv[1]
    else:
        file = None
    
    myapp = Cannibal(progPath=filePath, file=file)
    myapp.show()
    app.exec()


if __name__ == "__main__":
    main()
