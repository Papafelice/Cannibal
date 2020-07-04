# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './formList.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ListEdit(object):
    def setupUi(self, ListEdit):
        ListEdit.setObjectName("ListEdit")
        ListEdit.resize(237, 40)
        ListEdit.setModal(False)
        self.comboBox = QComboBoxEnter(ListEdit)
        self.comboBox.setGeometry(QtCore.QRect(0, 0, 231, 36))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")

        self.retranslateUi(ListEdit)
        QtCore.QMetaObject.connectSlotsByName(ListEdit)

    def retranslateUi(self, ListEdit):
        _translate = QtCore.QCoreApplication.translate
        ListEdit.setWindowTitle(_translate("ListEdit", "form list"))
from extraWidgets import QComboBoxEnter
