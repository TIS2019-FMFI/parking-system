from Record import Record
from Database import Database
from BOX import Box
import datetime
class Finder:
    def __init__(self):
        ...

    def findAll(self, fromDate, toDate):
        records = []
        rows = Database("kvant.db").selectAllRecords(fromDate, toDate)
        
        for row in rows:
            borr = False
            if row[7] == 'borrowed':
                borr = True
            #ECV, borrowed, companyID, boxID, boxCompanyId
            r = Record(row[1],borr,row[4],row[5], row[6])
            r.recordId = row[0]
            cas = row[2].split(" ")
            den = cas[0].split("-")
            hodziny = cas[1].split(":")
            r.arrivalTime = datetime.datetime(int(den[0]),int(den[1]),int(den[2]),int(hodziny[0]),int(hodziny[1]))
            cas = row[3].split(" ")
            den = cas[0].split("-")
            hodziny = cas[1].split(":")
            r.departureTime = datetime.datetime(int(den[0]),int(den[1]),int(den[2]),int(hodziny[0]),int(hodziny[1]))
            r.status = row[7]
            records.append(r)
        return records
        
