# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './applySignature.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AttachSignature(object):
    def setupUi(self, AttachSignature):
        AttachSignature.setObjectName("AttachSignature")
        AttachSignature.resize(529, 510)
        self.buttonBox = QtWidgets.QDialogButtonBox(AttachSignature)
        self.buttonBox.setGeometry(QtCore.QRect(310, 460, 211, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(AttachSignature)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 511, 141))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.KeyList = QtWidgets.QComboBox(AttachSignature)
        self.KeyList.setGeometry(QtCore.QRect(10, 160, 511, 31))
        font = QtGui.QFont()
        font.setFamily("Droid Sans Mono")
        self.KeyList.setFont(font)
        self.KeyList.setObjectName("KeyList")
        self.Appearance = QtWidgets.QComboBox(AttachSignature)
        self.Appearance.setGeometry(QtCore.QRect(130, 200, 391, 31))
        self.Appearance.setObjectName("Appearance")
        self.comboBox_2 = QtWidgets.QComboBox(AttachSignature)
        self.comboBox_2.setGeometry(QtCore.QRect(130, 240, 391, 31))
        self.comboBox_2.setObjectName("comboBox_2")
        self.Reason = QtWidgets.QLineEdit(AttachSignature)
        self.Reason.setGeometry(QtCore.QRect(130, 280, 391, 36))
        self.Reason.setObjectName("Reason")
        self.Location = QtWidgets.QLineEdit(AttachSignature)
        self.Location.setGeometry(QtCore.QRect(130, 320, 391, 36))
        self.Location.setObjectName("Location")
        self.lineEdit_3 = QtWidgets.QLineEdit(AttachSignature)
        self.lineEdit_3.setGeometry(QtCore.QRect(130, 360, 391, 36))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_1 = QtWidgets.QLabel(AttachSignature)
        self.label_1.setGeometry(QtCore.QRect(20, 210, 101, 22))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(AttachSignature)
        self.label_2.setGeometry(QtCore.QRect(20, 240, 101, 22))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(AttachSignature)
        self.label_3.setGeometry(QtCore.QRect(20, 280, 67, 22))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(AttachSignature)
        self.label_4.setGeometry(QtCore.QRect(20, 320, 67, 22))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(AttachSignature)
        self.label_5.setGeometry(QtCore.QRect(20, 360, 67, 22))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(AttachSignature)
        self.buttonBox.accepted.connect(AttachSignature.accept)
        self.buttonBox.rejected.connect(AttachSignature.reject)
        QtCore.QMetaObject.connectSlotsByName(AttachSignature)

    def retranslateUi(self, AttachSignature):
        _translate = QtCore.QCoreApplication.translate
        AttachSignature.setWindowTitle(_translate("AttachSignature", "Apply Signature"))
        self.label_1.setText(_translate("AttachSignature", "Apprearance"))
        self.label_2.setText(_translate("AttachSignature", "Certification"))
        self.label_3.setText(_translate("AttachSignature", "Reason"))
        self.label_4.setText(_translate("AttachSignature", "Location"))
        self.label_5.setText(_translate("AttachSignature", "Contact"))
