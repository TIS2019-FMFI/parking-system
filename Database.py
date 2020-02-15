from abc import ABC, abstractmethod
import sqlite3
from Logger import Logger

# Vytvorit zaznam a hned vratit ID - hned nastavi danemu reco
# Update zaznamu podla ID
# Vytvorit novu firmu
# Upravit firmu
# Zmazat firmu

# Indicate overriding
# https://stackoverflow.com/questions/1167617/in-python-how-do-i-indicate-im-overriding-a-method
def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider


class AbstractDatabase(ABC):

    @abstractmethod
    def createRecord(self, record):
        # insertne do DB a vrati ID daneho recordu
        raise NotImplementedError

    @abstractmethod
    def updateRecord(self, record):
        raise NotImplementedError

    @abstractmethod
    def createCompany(self, companyName):
        raise NotImplementedError

    @abstractmethod
    def updateCompany(self, companyID, newCompanyName):
        raise NotImplementedError

    @abstractmethod
    def deleteCompany(self, companyID):
        raise NotImplementedError

    @abstractmethod
    def createNotification(self, companyID):
        raise NotImplementedError

    @abstractmethod
    def deleteNotification(self, companyID):
        raise NotImplementedError
        
    
class Database(AbstractDatabase):
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        

    def execute(self, query, parameters=None):
        if(parameters is None):
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, parameters)

        self.commit()
            

    def commit(self):
        self.connection.commit()
        

    def fetchone(self):
        return self.cursor.fetchone()
    

    def fetchall(self):
        return self.cursor.fetchall()
    

    def parameterFromRecord(self, r):
        # ECV, arrivalTime, departureTime, companyId, boxID, phptoFileName, status
        return (r.ECV, r.arrivalTime, r.departureTime, r.companyId, r.boxId, r.photoFileName, r.status)


    @overrides(AbstractDatabase)
    def createRecord(self, record):
        par = self.parameterFromRecord(record)
        self.execute("INSERT INTO records(ecv, arrivalTime, departureTime, companyId, boxId," +
                     "photoFileName, status) VALUES (?,?,?,?,?,?,?)", par)
        
        return self.cursor.lastrowid    # vrati recordId


    @overrides(AbstractDatabase)
    def updateRecord(self, record):
        par = self.parameterFromRecord(record) + (record.recordId, )
        print(par)
        self.execute("UPDATE records SET ECV = ?, arrivalTime = ?, departureTime = ?, companyId = ?," +
                     "boxId = ?, photoFileName = ?, status = ? WHERE recordId = ?", par)


    @overrides(AbstractDatabase)
    def createCompany(self, companyName):
        self.execute("INSERT INTO companies(name) VALUES (?)", (companyName, ))


    @overrides(AbstractDatabase)
    def updateCompany(self, companyId, newCompanyName):
        par = (companyId, newCompanyName)
        self.execute("UPDATE companies SET name = ? WHERE companyId = ?", (newCompanyName, companyId))


    @overrides(AbstractDatabase)
    def deleteCompany(self, companyId):
        self.execute("DELETE FROM companies WHERE companyId = ?", (companyId, ))

    def selectAllRecords(self):
        self.execute("SELECT * FROM records WHERE departureTime is NOT NULL")
        return self.fetchall()

    def selectAllCompanies(self):
        self.execute("SELECT * FROM companies")
        return self.fetchall()
    
    @overrides(AbstractDatabase)
    def createNotification(self, text):
        self.execute("INSERT INTO notifications(name) VALUES (?)", (text, ))

    @overrides(AbstractDatabase)
    def deleteNotification(self, notificationId):
        self.execute("DELETE FROM notifications WHERE notificationId = ?", (notificationId, ))

    def selectAllNotifications(self):
        self.execute("SELECT * FROM notifications")
        return self.fetchall()

    def selectAllRecords(self, fromDate, toDate):
        self.execute("SELECT * FROM records WHERE departureTime is NOT NULL AND "
                     + "(arrivalTime >= ? OR departureTime <= ?)", (fromDate,toDate))
        return self.fetchall()

    def selectAllRecordsWithStatus(self, fromDate, toDate, status):
        self.execute('''SELECT *
                        FROM records
                        WHERE departureTime is NOT NULL
                          AND status == ?
                          AND (arrivalTime >= ? OR departureTime <= ?)''', (status, fromDate, toDate))
        return self.fetchall()

    def selectAllCompanies(self):
        self.execute("SELECT * FROM companies")
        return self.fetchall()
    
    def getCompanyNameById(self, id):
        self.execute("SELECT name FROM companies where companyID = ?",(id, ))
        company = self.fetchone()
        if company is None:
            return None
        return company[0]
    
    def getCompanyIdByName(self, name):
        self.execute("SELECT companyID FROM companies where name = ?",(name, ))
        company = self.fetchone()
        if company is None:
            return None
        return company[0]

    # Pri novom pusteni appky
    # Vrati vsetky zaznamy, ktore este neboli ukoncene
    def getAllRunningRecords(self):
        self.execute("SELECT * FROM records WHERE departureTime IS NULL")
        return self.fetchall()
        



        
