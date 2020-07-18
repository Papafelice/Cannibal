# -*- coding: utf-8; -*-
"""
Copyright (c) 2020 Felix Huber

treeview.py: helper functions to show PDF signature data

treeview.py is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with treeview.py. If not, see <http://www.gnu.org/licenses/>.

"""

# This is a dummy function until pymupdf can handle digital signatures

import sys
from PyQt5 import QtGui, QtWidgets

sigData = [
    ['Rev1 signed by John Doe',  'Check not ok', 'Date: 1.1.2020', 'Reason: unkown', 'Field: sigField on Page1'], 
    ['Rev2 signed by John Deer', 'Check not ok', 'Date: 2.1.2020', 'Reason: unkown', 'Field: sigField on Page1'], 
    ['Rev3 signed by John Dear', 'Check not ok', 'Date: 3.1.2020', 'Reason: unkown', 'Field: sigField on Page1']
    ]


class TreeView(QtWidgets.QTreeView):
    def __init__(self, parent=None, data=sigData):
        super().__init__()
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name'])
        self.header().setDefaultSectionSize(180)
        self.setModel(self.model)
        self.importSigData(data)
        self.expandAll()

    def importSigData(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        for sig in data:
            root.appendRow(QtGui.QStandardItem(sig[0]))
            child = root.child(root.rowCount() - 1)
            child.appendRow(QtGui.QStandardItem(sig[1]))
            child.appendRow(QtGui.QStandardItem(sig[2]))
            child.appendRow(QtGui.QStandardItem(sig[3]))
            child.appendRow(QtGui.QStandardItem(sig[4]))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TreeView()
    window.setGeometry(600, 50, 400, 250)
    window.show()
    app.exec()
