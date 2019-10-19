#BBD's Krita Script Starter Feb 2018

from krita import *
from PyQt5.Qt import QObject, pyqtSlot, QThread, QMetaObject, Qt, Q_ARG, Q_RETURN_ARG
from PyQt5.QtCore import QByteArray
import inspect
import json

EXTENSION_ID = 'pykrita_raccoonexport'
MENU_ENTRY = 'Export to Raccoon'

class Raccoonexport(Extension):

    def __init__(self, parent):
        #Always initialise the superclass, This is necessary to create the underlying C++ object 
        super().__init__(parent)

    def setup(self):
        pass
        
    def createActions(self, window):
        action = window.createAction(EXTENSION_ID, MENU_ENTRY, "tools/scripts")
        # parameter 1 =  the name that Krita uses to identify the action
        # parameter 2 = the text to be added to the menu entry for this script
        # parameter 3 = location of menu entry
        action.triggered.connect(self.action_triggered)        
        
    def action_triggered(self):
        doc = Krita.instance().activeDocument()

        print(doc.name())
        print(doc.width())
        print(doc.height())
        for c in doc.topLevelNodes():
            print("=========================")
            print(c.name(),c.type())
            if c.animated():
                data = self.getAnimationLength(c)
                print(len(data))
                print(c.bounds().x(),c.bounds().y(),c.bounds().width(),c.bounds().height())
                out = { "name": doc.name(),"width": doc.width(),"height": doc.height()}
                out.update({"bounds":{"x": c.bounds().x(), "y": c.bounds().y(), "width": c.bounds().width(), "height": c.bounds().height()}})
                #out.update({"data":data})
            #self.getInfo(c.node())

        print(out)
        pass # your active code goes here.
    def getAnimationLength(self,node):
        i = []
        counter = 0
        while(1):
            bytes = node.pixelDataAtTime(node.position().x(),node.position().y(),node.bounds().width(),node.bounds().height(),counter)
            if bytes.length() > 0:
                i.append(bytes)
                counter+= 1
            else: 
                break           
        return i
        pass
    def getInfo(self,target):
        [print(item) for item in inspect.getmembers(target) if not item[0].startswith('_')]

# And add the extension to Krita's list of extensions:
app=Krita.instance()
extension=Raccoonexport(parent=app) #instantiate your class
app.addExtension(extension)
extension.action_triggered()
