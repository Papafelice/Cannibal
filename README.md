# Cannibal
PDF document viewing, annotating and signing tool

**Caution**: this is unfinished software. It is merely an excercise because I wanted to improve my python skills with a real goal in mind: A FOSS tool to digitally sign PDFs in Linux. Most of the functions came from my daily work with PDFs, some are just there because I wanted to try out the QT tools.
The signing of PDFs is not implemented yet.


Cannibal is using pymupdf to load, render and manipulate PDF files. It is a front end to the functions of pymupdf with various dialogs to enter the required data.
Cannibal will open PDFs and other formats supported by the underlying library. Formats other than PDF will be converted on the fly to a PDF file.

You can insert text|image|stamp|form to add texts, images, stamps or a text form field to a page. 
Pages can be deleted, inserted at the current position or appended as the new last page.
A dokument can be inserted starting at the current page or appended.
Individual pages can be reordered by dragging their preview with the mouse

