from Record import Record
from Database import Database
from Box import Box
import datetime
class Finder:
    def __init__(self):
        self.db = Database("kvant.db")

    def findAll(self, fromDate, toDate):
        records = []
        rows = self.db.selectAllRecords(fromDate, toDate)
        
        for row in rows:
            # 0 = id, 1 = ecv, 2 = arrival, 3 = departure, 4 = companyId
            # 5 = boxId, 6 = photoFileName, 7 = status
            '''
            borrowed = False
            if row[7] == 'borrowed':
                borrowed = True
                
            #ECV, borrowed, companyID, boxId, boxCompanyId
            r = Record(row[1], borrowed, row[4], row[5], row[6])
            r.recordId = row[0]
            cas = row[2].split(" ")
            den = cas[0].split("-")
            hodziny = cas[1].split(":")
            r.arrivalTime = datetime.datetime(int(den[0]),int(den[1]),int(den[2]),int(hodziny[0]),int(hodziny[1]))
            cas = row[3].split(" ")
            den = cas[0].split("-")
            hodziny = cas[1].split(":")
            r.departureTime = datetime.datetime(int(den[0]),int(den[1]),int(den[2]),int(hodziny[0]),int(hodziny[1]))
            print(datetime.datetime(int(den[0]),int(den[1]),int(den[2]),int(hodziny[0]),int(hodziny[1])))
            r.status = row[7]
            '''
            r = Record(None, None, None, None, None)
            r.initFromDatabaseRecord(row)
            
            records.append(r)
        return records

    def findAllWithStatus(self, fromDate, toDate, status):
        records = []
        rows = self.db.selectAllRecordsWithStatus(fromDate, toDate, status)

        for row in rows:
            r = Record(None, None, None, None, None)    # Prazdny zaznam
            r.initFromDatabaseRecord(row)

            records.append(r)
        return records












        
