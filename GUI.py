import tkinter as tk 
from tkinter import *
from tkinter import ttk
import os
from Box import Box
from Statistics import Statistics
import datetime
from Database import Database
from Logger import Logger
from Record import Record
from tkinter import messagebox

boxes = []
           
class FrameCarPark:
    def __init__(self, nb, sizePerc, app, main):
        self.frame = tk.Frame(nb)
        nb.add(self.frame, text="Parkovisko")
        self.canvas = Canvas(self.frame, width=sizePerc[0], height=sizePerc[1])
        self.canvas.pack(side='left')
        self.canvas.pack_propagate(0)
        self.sizePerc = sizePerc

        # Parkovacie boxy
        self.createBoxes(app, main)
        self.loadRecords()

    # Vytvori boxy podla config filu a vykresli ich na obrazovku
    def createBoxes(self, app, main):

        def lineFromConfig(line):
            # 0 = ID_boxu, 1 = oznacenie boxu, 2 = X, 3 = Y, 4 = sirka, 5 = vyska, 6 = ID_firmy, 7 = ZTP
            result = dict()
            line = line.strip().split(';')
            
            result["boxId"] = int(line[0])
            result["boxLabel"] = str(line[1])
            result["x"] = float(line[2])
            result["y"] = float(line[3])
            result["width"] = float(line[4])
            result["height"] = float(line[5])
            result["companyId"] = int(line[6])
            result["invalid"] = bool(int(line[7]))

            return result


        configFile = open("konfig-parkoviska.txt", "r")
        Logger().info("ConfigFile úspešne otvorený")
        
        for line in configFile:
            line = lineFromConfig(line)

            # Vytvorim Box a vlozim jeho zakladne info do tabulky (pre statistiku)
            box = Box(line["boxId"], line["boxLabel"], line["companyId"], line["invalid"])

            # Vytvorenie tlacidla pre box
            companyName = Database("kvant.db").getCompanyNameById(line["companyId"])
            print(line["companyId"], companyName)
            if companyName is None:
                companyName = 'KVANT'
                box.companyId = Database("kvant.db").getCompanyIdByName('KVANT')
                      
            buttonText = "{0}\n{1}".format(line["boxLabel"], companyName)
            
            fontStyle = ('Helvetica ','9')
            if self.sizePerc[0] > 1080:                
                fontStyle = ('Helvetica ','12')
            button = tk.Button(self.canvas, bg="grey", text=buttonText, font = fontStyle,
                               command=lambda opt = box: openBoxWin(opt, app, main))
            button.place(x = int(line["x"] / 100 * self.canvas.winfo_screenwidth()),
                         y = int(line["y"] / 100 * self.canvas.winfo_screenheight()),
                         width = int(line["width"] / 100 * self.canvas.winfo_screenwidth()),
                         height = int(line["height"] / 100 * self.canvas.winfo_screenheight()))

            # Priradim tlacidlo a box dam do pola boxov
            box.setButton(button)
            boxes.append(box)
            Logger().info("Box (id = {}) úspešne vykreslený".format(line["boxId"]))
            
        configFile.close()
        Logger().info("ConfigFile úspešne dočitaný")
        Logger().info("Boxy úspešne vykreslené")

    # Pri spusteni aplikacie nacita zaznamy, ktore su stale aktualne
    # A priradi ich prislusnym boxom
    def loadRecords(self):
        
        def getBoxById(boxId):
            for b in boxes:
                if(b.boxId == boxId):
                    return b
        
        dbRecords = Database('kvant.db').getAllRunningRecords()
        for dbRecord in dbRecords:
            # Vytvori novy prazdny 'zaznam' a inicializuje ho hodnotami z DB
            newRecord = Record(None, None, None, None, None)
            newRecord.initFromDatabaseRecord(dbRecord)

            # A tento rekord priradi svojmu boxu
            box = getBoxById(newRecord.boxId)
            box.record = newRecord
            box.changeColor()
            Logger().info("Záznam (id = {}) úspešne obnovený z DB".format(newRecord.recordId))
            
                        
        
class FrameStatistics:
    def __init__(self, nb, sizePerc):
        self.frame = tk.Frame(nb)
        nb.add(self.frame, text="Štatistika")
        self.canvas = Canvas(self.frame,  width=sizePerc[0], height=sizePerc[1])
        self.canvas.pack(anchor='c', pady=30)
        self.canvas.pack_propagate(0)

        frameTime = tk.Frame(self.canvas)
        frameTime.pack(pady=20, anchor='c')

        fr1 = tk.Frame(self.canvas)
        fr1.pack(pady=5)

        fromDay = ttk.Combobox(frameTime, values = [i for i in range(1,32)], width = 3)
        fromDay.current(0)

        labelBodka1 = ttk.Label(frameTime, text = '. ')

        fromMonth = ttk.Combobox(frameTime, values = [i for i in range(1,13)], width = 3)
        fromMonth.current(0)

        labelBodka2 = ttk.Label(frameTime, text = '. ')

        fromYear = ttk.Combobox(frameTime, values = [i for i in range(2019,2050)], width = 4)
        fromYear.current(0)

        fromHour = ttk.Combobox(frameTime, values = [i for i in range(0,24)], width = 3)
        fromHour.current(0)

        labelDvojbodka1 = tk.Label(frameTime, text = ' : ')

        fromMinute = ttk.Combobox(frameTime, values = [i for i in range(00,60)], width = 3)
        fromMinute.current(0)

        labelPomlcka = tk.Label(frameTime, text = ' - ')

        toDay = ttk.Combobox(frameTime, values = [i for i in range(1,32)], width = 3)
        toDay.current(0)

        labelBodka3 = ttk.Label(frameTime, text = '. ')

        toMonth = ttk.Combobox(frameTime, values = [i for i in range(1,13)], width = 3)
        toMonth.current(0)

        labelBodka4 = ttk.Label(frameTime, text = '. ')

        toYear = ttk.Combobox(frameTime, values = [i for i in range(2019,2050)], width = 4)
        toYear.current(0)

        toHour = ttk.Combobox(frameTime, values = [i for i in range(0,24)], width = 3)
        toHour.current(0)

        labelDvojbodka2 = tk.Label(frameTime, text = ' : ')

        toMinute = ttk.Combobox(frameTime, values = [i for i in range(00,60)], width = 3)
        toMinute.current(0)

        fromDay.pack(side = 'left')        
        fromDay.pack_propagate(0)

        labelBodka1.pack(side = 'left')

        fromMonth.pack(side = 'left')        
        fromMonth.pack_propagate(0)

        labelBodka2.pack(side = 'left')

        fromYear.pack(side = 'left')        
        fromYear.pack_propagate(0)

        fromHour.pack(side = 'left')        
        fromHour.pack_propagate(0)

        labelDvojbodka1.pack(side = 'left')

        fromMinute.pack(side = 'left')
        fromMinute.pack_propagate(0)

        labelPomlcka.pack(side = 'left')

        toDay.pack(side = 'left')        
        toDay.pack_propagate(0)

        labelBodka3.pack(side = 'left')

        toMonth.pack(side = 'left')        
        toMonth.pack_propagate(0)

        labelBodka4.pack(side = 'left')

        toYear.pack(side = 'left')        
        toYear.pack_propagate(0)

        toHour.pack(side = 'left')
        toHour.pack_propagate(0)

        labelDvojbodka2.pack(side = 'left')

        toMinute.pack(side = 'left')
        toMinute.pack_propagate(0)
        

        def zaskrtni(var, polia):
            for p in polia:
                p.set(var.get())

        
        ecvSucetCasu = tk.IntVar()
        ecvPorusujuceParkovaniSucetCasu = ttk.Checkbutton(fr1, text='súčet času', var = ecvSucetCasu)
        ecvPocetZaznamov = tk.IntVar()
        ecvPorusujuceParkovaniPocetZaznamov = ttk.Checkbutton(fr1, text='počet záznamov', var = ecvPocetZaznamov)
        ecv = [ecvSucetCasu, ecvPocetZaznamov]

        ecvPorusujuceParkovaniVAR = tk.IntVar()
        ecvPorusujuceParkovani = ttk.Checkbutton(fr1, text='EČV porušujúce parkovanie', command = lambda: [zaskrtni(ecvPorusujuceParkovaniVAR, ecv)], var = ecvPorusujuceParkovaniVAR)
        ecvPorusujuceParkovani.pack(anchor='w')
        ecvPorusujuceParkovaniSucetCasu.pack(padx=20, anchor='w')
        ecvPorusujuceParkovaniPocetZaznamov.pack(padx=20, anchor='w')


        fr2 = tk.Frame(self.canvas)
        fr2.pack(pady=10)
        firmySucetCasu = tk.IntVar()
        firmyPorusujuceParkovaniSucetCasu = ttk.Checkbutton(fr2, text='súčet času', var = firmySucetCasu)
        firmyPocetZaznomov = tk.IntVar()
        firmyPorusujuceParkovaniPocetZaznamov = ttk.Checkbutton(fr2, text='počet záznamov', var = firmyPocetZaznomov)
        firmy = [firmySucetCasu, firmyPocetZaznomov]

        firmyPorusujuceParkovaniVAR = tk.IntVar()
        firmyPorusujuceParkovani = ttk.Checkbutton(fr2, text='Firmy porušujúce parkovanie', command = lambda: [zaskrtni(firmyPorusujuceParkovaniVAR, firmy)], var = firmyPorusujuceParkovaniVAR)
        firmyPorusujuceParkovani.pack(anchor='w')
        firmyPorusujuceParkovaniSucetCasu.pack(padx=20, anchor='w')
        firmyPorusujuceParkovaniPocetZaznamov.pack(padx=20, anchor='w')


        fr3 = tk.Frame(self.canvas)
        fr3.pack(pady=10)
        obsadenostKazdyBox = tk.IntVar()
        obsadenostBoxovKazdyBox = ttk.Checkbutton(fr3, text = 'každý box', var = obsadenostKazdyBox)
        obsadenostBoxCas = tk.IntVar()
        obsadenostBoxovKazdyBoxVCase = ttk.Checkbutton(fr3, text = 'každý box v čase ', var = obsadenostBoxCas)
        obsadenost = [obsadenostBoxCas, obsadenostKazdyBox]

        obsadenostBoxovVAR = tk.IntVar()
        obsadenostBoxov = ttk.Checkbutton(fr3, text = 'Obsadenosť boxov', command = lambda: [zaskrtni(obsadenostBoxovVAR, obsadenost)], var = obsadenostBoxovVAR)
        obsadenostBoxov.pack(anchor='w')
        obsadenostBoxovKazdyBox.pack(padx=20, anchor='w')
        #obsadenostBoxovKazdyBoxVCase.pack(padx=20, anchor='w')

        fr4 = tk.Frame(self.canvas)
        fr4.pack(pady=10)
        ZTPKazdyBox = tk.IntVar()
        vyuzivaniemiestaPreZtpKazdyBox = ttk.Checkbutton(fr4, text = 'každý box', var = ZTPKazdyBox)
        ZTPFirmy = tk.IntVar()
        vyuzivaniemiestaPreZtpPodlaFiriem = ttk.Checkbutton(fr4, text = 'podľa firiem', var = ZTPFirmy)
        ztp = [ZTPKazdyBox, ZTPFirmy]

        vyuzivaniemiestaPreZtpVAR = tk.IntVar()
        vyuzivaniemiestaPreZtp = ttk.Checkbutton(fr4, text = 'Využívanie miesta pre ZŤP', command = lambda: [zaskrtni(vyuzivaniemiestaPreZtpVAR, ztp)], var = vyuzivaniemiestaPreZtpVAR)
        vyuzivaniemiestaPreZtp.pack(anchor='w')
        vyuzivaniemiestaPreZtpKazdyBox.pack(padx=20, anchor='w')
        vyuzivaniemiestaPreZtpPodlaFiriem.pack(padx=20, anchor='w')

        buttonGenerate = ttk.Button(self.canvas, text='Vygeneruj',
                                    command = lambda: [Statistics(ecvSucetCasu, ecvPocetZaznamov,
                                                                 firmySucetCasu, firmyPocetZaznomov,
                                                                 obsadenostBoxCas, obsadenostKazdyBox,
                                                                 ZTPKazdyBox, ZTPFirmy, boxes,
                                                                 datetime.datetime(int(fromYear.get()), int(fromMonth.get()), int(fromDay.get()), int(fromHour.get()), int(fromMinute.get())),
                                                                 datetime.datetime(int(toYear.get()), int(toMonth.get()), int(toDay.get()), int(toHour.get()), int(toMinute.get()))),
                                                       messagebox.showinfo("Štatistika","Štatistika úspešne vygenerovaná!\nNájdete ju v zložke \"MyDocuments/Parkovanie/exports\".")])
        buttonGenerate.pack()
        
class FrameLessees:
    def __init__(self, nb, sizePerc):
        self.frame = tk.Frame(nb)
        nb.add(self.frame, text="Nájomníci")

        self.canvas = Canvas(self.frame, width = sizePerc[0], height = sizePerc[1])
        self.canvas.pack(anchor='c', pady = 30)
        self.canvas.pack_propagate(0)
        
        fr2 = Frame(self.canvas)
        fr2.pack(side='left',padx=30, pady=20)
        
        label = ttk.Label(fr2, text='Zoznam nájomníkov:')
        label.pack(padx = 5, pady = 5)
        
        self.fr21 = Frame(fr2)
        self.fr21.pack(padx = 10, pady = 10)

        fr3 = Frame(self.canvas)
        fr3.pack(side='right', padx=5)
        
        self.lessees = Database('kvant.db').selectAllCompanies()
        self.lb = Listbox(self.fr21, relief=SUNKEN)
        for i in self.lessees:
            self.lb.insert(END, i)

        scr = Scrollbar(self.fr21, command = self.lb.yview)
        scr.pack(side = RIGHT, fill = Y)
        
        self.lb.config(yscrollcommand=scr.set)
        self.lb.pack(side='left')
        
        buttonRemoveNajomnika = ttk.Button(fr2, text='Odstráň', command = lambda: self.removeNajomnika(self.lb.get(ACTIVE)))
        buttonRemoveNajomnika.pack(padx = 5, pady = 5)        

        self.entry = Entry(fr3)        
        self.entry.insert(0, 'Zadaj firmu.')
        self.entry.pack(padx = 5, pady = 5)

        buttonAddNajomnika = ttk.Button(fr3, text='Pridaj', command = lambda: self.addNajomnika(self.entry.get()))
        buttonAddNajomnika.pack(padx = 5, pady = 5)

        buttonUpdateNajomnika = ttk.Button(fr3, text='Premenuj', command = lambda: self.renameNajomnika(self.entry.get(), self.lb.get(ACTIVE)))
        buttonUpdateNajomnika.pack(padx = 5, pady = 5)

    def renameNajomnika(self, newName, oldName):
        Database('kvant.db').updateCompany(int(oldName[0]), newName)
        Logger().info('Premenovanie firmy '+ oldName[1]+' na '+ newName+'.')
        self.refreshLesses()
        messagebox.showinfo("Pozor","Vypnite a následne zapnite aplikáciu, prosím.")
        
    def removeNajomnika(self, var):
        if self.isRemovable(var):
            Database('kvant.db').deleteCompany(var[0])
            Logger().info('Vymazania firmy '+ str(var[0])+' '+ str(var[1])+'.')
            self.refreshLesses()
            messagebox.showinfo("Pozor", "Vypnite a následne zapnite aplikáciu, prosím.")
        else:
            messagebox.showinfo("Pozor","Firmu nemožno vymazať pokiaľ existujú jej bežiace záznamy na parkovisku.")
            
    def addNajomnika(self, var):
        Database('kvant.db').createCompany(var)
        Logger().info('Pridanie firmy '+ var +'.')
        self.refreshLesses()

    def refreshLesses(self):
        self.lessees = Database('kvant.db').selectAllCompanies()
        self.lb.delete(0, END)
        for i in self.lessees:
            self.lb.insert(END, i)
                      
    def isRemovable(self, var):
        for box in boxes:
            if box.record is not None:
                if int(box.record.companyId) == int(var[0]):
                    return False
        return True
    
## pomocne funkcie
def openBoxWin(box, app, main):
    if box.record == None:
        currentBox = NewBoxWindow(box, app, main)
    else:
        currentBox = BoxWindow(box, app)
    box.changeColor()

def changeBoxColorTo(b, color):
    b.config(background = color)

def getSizeForPercent(main, percento):
    width = (main.winfo_screenwidth()  // 100) * percento
    height =  (main.winfo_screenheight() // 100) * percento
    return (width, height)

class BoxWindow:
    def __init__(self, box, app):
        print(box.record)
        print("ECV = {0}".format(box.record.ECV))
        self.win = Toplevel()
        self.win.title('Box')
        sizePerc = getSizeForPercent(app, 60)
        self.win.geometry('{}x{}'.format(sizePerc[0], sizePerc[1]))

        self.canvas = Canvas(self.win, width = sizePerc[0]-100, height = sizePerc[1]-100)
        self.canvas.pack(anchor='c')

        # Nadpis
        label = ttk.Label(self.canvas, text = "Parkovací box {0}".format(box.boxLabel), font = ("Ariel", 25))
        label.grid(row = 0, column = 0, columnspan = 2)
        
        # Znacka auta
        labelEcv = ttk.Label(self.canvas, text = "ECV auta: {0}".format(box.record.ECV))
        labelEcv.grid(row = 1, column = 0, columnspan = 2)

        # Zaciatok parkovania
        startTime = ttk.Label(self.canvas, text = "Začiatok parkovania: {0}".format(box.record.arrivalTime)[:-7])
        startTime.grid(row = 2, column = 0, columnspan = 2)

        # Firma, ktorej auto parkuje
        print('box.record.companyId',type(box.record.companyId))
        companyName = Database("kvant.db").getCompanyNameById(int(box.record.companyId))
            
        firma = ttk.Label(self.canvas, text= "Firma auta: {0}".format(companyName))
        firma.grid(row = 3, column = 0, columnspan = 2)

        # Typ parkovania
        typParkovania = ttk.Label(self.canvas, text = "Status: {0}".format(box.record.getTypeOfParking()))
        typParkovania.grid(row = 4, column = 0, columnspan = 2)

        # Fotka parkovania
        if box.record.photo is not None:            
            myvar = tk.Button(self.canvas, image = box.record.photo)
            myvar.image = box.record.photo
            myvar.grid(row = 7, column = 0, columnspan = 2, pady = 20)
         
        buttonNahratFotku = tk.Button(self.canvas, text = 'Nahrať fotku', command= lambda: [box.addPhoto(box.record.ECV), self.win.destroy()])
        buttonNahratFotku.grid(row = 5, column = 0, columnspan = 2, pady = 20)

        buttonUkoncitParkovanie = tk.Button(self.canvas, text = 'Ukončiť parkovanie', command = lambda: [box.endParking(),self.win.destroy()])
        buttonUkoncitParkovanie.grid(row = 6, column = 0, columnspan = 2, pady = 20)
        
class NewBoxWindow:
    def __init__(self, box, app, main):
        print("Novy box {0}".format(box.boxLabel))
        
        self.win = Toplevel()
        self.win.title('Box')
        sizePerc = getSizeForPercent(app, 30)
        self.win.geometry('{}x{}'.format(sizePerc[0], sizePerc[1]))

        self.canvas = Canvas(self.win, width = sizePerc[0]-100, height = sizePerc[1]-100, borderwidth = 0, highlightthickness = 0)
        self.canvas.pack(anchor="c")

        label = ttk.Label(self.canvas, text='Parkovací box {0}'.format(box.boxLabel), font=("Ariel", 25))
        label.grid(row = 0, column = 0, columnspan = 2)

        # ECV vozidla        
        entryECVLabel = ttk.Label(self.canvas, text="Zadaj EČV vozidla:")
        entryECVLabel.grid(row = 1, column = 0, sticky = W, padx = 15)
        
        entryECV = Entry(self.canvas)
        entryECV.grid(row = 1, column = 1)

        # Firma, ktora zaparkovala
        lessees = Database('kvant.db').selectAllCompanies()
        
        firma = StringVar()
        comboBoxFirmyLabel = ttk.Label(self.canvas, text="Firma, ktorej patri auto:")
        comboBoxFirmyLabel.grid(row = 2, column = 0, sticky = W, pady = 5,  padx = 15)
        
        comboBoxFirmy = ttk.Combobox(self.canvas, values = lessees)
        comboBoxFirmy.grid(row = 2, column = 1, pady = 5, padx =10)
        
        # CheckButton pre zapozicanie
        checkBorrowed = IntVar()
        #checkBorrowed.set(False) #, onvalue = 1, offvalue = 0
        checkBoxBorrowed = tk.Checkbutton(self.canvas, text='Zapožičané', variable=checkBorrowed, onvalue=1, offvalue=0)
        checkBoxBorrowed.grid(row = 3, column = 0, columnspan = 2)
        
##        buttonNahratFotku = ttk.Button(self.canvas, text = 'Nahrať fotku',  command= lambda: box.addPhoto())
##        buttonNahratFotku.grid(row = 4, column = 0, columnspan = 2, pady = 20)

        buttonPotvrdit = ttk.Button(self.canvas, text = 'Potvrdiť', width=28, command = lambda: [box.newParking(entryECV.get().upper(), checkBorrowed.get(), str(int(comboBoxFirmy.get()[0]))),
                                                                                                 self.win.destroy()])
        buttonPotvrdit.grid(row = 5, column = 0, columnspan = 2, pady = 20)

class MainWindow():
    def __init__(self, root, title):
        self.app = root
        self.window(title)
        
        self.nb = ttk.Notebook(self.app)
        self.nb.pack()
        
        self.carPark = FrameCarPark(self.nb, getSizeForPercent(self.app, 90), self.app, self)
        self.statistics = FrameStatistics(self.nb, getSizeForPercent(self.app, 60))
        self.lessees = FrameLessees(self.nb, getSizeForPercent(self.app, 45))       

        self.app.mainloop()
        
    def window(self, title):
        self.app.title(title)
        self.app.geometry('{}x{}'.format(self.app.winfo_screenwidth(), self.app.winfo_screenheight()))
        

if __name__ == '__main__':
    Logger(mode="reset")
    Logger().info('Zapnutie aplikacie.')

    root = Tk()
    main = MainWindow(root, 'Parkovací systém')
    
    Logger().info('Vypnutie aplikacie.')



