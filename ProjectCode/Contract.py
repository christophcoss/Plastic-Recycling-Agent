from Types import CollectionType

class Contract:
    def __init__(self,municipality, recCompagny, amount, baseWaste, minRec, type, start, end, fine, seq):
        self.municipality = municipality
        self.recCompagny = recCompagny
        self.num = "C{:03d}_{:03d}_{:03d}_{:02d}".format(municipality.unique_id, recCompagny.unique_id,start,seq)
        self.baseWaste = baseWaste
        self.amount = amount
        self.minRec = minRec
        self.type = type
        self.start = start
        self.end = end
        self.fine = fine
        self.collectedWaste = 0
        self.collectedPlastic = 0
        self.full = False


    def plasticRate(self):
        if self.collectedWaste == 0 :
            return 1
        else :
            return self.collectedPlastic / self.collectedWaste




