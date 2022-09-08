# whiteSpriteExporter
Krita plugin for creating white sprite sheets for game development

By default will save sprites in the same folder als .kra file.
Otherwise location can be set through the Enviroment variable "KritaWhiteSpritesExporter".
Make sure to reload Krita when you've changed the Enviroment variable. 

Each Layer becomes it's own sprite. 
LayerGroups are ignored, locked layers are ignored and layers called "background" or "references" are ignored.

White sprites are usefull for Gameengines that can color sprites.
You only have to export one sprite and the game can color it differently depending on your needs
(or even animate the color)
