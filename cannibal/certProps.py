# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './certProps.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CertificateProperties(object):
    def setupUi(self, CertificateProperties):
        CertificateProperties.setObjectName("CertificateProperties")
        CertificateProperties.resize(533, 552)
        self.buttonBox = QtWidgets.QDialogButtonBox(CertificateProperties)
        self.buttonBox.setGeometry(QtCore.QRect(430, 510, 91, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.Issuer = QtWidgets.QLabel(CertificateProperties)
        self.Issuer.setGeometry(QtCore.QRect(10, 100, 511, 121))
        self.Issuer.setFrameShape(QtWidgets.QFrame.Box)
        self.Issuer.setText("")
        self.Issuer.setTextFormat(QtCore.Qt.RichText)
        self.Issuer.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Issuer.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.Issuer.setObjectName("Issuer")
        self.Subject = QtWidgets.QLabel(CertificateProperties)
        self.Subject.setGeometry(QtCore.QRect(10, 230, 511, 121))
        self.Subject.setFrameShape(QtWidgets.QFrame.Box)
        self.Subject.setText("")
        self.Subject.setTextFormat(QtCore.Qt.RichText)
        self.Subject.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Subject.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.Subject.setObjectName("Subject")
        self.Valid = QtWidgets.QLabel(CertificateProperties)
        self.Valid.setGeometry(QtCore.QRect(10, 360, 511, 51))
        self.Valid.setFrameShape(QtWidgets.QFrame.Box)
        self.Valid.setText("")
        self.Valid.setTextFormat(QtCore.Qt.RichText)
        self.Valid.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.Valid.setObjectName("Valid")
        self.Serial = QtWidgets.QLabel(CertificateProperties)
        self.Serial.setGeometry(QtCore.QRect(10, 420, 511, 71))
        self.Serial.setFrameShape(QtWidgets.QFrame.Box)
        self.Serial.setText("")
        self.Serial.setTextFormat(QtCore.Qt.RichText)
        self.Serial.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.Serial.setObjectName("Serial")
        self.KeyList = QtWidgets.QComboBox(CertificateProperties)
        self.KeyList.setGeometry(QtCore.QRect(10, 40, 511, 41))
        font = QtGui.QFont()
        font.setFamily("Droid Sans Mono")
        self.KeyList.setFont(font)
        self.KeyList.setObjectName("KeyList")

        self.retranslateUi(CertificateProperties)
        self.buttonBox.accepted.connect(CertificateProperties.accept)
        self.buttonBox.rejected.connect(CertificateProperties.reject)
        QtCore.QMetaObject.connectSlotsByName(CertificateProperties)

    def retranslateUi(self, CertificateProperties):
        _translate = QtCore.QCoreApplication.translate
        CertificateProperties.setWindowTitle(_translate("CertificateProperties", "Certificates"))
