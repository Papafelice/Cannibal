# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './addFile.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InsertFile(object):
    def setupUi(self, InsertFile):
        InsertFile.setObjectName("InsertFile")
        InsertFile.resize(445, 565)
        InsertFile.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(InsertFile)
        self.buttonBox.setGeometry(QtCore.QRect(30, 510, 401, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.append = QtWidgets.QCheckBox(InsertFile)
        self.append.setGeometry(QtCore.QRect(20, 490, 151, 28))
        self.append.setObjectName("append")
        self.label = QtWidgets.QLabel(InsertFile)
        self.label.setGeometry(QtCore.QRect(20, 423, 61, 31))
        self.label.setObjectName("label")
        self.fileName = QtWidgets.QPlainTextEdit(InsertFile)
        self.fileName.setGeometry(QtCore.QRect(20, 450, 301, 41))
        self.fileName.setObjectName("fileName")
        self.chooseFile = QtWidgets.QPushButton(InsertFile)
        self.chooseFile.setGeometry(QtCore.QRect(330, 450, 101, 40))
        self.chooseFile.setObjectName("chooseFile")
        self.horizontalLayoutWidget = QtWidgets.QWidget(InsertFile)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 9, 411, 421))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pdfView = PdfViewer(self.horizontalLayoutWidget)
        self.pdfView.setObjectName("pdfView")
        self.horizontalLayout.addWidget(self.pdfView)

        self.retranslateUi(InsertFile)
        self.buttonBox.accepted.connect(InsertFile.accept)
        self.buttonBox.rejected.connect(InsertFile.reject)
        QtCore.QMetaObject.connectSlotsByName(InsertFile)

    def retranslateUi(self, InsertFile):
        _translate = QtCore.QCoreApplication.translate
        InsertFile.setWindowTitle(_translate("InsertFile", "Insert file"))
        self.append.setText(_translate("InsertFile", "Append"))
        self.label.setText(_translate("InsertFile", "File"))
        self.chooseFile.setText(_translate("InsertFile", "Choose..."))
from QtPdfViewer import PdfViewer
