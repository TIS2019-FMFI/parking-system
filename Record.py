from Files import File
from Database import Database
import datetime

class Record:
    def __init__(self, ECV, borrowed, companyId, box, photoFileName = None):
        self.recordId = -1 # Nastavi sa pri inserte
        self.ECV = ECV
        self.borrowed = borrowed
        self.companyId = companyId # id firmy, ktorej auto zastavilo
        self.boxId = box.boxId
        self.status = None
        
        self.arrivalTime = self.getTime()
        self.departureTime = None
        
        self.photoFileName = photoFileName

        self.setStatus(box)

    def addPhoto(self):
        name = File.choosePhoto()
        self.photoFileName = name


    # Urcute status pre zaznam
    # 3 stavy - 'good', 'borrowed', 'wrong'
    def setStatus(self, box):
        status = "good"
        if(self.companyId != box.companyId):
            if(self.borrowed):
                status = "borrowed"
            else:
                status = "wrong"
                
        self.status = status
        

    # Vrati status
    def getStatus(self):
        return self.status
    

    # Slovensky vypis typu parkovania (status)
    def getTypeOfParking(self):
        typ = { "good": "Dobry, firma stoji na svojom boxe",
                "borrowed": "Dobry, firma si box docasne zapozicala",
                "wrong": "Zly, auto obsadilo box inej firme"}
        return typ[self.getStatus()]
            

    # Uklada Zaznam do databazy
    def save(self):
        recordId = Database("kvant.db").createRecord(self)
        self.recordId = recordId
        print(self)


    # Vracia aktualny systemovy cas
    def getTime(self):
        return datetime.datetime.now()


    # Pomocny vypis
    def __str__(self):
        return "Record {0} (ECV = {1}, companyId = {2}, boxId = {3})".format(self.recordId, self.ECV, self.companyId, self.boxId)






    
