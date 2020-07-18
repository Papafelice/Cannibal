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

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QComboBox


class QComboBoxEnter(QComboBox):
    """
    A class to finish editing in a combobox with enter
    """
    returnPressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.returnPressed.emit()
        else:
            QComboBox.keyPressEvent(self, event)  
