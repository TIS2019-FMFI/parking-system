from abc import ABC, abstractmethod
import sqlite3

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
        # insertne do DB a hned danemu recordu nastavi ID
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
        
    
class Database(AbstractDatabase):
    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    def execute(self, query, parameters=None):
        if(parameters is None):
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, parameters)

    def commit(self):
        self.connection.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def parameterFromRecord(self, r):
        # ECV, arrivalTime, departureTime, companyId, phptoFileName, status
        return (r.ECV, r.arrivalTime, r.departureTime, r.companyId, r.photoFileName, r.status)

    @overrides(AbstractDatabase)
    def createRecord(self, record):
        par = self.parameterFromRecord()
        self.execute("INSERT INTO records VALUES (?,?,?,?,?,?)", par)

    @overrides(AbstractDatabase)
    def updateRecord(self, r):
        par = self.parameterFromRecord() + (r.id, )
        self.execute('''UPDATE records SET ECV = ?, arrivalTime = ?, departureTime = ?, companyId = ?,
                        photoFileName = ?, status = ? WHERE id = ?''', par)

    @overrides(AbstractDatabase)
    def createCompany(self, companyName):
        self.execute("INSERT INTO companies VALUES (?)", (companyName))

    @overrides(AbstractDatabase)
    def updateCompany(self, companyID, newCompanyName):
        par = (companyID, newCompanyName)
        self.execute("UPDATE campanies SET name = ? WHERE id = ?")

    @overrides(AbstractDatabase)
    def deleteCompany(self, companyID):
        self.execute("DELETE FROM companies WHERE id = ?", (companyID))
