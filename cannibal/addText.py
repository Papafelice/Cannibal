# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './addText.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InsertText(object):
    def setupUi(self, InsertText):
        InsertText.setObjectName("InsertText")
        InsertText.resize(400, 474)
        InsertText.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(InsertText)
        self.buttonBox.setGeometry(QtCore.QRect(30, 430, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.userText = QtWidgets.QPlainTextEdit(InsertText)
        self.userText.setGeometry(QtCore.QRect(20, 220, 351, 91))
        self.userText.setObjectName("userText")
        self.everyPage = QtWidgets.QCheckBox(InsertText)
        self.everyPage.setGeometry(QtCore.QRect(20, 390, 151, 28))
        self.everyPage.setObjectName("everyPage")
        self.convertQR = QtWidgets.QCheckBox(InsertText)
        self.convertQR.setGeometry(QtCore.QRect(200, 390, 171, 28))
        self.convertQR.setObjectName("convertQR")
        self.label = QtWidgets.QLabel(InsertText)
        self.label.setGeometry(QtCore.QRect(20, 310, 91, 24))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(InsertText)
        self.label_2.setGeometry(QtCore.QRect(290, 310, 61, 24))
        self.label_2.setObjectName("label_2")
        self.fontSize = QtWidgets.QPlainTextEdit(InsertText)
        self.fontSize.setGeometry(QtCore.QRect(290, 340, 61, 41))
        self.fontSize.setObjectName("fontSize")
        self.fontName = QtWidgets.QComboBox(InsertText)
        self.fontName.setGeometry(QtCore.QRect(20, 340, 261, 41))
        self.fontName.setObjectName("fontName")
        self.pdfView = PdfViewer(InsertText)
        self.pdfView.setGeometry(QtCore.QRect(20, 20, 351, 192))
        self.pdfView.setObjectName("pdfView")

        self.retranslateUi(InsertText)
        self.buttonBox.accepted.connect(InsertText.accept)
        self.buttonBox.rejected.connect(InsertText.reject)
        QtCore.QMetaObject.connectSlotsByName(InsertText)

    def retranslateUi(self, InsertText):
        _translate = QtCore.QCoreApplication.translate
        InsertText.setWindowTitle(_translate("InsertText", "Insert text"))
        self.everyPage.setText(_translate("InsertText", "On every page"))
        self.convertQR.setText(_translate("InsertText", "Convert to QR"))
        self.label.setText(_translate("InsertText", "Font"))
        self.label_2.setText(_translate("InsertText", "Size"))
from QtPdfViewer import PdfViewer
