
# Cannibal
PDF document viewing, annotating and signing tool

**Caution**: this is unfinished software. It is merely an excercise because I wanted to improve my python skills with a real goal in mind: A FOSS tool to digitally sign PDFs in Linux. Most of the functions came from my daily work with PDFs, some are just there because I wanted to try out the QT tools.
The signing of PDFs is not implemented yet.


## Structure

Cannibal is using pymupdf to load, render and manipulate PDF files. It is a front end to the functions of pymupdf with various dialogs to enter the required data.


## Opening files
Cannibal will open PDFs and other formats supported by the underlying library. Formats other than PDF will be converted on the fly to a PDF file.

## Manipulating files
Use the menu function insert text|image|stamp|form to add texts, images, stamps or a text form field to a page. After selecting the function, the mouse cursor will display a cross shape. Select a rectangle to indicate the position and size of the area where the object will be added.

### Text
Enter the text to be displayed. A preview of the text is shown, the preview is empty if the text does not fit in the area anymore. Checking QR code will insert the text as a QR image. Checking "on every page" will insert the data on every page. The special value {} will be replaced by the current page number if text is inserted.

### Image
Choose the image to be inserted

### Stamp
Choose the language and stamp to be inserted, some sample stamps are included. New stamps can be added by creating transparent png images and placing them in stamp directory.

### Form field
A text form field is inserted that can edited by clicking with mouse in it.

### Sign
to be implemented

## PDF forms
PDF files with form fields can be filled out by clicking with the mouse when the shape of the mouse pointer changes to a hand.

## Other functions
Rotate will change the orientation of the current page

Pages can be deleted, inserted at the current position or appended as the new last page.

A dokument can be inserted starting at the current page or appended.

Individual pages can be reordered by dragging their preview with the mouse

