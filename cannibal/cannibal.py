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

__version__ = '0.36.18' 

import os
from sys import exit, argv, path
path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import platform

import fitz
if fitz.VersionBind.split(".") < ["1", "17", "2"]:
    exit("PyMuPDF v1.17.2+ is needed.")

from PyQt5 import QtGui
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, QTranslator, QLocale, qVersion, QSettings, QPointF
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.QtWidgets import QMessageBox, QDialog, QLineEdit
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

from main_gui import Ui_MainWindow
from pdfTools import PdfDoc
from addObjects import InsertTextDlg, InsertImageDlg, InsertStampDlg, InsertFileDlg
from formEdit import EditFormText, EditFormList
from certificates import CertificatesDlg, ApplySigDlg


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
        
        # Connect to all menu triggers
        self.ui.actionZoom_original.triggered.connect(self.ui.pdfView.zoomOriginal)
        self.ui.actionZoom_fit_best.triggered.connect(self.ui.pdfView.zoomFitBest)
        self.ui.actionZoom_in.triggered.connect(self.ui.pdfView.zoomIn)
        self.ui.actionZoom_out.triggered.connect(self.ui.pdfView.zoomOut)
        handlers = {
            "Quit": "closeEvent",
            "New": "newPdf", "Open": "openPdf", "Close": "closePdf",
            "Save": "savePdf", "Save_as": "savePdfAs",
            "Document_Info": "documentInfo",
            "Sign": "sign",
            "Insert_form": "insertForm", "Insert_text": "insertText",
            "Insert_image": "insertImage", "Insert_stamp": "insertStamp",
            "Rotate_left": "rotateLeft", "Rotate_right": "rotateRight",
            "First_page": "firstPage", "Previous_page": "prevPage",
            "Next_page": "nextPage", "Last_page": "lastPage",
            "Delete_page": "deletePage", "Insert_page": "insertPage",
            "Append_page": "appendPage", "Clean_page": "cleanPage",
            "Insert_document": "insertDocument",
            "Manage_certificate": "manageCertificate",
            "About": "aboutCannibal", "Help": "help"
        }
        handlers["Print"] = "print"

        for t, h in handlers.items():
            self.connectTrigger(t, h)
        
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
        self.ui.thumbs.dropped.connect(self.thumbDropped)

        
        self.guiElements = [self.ui.actionSave, self.ui.actionSave_as,
                            self.ui.actionPrint,
                            self.ui.actionClose, self.ui.actionDocument_Info,
                            self.ui.actionSign, self.ui.actionSign_invisibly,
                            self.ui.actionInsert_text, self.ui.actionInsert_image,
                            self.ui.actionInsert_stamp, self.ui.actionInsert_form,
                            self.ui.actionDelete_page, self.ui.actionInsert_page,
                            self.ui.actionAppend_page, self.ui.actionClean_page,
                            self.ui.actionInsert_document,
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
        self.ui.pdfView.MouseMoved.connect(self.handleMouseMoved)

        # Initialize variables
        self.mode = None
        self.fileName = None
        self.isOpen = False
        self.isDirty = False
        self.pageNum = 0
        self.pageCount = 0
        self.page = None
        self.inField = False
                
        if file is not None:
            self.openPdf(file=file)
        
    def connectTrigger(self, trigger, handler):
        """
        Connect a handler to a trigger event
        """
        t = getattr(self.ui, "action%s" % trigger)
        h = getattr(self, handler)
        t.triggered.connect(h)
        
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
            #widget.layout.update()
            #widget.layout.activate()
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
    
    def setDirty(self, dirty, reLoad=False):
        self.isDirty = dirty
        title = "Cannibal"
        if self.isOpen:
            if reLoad:
                self.page = self.pdf.reloadPage(self.page)
            title = " - " + title
            if self.isDirty:
                title = " *" + title
            title = self.fileName + title
            self.resetPreview(self.pageNum)
                
        self.setWindowTitle(title)

    def newPdf(self):
        self.openPdf(newFile=True)
        
    def openPdf(self, file=None, newFile=False):
        """
        This method is invoked by selecting "Open" from the "file" menu.

        :return: -
        """
        
        # check for file in memory
        if not self.confirmChanged():
            return
        if newFile is False and file is False:
            # Open the file dialog
            fileName, dummy = QFileDialog.getOpenFileName(None, self.tr("Open File"),
                        self.filePath, self.tr("PDF Files (*.pdf);; All files ()"))
            if not fileName or not os.path.isfile(fileName):
                return
        else:
            fileName = file

        self.setDirty(False)
        self.closePdf()
        if newFile is True:
            self.fileName = self.tr("NoName")
        else:
            self.filePath, self.fileName = os.path.split(fileName) 
            
        ret = self.pdf.openPdf(fileName)

        if ret != 0:                                    
            # Show the signature tree
            self.showWidget(self.ui.tabs, pos=0)
            # Show the page view
            self.showWidget(self.ui.pdfView, pos=1)
            # Activate GUI elements
            self.activateGuiElements(self.guiElements, True)
    
            if newFile:
                self.pdf.insertPage(0)
            self.pageNum = 0;
            self.pageCount = self.pdf.getPageCount()
            self.ui.pdfView.clear()
            self.resetPreview(None)
            self.isOpen = True
            if (ret == 2):
                self.setDirty(True)
            else:
                self.setDirty(False)
           
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

        :return: True if saved
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
            self.openPdf(file=filename)
            return True
        return False

    def confirmChanged(self):
        """
        confirm losses of changed document

        :return: False if user aborts
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
        return saved

    def closePdf(self):
        """
        close the current pdf

        :return: True if pdf is saved or willingly abandoned
        """
        saved = self.confirmChanged()
            
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

    def print(self):
        from printing import printPDF
        printer = QPrinter(QPrinter.HighResolution)
        printer.setFromTo(1, self.pageCount)
        printDialog = QPrintDialog(printer, self)
        
        if printDialog.exec_() == QDialog.Accepted:
            printPDF(printer, self.pdf, self.fileName)
        
    def showPage(self):
        """
        render and show the current page
        update the number and preview selection
        """
        self.page = self.pdf.getPage(self.pageNum)
        self.ui.pdfView.showPage(self.page)
        self.currPage.setText(str(self.pageNum+1))
        
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

    def resetPreview(self, pageNum = None):
        """
        fill the preview list with thumbnails of pages
        """
        self.ui.thumbs.resetPreview(self.pageCount, pageNum)
        self.fillPreview()

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
        
    def thumbDropped(self, index):
        if index == self.pageNum:
            pass
        self.pageNum = self.pdf.movePage(self.pageNum, index)
        self.resetPreview(self.pageNum)
        self.setDirty(True)
        
    def deletePage(self):
        self.pdf.deletePage(self.pageNum)
        self.pageCount = self.pdf.getPageCount()
        if self.pageNum >= self.pageCount:
            self.pageNum = self.pageCount - 1
        self.setPage(self.pageNum)
        self.setDirty(True)

    def insertPage(self):
        self._insertPage(self.pageNum)
        
    def appendPage(self):
        self._insertPage(-1)
        
    def cleanPage(self):
        self.page.cleanContents()
        self.setDirty(True)
        
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
        release of left button calls the mode dispatcher function

        :return: -
        """
        if self.mode is None:
            self.ui.pdfView.setPan(False)
            self.mode = mode
            QApplication.setOverrideCursor(Qt.CrossCursor)

    def setHandCursor(self, setOn=False):
        """
        change mouse cursor to hand symbol

        :return: -
        """
        if setOn is True:
            if self.inField is False:
                QApplication.setOverrideCursor(Qt.PointingHandCursor)
                self.inField = True
        else:
            if self.inField is True:
                QApplication.restoreOverrideCursor()
                self.inField = False
        
    def handleMouseMoved(self, x, y):
        """
        check if mouse is over a form widget

        :return: -
        """
        field = self.findField(x, y)
        if field is not None:
            self.setHandCursor(True)
        else:
            self.setHandCursor(False)
 
    def handleLeftRectRelease(self, x0, y0, x1, y1):
        """
        Dispatch mouse rect to initiating function
        """
        self.ui.pdfView.setPan(True)
        QApplication.restoreOverrideCursor()
        # x,y are image coordinates
        # dispatch to worker 
        if self.mode is not None:
            insertFunction = getattr(self, "doInsert_%s" % self.mode)
            insertFunction(x0, y0, x1, y1)
            self.mode = None

    def findField(self, x, y):
        """
        check whether mouse is over a form widget
        """
        if self.mode is None:
            p = fitz.Point(x, y)
            inField = False
            for field in self.page.widgets():
                if field.rect.contains(p):
                    inField = True
                    break
            if inField is True:
                return field
        return None

    def updateField(self, field):
        field.update()
        self.setDirty(True)

    def mapToScreen(self, x, y):
        """
        convert pdf coordinates to absolute screen cordinates
        """
        p = QPointF(x, y)
        pw = self.ui.pdfView.mapFromImg(p)
        pg = self.ui.pdfView.mapToGlobal(pw)
        return pg

    def handleLeftButtonRelease(self, x, y):
        field = self.findField(x, y)
        if field is None:
            return
        self.setHandCursor(False)
        if field.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
            field.field_value = False if field.field_value == "Yes" else True
            self.updateField(field)
        elif field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
            pg = self.mapToScreen(field.rect.x0, field.rect.y0)
            dlg = EditFormText(pg, field.field_value)
            if dlg.exec() == QDialog.Accepted:
                field.field_value = dlg.getText()
                self.updateField(field)
        elif field.field_type == fitz.PDF_WIDGET_TYPE_COMBOBOX:
            print("Combo FLags %s" % (hex(field.field_flags),))
            pg = self.mapToScreen(field.rect.x0, field.rect.y0)
            dlg = EditFormList(pg)
            dlg.fillList(field.choice_values)
            dlg.setText(field.field_value)
            if dlg.exec() == QDialog.Accepted:
                field.field_value = dlg.getText()
                self.updateField(field)
        elif field.field_type == fitz.PDF_WIDGET_TYPE_SIGNATURE:
            print("Signature Name: %s, signed %s, value: %s, flags: %s, xref: %s" %
                (field.field_name, field.is_signed, field.field_value, field.field_flags, field.xref))
            doc = self.pdf.getDoc()
            print(doc.xrefObject(field.xref, compressed=False))
        else:
            print("Field type %s unimplemented" % field.field_type)
        
    def sign(self):
        self.changeMode("Sign")

    def doInsert_Sign(self, x0, y0, x1, y1):
        # Todo: get signature data dialog
        dlg = ApplySigDlg(self.settings)
        if dlg.exec() == QDialog.Accepted:
            self.pdf.addSignature(self.page, x0, y0, x1, y1)
            self.setDirty(True, True)
        
        
    def insertForm(self):
        self.changeMode("Form")

    def doInsert_Form(self, x0, y0, x1, y1):
        """
        insert text form into rectangle area
        called after rectangle was selected

        :return: -
        """
        self.pdf.addTextForm(self.page, x0, y0, x1, y1, self.page.rotation)
        self.setDirty(True, True)
        
    def insertText(self):
        self.changeMode("Text")

    def doInsert_Text(self, x0, y0, x1, y1):
        """
        insert text into rectangle area
        called after rectangle was selected

        :return: -
        """
        dlg = InsertTextDlg(self.settings, x1-x0, y1-y0, self.pageNum)
        dlg.enableConvertQR(self.pdf.canQR())
        
        if dlg.exec() == QDialog.Accepted:
            self.pdf.addText(self.page, x0, y0, x1, y1,
                             dlg.getText(), dlg.getFontSize(),
                             dlg.getFontName(), dlg.getAllPages(),
                             dlg.getConvertQR(), self.page.rotation)
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
                QMessageBox.question(self, self.tr("Error"),
                                     self.tr("Couldn't insert image (unknown format?)"),
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

    def manageCertificate(self):
        dlg = CertificatesDlg(self.settings)
        dlg.exec()

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

    def help(self):
        from subprocess import call
        prg = os.path.join(self.progPath, "showhelp.py")
        hlp = os.path.join(self.progPath, "help", self.tr("help.md")) 
        call(["python3", prg, hlp])

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
