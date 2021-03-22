from krita import *
application = Krita.instance()
currentDoc = application.activeDocument()
activeNode = currentDoc.activeNode()

nodesList = currentDoc.topLevelNodes()

path = 'D:\Eigene Dateien\Dokumente\GitHub\Master\BeatMania\Assets\Resources\BackgroundTextures'

file = currentDoc.fileName()
file = file.split('/')[-1]
file = file.split('.')[0]
#for each individual layer make visible and savev
i= 0
for layer in nodesList:
    if not layer.locked():# ignore locked layers
        if layer.childNodes():
            print(layer.name())
        else:
            i +=1
            name = file+str(i)+('.png')
            print(name
            )
            ret = currentDoc.exportImage(name, InfoObject())
            print(ret)            
            