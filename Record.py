from Files import File
from Database import Database
import datetime

class Record:
    def __init__(self, ECV, borrowed, companyId, boxId, boxCompanyId, photoFileName = None):
        self.recordId = -1 # Nastavi sa pri inserte
        self.ECV = ECV
        self.borrowed = borrowed
        self.companyId = companyId # id firmy, ktorej auto zastavilo
        self.boxId = boxId
        self.status = None
        
        self.arrivalTime = self.getTime()
        self.departureTime = None
        
        self.photoFileName = photoFileName

        self.setStatus(boxCompanyId)

    def addPhoto(self):
        name = File.choosePhoto()
        self.photoFileName = name
        


    # Urcute status pre zaznam
    # 3 stavy - 'good', 'borrowed', 'wrong'
    def setStatus(self, boxCompanyId):
        status = "good"
     
        if(str(self.companyId) != str(boxCompanyId)):
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
        # print(self)


    # Vracia aktualny systemovy cas
    def getTime(self):
        return datetime.datetime.now()


    # Pomocny vypis
    def __str__(self):
        return "Record {0} (ECV = {1}, companyId = {2}, boxId = {3})".format(self.recordId, self.ECV, self.companyId, self.boxId)


    # Updatne záznam pri ukončení parkovania
    def update(self):
        self.departureTime = self.getTime()
        Database("kvant.db").updateRecord(self)


    # Podla nacitaneho zaznamu z DB initne aktualny zaznam
    def initFromDatabaseRecord(self, record):
        # 0 = id, 1 = ecv, 2 = arrival, 3 = departure, 4 = companyId
        # 5 = boxId, 6 = photoFileName, 7 = status
        self.recordId = record[0]
        self.ECV = record[1]
        self.arrivalTime = datetime.datetime.strptime(record[2], '%Y-%m-%d %H:%M:%S.%f')
        self.departureTime = None
        self.companyId = record[4]
        self.boxId = record[5]
        self.photoFileName = record[6]
        self.status = record[7]

        self.borrowed = True if (record[7] == "borrowed") else False

