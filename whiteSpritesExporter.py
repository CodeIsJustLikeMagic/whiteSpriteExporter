from PyQt5.QtGui import QColor, QImage
from krita import *
import os
from PyQt5.QtWidgets import QFileDialog

class WhiteSpriteExporter(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("pykrita_exportInWhite", "Export as White Sprite", "tools/scripts")
        action.triggered.connect(self.exportDocument)

    def exportDocument(self):
        self.application = Krita.instance()
        self.currentDoc = self.application.activeDocument()
        self.application.setBatchmode(True)
        self.path = os.environ.get("KritaWhiteSpritesExporter")#"D:/Eigene Dateien/Dokumente/GitHub/Master/BeatMania/Assets/Resources/BackgroundTextures"
        if self.path is None:
            self.path = self.currentDoc.fileName()
            self.saveMessage = "Saved next to .kra file: "+self.path+"\nSet custom save directory with System Enviroment Variable named 'KritaWhiteSpritesExporter'."
        else:
            self.path += "/"
            self.saveMessage = "Saved to custom directory: "+ self.path;


        self.file = self.currentDoc.fileName()
        self.file = self.file.split('/')[-1]
        self.file = self.file.split('.')[0]
        self.i = 0
        #all layers invisible
        nodesList = self.currentDoc.topLevelNodes()
        visArray = []
        for layer in nodesList:
            visArray.append(layer.visible())
            layer.setVisible(False)

        #for each individual layer make visible and savev
        for layer in nodesList:
            if layer.name().lower() in ["background", "references"]:
                continue
            if layer.locked():
                continue
            if layer.childNodes():
                continue

            layer.setVisible(True)
            self.make_white(layer)
            layer.setVisible(False)

        for layer, visibility in zip(nodesList, visArray):
            layer.setVisible(visibility)

        self.currentDoc.refreshProjection()
        self.application.setBatchmode(False)
        if self.path == "":
            message = "All done!\nSaved next to "
        QMessageBox.information(self.application.activeWindow().qwindow(), "All done!", self.saveMessage)

    def make_white(self, layer):
        pixelBytes = layer.pixelData(0, 0, self.currentDoc.width(), self.currentDoc.height())
        imageData = QImage(pixelBytes, self.currentDoc.width(), self.currentDoc.height(), QImage.Format_RGBA8888)

        for x in range(0, self.currentDoc.width()):
            for y in range(0, self.currentDoc.height()):
                pixel = imageData.pixelColor(x, y)
                imageData.setPixelColor(x, y, QColor(255, 255, 255, pixel.alpha()))

        ptr = imageData.constBits()
        ptr.setsize(imageData.byteCount())
        layer.setPixelData(bytes(ptr.asarray()), 0, 0, self.currentDoc.width(), self.currentDoc.height())
        self.currentDoc.refreshProjection()

        name = layer.name()
        if "Layer" in layer.name():
            self.i += 1
            name = str(self.i)

        self.save(layer, self.path+self.file+name+'.png')

        layer.setPixelData(pixelBytes, 0, 0, self.currentDoc.width(), self.currentDoc.height())
        self.currentDoc.refreshProjection()

    def save(self, layer,path):
        info = InfoObject()
        info.setProperty("alpha", True)
        info.setProperty("compression", 9)
        info.setProperty("forceSRGB", False)
        info.setProperty("indexed", False)
        info.setProperty("interlaced", False)
        info.setProperty("saveSRGBProfile", False)
        info.setProperty("transparencyFillcolor", [0, 0, 0])
        layer.save(path, self.currentDoc.resolution(), self.currentDoc.resolution(), info)
# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(WhiteSpriteExporter(Krita.instance()))
