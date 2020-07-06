# -*- coding: utf-8; -*-
"""
Copyright (c) 2020 Felix Huber

pdfTool.py: herlper functions for PDF file manipulation using pymuPDF

pdfTool.py is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pdfTool.py. If not, see <http://www.gnu.org/licenses/>.

"""


import os
import tempfile
import fitz
from PyQt5.QtGui import QImage, QTransform
try:
    import pyqrcode
    import png
except:
    canQR = False
else:
    canQR = True


class PdfDoc:
    """
    PDF helper functions using mymupdf

    """
    
    def __init__(self):
        """
        Initialize
        """
        self.doc = None
        self.textNum = 0

    def canQR(self):
        """
        Return whether QR can be generated.
        Needs pyqrcode and pyng modules in serach path
        
        :return: True if QR can be generated
        """
        return canQR
    
    def openPdf(self, fileName=None):
        """
        Open a document using pymupdf.
        If the file is not in PDF format, it will be converted on the fly
        :param fileName: full path of file to opened or None to create a new file
        
        :return: 0 on failure, 1 on success, 2 on success with converted file and doc object
        """

        try:
            ret = 1
            self.doc = fitz.open(fileName)
            if self.doc.isPDF is False:
                # convert other formats to PDF on the fly
                pdfbytes = self.doc.convertToPDF()
                self.doc.close()
                self.doc = fitz.open("pdf", pdfbytes)
                ret = 2
        except:
            pass
        if self.doc is None:
            ret = 0
        return ret
                    
    def printSignatures(self):
        #return
        if self.doc is not None:
            for page in self.doc:
                for field in page.widgets(types=(fitz.PDF_WIDGET_TYPE_TEXT,)):
                    print("Text Name: %s, rect: %s, Label: %s, Value: %s, flags: %s, xref: %s" %  (field.field_name, field.rect,
                        field.field_label, field.field_value,
                        field.field_flags, field.xref))
                for field in page.widgets(types=(fitz.PDF_WIDGET_TYPE_SIGNATURE,)):
                    print("Signature Name: %s, rect: %s, signed %s, flags: %s, xref: %s" %
                        (field.field_name, field.rect, field.is_signed,
                        field.field_flags, field.xref))
            return field.rect

    def isNewPdf(self):
        if not self.doc.name:
            return True
        else:
            return False
        
    def closePdf(self):
        """
        Close document and free memory.
        
        :return: -
        """

        if self.doc is not None:
            self.doc.close()
            self.doc = None

    def savePdf(self, fileName=None):
        """
        Save a PDF document using pymupdf.
        :param fileName: full path of new pdf file to be saved or None to update the current file
        
        :return: True on success
        """

        if self.doc is not None:
            if fileName is None:
                self.doc.save(self.doc.name, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
            else:
                self.doc.save(fileName, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)

    def metadata(self):
        """
        Get metadata of document.
        
        :return: metadata list
        """

        if self.doc is not None:
            return self.doc.metadata
        else:
            return None

    def getDoc(self):
        return self.doc
        
    def insertPage(self, pageNum, w=595, h=842):
        """
        Insert a new empty page.
        :param pageNum: zero-based page number, page inserted before this page
        
        :return: -
        """

        if self.doc is not None:
            self.doc.insertPage(pageNum, width=w, height=h)

    def deletePage(self, pageNum):
        """
        Delete a page.
        :param pageNum: zero-based page number
        
        :return: -
        """

        if self.doc is not None:
            if 0 <= pageNum < self.doc.pageCount:
                self.doc.deletePage(pageNum)

    def getPage(self, pageNum):
        """
        Return a pymupdf page object.
        :param pageNum: zero-based page number
        
        :return: page object
        """

        if self.doc is not None:
            if 0 <= pageNum < self.doc.pageCount:
                return self.doc.loadPage(pageNum)
        return None

    def getPageCount(self):
        """
        Return number of pages in doc.
        
        :return: number of pages
        """

        return self.doc.pageCount

    def insertDocument(self, doc, pageNum=-1):
        if self.doc is not None:
            self.doc.insertPDF(doc, start_at=pageNum)

    def addText(self, page, x0, y0, x1, y1, text, fontsize, fontname, allPages=False, doQR=False, direction=0):
        """
        Insert text field(s) into document.
        Either in page (allPages = False) or all pages

        :param page: page to insert a single text object of allPages=false.
        :param x0, y0, x1, y1: bounding rectangle top left and bottom right for insertion
        :param text: text to be inserted
        :param fontsize: size of text in points
        :param fontname: one of the 14 standard pdf font names
        :param allPages: if true, text will be inserted on every page, param page is ignored
        :param doQR: text is inserted as a QR code, sized to the largest square that fits in the rectangle
        :param direction: direction of text in 90 degree steps
        
        :return: -
        """

        if doQR is True:
            qrC = pyqrcode.create(text)
            fd, fileName = tempfile.mkstemp(suffix=".png", prefix="cnb_")
            qrC.png(fileName, scale=8)
            w = x1 - x0
            h = y1 - y0
            # make bounding rect a square
            if h < w:
                x1 = x0 + h
            elif w < h:
                y1 = y0 + w
            self.addImage(page, x0, y0, x1, y1, fileName, allPages, 0, direction)
            os.close(fd)
            os.remove(fileName)
        else:
            #rect = fitz.Rect(fitz.TOOLS._derotate_rect(page, fitz.Rect(x0, y0, x1, y1)))
            rect = fitz.Rect(x0, y0, x1, y1)
            if allPages is True:
                count = 1
                for page in self.doc:
                    # insert a counter if and only if {} is in text
                    try:
                        text2 = text.format(count)
                        count += 1
                    except:
                        text2 = text
                    page.insertTextbox(rect, text2, fontsize=int(fontsize),
                            color=(0,0,0), fontname=fontname, rotate=direction)
            else:
                try:
                    text2 = text.format(page.number+1)
                except:
                    text2 = text
                page.insertTextbox(rect, text2, fontsize=int(fontsize),
                            color=(0,0,0), fontname=fontname, rotate=direction)

    def compensateRotation(self, x0, y0, x1, y1, angle):
        """
        Compensate the shrinking of an image when rotated
        """
        from math import cos
        angle = angle % 90
        if angle > 45:
            angle = 90 - angle
        scale = cos(angle/180*3.14)
        xc = (x0+x1)/2
        yc = (y0+y1)/2
        xs = (x1-x0)/2/scale
        ys = (y1-y0)/2/scale
        x0 = xc-xs
        x1 = xc+xs
        y0 = yc-ys
        y1 = yc+ys
        return fitz.Rect(x0, y0, x1, y1)

    def addImage(self, page, x0, y0, x1, y1, fileName, allPages=False, Angle=0, direction=0):
        """
        Insert image(s) into document.
        Either in page (allPages = False) or all pages

        :param page: page to insert a single text object of allPages=false.
        :param x0, y0, x1, y1: bounding rectangle top left and bottom right for insertion
        :param fileName: full path of image to be inserted
        :param allPages: if true, image will be inserted on every page, param page is ignored
        :param Angle: angle in degrees to rotate image
        :param direction: direction of image in 90 degree steps
        :return: -
        """
        rect = fitz.Rect(x0, y0, x1, y1)
        try:
            if int(Angle) != 0:
                rect = self.compensateRotation(x0, y0, x1, y1, Angle)
                # Fixme: get rid of temp file
                transform = QTransform()
                transform.rotate(-Angle)
                image = QImage(fileName)
                image = image.transformed(transform)
                fd, tempName = tempfile.mkstemp(suffix=".png", prefix="cnb_")
                image.save(tempName)
                pixmap = fitz.Pixmap(tempName)
                os.close(fd)
                os.remove(tempName)
            else:
                pixmap = fitz.Pixmap(fileName)
            if allPages is True:
                for page in self.doc:
                    page.insertImage(rect, pixmap=pixmap, overlay=True, rotate=direction)
            else:
                page.insertImage(rect, pixmap=pixmap, overlay=True, rotate=direction)
        except:
            raise

    def addTextForm(self, page, x0, y0, x1, y1, rotation):
        """
        Insert text form field into document.

        :param page: page to insert a single text form
        :param x0, y0, x1, y1: bounding rectangle top left and bottom right for insertion
        :param rotation: current rotation of the page
       
        :return: -
        """
        
        widget = fitz.Widget()                 # create a new empty widget object
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = "Textfield%s" % self.textNum
        widget.border_color = (0.7,)
        widget.border_width = (1)
        widget.fill_color = (0.98,)
        self.textNum += 1
        #widget.flags = 4096
        widget.text_fontsize = 11
        widget.field_value = "Text"
        
        rect = fitz.Rect(x0, y0, x1, y1)
        page.setRotation(0)
        widget.rect = rect  # where to locate the field
        page.addWidget(widget)         # add the widget
        page.setRotation(rotation)

    def addSignature(self, page, x0, y0, x1, y1):
        """
        Unfinished. Needs signature support in pymupdf
        """
        
        widget = fitz.Widget()                 # create a new empty widget object
        widget.rect = fitz.Rect(x0, y0, x1, y1)  # where to locate the field
        widget.field_type = fitz.PDF_WIDGET_TYPE_SIGNATURE
        widget.field_name = "Signature1"
        widget.field_value = "Reference goes here"
        page.addWidget(widget)         # add the widget

if __name__ == '__main__':
        
    pdf = PdfDoc()
        
    pdf.openPdf()
    pdf.insertPage(0)
    pdf.insertPage(1)
    page = pdf.getPage(0)
    pdf.addText(page, 100,100, 200,200, "Text", 12, "Helv", allPages=True)
    pdf.addText(page, 150,100, 200,200, "QR\nCode", 12, "Helv", allPages=True, doQR=True)
    page = pdf.getPage(1)
    pdf.addSignature(page, 50,50, 150,100)
    pdf.savePdf("testsig.pdf")
    pdf.closePdf()
    pdf.openPdf("testsig.pdf")
    pdf.printSignatures()
    pdf.closePdf()
