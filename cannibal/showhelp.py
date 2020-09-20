#!/usr/bin/env python3
# -*- coding: utf-8; -*-
"""
Simple program to display a md file as help
"""

import os
from sys import exit, argv, path

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit


class Help(QTextEdit):
    def __init__(self, file):
        super().__init__()
        md = self.get_markdown(file)
        if md is None:
            exit()
        self.setReadOnly(True)
        self.resize(640,768)
        self.setWindowTitle(os.path.basename(file))
        self.setMarkdown(md)

    def get_markdown(self, file):
        try:
            with open(file, encoding="utf-8") as f:
                return f.read()
        except:
            return None


def main():
    filePath = os.path.dirname(os.path.realpath(__file__))
    
    app = QApplication(argv)    
    app.setWindowIcon(QtGui.QIcon(os.path.join(filePath, "icons/Logo.png")))

    if len(argv) > 1:
        file = argv[1]
    else:
        exit()

    myapp = Help(file)
    myapp.show()
    app.exec()


if __name__ == "__main__":
    main()
