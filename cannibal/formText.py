# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './formText.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TextEdit(object):
    def setupUi(self, TextEdit):
        TextEdit.setObjectName("TextEdit")
        TextEdit.resize(204, 37)
        TextEdit.setModal(True)
        self.lineEdit = QtWidgets.QLineEdit(TextEdit)
        self.lineEdit.setGeometry(QtCore.QRect(0, 0, 201, 36))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(TextEdit)
        QtCore.QMetaObject.connectSlotsByName(TextEdit)

    def retranslateUi(self, TextEdit):
        _translate = QtCore.QCoreApplication.translate
        TextEdit.setWindowTitle(_translate("TextEdit", "form text"))
