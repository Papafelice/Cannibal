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

from PyQt5.QtCore import Qt, pyqtSignal, QRect, QPoint
from PyQt5.QtWidgets import QDialog, QComboBox

from formText import Ui_TextEdit
from formList import Ui_ListEdit

class EditFormText(QDialog):
    """
    A class to edit a text form field
    """
    def __init__(self, pos, text=None):
        super().__init__()
        self.ui = Ui_TextEdit()
        self.ui.setupUi(self)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(pos)
        
        self.ui.lineEdit.setText(text)

        # handler for enter
        self.ui.lineEdit.returnPressed.connect(self.returnPressed)
        
        self.show()
        
    def getText(self):
        return self.ui.lineEdit.text()
    
    def returnPressed(self):
        self.done(QDialog.Accepted)


class EditFormList(QDialog):
    """
    A class to edit a list form field
    """
    def __init__(self, pos):
        super().__init__()
        self.ui = Ui_ListEdit()
        self.ui.setupUi(self)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(QPoint(pos))
        
        # handlers for enter and selection change
        self.ui.comboBox.returnPressed.connect(self.returnPressed)
        self.ui.comboBox.currentIndexChanged.connect(self.returnPressed)
        
        self.show()
        
    def fillList(self, choices):
        for item in choices:
            self.ui.comboBox.addItem(item)

    def setText(self, text):
        index = self.ui.comboBox.findText(text)        
        if index != -1:
            self.ui.comboBox.setCurrentIndex(index)

    def getText(self):
        return self.ui.comboBox.currentText()
    
    def returnPressed(self):
        self.done(QDialog.Accepted)

