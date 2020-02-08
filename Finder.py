from Record import Record
from Database import Database
from BOX import Box

class Finder:
    def __init__(self):
        ...

    def findAll(self):
        records = []
        rows = Database("kvant.db").selectAllRecords()
        
        for row in rows:
            borr = False
            if row[7] == 'borrowed':
                borr = True
            #ECV, borrowed, companyID, boxID, boxCompanyId
            r = Record(row[2],borr,row[4],row[5], row[6])
            r.recordId = row[0]
            r.departureTime = row[3]
            records.append(r)
        return records
        
