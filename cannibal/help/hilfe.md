
# Cannibal
PDF Dokumente anzeigen, kommentieren und signieren.

**Achtung**: Dies ist unfertige Software. Es ist lediglich eine Übung weil ich meine Python Fähigkeiten verbessern wollte mit einem richtigen Ziel vor Augen: Ein FOSS Werkzeug mit dem man unter Linux PDF Dateien digital signieren kann. Die meisten Funktionen entspringen meiner täglichen Arbeit mit PDF Dateien, manche sind nur da, weil ich die QT Werkzeuge ausprobieren wollte.
Das Signieren von PDF Dateien ist noch nicht implementiert.

## Struktur

Cannibal nutzt pymupdf zum laden, darstellen und manipulieren von PDF Sateien. Es ist eine Präsentationschicht zu den Funktionen von pymupdf mit diversen Dialogen, um die nötigen Daten einzugeben.


## Öffnen von Dateien
Cannibal kann PDF und andere Formate, die von der zu Grunde liegenden Bibliothek unterstützt werden, öffnen. Nicht-PDF-Formate werden transparent zu PDF konvertiert.

## Ändern von Dateien
Mit den Menü-Funktionen Text|Bild|Stempel|Formular einfügen können Texte, Bilder, Stempel oder Text Formularfelder in der aktuellen Seite eingefügt werden. Nach der Auswahl der Funktion ändert sich der Mauszeiger zu einem Kreuz, mit dem ein rechteckiger Bereich für die Größe und Position der Einfügung aufgewählt werden kann.

### Text
Im Eingabefeld kann der Text eingegeben werden. Eine Vorschau des Textes wird angezeigt, sie ist leer, wenn der Text nicht mehr in das Rechteck paßt. Das Markieren der Auswahl "in QR umwandeln" fügt den Text als einen QR Kode ein. Die Auswahl "auf jeder Seite" fügt die Daten auf allen Seiten ein. Die besondere Folge {} wird auf jeder Seite durch die aktuelle Seitenzahl ersetzt, wenn Text eingefügt wird.

### Bilder
Wählen Sie die Bilddatei aus, die eingefügt werden soll.

### Stempel
Wählen Sie die Sprache und den einzufügenden Stempel aus den beigefügten Beispielstempeln aus. Neue Stempel können hinzugefügt werden durch das Erzeugen von transparen PNG Bildern, die im "stamp" Ordner abgelegt werden.

### Formular Felder
Ein Text Formularfeld wird eingefügt, das durch Klicken mit der Maus bearbeitet werden kann, sobald der Mauszeiger sich über ihm befindet.

### Signieren
Nicht nicht implementiert.

## PDF formulare
PDF Dateien mit Formularfeldern können ausgefüllt werden, indem mit der Maus darauf geklickt wird, wenn sich die Zeigerform zu einer Hand ändert.

## Sonstige Funktionnen
Rotieren ändert die Orientierung der aktuellen Seite.

Seiten können gelöscht und eingefügt werden an der aktuellen Position oder an das Ende angehängt werden.

Ein Dokument kann ab der aktuellen Seite eingefügt werden oder an das Ende angehängt werden.

Individuelle Seiten können umsortiert werden, indem sie durch Ziehen mit der Maus in den Vorschaubilder verschoben werden.

