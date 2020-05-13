# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './addStamp.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InsertStamp(object):
    def setupUi(self, InsertStamp):
        InsertStamp.setObjectName("InsertStamp")
        InsertStamp.resize(445, 341)
        InsertStamp.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(InsertStamp)
        self.buttonBox.setGeometry(QtCore.QRect(30, 300, 401, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.everyPage = QtWidgets.QCheckBox(InsertStamp)
        self.everyPage.setGeometry(QtCore.QRect(20, 260, 151, 28))
        self.everyPage.setObjectName("everyPage")
        self.label = QtWidgets.QLabel(InsertStamp)
        self.label.setGeometry(QtCore.QRect(20, 193, 81, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(InsertStamp)
        self.label_2.setGeometry(QtCore.QRect(340, 200, 71, 24))
        self.label_2.setObjectName("label_2")
        self.stampName = QtWidgets.QComboBox(InsertStamp)
        self.stampName.setGeometry(QtCore.QRect(20, 220, 211, 41))
        self.stampName.setObjectName("stampName")
        self.label_3 = QtWidgets.QLabel(InsertStamp)
        self.label_3.setGeometry(QtCore.QRect(240, 190, 91, 41))
        self.label_3.setObjectName("label_3")
        self.stampLang = QtWidgets.QComboBox(InsertStamp)
        self.stampLang.setGeometry(QtCore.QRect(240, 220, 71, 41))
        self.stampLang.setObjectName("stampLang")
        self.horizontalLayoutWidget = QtWidgets.QWidget(InsertStamp)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 9, 411, 191))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.angle = QtWidgets.QLineEdit(InsertStamp)
        self.angle.setGeometry(QtCore.QRect(330, 230, 71, 31))
        self.angle.setObjectName("angle")

        self.retranslateUi(InsertStamp)
        self.buttonBox.accepted.connect(InsertStamp.accept)
        self.buttonBox.rejected.connect(InsertStamp.reject)
        QtCore.QMetaObject.connectSlotsByName(InsertStamp)

    def retranslateUi(self, InsertStamp):
        _translate = QtCore.QCoreApplication.translate
        InsertStamp.setWindowTitle(_translate("InsertStamp", "Add stamp"))
        self.everyPage.setText(_translate("InsertStamp", "On every page"))
        self.label.setText(_translate("InsertStamp", "Stamp"))
        self.label_2.setText(_translate("InsertStamp", "Angle"))
        self.label_3.setText(_translate("InsertStamp", "Language"))
