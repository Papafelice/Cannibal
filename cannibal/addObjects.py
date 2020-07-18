# -*- coding: utf-8; -*-
"""
Copyright (c) 2020 Felix Huber

This file is part of the digital signature tool for pdf files.

cannibal is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with cannibal.  If not, see <http://www.gnu.org/licenses/>.

"""

import platform
import os.path
from os import listdir
import fitz

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtWidgets import QDialog, QGraphicsScene
from PyQt5.QtGui import QImage, QPixmap, QTransform, QIntValidator

from QtPdfViewer import ImgViewer, PdfViewer
from addText import Ui_InsertText
from addImage import Ui_InsertImage
from addStamp import Ui_InsertStamp
from addFile import Ui_InsertFile
from pdfTools import PdfDoc


class InsertTextDlg(QDialog):
    """
    A class to show a dialog where the user can enter text to be inserted 
    """

    def __init__(self, settings, w, h, pageNum):
        super().__init__()
        self.ui = Ui_InsertText()
        self.ui.setupUi(self)

        self.settings = settings
        self.w = w
        self.h = h
        self.pageNum = pageNum
        
        # fill in standard PDF font names
        for k, v in fitz.Base14_fontdict.items():
            self.ui.fontName.addItem(v)

        # reload old values
        try:
            text = self.settings.value('Insert/Text', "Text")
            self.ui.userText.setPlainText(text)
            size = self.settings.value('Insert/FontSize', "11")
            self.ui.fontSize.setPlainText(size)
            name = self.settings.value('Insert/FontName', "Helvetica")
            index = self.ui.fontName.findText(name)
            if index != -1:
                self.ui.fontName.setCurrentIndex(index)
        except:
            pass

        # create an empty PDF for the preview
        self.pdf = PdfDoc()
        self.pdf.openPdf()
        self.pdf.insertPage(0, self.w, self.h)

        # handlers for the changed fields
        self.ui.userText.textChanged.connect(self.setPreview)
        self.ui.fontSize.textChanged.connect(self.setPreview)
        self.ui.fontName.currentTextChanged.connect(self.setPreview)

        self.show()
        self.setPreview()

    def getText(self):
        return self.ui.userText.toPlainText()

    def getFontSize(self):
        return self.ui.fontSize.toPlainText()
    
    def getFontName(self):
        return self.ui.fontName.currentText()
    
    def getAllPages(self):
        return self.ui.everyPage.isChecked()

    def getConvertQR(self):
        return self.ui.convertQR.isChecked()
    
    def enableConvertQR(self, enable):
        self.ui.convertQR.setEnabled(enable)

    def setPreview(self):
        self.pdf.deletePage(0)
        self.pdf.insertPage(0, self.w, self.h)
        page = self.pdf.getPage(0)
        try:
            text2 = self.getText().format(self.pageNum+1)
        except:
            text2 = self.getText()
        ret = self.pdf.addText(page, 0, 0, self.w, self.h,
                               text2, self.getFontSize(),
                               self.getFontName(), False,
                               False, 0)
        self.ui.pdfView.showPage(page)
            
    def accept(self):
        self.settings.setValue('Insert/Text', self.getText())
        self.settings.setValue('Insert/FontSize', self.getFontSize())
        self.settings.setValue('Insert/FontName', self.getFontName())
        self.pdf.closePdf()
        self.done(QDialog.Accepted)


class InsertImageDlg(QDialog):
    """
    A class to show a dialog where the user can select an image file
    to  be inserted with preview
    """
    def __init__(self, settings):
        super().__init__()
        self.ui = Ui_InsertImage()
        self.ui.setupUi(self)
        
        self.settings = settings
        
        # img viewer instance for the image preview
        self.imgView = ImgViewer()
        self.ui.horizontalLayout.insertWidget(0, self.imgView)
        self.imgView.show()
        
        # handler for the button
        self.ui.chooseFile.clicked.connect(self.chooseFile)
        
        self.show()
        
        # reload old values
        try:
            fileName = self.settings.value('Insert/ImageFile')
            if fileName is not None:
                self.setFileName(fileName)
        except:
            pass

    def chooseFile(self):
        # Open the file dialog
        fileName, dummy = QFileDialog.getOpenFileName(None, self.tr("Open image"), ".",
                                                      self.tr("Images (*.png *.jpg *.bmp);; All files ()"))
        self.setFileName(fileName)
            
    def setFileName(self, fileName):
        if fileName and os.path.isfile(fileName):
            self.ui.fileName.setPlainText(fileName)
            self.setPreview()

    def getFileName(self):
        return self.ui.fileName.toPlainText()
    
    def getAllPages(self):
        return self.ui.everyPage.isChecked()

    def setPreview(self):
        try:
            image = QImage(self.ui.fileName.toPlainText())
            self.imgView.setImage(image)
        except:
            pass

    def accept(self):
        self.settings.setValue('Insert/ImageFile', self.getFileName())
        self.done(QDialog.Accepted)


class InsertStampDlg(QDialog):
    """
    A class to show a dialog where the user can select a stamp image
    to  be inserted with preview
    """
    def __init__(self, settings, progPath="."):
        super().__init__()
        self.ui = Ui_InsertStamp()
        self.ui.setupUi(self)
        self.ui.angle.setValidator(QIntValidator())
        
        self.settings = settings
        self.stampPath = os.path.join(progPath, "stamps")
        self.fileName = None
        
        # img viewer instance for the stamp preview
        self.imgView = ImgViewer()
        self.ui.horizontalLayout.insertWidget(0, self.imgView)
        self.imgView.show()
                
        # fill in stamp names
        for dirs in next(os.walk(self.stampPath))[1]:
            self.ui.stampLang.addItem(dirs)

        # reload old lang values
        try:
            lang = self.settings.value('Insert/StampLang', "de")
            index = self.ui.stampLang.findText(lang)
            if index != -1:
                self.ui.stampLang.setCurrentIndex(index)
        except:
            pass
        
        self.fillStamps()

        # reload old values
        try:
            size = self.settings.value('Insert/StampAngle', "0")
            self.ui.angle.setText(str(size))
            name = self.settings.value('Insert/StampName', "Original.png")
            index = self.ui.stampName.findText(name)
            if index != -1:
                self.ui.stampName.setCurrentIndex(index)
        except:
            pass

        self.ui.stampLang.currentIndexChanged.connect(self.langChange)
        self.ui.stampName.currentIndexChanged.connect(self.nameChange)
        self.ui.angle.editingFinished.connect(self.angleChange)

        self.show()
        self.nameChange(0)
            
    def langChange(self, i):
        self.fillStamps()
        self.nameChange(0)

    def fillStamps(self):
        self.ui.stampName.clear()
        path = os.path.join(self.stampPath, self.ui.stampLang.currentText())
        onlyfiles = [f for f in listdir(path) if os.path.isfile(os.path.join(path, f))]
        for v in onlyfiles:
            self.ui.stampName.addItem(v)

    def nameChange(self, i):
        self.setFileName(self.ui.stampName.currentText())
    
    def angleChange(self):
        self.setPreview()
        
    def getStampAngle(self):
        return self.ui.angle.text()
    
    def getStampName(self):
        return self.ui.stampName.currentText()
    
    def getStampLang(self):
        return self.ui.stampLang.currentText()

    def setFileName(self, fileName):
        if fileName:
            path = os.path.join(self.stampPath, self.getStampLang(), self.getStampName())
            if os.path.isfile(path):
                self.fileName = path
                self.setPreview()

    def getFileName(self):
        return self.fileName

    def getAllPages(self):
        return self.ui.everyPage.isChecked()

    def setPreview(self):
        try:
            image = QImage(self.fileName)            
            angle = self.getStampAngle()
            try:
                angle = int(angle)
            except:
                angle = 0
            if angle != 0:
                transform = QTransform()
                transform.rotate(-angle)
                image = image.transformed(transform)
            self.imgView.setImage(image)
        except:
            pass

    def accept(self):
        self.settings.setValue('Insert/StampName', self.getStampName())
        self.settings.setValue('Insert/StampAngle', self.getStampAngle())
        self.settings.setValue('Insert/StampLang', self.getStampLang())
        self.done(QDialog.Accepted)


class InsertFileDlg(QDialog):
    """
    A class to show a dialog where the user can select a PDF file
    to  be inserted/appended with preview
    """
    def __init__(self, settings):
        super().__init__()
        self.ui = Ui_InsertFile()
        self.ui.setupUi(self)
        
        self.settings = settings
                
        # handler for the button
        self.ui.chooseFile.clicked.connect(self.chooseFile)
        
        self.show()
        
        # reload old values
        try:
            fileName = self.settings.value('Insert/InsertFile')
            if fileName is not None:
                self.setFileName(fileName)
        except:
            pass

    def chooseFile(self):
        # Open the file dialog
        fileName, dummy = QFileDialog.getOpenFileName(None, self.tr("Open file"), ".",
                                                      self.tr("PDF Files (*.pdf);; All files ()"))
        self.setFileName(fileName)
            
    def setFileName(self, fileName):
        if fileName and os.path.isfile(fileName):
            self.ui.fileName.setPlainText(fileName)
            self.setPreview()

    def getFileName(self):
        return self.ui.fileName.toPlainText()
    
    def getAppend(self):
        return self.ui.append.isChecked()

    def getDoc(self):
        return self.pdf.doc
    
    def closeDoc(self):
        self.pdf.closePdf()
        self.pdf = None
        
    def setPreview(self):
        self.pdf = PdfDoc()
        ret = self.pdf.openPdf(self.getFileName())
        if ret != 0:
            self.ui.pdfView.showPage(self.pdf.getPage(0))
        else:
            self.doc = None

    def accept(self):
        self.settings.setValue('Insert/InsertFile', self.getFileName())
        self.done(QDialog.Accepted)
