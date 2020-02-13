import tkinter as tk
from Record import Record
#from GUI import openBoxWin

class Box:
    def __init__(self, boxId, boxLabel, companyId, invalid):
        # info o boxe
        self.boxId = boxId
        self.boxLabel = boxLabel
        self.companyId = companyId
        self.invalid = invalid
        
        # buttom
        self.button = None

        # zaznam
        self.record = None
        

    def setButton(self, button):
        if(self.button is None):
            self.button = button
            self.changeColor()
            

    # companyId je firmy, ktora zaparkovala
    # nie firmy, ktorej box patri!
    def newParking(self, ECV, borrowed, companyId):
        if self.record is None:
            # Vytvori zaznam a ulozi ho do databazy
            self.record = self.createRecord(ECV, borrowed, companyId, self.boxId, self.companyId)
            self.record.save()
            self.changeColor()
            

    def endParking(self):
        self.endRecord()
        self.record = None
        self.changeColor()
    

    # Urci farbu podla record.status
    def getColor(self):
        color = "grey"
        if(self.record is not None):
            status = self.record.getStatus()
            if(status == "good"):
                color = "green"
            elif(status == "borrowed"):
                color = "orange"
            else:
                color = "red"

        return color
    

    # Nastavi farbu
    # highlightbackground som pouzival na macu, zvyraznuje to okraje buttonu
    def changeColor(self):
        self.button.config(background = self.getColor(),
                           highlightbackground = self.getColor())
        # print("Farba boxu {0} zmenena".format(self.boxLabel))

    def addPhoto(self):
        self.record.addPhoto()
        

    #vytvor instanciu záznamu a vrat ju
    def createRecord(self, ECV, borrowed, companyId, boxId, boxCompanyID):
        #print('Vytvaram parkovaci zaznam pre Box c.{0}'.format(self.boxId))
        return Record(ECV, borrowed, companyId, boxId, boxCompanyID)


    # DOKONCIT !!!
    def endRecord(self):
        self.record.update()
