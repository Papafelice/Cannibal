# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './addImage.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InsertImage(object):
    def setupUi(self, InsertImage):
        InsertImage.setObjectName("InsertImage")
        InsertImage.resize(445, 341)
        InsertImage.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(InsertImage)
        self.buttonBox.setGeometry(QtCore.QRect(30, 300, 401, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.everyPage = QtWidgets.QCheckBox(InsertImage)
        self.everyPage.setGeometry(QtCore.QRect(20, 260, 151, 28))
        self.everyPage.setObjectName("everyPage")
        self.label = QtWidgets.QLabel(InsertImage)
        self.label.setGeometry(QtCore.QRect(20, 193, 61, 31))
        self.label.setObjectName("label")
        self.fileName = QtWidgets.QPlainTextEdit(InsertImage)
        self.fileName.setGeometry(QtCore.QRect(20, 220, 301, 41))
        self.fileName.setObjectName("fileName")
        self.chooseFile = QtWidgets.QPushButton(InsertImage)
        self.chooseFile.setGeometry(QtCore.QRect(330, 220, 110, 40))
        self.chooseFile.setObjectName("chooseFile")
        self.horizontalLayoutWidget = QtWidgets.QWidget(InsertImage)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 9, 411, 191))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.retranslateUi(InsertImage)
        self.buttonBox.accepted.connect(InsertImage.accept)
        self.buttonBox.rejected.connect(InsertImage.reject)
        QtCore.QMetaObject.connectSlotsByName(InsertImage)

    def retranslateUi(self, InsertImage):
        _translate = QtCore.QCoreApplication.translate
        InsertImage.setWindowTitle(_translate("InsertImage", "Insert image"))
        self.everyPage.setText(_translate("InsertImage", "On every page"))
        self.label.setText(_translate("InsertImage", "Image"))
        self.chooseFile.setText(_translate("InsertImage", "Choose..."))
