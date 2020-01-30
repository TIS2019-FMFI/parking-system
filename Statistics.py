from Record import Record
from BOX import Box
import csv
import datetime


class Statistics:
    def __init__(self, ecvTime, ecvNum, firmTime, firmNum, box, boxTime, ztp, ztpFirm, fromDate= None, toDate= None):
        self.ecvTime = ecvTime
        self.ecvNum = ecvNum
        self.firmTime = firmTime
        self.firmNum = firmNum
        self.box = box
        self.boxTime = boxTime
        self.ztp = ztp
        self.ztpFirm = ztpFirm
        self.fromDate = fromDate
        self.toDate = toDate
        print(fromDate)
        self.generate()

    def generate(self):
        
        if self.ecvTime:
            self.exportFile('ecvByTime.csv', ['ecv','time'], self.ecvByTime())
        if self.ecvNum:
            self.exportFile('ecvByNum.csv', ['ecv','num'], self.ecvByNum())
        if self.firmTime:
            self.exportFile('firmByTime.csv', ['firm','time'], self.firmByTime())
        if self.firmNum:
            self.exportFile('firmByNum.csv', ['firm','num'], self.firmByNum())
        if self.box:
            self.exportFile('everyBox.csv', ['box','%'], self.everyBox())
        if self.boxTime:
            self.exportFile('boxInTime.csv', ['box','%'], self.boxInTime(self.fromDate,self.toDate))
        if self.ztp:
            self.exportFile('ztp.csv', ['box','%'], self.ztp())
        if self.ztpFirm:
            self.exportFile('zptByFirm.csv', ['firm','%'], self.ztpByFirm())

    def exportFile(self, name, names, data):
        with open(name, mode = 'w') as file:
            writer = csv.writer(file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            writer.writerow(names)
            for key,value in data.items:
                writer.writerow([key, value])

    def ecvByTime(self):
        records = Record.getRecords()
        stats = dict()
        for rec in records:
            if rec.ECV in stats:
                stats[rec.ECV] = stats[rec.ECV] + (rec.endParking - rec.startParking)
            else:
                stats[rec.ECV] = (rec.endParking - rec.startParking)
        sortedStats = sorted(stats.items(), key = lambda kv: kv[1], reverse = True)
        return sortedStats

    def ecvByNum(self):
        records = Record.getRecords()
        stats = dict()
        for rec in records:
            if rec.ECV in stats:
                stats[rec.ECV] = stats[rec.ECV] + 1
            else:
                stats[rec.ECV] = 1
        sortedStats = sorted(stats.items(), key = lambda kv: kv[1], reverse = True)
        return sortedStats

    def firmByTime(self):
        records = Record.getRecords()
        stats = dict()
        for rec in records:
            if rec.id_company in stats:
                stats[rec.id_company] = stats[rec.id_company] + (rec.endParking - rec.startParking)
            else:
                stats[rec.id_company] = (rec.endParking - rec.startParking)
        sortedStats = sorted(stats.items(), key = lambda kv: kv[1], reverse = True)
        return sortedStats

    def firmByNum(self):
        records = Record.getRecords()
        stats = dict()
        for rec in records:
            if rec.id_company in stats:
                stats[rec.id_company] = stats[rec.id_company] + 1
            else:
                stats[rec.id_company] = 1
        sortedStats = sorted(stats.items(), key = lambda kv: kv[1], reverse = True)
        return sortedStats

    def everyBox(self, dayCount):
        records = Record.getRecords()
        stats = dict()
        for rec in records:
            if rec.boxID in stats:
                stats[rec.boxID] = stats[rec.boxID] + (((rec.endParking - rec.startParking)/24)/dayCount)
            else:
                stats[rec.boxID] + (((rec.endParking - rec.startParking)/24)/dayCount)
                #ked to bude zle tak sorry
        sortedStats = sorted(stats.items(), key = lambda kv: kv[1], reverse = True)
        return sortedStats                
                
                

    def boxInTime(self, dayCount, startRegion, endRegion):
        records = Record.getRecords()
        stats = dict()
        startParking = None
        endParking = None
        for rec in records:
            if rec.startParking < endRegion:
                if rec.endParking > startRegion:
                    if rec.endParking > endRegion:
                        endParking = endRegion
                    else:
                        endParking = rec.endParking
                    if rec.startParking > startRegion:
                        startParking = startRegion
                    else:
                        startParking = rec.startParking
                        
                    if rec.boxID in stats:
                        stats[rec.boxID] = stats[rec.boxID] + (((endParking - startParking)/(endRegion - startRegion))/dayCount)
                    else:
                        stats[rec.boxID] + (((endParking - startParking)/(endRegion - startRegion))/dayCount)
        sortedStats = sorted(stats.items(), key = lambda kv: kv[1], reverse = True)
        return sortedStats
        

    def ztp(self, dayCount):
        records = Record.getRecords()
        stats = dict()
        ztpBoxes = set()
        for box in FrameCarPark.boxes:
            if box.ztp:
                ztpBoxes.add(box.number)
        for rec in records:
            if rec.boxID in ztpBoxes:
                if rec.boxID in stats:
                    stats[rec.boxID] = stats[rec.boxID] + (((rec.endParking - rec.startParking)/24)/dayCount)
                else:
                    stats[rec.boxID] + (((rec.endParking - rec.startParking)/24)/dayCount)
        sortedStats = sorted(stats.items(), key = lambda kv: kv[1], reverse = True)
        return sortedStats
                

    def ztpByFirm(self):
        records = Record.getRecords()
        stats = dict()
        ztpBoxes = set()
        for box in FrameCarPark.boxes:
            if box.ztp:
                ztpBoxes.add(box.number)
        for rec in records:
            if rec.boxID in ztpBoxes:
                if rec.id_company in stats:
                    stats[rec.id_company] = stats[rec.id_commpany] + (((rec.endParking - rec.startParking)/24)/dayCount)
                else:
                    stats[rec.id_company] + (((rec.endParking - rec.startParking)/24)/dayCount)
        sortedStats = sorted(stats.items(), key = lambda kv: kv[1], reverse = True)
        return sortedStats

            
    
