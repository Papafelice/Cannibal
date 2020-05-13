# -*- coding: utf-8; -*-
"""
Copyright (c) 2020 Felix Huber

QtPdfViewer.py: PyQt image viewer widget for a PDF file in a QGraphicsView scene
with zooming and panning using pymuPDF via pdfTools

Image display functions were inspired by QtImageViewer

QtPdfViewer.py is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with QtPdfViewer. If not, see <http://www.gnu.org/licenses/>.

"""


import os
from sys import argv
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QSize
from PyQt5.QtGui import QImage, QPixmap, QPainterPath, QIcon
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QFileDialog
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QListView
import fitz
from pdfTools import PdfDoc


class ImgViewer(QGraphicsView):
    """
    Image viewer widget in a QGraphicsView scene with mouse panning.
    
    Mouse interaction:
        Left mouse button drag: Pan image        (canPan = True)
                                Select rectangle (canPan = False)
    """
    # Mouse button signals emit in image scene (x, y) coordinates.
    leftMouseButtonPressed = pyqtSignal(float, float)
    leftMouseButtonReleased = pyqtSignal(float, float)
    leftMouseRectReleased = pyqtSignal(float, float, float, float)
    
    def __init__(self, parent=None):
        """
        Initialize
        """

        super().__init__(parent)

        # Img is displayed as a QPixmap in a QGraphicsScene attached to this QGraphicsView.
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # set background
        self.scene.setBackgroundBrush(Qt.gray)

        # The scene's current image pixmap.
        self._pixmap = None

        # Scroll bar behaviour.
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.clear()

    def clear(self):
        # Default is to allow panning with left mouse button.
        self.setPan()                        
        self.zoom = 1
        self.pWidth = 1
        self.pHeight = 1
        
    def setPan(self, pan=True):
        """ Set panning mode
        """
        self.canPan = pan

    def mousePressEvent(self, event):
        """ Start mouse pan or rect select mode.
        """
        scenePos = self.mapToScene(event.pos())
        if event.button() == Qt.LeftButton:
            if self.canPan:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
            else:
                self.setDragMode(QGraphicsView.RubberBandDrag)
            self.leftMouseButtonPressed.emit(scenePos.x(), scenePos.y())
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        """ Stop mouse pan or rect select mode.
        """
        QGraphicsView.mouseReleaseEvent(self, event)
        scenePos = self.mapToScene(event.pos())
        if event.button() == Qt.LeftButton:
            if self.canPan:
                self.setDragMode(QGraphicsView.NoDrag)
                self.leftMouseButtonReleased.emit(scenePos.x(), scenePos.y())
            else:
                rect = self.scene.selectionArea().boundingRect()
                # Clear selection area.
                self.scene.setSelectionArea(QPainterPath())
                self.setDragMode(QGraphicsView.NoDrag)
                # Convert to muPDF coordinates (always 72DPI)
                self.leftMouseRectReleased.emit(
                    int(rect.x()/self.zoom/self.scale),
                    int(rect.y()/self.zoom/self.scale),
                    int((rect.x()+rect.width())/self.zoom/self.scale),
                    int((rect.y()+rect.height())/self.zoom/self.scale))
            
    def setImage(self, image):
        """ Set the scene's current image.
        :param image: QImage to be displayed
        """
        pixmap = QPixmap.fromImage(image)
        if self._pixmap is not None:
            self._pixmap.setPixmap(pixmap)
        else:
            self._pixmap = self.scene.addPixmap(pixmap)
        # Set scene size to image size.
        self.setSceneRect(QRectF(pixmap.rect()))
        self.pWidth = pixmap.width()
        self.pHeight = pixmap.height()

    def updateView(self):
        """
            Update the view with current zoom and size
            Can be overloaded to update the DPI for vector formats
        """
        # QRectF zoom rect is in scene coordinates.
        zoomRect = QRectF(0, 0, self.pWidth/self.zoom, self.pHeight/self.zoom)
        self.fitInView(zoomRect, Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        self.updateView()

    def zoomIn(self):
        if self.zoom < 4:
            self.zoom = self.zoom * 1.41422
            self.updateView()        

    def zoomOut(self):
        if self.zoom > 0.5:
            self.zoom = self.zoom * 0.7071
            self.updateView()        

    def zoomOriginal(self):
        self.zoom = 1
        self.updateView()        
        
        
def _renderPage(page, scale):
    """
    Helper function to render a PDF page into a QImage
    """
    # generate final scaling matrix 
    mat = fitz.Matrix(scale, scale)
    # Render current page
    pix = page.getPixmap(matrix=mat)
    # set the correct QImage format depending on alpha
    fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
    qtimg = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
    return qtimg

        
class PdfViewer(ImgViewer):
    """
    PDF viewer widget using ImgViewer.
    
    """
    
    def __init__(self, parent=None):
        """
        Initialize
        """

        super().__init__(parent)

        self.page = None
        self.scale = 1

    def clearPage(self):
        self.page = None

    def showPage(self, page=None):
        """
        set new page to be displayed
        and/or render it with compatible resolution
        """
        if page is not None:
            self.page = page
        
        if self.page is not None:
            # get size of view and calculate matrix
            # such that the DPI of the page fit the pixels on the screen
            scaleX = self.size().width() / self.page.rect.width
            scaleY = self.size().height() / self.page.rect.height
            self.scale = scaleY if scaleY < scaleX else scaleX
            #fixme generates lockup due to scroll bars
            #self.bestScale = scaleX
            self.bestScale = self.scale
            
            self.setImage(_renderPage(self.page, self.zoom*self.scale))

    def updateView(self):
        """
            Overloaded to recalculate DPIs
            on size and zoom change
        """
        self.showPage()        
        super().updateView()
 
    def zoomFitBest(self):
        self.zoom = self.bestScale/self.scale
        self.updateView()


class ThumbList(QListWidget):
    """
    A scrollable thumbnail preview list using a QListWidget
    """
    
    scrollUp = pyqtSignal()
    scrollDown = pyqtSignal()
    
    def __init__(self, parent=None, thumbSize=200):
        """
        Initialize
        """

        super().__init__(parent)
        
        self.setThumbSize(thumbSize)
        self.setResizeMode(QListView.Adjust)
        
    def setThumbSize(self, size):
        """
        Set size of thumbnail image in pixels
        """
        self.thumbSize = size
        self.setIconSize(QSize(self.thumbSize, self.thumbSize))
        
    def setThumbImage(self, index, page):
        """
        Set thumbnail image
        """
        # get size of view and calculate matrix
        # such that the DPI of the page fit the pixels on the screen
        scaleX = self.thumbSize / page.rect.width
        scaleY = self.thumbSize / page.rect.height
        if scaleY < scaleX:
            scale = scaleY
        else:
            scale = scaleX

        qtimg = _renderPage(page, scale)
        self.item(index).setIcon(QIcon(QPixmap(qtimg)))

    def getVisibleRows(self):
        """
        Return top and bottom row of first and last item
        """
        # get height of drawing area
        height = self.height()
        # get item at top coordinates
        item1 = self.itemAt(0, 0)
        row1 = self.row(item1) 
        # get item at bottom coordinates
        item2 = self.itemAt(0, height)
        row2 = self.row(item2)
        # check if list is only partially filled
        return row1, row2

    def resetPreview(self, pageCount, pageNum):
        """
        fill the preview list with thumbnails of pages
        """
        self.clear()
        for i in range(pageCount):
            item = QListWidgetItem(str(i+1))
            item.setSizeHint(QSize(item.sizeHint().width(), self.thumbSize))
            self.addItem(item)
        self.setCurrentRow(pageNum)

    def wheelEvent(self, wheelEvent):
        """
        emits up or down event according to scroll direction
        """
        if wheelEvent.angleDelta().y() > 0:
            self.scrollUp.emit()
        else:
            self.scrollDown.emit()


if __name__ == '__main__':
    # Demo for handling mouse clicks.
    # Just prints the xy coords of the image pixel that was clicked on.
    def handleLeftMouse(x, y):
        print("LeftPixel (x="+str(int(x))+", y="+str(int(y))+")")

    # Create the QApplication.
    app = QApplication(argv)
        
    pdfView = PdfViewer()
    pdf = PdfDoc()
    
    # Open the file dialog
    fileName, dummy = QFileDialog.getOpenFileName(None,
                        "Open File", ".", "PDF Files (*.pdf)")
    if fileName and os.path.isfile(fileName):
        pdf.openPdf(fileName)
        pdfView.showPage(pdf.getPage(0))
 
        # Handle left mouse clicks
        # handleLeftMouse(x, y). (x, y) are image coordinates.
        pdfView.leftMouseButtonReleased.connect(handleLeftMouse)
        
        # Show the viewer and run the application.
        pdfView.show()
        app.exec()
