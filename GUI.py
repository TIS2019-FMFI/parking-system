import tkinter as tk 
from tkinter import *
from tkinter import ttk
import os
from BOX import Box
from Statistics import Statistics
import datetime
from Database import Database

boxes = []

##docasna funkcia len
def find(arr, key):
    for i in arr:
        if i[1] == int(key):
            if(len(i[0]) > 8):
                return i[0][0:8]+'..'
            else:
                return i[0]
    return 'NIC'

           
class FrameCarPark:
    def __init__(self, nb, sizePerc, app, main):
        self.frame = tk.Frame(nb)
        nb.add(self.frame, text="Parkovisko")
        self.canvas = Canvas(self.frame, width=sizePerc[0], height=sizePerc[1])
        self.canvas.pack(side='left')
        self.canvas.pack_propagate(0)
        # MALI BY SA NACITAVAT Z DB notifikacie
        # DOROBIT !!!
        self.notifications = ['Box c. 15 konci.', 'Box c. 5 konci', 'Box c. 3435 konci', 'Box c. 6543 konci']
        self.lb = Listbox(self.frame, relief = SUNKEN)
        for i in self.notifications:
            self.addNotification(i)
        self.lb.bind("<<ListboxSelect>>", onClickOnNotification)
        self.lb.pack(side = 'right')

        # Parkovacie boxy
        
        self.createBoxes(app, main)
        
        '''
        companies = [('KVANT',0),('Integard',1),('KVANTN',3),('skola.sk',4),('D4R7',5),('MKMs',6),('MTRUST',7),('BusinessMedia',8),('RESTAURACIA',9),('NIKTO',10)]
        t = open('konfig-parkoviska.txt', 'r')
        line = t.readline()
        
        while line != '':
            r = line.split(';')
            # id boxu, oznacenie boxu, X, Y, sirka, vyska, ID_firmy, ZTP
            #print(r[0] + ';' + r[1] + ';' + str(int(float(r[2])) / self.canvas.winfo_screenwidth() * 100) + ';' + str(int(float(r[3])) / self.canvas.winfo_screenheight() * 100) + ';' + str(int(float(r[4])) / self.canvas.winfo_screenwidth() * 100) + ';' + str(int(float(r[5])) / self.canvas.winfo_screenheight() * 100) + ';' +r[6] + ';' + r[7])
            box = Box(str(r[0]), str(r[1]), int(r[6]), self.canvas, app, tk.Button())
            box.button = tk.Button(self.canvas, bg = 'gray', text = 'Box '+ str(r[1]) + '\n' + 'firma', command = lambda opt = box: openBoxWin(opt, app))
            box.ztp = int(r[7])
            box.button.place(x = (int(float(r[2]))/100*self.canvas.winfo_screenwidth() ), y = (int(float(r[3]))/100 *self.canvas.winfo_screenheight()), width = (int(float(r[4]))/100 * self.canvas.winfo_screenwidth()), height = (int(float(r[5])) / 100 * self.canvas.winfo_screenheight()))
            self.boxes.append(box)
            line = t.readline()
        t.close()
        '''

    def addNotification(self, text):
        self.lb.insert(END, text)

    def createBoxes(self, app, main):

        def lineFromConfig(line):
            # 0 = ID_boxu, 1 = oznacenie boxu, 2 = X, 3 = Y, 4 = sirka, 5 = vyska, 6 = ID_firmy, 7 = ZTP
            result = dict()
            line = line.split(';')
            
            result["boxId"] = int(line[0])
            result["boxLabel"] = str(line[1])
            result["x"] = float(line[2])
            result["y"] = float(line[3])
            result["width"] = float(line[4])
            result["height"] = float(line[5])
            result["companyId"] = int(line[6])
            result["invalid"] = bool(line[7])
            
            return result


        configFile = open("konfig-parkoviska.txt", "r")
        for line in configFile:
            line = lineFromConfig(line)

            # Vytvorim Box
            box = Box(line["boxId"], line["boxLabel"], str(int(line["companyId"])+1), line["invalid"])

            # Vytvorenie tlacidla pre box
            companyName = Database("kvant.db").getCompanyNameById(int(line["companyId"])+1)
            buttonText = "{0}\n{1}".format(line["boxLabel"], companyName)
            button = tk.Button(self.canvas, bg="grey", text=buttonText,
                               command=lambda opt = box: openBoxWin(opt, app, main))
            button.place(x = int(line["x"] / 100 * self.canvas.winfo_screenwidth()),
                         y = int(line["y"] / 100 * self.canvas.winfo_screenheight()),
                         width = int(line["width"] / 100 * self.canvas.winfo_screenwidth()),
                         height = int(line["height"] / 100 * self.canvas.winfo_screenheight()))

            # Priradim tlacidlo a box dam do pola boxov
            box.setButton(button)
            boxes.append(box)
                        
        
class FrameStatistics:

    def __init__(self, nb, sizePerc):

        self.frame = tk.Frame(nb)

        nb.add(self.frame, text="Štatistika")



        self.canvas = Canvas(self.frame,  width=sizePerc[0], height=sizePerc[1])

        self.canvas.pack(anchor='c', pady=30)

        self.canvas.pack_propagate(0)


        frameTime = tk.Frame(self.canvas)
        frameTime.pack(pady=20,padx=20, anchor='c')
        
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

        fromHour = ttk.Combobox(frameTime, values = [i for i in range(1,24)], width = 3)
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

        toHour = ttk.Combobox(frameTime, values = [i for i in range(1,24)], width = 3)
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


        ecvSucetCasu = tk.BooleanVar()

        ecvPorusujuceParkovaniSucetCasu = ttk.Checkbutton(fr1, text='súčet času', var = ecvSucetCasu)

        ecvPocetZaznamov = tk.BooleanVar()

        ecvPorusujuceParkovaniPocetZaznamov = ttk.Checkbutton(fr1, text='počet záznamov', var = ecvPocetZaznamov)

        ecv = [ecvSucetCasu, ecvPocetZaznamov]



        def checkEcv():

            for i in ecv:

                i.set(True)



        ecvPorusujuceParkovani = ttk.Checkbutton(fr1, text='EČV porušujúce parkovanie', command = checkEcv)

        ecvPorusujuceParkovani.pack(anchor='w')

        ecvPorusujuceParkovaniSucetCasu.pack(padx=20, anchor='w')

        ecvPorusujuceParkovaniPocetZaznamov.pack(padx=20, anchor='w')



        fr2 = tk.Frame(self.canvas)

        fr2.pack(pady=10)

        firmySucetCasu = tk.BooleanVar()

        firmyPorusujuceParkovaniSucetCasu = ttk.Checkbutton(fr2, text='súčet času', var = firmySucetCasu)

        firmyPocetZaznomov = tk.BooleanVar()

        firmyPorusujuceParkovaniPocetZaznamov = ttk.Checkbutton(fr2, text='počet záznamov', var = firmyPocetZaznomov)

        firmy = [firmySucetCasu, firmyPocetZaznomov]

        def checkFirmy():

            for i in firmy:

                i.set(True)

        firmyPorusujuceParkovani = ttk.Checkbutton(fr2, text='Firmy porušujúce parkovanie', command = checkFirmy)

        firmyPorusujuceParkovani.pack(anchor='w')

        firmyPorusujuceParkovaniSucetCasu.pack(padx=20, anchor='w')

        firmyPorusujuceParkovaniPocetZaznamov.pack(padx=20, anchor='w')



        fr3 = tk.Frame(self.canvas)

        fr3.pack(pady=10)

        obsadenostKazdyBox = tk.BooleanVar()

        obsadenostBoxovKazdyBox = ttk.Checkbutton(fr3, text = 'každý box', var = obsadenostKazdyBox)

        

        

        obsadenostBoxCas = tk.BooleanVar()

        obsadenostBoxovKazdyBoxVCase = ttk.Checkbutton(fr3, text = 'každý box v čase ', var = obsadenostBoxCas)

        
        obsadenost = [obsadenostBoxCas, obsadenostKazdyBox]



        def checkObsadenost():

            for i in obsadenost:

                i.set(True)

        

        obsadenostBoxov = ttk.Checkbutton(fr3, text = 'Obsadenosť boxov', command= checkObsadenost)

        obsadenostBoxov.pack(anchor='w')

        obsadenostBoxovKazdyBox.pack(padx=20, anchor='w')

        obsadenostBoxovKazdyBoxVCase.pack(side = 'left')

        



        fr4 = tk.Frame(self.canvas)

        fr4.pack(pady=10)

        ZTPKazdyBox = tk.IntVar()

        vyuzivaniemiestaPreZtpKazdyBox = ttk.Checkbutton(fr4, text = 'každý box', var = ZTPKazdyBox)

        ZTPFirmy = tk.IntVar()

        vyuzivaniemiestaPreZtpPodlaFiriem = ttk.Checkbutton(fr4, text = 'podľa firiem', var = ZTPFirmy)

        ztp = [ZTPKazdyBox, ZTPFirmy]

        

        def checkZTP():

            for i in ztp:

                i.set(1)

                

        vyuzivaniemiestaPreZtp = ttk.Checkbutton(fr4, text = 'Využívanie miesta pre ZŤP', command = checkZTP)

        vyuzivaniemiestaPreZtp.pack(anchor='w')

        vyuzivaniemiestaPreZtpKazdyBox.pack(padx=20, anchor='w')

        vyuzivaniemiestaPreZtpPodlaFiriem.pack(padx=20, anchor='w')

        



        buttonGenerate = ttk.Button(self.canvas, text='Vygeneruj',

                                    command = lambda: Statistics(ecvSucetCasu.get(), ecvPocetZaznamov.get(),

                                                                 firmySucetCasu.get(), firmyPocetZaznomov.get(),

                                                                 obsadenostBoxCas.get(), obsadenostKazdyBox.get(),

                                                                 ZTPKazdyBox.get(), ZTPFirmy.get(), boxes,

                                                                 datetime.datetime(int(fromYear.get()), int(fromMonth.get()), int(fromDay.get()), int(fromHour.get()), int(fromMinute.get())),

                                                                 datetime.datetime(int(toYear.get()), int(toMonth.get()), int(toDay.get()), int(toHour.get()), int(toMinute.get()))))

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
        
        fr21 = Frame(fr2)
        fr21.pack(padx = 10, pady = 10)

        fr3 = Frame(self.canvas)
        fr3.pack(side='right', padx=5)
        
        self.lessees = ['Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo']
        self.lessees = Database("kvant.db").selectAllCompanies()
        self.lb = Listbox(fr21, relief=SUNKEN)
        for i in self.lessees:
            self.lb.insert(END, i)
        #self.lb.bind("<<ListboxSelect>>", onClickOnNotification)

        scr = Scrollbar(fr21, command = self.lb.yview)
        scr.pack(side = RIGHT, fill = Y)
        
        self.lb.config(yscrollcommand=scr.set)
        self.lb.pack(side='left')
        
        buttonRemoveNajomnika = ttk.Button(fr2, text='Odstráň', command = lambda: removeNajomnika(self.lb.get(ACTIVE)))
        buttonRemoveNajomnika.pack(padx = 5, pady = 5)        

        self.entry = Entry(fr3)        
        self.entry.insert(0, 'Zadaj firmu.')
        self.entry.pack(padx = 5, pady = 5)

        #self.entry.get()
        buttonAddNajomnika = ttk.Button(fr3, text='Pridaj', command = lambda: addNajomnika(self.entry.get()))
        buttonAddNajomnika.pack(padx = 5, pady = 5)
        
        buttonSaveChanges = ttk.Button(fr3, text='Ulož')
        buttonSaveChanges.pack(side='bottom', padx = 5, pady = 40)

## pomocne funkcie
def openBoxWin(box, app, main):
    if box.record == None:
        currentBox = NewBoxWindow(box, app, main)
    else:
        currentBox = BoxWindow(box, app)

    box.changeColor()
    print("farba zmenena")

def changeBoxColorTo(b, color):
    b.config(background = color)

def removeNajomnika(var):
    print('removeNajomnika')
    print(' ', var)

def addNajomnika(var):
    print('zavolam db pre addNajomnika')
    print(' ', var)

def onClickOnNotification(val):
    print(val)
    pass

def getSizeForPercent(main, percento):
    width = (main.winfo_screenwidth()  // 100) * percento
    height =  (main.winfo_screenheight() // 100) * percento
    return (width, height)

class BoxWindow:
    def __init__(self, box, app):
        print(box.record)
        print("ECV = {0}".format(box.record.ECV))
        self.win = Tk()
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
        startTime = ttk.Label(self.canvas, text = "Začiatok parkovania: {0}".format(box.record.arrivalTime))
        startTime.grid(row = 2, column = 0, columnspan = 2)

        # Firma, ktorej auto parkuje
        # companyName = Database.getCompanyNameById(line["conpanyId"])
        companyName = "PLACEHOLDER"
        firma = ttk.Label(self.canvas, text= "Firma auta: {0}".format(companyName))
        firma.grid(row = 3, column = 0, columnspan = 2)

        # Typ parkovania
        typParkovania = ttk.Label(self.canvas, text = "{0}".format(box.record.getTypeOfParking()))
        typParkovania.grid(row = 4, column = 0, columnspan = 2)

        buttonNahratFotku = tk.Button(self.canvas, text = 'Nahrať fotku', command= lambda: box.addPhoto())
        buttonNahratFotku.grid(row = 5, column = 0, columnspan = 2, pady = 20)

        buttonUkoncitParkovanie = tk.Button(self.canvas, text = 'Ukončiť parkovanie', command = lambda: [box.endParking(),self.win.destroy()])
        buttonUkoncitParkovanie.grid(row = 6, column = 0, columnspan = 2, pady = 20)
        
class NewBoxWindow:
    def __init__(self, box, app, main):
        print("Novy box {0}".format(box.boxLabel))
        
        self.win = Tk()
        self.win.title('Box')
        sizePerc = getSizeForPercent(app, 30)
        self.win.geometry('{}x{}'.format(sizePerc[0], sizePerc[1]))

        self.canvas = Canvas(self.win, width = sizePerc[0]-100, height = sizePerc[1]-100)
        self.canvas.pack(anchor="c")

        label = ttk.Label(self.canvas, text='Parkovací box {0}'.format(box.boxLabel), font=("Ariel", 25))
        label.grid(row = 0, column = 0, columnspan = 2)

        # ECV vozidla        
        entryECVLabel = ttk.Label(self.canvas, text="Zadaj EČV vozidla:")
        entryECVLabel.grid(row = 1, column = 0, sticky = W)
        
        entryECV = Entry(self.canvas)
        entryECV.grid(row = 1, column = 1)

        # Firma, ktora zaparkovala
        lessees = ['Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo']
        lessees = Database("kvant.db").selectAllCompanies()
        print(lessees)
        firma = StringVar()
        comboBoxFirmyLabel = ttk.Label(self.canvas, text="Firma, ktorej patri auto:")
        comboBoxFirmyLabel.grid(row = 2, column = 0, sticky = W, pady = 5)
        
        comboBoxFirmy = ttk.Combobox(self.canvas, values = lessees)
        comboBoxFirmy.grid(row = 2, column = 1, pady = 5)
        
        # CheckButton pre zapozicanie
        checkBoxBorowed = ttk.Checkbutton(self.canvas, text = 'Zapožičané')
        checkBoxBorowed.grid(row = 3, column = 0, columnspan = 2)

        buttonNahratFotku = ttk.Button(self.canvas, text = 'Nahrať fotku')
        buttonNahratFotku.grid(row = 4, column = 0, columnspan = 2, pady = 20)

        buttonPotvrdit = ttk.Button(self.canvas, text = 'Potvrdiť', width=28, command = lambda: [box.newParking(entryECV.get(), checkBoxBorowed.instate(['selected']), Database("kvant.db").getCompanyNameByName(comboBoxFirmy.get())),
                                                                                                 main.addNotification("record in box {0}".format(box.boxLabel)),
                                                                                                 self.win.destroy()])
        buttonPotvrdit.grid(row = 5, column = 0, columnspan = 2, pady = 20)
        
        self.win.mainloop()
        
class MainWindow:
    def __init__(self):
        self.app = Tk()
        self.window()
        
        self.nb = ttk.Notebook(self.app)
        self.nb.pack()
        
        self.carPark = FrameCarPark(self.nb, getSizeForPercent(self.app, 90), self.app)
        self.statistics = FrameStatistics(self.nb, getSizeForPercent(self.app, 60))
        self.lessees = FrameLessees(self.nb, getSizeForPercent(self.app, 45))

        self.app.mainloop()


    def addNotification(self, text):
        self.carPark.addNotification(text)
        
    def window(self):
        self.app.title('Parkovací systém')
        self.app.geometry('{}x{}'.format(self.app.winfo_screenwidth(), self.app.winfo_screenheight()))

class MarekWindow():
    def __init__(self, root, title):
        self.app = root
        self.window(title)
        
        self.nb = ttk.Notebook(self.app)
        self.nb.pack()
        
        self.carPark = FrameCarPark(self.nb, getSizeForPercent(self.app, 90), self.app, self)
        self.statistics = FrameStatistics(self.nb, getSizeForPercent(self.app, 60))
        self.lessees = FrameLessees(self.nb, getSizeForPercent(self.app, 45))
       

        self.app.mainloop()


    def addNotification(self, text):
        self.carPark.addNotification(text)
        
    def window(self, title):
        self.app.title(title)
        self.app.geometry('{}x{}'.format(self.app.winfo_screenwidth(), self.app.winfo_screenheight()))

if __name__ == '__main__':
    root = Tk()
    main = MarekWindow(root, 'Parkovací systém')
