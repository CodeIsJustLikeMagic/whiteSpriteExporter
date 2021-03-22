from krita import *
application = Krita.instance()
currentDoc = application.activeDocument()
activeNode = currentDoc.activeNode()

pixelBytes = activeNode.pixelData(0,0, currentDoc.width(), currentDoc.height())
imageData = QImage(pixelBytes, currentDoc.width(), currentDoc.height(),QImage.Format_RGBA8888)

for x in range(0,currentDoc.width()):
    for y in range(0, currentDoc.height()):
        pixel = imageData.pixelColor(x,y)
        imageData.setPixelColor(x,y, QColor(255,255,255, pixel.alpha()))

imageData.save("test.png")
     
ptr = imageData.constBits()
ptr.setsize(imageData.byteCount())
activeNode.setPixelData(bytes(ptr.asarray()),0,0,currentDoc.width(), currentDoc.height())
currentDoc.refreshProjection()